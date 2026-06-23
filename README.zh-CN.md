# cmd

**macOS 终端命令导航器** — 命令卡片、示例、fzf 浏览器、快捷键。

<p align="center">
  <strong>文档</strong>:
  <a href="README.md">English</a> ·
  <a href="README.ru.md">Русский</a> ·
  <a href="README.zh-CN.md"><b>中文</b></a>
</p>

<p align="center">
  <a href="https://github.com/godshiba/cmd/releases"><img src="https://img.shields.io/github/v/release/godshiba/cmd?style=flat-square" alt="Release"></a>
  <img src="https://img.shields.io/badge/platform-macOS%2013+-000?style=flat-square" alt="macOS">
  <img src="https://img.shields.io/badge/python-3.9+-3776ab?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/shell-zsh%205.8+-89b4fa?style=flat-square" alt="zsh">
  <img src="https://img.shields.io/badge/fzf-0.30+-fb4934?style=flat-square" alt="fzf">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT">
</p>

---

## 目录

- [简介](#简介)
- [系统要求](#系统要求)
- [安装](#安装)
- [文档语言](#文档语言)
- [应用语言](#应用语言)
- [快捷键](#快捷键)
- [命令](#命令)
- [仓库结构](#仓库结构)
- [更新日志与许可证](#更新日志与许可证)

---

## 简介

`cmd` 是终端中的**个人命令参考**：卡片、示例、fzf 浏览器、Ctrl+O 快捷键。

## 系统要求

| 组件 | 版本 | 说明 |
|------|------|------|
| **macOS** | 13+ | 通过 `apropos` 建索引 |
| **Python** | 3.9+ | 仅标准库 |
| **zsh** | 5.8+ | 默认 shell |
| **fzf** | 0.30+ | `brew install fzf` |

```bash
sw_vers && python3 --version && zsh --version && fzf --version && cmd --version
```

## 安装

```bash
brew install fzf
git clone https://github.com/godshiba/cmd.git ~/scripts/cmd
cd ~/scripts/cmd && ./cmd index
```

`~/.zshrc`：

```bash
unalias cmd 2>/dev/null
export PATH="$HOME/scripts/cmd:$PATH"
source "$HOME/scripts/cmd/shell/cmd.widget.zsh"
```

## 文档语言

| 语言 | 文件 |
|------|------|
| English | [README.md](README.md) |
| Русский | [README.ru.md](README.ru.md) |
| **中文** | [README.zh-CN.md](README.zh-CN.md) |

链接：https://github.com/godshiba/cmd/blob/main/README.zh-CN.md

## 应用语言

```bash
cmd lang        # 语言菜单 (fzf)
cmd lang zh     # 直接设为中文
```

浏览器顶部提示：`语言: cmd lang`

## 快捷键

| 按键 | 作用 |
|------|------|
| **Ctrl+O** | 浏览器 |
| **F2** | 备用 |

## 命令

| 命令 | 说明 |
|------|------|
| `cmd` | 浏览器 |
| `cmd ls` | 命令卡片 |
| `cmd index` | 重建索引 |
| `cmd lang` | 界面语言 |
| `cmd --version` | 版本号 |

## 仓库结构

```
cmd/                     → github.com/godshiba/cmd
├── README.md / .ru.md / .zh-CN.md
├── VERSION, CHANGELOG.md, LICENSE
├── cmd, main.py, data/, lib/, shell/
└── ~/.cmd/              → 用户数据
```

## 更新日志与许可证

- [CHANGELOG.md](CHANGELOG.md)
- [Releases](https://github.com/godshiba/cmd/releases)
- [MIT](LICENSE)