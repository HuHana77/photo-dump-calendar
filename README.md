# Photo Dump Calendar · 照片日历短片

上传一张底图和一组照片，生成约 8 秒的竖屏月度回顾。小照片会在真实月份的日历格中依次出现，再逐格退场。

## 安装

把下面这句话发给支持 Skills 的 Codex：

> 请从 https://github.com/HuHana77/photo-dump-calendar 安装 Photo Dump Calendar Skill。安装目录是仓库里的 `photo-dump-calendar/`。

渲染环境需要 Python 3、Pillow 10.1 或更新版，以及支持 libx264 的 FFmpeg。

## 使用

上传照片，然后复制这句话：

> 用 Photo Dump Calendar。第一张当底图，其他放进日历格，标题写 October dump，先做一版。

分批上传时，可以先说「还没发完」。也可以指定年份、把某张图放到某一天。输出为 1080 × 1920 MP4。

## 配乐

上传音乐或带音轨的参考视频，并告诉 Codex 使用哪份音频。你也可以把一份可访问的音频指定为自己的默认配乐。单次指定的音乐优先。如果还没有配乐，Skill 会请你提供一份，或者选择静音。仓库提供渲染代码，配乐由使用者提供。

## 文件

- [SKILL.md](photo-dump-calendar/SKILL.md) 是 Skill 的使用入口。
- [render.py](photo-dump-calendar/scripts/render.py) 负责排版、动画和视频导出。
