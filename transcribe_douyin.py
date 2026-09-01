"""
抖音口播稿离线提取（yt-dlp 拉流 + 本地 Whisper 转写）
=====================================================
完全离线、零 API 费、内容不出本机。适合把竞品/对标视频的口播稿
提取成文本，用于知识库蒸馏、选题拆解、脚本改写。

依赖（本地 Python venv，装 D 盘，不占 C 盘）：
    pip install yt-dlp openai-whisper imageio-ffmpeg

用法：
    # 老付本机（ffmpeg 在 D:/WB工作空间/工具）：
    python transcribe_douyin.py "https://www.douyin.com/video/xxxx"

    # 别人 clone 后，指定 ffmpeg 目录与输出：
    python transcribe_douyin.py "URL" --ffmpeg-dir "C:/ffmpeg/bin" --out out.txt --model small

注意：抖音需带已登录浏览器的 cookie 才能拉流（--cookies 默认 edge）。
提取前请确保该浏览器完全退出（后台进程会锁住 cookie 数据库）。
"""
import os
import argparse
import subprocess
import pathlib


# ffmpeg 目录默认值（老付本机）。Windows 下 Whisper 调 ffmpeg 子进程时，
# 必须把它以反斜杠形式注入 PATH，否则 subprocess 找不到 ffmpeg.exe。
DEFAULT_FFMPEG_DIR = r"D:\WB工作空间\工具"


def parse_args():
    ap = argparse.ArgumentParser(
        description="本地抖音口播稿提取：yt-dlp 拉流 + Whisper 转写（离线零 API 费）"
    )
    ap.add_argument("url", help="抖音视频 URL，如 https://www.douyin.com/video/xxxx")
    ap.add_argument("--out", default=None, help="输出 txt 路径（默认与音频同目录，同名 .txt）")
    ap.add_argument("--model", default="base",
                    help="Whisper 模型大小：tiny/base/small/medium/large（越大越准越慢）")
    ap.add_argument("--ffmpeg-dir", default=DEFAULT_FFMPEG_DIR,
                    help="ffmpeg.exe 所在目录（Windows 需注入 PATH）")
    ap.add_argument("--cookies", default="edge",
                    help="yt-dlp cookie 来源：edge / chrome / 或 cookie 文件路径")
    return ap.parse_args()


def main():
    args = parse_args()

    # 注入 ffmpeg 到 PATH（Windows 必须）
    os.environ["PATH"] = args.ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    import whisper  # 延迟导入，便于 --help 不依赖 torch

    out_dir = pathlib.Path(args.out).parent if args.out else pathlib.Path(".")
    out_dir.mkdir(parents=True, exist_ok=True)
    audio_tpl = str(out_dir / "audio.%(ext)s")

    # 1) 下载音轨
    cmd = ["yt-dlp", "--cookies-from-browser", args.cookies,
           "-f", "bestaudio/best", "--no-playlist", "-o", audio_tpl, args.url]
    print(">>> 下载音轨:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    audio_files = sorted(out_dir.glob("audio.*"))
    if not audio_files:
        raise SystemExit("未找到下载的音频文件，请检查 URL 与 cookie 来源")
    src = audio_files[-1]

    # 2) Whisper 转写
    dst = args.out or str(src.with_suffix(".txt"))
    print(f"loading {args.model} model ...")
    model = whisper.load_model(args.model)
    print("transcribing ...")
    result = model.transcribe(str(src), language="zh")
    text = result["text"].strip()
    with open(dst, "w", encoding="utf-8") as f:
        f.write(text)
    print("DONE chars=", len(text))
    print("---- preview ----")
    print(text[:500])


if __name__ == "__main__":
    main()
