# Photo Dump Calendar · 照片日历短片

上传一张底图和一组照片，生成约 8 秒的竖屏月度回顾。小照片会在真实月份的日历格中依次出现，再逐格退场。

## 安装

把下面这句话发给支持 Skills 的 Codex：

> 请从 https://github.com/HuHana77/photo-dump-calendar 安装 Photo Dump Calendar Skill。安装目录是仓库里的 `photo-dump-calendar/`。

渲染环境需要 Python 3、Pillow 10.1 或更新版，以及支持 libx264 的 FFmpeg。

## 使用

上传照片，然后复制这句话：

> 用 Photo Dump Calendar。第一张当底图，其他放进日历格，标题写 October dump，先做一版。

分批上传时，可以先说「还没发完」。也可以指定年份、把某张图放到某一天，或上传配乐。默认输出 1080 × 1920 的无声 MP4。

## 文件

- [SKILL.md](photo-dump-calendar/SKILL.md) 是 Skill 的使用入口。
- [render.py](photo-dump-calendar/scripts/render.py) 负责排版、动画和视频导出。
