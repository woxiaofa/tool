# 文本格式化工具箱 · Text Formatter Toolbox

> 免费开源的纯前端在线文本格式化工具 —— CSS/HTML 压缩美化、Markdown 与 HTML 互转、段落整理、中英排版、JSON/URL/Base64 编解码。
> **纯浏览器本地运行，输入内容不上传服务器，可离线使用。**

A free & open-source, single-file, **pure front-end** text formatter toolbox:
CSS/HTML minify & beautify, Markdown ↔ HTML conversion, paragraph cleanup, CJK–Latin typography spacing, punctuation full/half-width conversion, and JSON/URL/Base64 codecs.
**100% local — nothing ever leaves your browser. Works offline.**

在线使用 · Live Demo: **https://woxiaofa.github.io/tool/** · English: **[/en/](https://woxiaofa.github.io/tool/en/)**

> ☕ 如果这个工具帮到了你，欢迎[赞助支持](#-赞助支持--sponsor) /
> If this tool helps you, consider [supporting the author](#-赞助支持--sponsor).
>
> <img src="assets/alipay-qr.jpg" alt="支付宝 / Alipay" width="120"> <img src="assets/wechat-qr.jpg" alt="微信 / WeChat Pay" width="120">

[![GitHub License](https://img.shields.io/github/license/woxiaofa/tool?style=flat-square)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/woxiaofa/tool?style=flat-square)](https://github.com/woxiaofa/tool/stargazers)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](https://github.com/woxiaofa/tool/pulls)
[![Vanilla JS](https://img.shields.io/badge/dependency-none-informational?style=flat-square)](#特性--features)
[![GitHub Pages](https://img.shields.io/badge/deploy-GitHub%20Pages-222?style=flat-square)](https://pages.github.com/)

---

## ✨ 特性 · Features

| | 功能 | 说明 |
|---|------|------|
| 1 | **CSS 压缩 / 美化** | 压缩、多行格式化、单行格式化，支持一键还原原始内容；字符串与注释先保护再处理，不会误删 `content: "a b"` 里的空格 |
| 2 | **HTML ↔ Markdown 互转** | 双向转换 + HTML 自身的压缩与美化；支持表格、嵌套列表、任务列表、围栏代码块 |
| 3 | **段落整理** | 去首行/行尾空格、合并空行、段落智能拼接、按标点一句一行、去重、排序 |
| 4 | **中英排版** | 中英文之间自动加空格、英文标点后补空格、中英标点互转、全半角互转、大小写转换；自动保护 URL / 邮箱 / 代码块 |
| 5 | **通用转换** | JSON 美化与压缩、HTML 实体转义/反转义、URL 编解码、Base64 编解码（UTF-8 中文无乱码） |

## 🚀 快速开始 · Quick Start

### 在线使用（推荐）

直接打开 **https://woxiaofa.github.io/tool/** 即可，无需安装、无需注册。

### 本地使用

整个工具就是 **一个 `index.html` 文件，零依赖**，下载后双击打开即可：

```bash
git clone https://github.com/woxiaofa/tool.git
# 然后直接用浏览器打开 tool/index.html
```

也可以从发布页下载 `tool.zip`，解压即用 —— 适合内网/无网环境。

### 本地开发预览

```bash
# 任选一种静态服务器
npx serve .
python -m http.server 8080
```

## 📖 使用方法 · How to Use

1. 把文本粘贴到左侧 **输入** 框（或点「填入示例」）；
2. 左侧分类切换工具，点按钮执行；快捷键 `Ctrl + Enter`（macOS `⌘ + Enter`）执行默认操作；
3. 右侧 **输出** 框查看结果，一键复制，或「结果回填输入框」叠加第二次处理。

URL 锚点直达具体工具：`#css` · `#htmlmd` · `#para` · `#typo` · `#common` · `#faq`

## 🔒 隐私 · Privacy

- ❌ 无后端接口　❌ 无统计脚本　❌ 无第三方 CDN　❌ 无 Cookie 追踪
- ✅ 唯一存储：深色模式偏好保存在浏览器 `localStorage`
- 适合处理配置文件、合同文本、内部文档等敏感内容

## 🛠 技术栈 · Tech

- 单文件 `index.html`，原生 JavaScript（约 900 行，含自研 CSS 词法保护与 Markdown 解析器）
- CSS 变量实现明暗主题，响应式布局，PWA（manifest + Service Worker）可安装离线使用
- 结构化数据：Schema.org（`SoftwareApplication` / `FAQPage` / `HowTo`）+ `llms.txt`，对搜索引擎与 AI 助手友好

## 🤝 贡献 · Contributing

欢迎 Issue 与 PR！新功能建议按「纯前端、零依赖、单文件」的约束实现。

## 📄 许可证 · License

[MIT](LICENSE) © 2026

---

**关键词 Keywords**: CSS压缩, CSS格式化, CSS美化, HTML压缩, HTML美化, Markdown转HTML, HTML转Markdown, 中英文之间加空格, 中英混排, 全角半角转换, 中文标点转换, JSON美化, Base64编码, URL编码, 在线文本格式化, 文本处理工具, css minifier, html formatter, markdown converter, cjk spacing, pangu spacing
