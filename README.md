# BiliRecap

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)

一个轻量级的 哔哩哔哩 缓存视频提取脚本，专为 macOS 优化。能够自动修复 `.m4s` 文件头，并将分离的音视频流合并为完整的 `.mp4` 格式。

---

## ✨ 功能特点 (Features)

* **🍎 macOS 深度优化**：完美处理 Mac 终端拖拽文件夹产生的路径转义符（空格、引号）。
* **⚡️ 无损合成**：基于 FFmpeg 的流拷贝（Stream Copy）技术，不重编码，秒级完成，画质 100% 还原。
* **📂 自动命名**：解析 `videoInfo.json`，自动提取视频标题并清理系统非法字符。
* **📦 批量处理**：支持一次性拖入多个文件夹或父目录进行递归扫描。

---

## 🔬 核心原理 (Technical Principles)

### 1. 文件头去混淆 (Deobfuscation)
B 站移动端及 PC 端缓存的 `.m4s` 文件并非标准的 MP4 格式，其头部被填充了若干字节的无效数据。
* **修复逻辑**：脚本在二进制流中检索 `ftyp` (File Type Box) 标志位。
* **定位公式**：
    $$StartPoint = \text{Offset}(b'ftyp') - 4$$
    定位后截取该位置之后的所有数据，即可恢复标准 ISOBMFF 容器结构。

### 2. 音视频混流 (Muxing)
由于 B 站采用 DASH 流媒体技术，视频（体积最大）与音频（体积最小）是分离存储的。
* **处理方案**：程序自动匹配文件夹内大小极端的两个 `.m4s` 文件，调用 FFmpeg 将其封装进 `.mp4` 容器。

---

## 🛠 安装指南 (Installation)

### 1. 环境依赖 (macOS)
确保你的系统中已安装 **Python 3** 和 **FFmpeg**。
推荐使用 [Homebrew](https://brew.sh/) 安装：
```bash
brew install ffmpeg
```
### 2. 获取工具
```Bash
git clone [https://github.com/GolLight/BiliRecap.git](https://github.com/GolLight/BiliRecap.git)
cd BiliRecap
📖 使用方法 (Usage)
运行脚本：

```Bash
python3 main.py
```
#### 第一步：将你想提取的缓存文件夹（一个或多个,多个需要多次拖入需要空格）直接拖入终端窗口。

#### 第二步：设置输出目录

## ⚠️ 免责声明 (Disclaimer)
本工具仅供学习研究 Python 文件 IO 与二进制流处理之用。

请勿将本工具用于任何侵犯版权或非法下载的行为。

衍生出的任何法律责任由使用者自行承担。

后续计划：本项目后续可能开发基于跨端框架的图形界面程序（GUI），敬请期待。
