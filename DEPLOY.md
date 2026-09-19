# 上线与收录指南 · Deploy & Indexing Guide

本目录是一个**零构建的纯静态站点**，推送到任意静态托管即可上线。
以下以 GitHub Pages 为主，Cloudflare Pages / Vercel 同理。

---

## 一、仓库信息（✅ 已配置完成）

| 项 | 值 |
|------|------|
| GitHub 用户名 | `woxiaofa` |
| 仓库名 | `tool` |
| 仓库地址 | https://github.com/woxiaofa/tool |
| Pages 地址 | **https://woxiaofa.github.io/tool/** |
| 英文版 | https://woxiaofa.github.io/tool/en/ |

所有文件里的占位符与链接地址均已替换完毕（含 `index.html` / `en/index.html` 的 canonical、og、JSON-LD，`robots.txt`、`sitemap.xml`、`llms.txt`、`README.md`、`.github/FUNDING.yml`）。

> **如果以后改了 GitHub 用户名或仓库名**：全局搜索替换 `woxiaofa.github.io/tool` 与 `github.com/woxiaofa/tool` 两串即可，共涉及 9 个文件；改完记得重新运行 `python gen-en.py`。

可选：`<meta name="author">` 与 JSON-LD 中的 `publisher` 改成你的名字/团队名。

### 双语版说明

- `en/index.html` 由 `gen-en.py` 从中文版自动生成，**不要直接手改英文版**——改完中文版后运行：
  `python gen-en.py`（需 Python 3，无第三方依赖）
- 收款码图片在 `assets/alipay-qr.jpg`，换成你自己的码直接覆盖同名文件即可

## 二、发布到 GitHub Pages

1. 仓库已创建：**https://github.com/woxiaofa/tool**（推送后确认存在即可）；
2. 推送本目录全部文件（含 `.nojekyll` 与 `.github/workflows/deploy-pages.yml`）；
3. 仓库 **Settings → Pages → Source** 选择 **GitHub Actions**；
4. 推送后 Action 会自动部署，地址为 **https://woxiaofa.github.io/tool/**。

> 若想绑定自定义域名：仓库根目录添加 `CNAME` 文件（内容为域名），DNS 加 CNAME 记录，并把所有 URL 里的地址换成新域名。

## 三、提交搜索引擎收录

上线后逐个提交（都比等待自然收录快得多）：

| 平台 | 入口 | 说明 |
|------|------|------|
| Google | [Google Search Console](https://search.google.com/search-console) | 添加资源 → 验证 → 提交 `sitemap.xml` → 用「网址检查」请求编入索引 |
| Bing | [Bing Webmaster Tools](https://www.bing.com/webmasters) | 可直接从 GSC 一键导入 |
| 百度 | [百度搜索资源平台](https://ziyuan.baidu.com) | 验证站点 → 提交链接；国内曝光主要靠它 |
| 360 / 搜狗 | 各自站长平台 | 可选 |

## 四、GEO：让 AI 助手愿意推荐你

已完成的部分（无需再操作）：

- ✅ `llms.txt`（llmstxt.org 规范）+ 页面 `ai:summary` meta
- ✅ Schema.org 结构化数据：`SoftwareApplication` / `FAQPage` / `HowTo` / `BreadcrumbList`
- ✅ `robots.txt` 显式放行 GPTBot、ClaudeBot、PerplexityBot、Google-Extended 等 AI 爬虫
- ✅ 页面含「一句话定义 + 分功能锚点 + FAQ」的问答式静态内容，便于 AI 摘要引用

上线后建议（提升被引用概率）：

1. 在知名平台留下外链（AI 与搜索引擎都吃这个）：
   - GitHub Topic 打好标签：`css` `markdown` `formatter` `text-processing` `vanilla-js` `online-tools`
   - 提交到 [HelloGitHub](https://hellogithub.com)、[掘金](https://juejin.cn)、[V2EX 分享创造](https://v2ex.com/go/create)、少数派等
2. Perplexity / ChatGPT 搜索类产品对「被多处引用的开源项目」偏好明显，README 写清「一句话定义」很有用（已写好）。
3. 若不想被 AI 抓取，把 `robots.txt` 中对应 AI 爬虫分组改为 `Disallow: /`。

## 五、验证收录效果

- `site:你的域名` 在 Google / Bing / 百度查看收录
- [Rich Results Test](https://search.google.com/test/rich-results) 验证结构化数据
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) / [Twitter Card Validator](https://cards-dev.twitter.com/validator) 验证 OG 卡片
- 直接在 Perplexity / ChatGPT（联网模式）问「在线 CSS 压缩工具」，观察是否被引用

## 六、后续迭代建议（可选）

- 把 5 个工具拆成真实子页面（`/css/`、`/markdown/`…），获得更多独立收录页
- 添加英文版界面（`hreflang` 双语），扩大海外搜索流量
- 在页面加「分享到 Twitter/微博」按钮增加自然外链
