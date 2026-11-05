"""Render an eight-second photo-dump calendar from a JSON manifest."""
import argparse
import calendar
import json
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageOps

WIDTH, HEIGHT = 1080, 1920
FPS, FRAMES = 30, 249
PREFERRED = [3, 12, 20, 22, 24, 7, 6, 16, 33, 9, 28, 1, 18, 26, 31]


def render(manifest, output):
    config = json.loads(manifest.read_text(encoding="utf-8"))
    config.setdefault("audio", str(Path(__file__).resolve().parents[1] /
                                   "assets" / "Reference_Piano_Left_Hand.wav"))
    weeks = calendar.monthcalendar(config["year"], config["month"])
    dates = {day: row * 7 + col for row, week in enumerate(weeks)
             for col, day in enumerate(week) if day}
    photos = [dict(path=item) if isinstance(item, str) else dict(item)
              for item in config["photos"]]
    if not photos:
        raise ValueError("Include at least one tile photo.")

    def load(path):
        with Image.open(manifest.parent / path) as source:
            return ImageOps.exif_transpose(source).convert("RGB")

    cell, x0, y0 = 134, 71, 634
    slots = len(weeks) * 7
    assigned = []
    for photo in photos:
        slot = dates[photo["day"]] if "day" in photo else photo.get("slot")
        if slot is not None and (not isinstance(slot, int) or not 0 <= slot < slots):
            raise ValueError(f"Invalid calendar slot: {slot}")
        assigned.append(slot)
    reserved = {slot for slot in assigned if slot is not None}
    order = list(dict.fromkeys(PREFERRED + list(range(slots))))
    free = [slot for slot in order if slot < slots and slot not in reserved]

    base = Image.new("RGB", (WIDTH, HEIGHT), "black")
    base.paste(ImageOps.fit(load(config["background"]), (WIDTH, 1440),
                            Image.Resampling.LANCZOS), (0, 240))
    grid = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(grid)
    small = ImageFont.load_default(size=22)
    title = ImageFont.load_default(size=44)
    draw.text((540, 521), config["title"], font=title, fill="white", anchor="mm")
    for col, day in enumerate(("mon", "tue", "wed", "thu", "fri", "sat", "sun")):
        draw.text((x0 + col * cell + cell // 2, y0 - 22), day,
                  font=small, fill="white", anchor="mm")
    for col in range(8):
        x = x0 + col * cell
        draw.line((x, y0, x, y0 + len(weeks) * cell), fill=(255, 255, 255, 120), width=2)
    for row in range(len(weeks) + 1):
        y = y0 + row * cell
        draw.line((x0, y, x0 + 7 * cell, y), fill=(255, 255, 255, 120), width=2)

    tiles = []
    layout = []
    occupied = {}
    for index, (photo, slot) in enumerate(zip(photos, assigned)):
        if slot is None:
            slot = free.pop(0) if free else min(range(slots), key=lambda s: occupied.get(s, 0))
        occupied[slot] = occupied.get(slot, 0) + 1
        image = load(photo["path"])
        if "crop" in photo:
            image = image.crop(photo["crop"])
        tile = ImageOps.fit(image, (cell, cell), Image.Resampling.LANCZOS,
                            centering=tuple(photo.get("center", (.5, .5))))
        row, col = divmod(slot, 7)
        start = photo.get("start", .37 + 3.0 * index / max(8, len(photos) - 1))
        end = photo.get("end", 5.83 + ((index * 7 + 3) % 9) * .2)
        if not 0 <= start < end <= FRAMES / FPS:
            raise ValueError(f"Invalid timing for {photo['path']}")
        # Duplicate slots behave as a swap, with the most recent tile on top.
        tiles.append((tile, (x0 + col * cell, y0 + row * cell), start, end))
        layout.append({**photo, "slot": slot, "start": start, "end": end})

    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-"]
    if config.get("audio"):
        cmd += ["-i", str(manifest.parent / config["audio"])]
    cmd += ["-map", "0:v:0"]
    if config.get("audio"):
        cmd += ["-map", "1:a:0",
                "-c:a", "aac", "-b:a", "192k", "-t", str(FRAMES / FPS)]
    cmd += ["-c:v", "libx264", "-threads", "4", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart"]
    with tempfile.TemporaryDirectory(dir=output.parent) as work:
        staged = Path(work) / "calendar.mp4"
        with subprocess.Popen([*cmd, str(staged)], stdin=subprocess.PIPE) as encoder:
            previous = None
            for frame_index in range(FRAMES):
                t = frame_index / FPS
                visible = tuple(i for i, (_, _, start, end) in enumerate(tiles) if start <= t < end)
                if visible != previous:
                    frame = base.copy()
                    for i in sorted(visible, key=lambda i: tiles[i][2]):
                        tile, position, _, _ = tiles[i]
                        frame.paste(tile, position)
                    frame.paste(grid, mask=grid.getchannel("A"))
                    draw = ImageDraw.Draw(frame)
                    for day, slot in dates.items():
                        row, col = divmod(slot, 7)
                        draw.text((x0 + col * cell + 8, y0 + row * cell + 5),
                                  str(day), font=small, fill="white", stroke_width=1,
                                  stroke_fill=(65, 71, 73))
                    raw = frame.tobytes()
                    previous = visible
                encoder.stdin.write(raw)
            encoder.stdin.close()
            if encoder.wait():
                raise RuntimeError("FFmpeg could not encode the calendar video.")
        staged.replace(output)
    print(json.dumps({**config, "photos": layout}, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    render(args.manifest.resolve(), args.output.resolve())
