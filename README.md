# yoyozai-ai-toolkit

> 老付 / 悠仔(WorkBuddy) 的 AI 实用工具箱。沉淀经实战验证的自用脚本，践行「别从零造轮子」——能复用开源就复用，能白嫖现成就白嫖。

本仓是 **[GitHub×AI 杠杆工作法]** 的实体化：一个非程序员，用 AI 在 GitHub 上搜现成开源 → 复用改造 → 把重复劳动交给工具。仓库本身也是「AI 帮我干活」的样板。

## 内容

| 文件 | 用途 | 来源 |
|---|---|---|
| `transcribe_douyin.py` | 本地抖音视频口播稿提取（`yt-dlp` 拉流 + 本地 `Whisper` 转写），离线零 API 费、内容不出本机 | 对标视频《你想到的项目 GitHub 上 99% 已有》（姜学长）实践 |

## 快速开始

```bash
# 1. 准备 Python 环境（建议 venv 装 D 盘，不占 C 盘）
python -m venv D:/WB工作空间/工具/venv
D:/WB工作空间/工具/venv/Scripts/pip install yt-dlp openai-whisper imageio-ffmpeg

# 2. 提取某条抖音视频的口播稿
python transcribe_douyin.py "https://www.douyin.com/video/xxxx"
```

### 参数

```text
url            抖音视频 URL（必填）
--out          输出 txt 路径（默认与音频同目录，同名 .txt）
--model        Whisper 模型大小：tiny/base/small/medium/large（越大越准越慢，默认 base）
--ffmpeg-dir   ffmpeg.exe 所在目录（Windows 必须注入 PATH，默认老付本机路径）
--cookies      yt-dlp cookie 来源：edge / chrome / 或 cookie 文件路径（默认 edge）
```

### 注意事项

- **抖音需带已登录浏览器的 cookie 才能拉流**（`--cookies` 默认 `edge`）。
- **提取前请完全退出该浏览器**（Windows 默认「关闭后继续运行后台应用」会残留进程，锁住 cookie 数据库导致失败）。用任务管理器结束所有 `msedge.exe` / `chrome.exe` 后再跑。
- 机器转写稿会有 ASR 错字，建议人工润色后再入库 / 发布。

## 原则

- **本地优先、零常驻、不占 C 盘**：大文件与 Python 环境装 D 盘，不装任何后台常驻服务。
- **仓库不含任何敏感信息**：真实姓名、账号、密码、执照、身份证、资金类数据不进仓（见 `.gitignore`）。
- 所有脚本默认走「AI 帮我干活」思路，把重复劳动交给工具。

## 关联（知识库主线）

- AI 服务（贴钱不贴技术）+ 副业变现 5 法（方法 5 最稳：AI×原有技能）。
- `GitHub×AI杠杆工作法`：非程序员用 AI 搜 GitHub 复用现成开源，本仓即实践。

## License

代码以 MIT 协议开源，可自由使用、修改、商用。引用时保留出处即可。
