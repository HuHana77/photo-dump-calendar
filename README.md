# Photo Dump Calendar · 照片日历短片

上传一张底图和一组照片，生成约 8 秒的竖屏月度回顾。小照片会在真实月份的日历格中依次出现，再逐格退场。每次同时生成 MP4 视频和约 4 秒的双倍速循环 GIF。

## 安装

把下面这句话发给支持 Skills 的 Codex：

> 请从 https://github.com/HuHana77/photo-dump-calendar 安装 Photo Dump Calendar Skill。安装目录是仓库里的 `photo-dump-calendar/`。

渲染环境需要 Python 3、Pillow 10.1 或更新版，以及支持 libx264、GIF、palettegen 和 paletteuse 的 FFmpeg。

## 使用

上传照片，然后复制这句话：

> 用 Photo Dump Calendar。第一张当底图，其他放进日历格，标题写 October dump，先做一版。

分批上传时，可以先说「还没发完」。也可以指定年份、把某张图放到某一天。同时输出 1080 × 1920、30 帧/秒、约 8.3 秒的 MP4，以及 540 × 960、20 帧/秒、约 4.15 秒的 GIF。GIF 保留完整出入场动画，以双倍速持续循环播放。MP4 使用下述配乐规则。

## 配乐

Skill 自带钢琴配乐 [Reference_Piano_Left_Hand.wav](photo-dump-calendar/assets/Reference_Piano_Left_Hand.wav)，没有提供音乐时会自动加入视频。

你也可以上传音乐或带音轨的参考视频，并告诉 Codex 使用哪份音频，或指定一份可访问的音频作为自己的默认配乐。单次指定的音乐优先，其次使用你指定的默认配乐，否则使用 Skill 自带的钢琴配乐。明确要求静音时输出静音版。

直接运行渲染脚本时，省略 manifest 的 `audio` 字段会使用自带配乐，填写音频路径会使用该文件，设置 `"audio": null` 会输出静音版。

运行 `python photo-dump-calendar/scripts/render.py manifest.json output.mp4`，会在同一目录生成 `output.mp4` 和 `output.gif`。修改照片或时间后重新运行，会同时更新两个成片。

## 文件

- [SKILL.md](photo-dump-calendar/SKILL.md) 是 Skill 的使用入口。
- [render.py](photo-dump-calendar/scripts/render.py) 负责排版、动画和视频导出。
