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
- [应用语言](#应用语言)
- [快捷键](#快捷键)
- [命令](#命令)
- [仓库结构](#仓库结构)
- [更新日志与许可证](#更新日志与许可证)

---

## 简介

`cmd` 是终端中的**个人命令参考**：

- **卡片** — 命令作用、何时使用、何时不用
- **示例** — 可直接复制的命令（`ls -la`、`cd ..` 等）
- **浏览器** — Essential → Recent → Useful，fzf 搜索
- **快捷键** — 在 zsh 提示符按 Ctrl+O / F2

不能替代 `man`，但能让你**更快找到并记住**命令。

## 系统要求

| 组件 | 版本 | 说明 |
|------|------|------|
| **macOS** | 13+ | 通过 `apropos` 建索引 |
| **Python** | 3.9+ | 仅标准库 |
| **zsh** | 5.8+ | 默认 shell |
| **fzf** | 0.30+ | `brew install fzf` — 浏览器必需 |
| **Terminal** | 任意 | 快捷键仅在 zsh 输入行生效 |

```bash
sw_vers                    # macOS
python3 --version          # Python 3.9+
zsh --version              # zsh 5.8+
fzf --version              # fzf 0.30+
cmd --version              # cmd 0.1.0
```

## 安装

```bash
brew install fzf
git clone https://github.com/godshiba/cmd.git ~/scripts/cmd
cd ~/scripts/cmd
bash install.sh
./cmd index
```

`~/.zshrc`：

```bash
unalias cmd 2>/dev/null
export PATH="$HOME/scripts/cmd:$PATH"
source "$HOME/scripts/cmd/shell/cmd.widget.zsh"
```

```bash
source ~/.zshrc
cmd ls
cmd lang zh    # 界面语言
```

## 应用语言

```bash
cmd lang        # 语言菜单 (fzf)
cmd lang zh     # 直接设为中文
cmd lang en     # English
cmd lang ru     # Русский
```

或 `export CMD_LANG=zh` — 保存在 `~/.cmd/config.json`。

浏览器顶部提示：`语言: cmd lang`

## 快捷键

| 按键 | 作用 |
|------|------|
| **Ctrl+O** | 浏览器 |
| **F2** | 备用 |

`cmd-keys` — 查看快捷键绑定

## 命令

| 命令 | 说明 |
|------|------|
| `cmd` | fzf 浏览器 |
| `cmd ls` | 命令卡片 |
| `cmd <关键词>` | 关键词搜索（如 `cmd grep`） |
| `cmd related ls` | 相关命令 |
| `cmd --pick` | 选择命令（shell 组件） |
| `cmd --pick-example ls` | 选择示例 |
| `cmd --copy ls` | 复制第一个示例 |
| `cmd --all` | 包含所有系统命令 |
| `cmd index` | 重建 macOS 索引 |
| `cmd edit 名称` | 个人卡片 |
| `cmd lang` | 语言菜单 (fzf) |
| `cmd lang en\|ru\|zh` | 直接设置语言 |
| `cmd --version` | 显示版本 |

**浏览器：** Enter = 卡片 · Ctrl+E = 示例 · Esc = 关闭

完整英文文档：[README.md](README.md)

## 仓库结构

```
cmd/                              # https://github.com/godshiba/cmd
├── README.md / README.ru.md / README.zh-CN.md
├── VERSION                       # 0.1.0
├── install.sh                    # PATH 与权限
├── scripts/verify.sh             # 本地测试
├── scripts/migrate_legacy.py     # 迁移 data/*.json → data/legacy/
├── scripts/capture_evidence.py   # 验证产物 (CMD_SCRATCH)
├── tests/                        # smoke + evidence 测试
├── CHANGELOG.md, LICENSE
├── cmd, main.py
├── data/
│   ├── locales/{en,ru,zh}/       # 主数据
│   ├── legacy/                   # categories + useful fallback（见 LEGACY.md）
│   └── LEGACY.md
├── lib/, shell/cmd.widget.zsh
└── ~/.cmd/                       # 用户数据
```

## 更新日志与许可证

- [CHANGELOG.md](CHANGELOG.md)
- [Releases](https://github.com/godshiba/cmd/releases)
- [MIT](LICENSE)