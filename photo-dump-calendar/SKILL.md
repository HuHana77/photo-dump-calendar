---
name: photo-dump-calendar
description: Turn uploaded photos into a vertical photo-dump calendar MP4 and a double-speed looping GIF with a background image, monthly calendar grid, and photos appearing and disappearing in individual squares. Use for 照片日历短片、月度 dump、十月 dump or requests to make or revise this style of video.
---

# Photo Dump Calendar

If no photos are available, ask the user to upload a background and at least one tile photo, and give an example: “第一张当底图，其他放进去，标题 October dump，先做一版。” If the user says more uploads are coming, wait until they say they are done or ask for a first version.

Use the marked background or the first photo in attachment order. Include every other photo. Use the supplied month/year, infer the month from the title if possible, and default to the current year. If no month or title is supplied, use the current month and an English title such as October dump. Treat default photo placements as visual choices. Assign a date only when the user specifies it. Reuse prior placements and timings for revisions where possible.

Run the bundled renderer with Python 3, Pillow 10.1+ and FFmpeg with libx264, GIF, palettegen and paletteuse support. Use available local copies of the uploads. Check dependencies before rendering and obtain missing ones using the environment's supported workflow.

Use the soundtrack the user explicitly requests first. Otherwise reuse an accessible audio file or reference video the user previously designated as their default soundtrack. Set `audio` to the local path of that file. When the user has supplied no soundtrack, omit `audio` to use the bundled `assets/Reference_Piano_Left_Hand.wav` automatically. This asset is resolved relative to the installed skill, independently of the manifest location. Set `audio` to null only when the user requests silence. If a user-specified soundtrack cannot be read or has no audio stream, ask for a replacement.

Run `python scripts/render.py manifest.json output.mp4` with paths to the script, manifest and output in the current environment. Each run creates both `output.mp4` and `output.gif` in the same output directory. The MP4 is 1080×1920 at 30 fps and approximately 8.3 seconds. The GIF preserves the full animation at double speed, approximately 4.15 seconds, at 540×960 and 20 fps with infinite looping. GIF has no audio; the MP4 follows the soundtrack rules above. Stage both files successfully before delivery, and regenerate both on revisions. The manifest uses absolute or manifest-relative paths:

```json
{
  "background": "beach.jpg",
  "title": "October dump",
  "year": 2026,
  "month": 10,
  "photos": ["first.jpg", {"path": "second.jpg", "day": 15, "center": [0.5, 0.3]}]
}
```

Photo objects optionally accept `slot` (zero-based grid cell), `crop` (left, top, right, bottom in source pixels after orientation), `center` (two normalized crop anchors), and `start` and `end` in seconds. Inspect the source thumbnails when choosing custom crops. Use the renderer’s printed JSON as a record of resolved placements and times for revisions. Keep manifest and source photos in the current working session when available.
 If multiple photos share a slot, stagger their appearance and use explicit end times to avoid covering a photo before it can be seen.

Check the video dimensions, duration, and verify with ffprobe that an audio stream is present whenever a soundtrack is expected. Check the GIF dimensions, total duration, animated frames, and infinite looping. Inspect the empty opening, middle collage, and empty ending in both formats for readable text, correct dates, and usable crops. Use the renderer's `outputs` paths to deliver both MP4 and GIF through the current environment's artifact mechanism.
