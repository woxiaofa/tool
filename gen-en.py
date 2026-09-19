# -*- coding: utf-8 -*-
"""
gen-en.py — 从 index.html（中文版）生成 en/index.html（英文版）
策略：
  1. 结构级替换：SEO 内容区、JSON-LD、canonical 自动修正脚本 → 英文版
  2. 文案字典替换：UI 按钮/工具名/分组/提示语（按长度降序，避免子串误替换）
  3. 相对资源路径加 ../ 前缀；canonical / og:url 指向 /en/
之后如修改中文版，重跑本脚本即可同步英文版。
"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'index.html')
DST = os.path.join(BASE, 'en', 'index.html')

ROOT = 'https://woxiaofa.github.io/tool/'
EN = 'https://woxiaofa.github.io/tool/en/'

# ---------------------------------------------------------------
# 1. 英文版 SEO 内容区（id 与中文版一致，锚点互通）
# ---------------------------------------------------------------
EN_SEO = '''<div class="seo">

    <article class="card seo-card" id="intro">
        <h2>What is Text Formatter Toolbox?</h2>
        <p class="lead">
            <strong>Text Formatter Toolbox is a free, open-source, pure front-end online text toolkit</strong>
            covering <b>CSS minify &amp; beautify</b>, <b>HTML minify &amp; format</b>,
            <b>Markdown &harr; HTML conversion</b>, <b>paragraph cleanup</b>,
            <b>CJK&ndash;Latin typography spacing</b>, <b>full/half-width punctuation conversion</b>,
            plus URL, Base64 and JSON codecs. 5 categories, 30+ one-click actions &mdash;
            <strong>no sign-up, no limits, no uploads</strong>.
        </p>
        <p>
            Every conversion runs <strong>locally in your browser</strong> with JavaScript &mdash;
            nothing is ever sent to a server, and no cookies or tracking are involved. It works offline
            (installable as a PWA). The whole toolbox is a single HTML file with zero dependencies
            and zero external requests &mdash; save it to disk and it works as a desktop app.
        </p>
        <div class="chips">
            <a class="chip" href="#css">CSS Minify</a>
            <a class="chip" href="#htmlmd">Markdown</a>
            <a class="chip" href="#para">Paragraphs</a>
            <a class="chip" href="#typo">CJK Spacing</a>
            <a class="chip" href="#common">Base64 / URL</a>
            <a class="chip" href="#faq">FAQ</a>
        </div>
    </article>

    <article class="card seo-card" id="features">
        <h2>Features: 5 categories of text tools</h2>
        <div class="feature-grid">
            <section class="feature-card" id="css">
                <h3>1. CSS Minify / Beautify</h3>
                <p>Expand one-line stylesheets into readable form, or strip all whitespace for production.</p>
                <ul>
                    <li>CSS minify (comments, whitespace, trailing semicolons)</li>
                    <li>Format multi-line (one declaration per line)</li>
                    <li>Format single-line (one rule per line)</li>
                    <li>Restore original anytime</li>
                </ul>
            </section>
            <section class="feature-card" id="htmlmd">
                <h3>2. HTML &harr; Markdown</h3>
                <p>Switch between writing documents and writing web pages, keeping headings, lists and tables.</p>
                <ul>
                    <li>HTML &rarr; Markdown</li>
                    <li>Markdown &rarr; HTML</li>
                    <li>HTML minify / beautify</li>
                    <li>Code blocks, tables, task lists supported</li>
                </ul>
            </section>
            <section class="feature-card" id="para">
                <h3>3. Paragraph Cleanup</h3>
                <p>Fix messy text copied from Word, PDF or web pages.</p>
                <ul>
                    <li>Trim leading / trailing spaces</li>
                    <li>Merge or remove blank lines</li>
                    <li>Smart paragraph joining</li>
                    <li>One sentence per line, dedupe, sort lines</li>
                </ul>
            </section>
            <section class="feature-card" id="typo">
                <h3>4. CJK&ndash;Latin Typography</h3>
                <p>Solve the most common Chinese-English mixed-text typesetting issues.</p>
                <ul>
                    <li>Auto space between CJK and Latin/digits</li>
                    <li>Add space after punctuation</li>
                    <li>Chinese &harr; English punctuation</li>
                    <li>Full-width &harr; half-width</li>
                    <li>Letter case: UPPER / lower / Title / Sentence / iNVERSE</li>
                </ul>
            </section>
            <section class="feature-card" id="common">
                <h3>5. General Conversion</h3>
                <p>Everyday encoding and escaping utilities for developers and writers.</p>
                <ul>
                    <li>JSON beautify / minify</li>
                    <li>HTML entity escape / unescape</li>
                    <li>URL encode / decode</li>
                    <li>Base64 encode / decode (UTF-8 safe)</li>
                </ul>
            </section>
        </div>
    </article>

    <article class="card seo-card" id="how-to">
        <h2>How to use &mdash; three steps</h2>
        <ol class="steps">
            <li><b>Paste text</b>Paste your CSS / HTML / Markdown / plain text into the Input box, or click &ldquo;Load sample&rdquo; to try it.</li>
            <li><b>Pick an action</b>Switch categories on the left and click a button; or press <span class="kbd">Ctrl</span> + <span class="kbd">Enter</span> to run the default action.</li>
            <li><b>Copy the result</b>The Output box updates live. Click &ldquo;Copy result&rdquo;, or feed the result back as input to chain another action.</li>
        </ol>
        <p style="font-size:13px;color:var(--muted)">
            Tip: feed the result back into the input to chain actions, e.g. &ldquo;Markdown &rarr; HTML&rdquo; then &ldquo;HTML minify&rdquo;.
        </p>
    </article>

    <article class="card seo-card" id="faq">
        <h2>FAQ</h2>

        <details class="faq" open>
            <summary>Is this text formatter free?</summary>
            <p>Yes &mdash; completely free and open source under the MIT license. No usage limits, no sign-up, no watermark.</p>
        </details>

        <details class="faq">
            <summary>Is my text uploaded to a server?</summary>
            <p>No. This is a pure front-end tool: every conversion runs in your browser with JavaScript. The page makes no network requests, works offline, and can be installed as a local app.</p>
        </details>

        <details class="faq">
            <summary>Will CSS minification break my styles?</summary>
            <p>Strings, comments and URLs are protected before whitespace removal, so spaces inside <code>content: "a b"</code> are preserved. There is also a &ldquo;Restore original&rdquo; button to roll back anytime.</p>
        </details>

        <details class="faq">
            <summary>Which Markdown syntax is supported?</summary>
            <p>ATX and Setext headings, ordered/unordered/nested lists, task lists, fenced code blocks (with language), blockquotes, horizontal rules, tables with alignment, images, links, autolinks, bold, italic, strikethrough and inline code.</p>
        </details>

        <details class="faq">
            <summary>Why add spaces between Chinese and English?</summary>
            <p>Mixed CJK&ndash;Latin text reads better with a thin gap between Han characters and Latin letters or digits &mdash; a widely recommended Chinese typesetting convention. The tool protects URLs, emails, code blocks and HTML tags, so it never inserts spaces inside them.</p>
        </details>

        <details class="faq">
            <summary>Can I convert Chinese punctuation to English punctuation in bulk?</summary>
            <p>Yes. The CJK&ndash;Latin Typography category offers both directions, covering commas, periods, question/exclamation marks, colons, semicolons and brackets, while skipping decimal points and thousands separators.</p>
        </details>

        <details class="faq">
            <summary>Does Base64 support Chinese characters?</summary>
            <p>Yes. Text is UTF-8 encoded before Base64 and decoded back as UTF-8, so Chinese never turns into mojibake. Line breaks and spaces are ignored when decoding.</p>
        </details>

        <details class="faq">
            <summary>Does it work on mobile? Any shortcuts?</summary>
            <p>Yes, the layout is responsive &mdash; input and output stack vertically on phones. Desktop shortcut: <span class="kbd">Ctrl</span> + <span class="kbd">Enter</span> (macOS: <span class="kbd">&#8984;</span> + <span class="kbd">Enter</span>) runs the first action.</p>
        </details>

        <details class="faq">
            <summary>Can I use it offline?</summary>
            <p>Yes. The whole toolbox is a single index.html with no external dependencies &mdash; save it and double-click to run, or install it to your home screen for offline use.</p>
        </details>
    </article>

    <article class="card seo-card" id="privacy">
        <h2>Privacy</h2>
        <p>
            No backend API, no analytics scripts, no third-party CDN, no tracking cookies.
            The only thing stored is your dark/light theme preference in localStorage.
            Safe for config files, contracts and internal documents.
        </p>
    </article>

    <article class="card seo-card" id="sponsor">
        <h2>Support this project</h2>
        <div class="sponsor-flex">
            <div class="sponsor-info">
                <p>
                    This toolbox is 100% <b>free, ad-free and open-source</b>; hosting and development
                    are paid out of the author's own pocket. If it saved you time,
                    buying the author a coffee is much appreciated &ndash;
                </p>
                <p style="margin-top:10px;font-size:13px;color:var(--muted)">
                    Scan the QR code with Alipay to support &middot; click the code to enlarge
                </p>
            </div>
            <a class="sponsor-qr" href="../assets/alipay-qr.jpg" target="_blank" rel="noopener" title="Alipay QR code (click to enlarge)">
                <img src="../assets/alipay-qr.jpg" alt="Alipay QR code" width="168" height="252" loading="lazy">
            </a>
        </div>
    </article>
</div>

'''

# ---------------------------------------------------------------
# 2. 英文版 JSON-LD
# ---------------------------------------------------------------
EN_JSONLD = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "WebSite",
      "@id": "ENURL#website",
      "url": "ENURL",
      "name": "Text Formatter Toolbox",
      "alternateName": ["文本格式化工具箱", "Online Text Formatter", "CSS Minifier", "Markdown Converter"],
      "description": "A free, open-source, pure front-end online text toolkit: CSS/HTML minify & beautify, Markdown & HTML conversion, paragraph cleanup, CJK-Latin typography and codecs.",
      "inLanguage": "en",
      "license": "https://opensource.org/licenses/MIT",
      "publisher": { "@id": "ENURL#app" }
    },
    {
      "@type": "WebPage",
      "@id": "ENURL#webpage",
      "url": "ENURL",
      "name": "CSS Minifier · Markdown Converter · CJK Typography | Text Formatter Toolbox",
      "isPartOf": { "@id": "ENURL#website" },
      "description": "Free online text formatter toolbox with 5 categories and 30+ one-click actions. Runs entirely in your browser — nothing is uploaded.",
      "inLanguage": "en",
      "dateModified": "2026-09-20",
      "primaryImageOfPage": "ROOTURLog-image.png",
      "breadcrumb": { "@id": "ENURL#breadcrumb" }
    },
    {
      "@type": "BreadcrumbList",
      "@id": "ENURL#breadcrumb",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Home", "item": "ROOTURL" },
        { "@type": "ListItem", "position": 2, "name": "Text Formatter Toolbox", "item": "ENURL" }
      ]
    },
    {
      "@type": ["SoftwareApplication", "WebApplication"],
      "@id": "ENURL#app",
      "name": "Text Formatter Toolbox",
      "url": "ENURL",
      "applicationCategory": "DeveloperApplication",
      "applicationSubCategory": "Text Formatter / Code Beautifier",
      "operatingSystem": "Any (Web Browser)",
      "browserRequirements": "Requires JavaScript. No plugins needed.",
      "softwareVersion": "1.0.0",
      "datePublished": "2026-09-20",
      "dateModified": "2026-09-20",
      "inLanguage": "en",
      "isAccessibleForFree": true,
      "description": "Text Formatter Toolbox is a free, pure front-end online text toolkit offering CSS/HTML minify and beautify, Markdown-HTML conversion, paragraph cleanup, CJK-Latin spacing, punctuation full/half-width conversion, and URL/Base64/JSON codecs. All processing happens locally in the browser — nothing is uploaded.",
      "featureList": [
        "CSS minify", "CSS beautify (multi-line / single-line)", "HTML minify", "HTML beautify",
        "Markdown to HTML", "HTML to Markdown", "JSON beautify & minify",
        "Paragraph & blank-line cleanup", "Dedupe & sort lines", "Auto space between CJK and Latin",
        "Chinese & English punctuation conversion", "Full-width / half-width conversion", "Letter case conversion",
        "HTML entity escape / unescape", "URL encode / decode", "Base64 encode / decode (UTF-8)"
      ],
      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD", "availability": "https://schema.org/InStock" },
      "publisher": { "@type": "Person", "name": "wxf_m" },
      "codeRepository": "https://github.com/woxiaofa/tool",
      "license": "https://opensource.org/licenses/MIT",
      "privacyPolicyURL": "ENURL#privacy"
    },
    {
      "@type": "FAQPage",
      "@id": "ENURL#faq",
      "mainEntity": [
        { "@type": "Question", "name": "Is this text formatter free?", "acceptedAnswer": { "@type": "Answer", "text": "Yes — completely free and open source under the MIT license. No usage limits, no sign-up, no watermark." } },
        { "@type": "Question", "name": "Is my text uploaded to a server?", "acceptedAnswer": { "@type": "Answer", "text": "No. Every conversion runs locally in your browser with JavaScript. The page makes no network requests, works offline, and can be installed as a local app." } },
        { "@type": "Question", "name": "Will CSS minification break my styles?", "acceptedAnswer": { "@type": "Answer", "text": "Strings, comments and URLs are protected before whitespace removal, so spaces inside content strings are preserved. A Restore-original button rolls back anytime." } },
        { "@type": "Question", "name": "Which Markdown syntax is supported?", "acceptedAnswer": { "@type": "Answer", "text": "ATX and Setext headings, ordered/unordered/nested lists, task lists, fenced code blocks, blockquotes, horizontal rules, tables with alignment, images, links, autolinks, bold, italic, strikethrough and inline code." } },
        { "@type": "Question", "name": "Why add spaces between Chinese and English?", "acceptedAnswer": { "@type": "Answer", "text": "Mixed CJK-Latin text reads better with a gap between Han characters and Latin letters or digits — a widely recommended Chinese typesetting convention. URLs, emails, code blocks and HTML tags are protected." } },
        { "@type": "Question", "name": "Can I convert Chinese punctuation to English punctuation in bulk?", "acceptedAnswer": { "@type": "Answer", "text": "Yes, both directions are provided, covering commas, periods, question and exclamation marks, colons, semicolons and brackets, while skipping decimal points and thousands separators." } },
        { "@type": "Question", "name": "Does Base64 support Chinese characters?", "acceptedAnswer": { "@type": "Answer", "text": "Yes. Text is UTF-8 encoded before Base64 and decoded back as UTF-8, so Chinese never turns into mojibake." } },
        { "@type": "Question", "name": "Does it work on mobile? Any shortcuts?", "acceptedAnswer": { "@type": "Answer", "text": "Yes, the layout is responsive. Desktop shortcut: Ctrl + Enter (macOS: Command + Enter) runs the first action of the current tool." } },
        { "@type": "Question", "name": "Can I use it offline?", "acceptedAnswer": { "@type": "Answer", "text": "Yes. The whole toolbox is a single index.html with no external dependencies — save it and open locally, or install it to your home screen." } }
      ]
    },
    {
      "@type": "HowTo",
      "@id": "ENURL#howto",
      "name": "How to format text with Text Formatter Toolbox",
      "description": "Three steps: paste text, pick an action, copy the result.",
      "totalTime": "PT1M",
      "step": [
        { "@type": "HowToStep", "position": 1, "name": "Paste text", "text": "Paste your text into the Input box, or click Load sample." },
        { "@type": "HowToStep", "position": 2, "name": "Pick an action", "text": "Switch categories on the left and click a button, or press Ctrl + Enter." },
        { "@type": "HowToStep", "position": 3, "name": "Copy the result", "text": "Click Copy result, or feed the result back as input to chain another action." }
      ]
    },
    {
      "@type": "ItemList",
      "@id": "ENURL#tools",
      "name": "Tool categories",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "CSS Minify / Beautify", "url": "ENURL#css" },
        { "@type": "ListItem", "position": 2, "name": "HTML <-> Markdown", "url": "ENURL#htmlmd" },
        { "@type": "ListItem", "position": 3, "name": "Paragraph Cleanup", "url": "ENURL#para" },
        { "@type": "ListItem", "position": 4, "name": "CJK-Latin Typography", "url": "ENURL#typo" },
        { "@type": "ListItem", "position": 5, "name": "General Conversion (JSON / URL / Base64)", "url": "ENURL#common" }
      ]
    }
  ]
}
</script>'''

# ---------------------------------------------------------------
# 3. 英文版 canonical 自动修正脚本（不改动 og:image，图片在根目录）
# ---------------------------------------------------------------
EN_FIX = ("<script>(function(){var O='" + EN + "';if(/^file:/.test(location.href))return;"
          "var T=location.origin+location.pathname.replace(/index\\.html$/,'');"
          "document.querySelectorAll('link[rel=canonical]').forEach(function(e){"
          "e.setAttribute('href',e.getAttribute('href').replace(O,T));});"
          "document.querySelectorAll('meta[property=\"og:url\"]').forEach(function(e){"
          "e.setAttribute('content',e.getAttribute('content').replace(O,T));});})();</script>")

# ---------------------------------------------------------------
# 4. 文案字典（长度降序应用，避免子串误替换）
# ---------------------------------------------------------------
PAIRS = [
    ('结果回填输入框', 'Use result as input'),
    ('没有可复制的内容', 'Nothing to copy'),
    ('已复制到剪贴板', 'Copied to clipboard'),
    ('复制失败，请手动 Ctrl+C', 'Copy failed — press Ctrl+C manually'),
    ('没有可下载的结果', 'Nothing to download'),
    ('处理出错，请检查输入内容', 'Processing error — please check the input'),
    ('处理失败：', 'Failed: '),
    ('英文标点后加空格', 'Add space after punctuation'),
    ('全部处理（留白+标点）', 'Process all (spacing + punct)'),
    ('中英文之间加空格', 'Space CJK & Latin'),
    ('段落合并（智能拼接）', 'Join paragraphs (smart)'),
    ('去掉段落首行空格', 'Trim leading spaces'),
    ('一次清理首尾空格', 'Trim both ends'),
    ('按标点一句一行', 'One sentence per line'),
    ('句首字母大写', 'Sentence case'),
    ('中文标点 → 英文标点', 'CN punct → EN punct'),
    ('英文标点 → 中文标点', 'EN punct → CN punct'),
    ('llms.txt（AI 阅读版说明）', 'llms.txt (AI-readable summary)'),
    ('llms.txt（AI 阅读版）', 'llms.txt (for AI)'),
    ('合并多余空行', 'Merge blank lines'),
    ('删除所有空行', 'Remove blank lines'),
    ('CSS 压缩 / 美化', 'CSS Minify / Beautify'),
    ('压缩、多行格式化、单行格式化，随时一键还原', 'Minify, multi-/single-line formatting, one-click restore'),
    ('互转 + HTML 自身的压缩与美化', 'Two-way conversion + HTML minify & beautify'),
    ('去首行/行尾空格、合并空行、按标点断句、去重与排序', 'Trim spaces, merge blank lines, split sentences, dedupe & sort'),
    ('中英文留白、标点后空格、标点与全半角转换', 'CJK–Latin spacing, punctuation & full/half-width conversion'),
    ('JSON 美化与实体、URL、Base64 编解码', 'JSON beautify, HTML entities, URL & Base64 codecs'),
    ('段落整理', 'Paragraph Cleanup'),
    ('中英排版', 'CJK–Latin Typography'),
    ('通用转换', 'General Conversion'),
    ('压缩与格式化', 'Minify & Format'),
    ('格式（多行）', 'Format (multi-line)'),
    ('格式（单行）', 'Format (single-line)'),
    ('还原原始内容', 'Restore original'),
    ('HTML 处理', 'HTML Processing'),
    ('HTML 压缩', 'HTML Minify'),
    ('HTML 美化', 'HTML Beautify'),
    ('空格处理', 'Whitespace'),
    ('去掉行尾空格', 'Trim trailing spaces'),
    ('段落结构', 'Paragraph Structure'),
    ('行操作', 'Line Operations'),
    ('去除重复行', 'Remove duplicate lines'),
    ('行排序（升序）', 'Sort lines (A→Z)'),
    ('行排序（降序）', 'Sort lines (Z→A)'),
    ('留白', 'Spacing'),
    ('标点', 'Punctuation'),
    ('全角 / 半角', 'Full / Half Width'),
    ('全角 → 半角', 'Full-width → Half-width'),
    ('半角 → 全角', 'Half-width → Full-width'),
    ('英文大小写', 'Letter Case'),
    ('全部大写', 'UPPERCASE'),
    ('全部小写', 'lowercase'),
    ('首字母大写', 'Title Case'),
    ('大小写互换', 'iNVERSE cASE'),
    ('JSON 美化', 'JSON Beautify'),
    ('JSON 压缩', 'JSON Minify'),
    ('HTML 实体', 'HTML Entities'),
    ('实体转义', 'Escape entities'),
    ('实体反转义', 'Unescape entities'),
    ('URL 编码', 'URL encode'),
    ('URL 解码', 'URL decode'),
    ('Base64 编码', 'Base64 encode'),
    ('Base64 解码', 'Base64 decode'),
    ('功能分类导航', 'Tool categories'),
    ('功能分类', 'Categories'),
    ('工具操作区', 'Tool workspace'),
    ('切换深色 / 浅色主题', 'Toggle dark / light theme'),
    ('深色模式', 'Dark mode'),
    ('浅色模式', 'Light mode'),
    ('跳到工具区', 'Skip to tools'),
    ('填入示例', 'Load sample'),
    ('已填入示例内容', 'Sample loaded'),
    ('文本格式化工具箱', 'Text Formatter Toolbox'),
    ('CSS / HTML / Markdown / 中英排版 · 纯本地运行，内容不会上传',
     'CSS / HTML / Markdown / CJK–Latin typography · Runs locally, nothing is uploaded'),
    ('复制结果', 'Copy result'),
    ('0 字符', '0 chars'),
    ('在此粘贴需要处理的文本…', 'Paste the text you want to process here…'),
    ('处理后的结果会显示在这里…', 'The processed result will appear here…'),
    ('已粘贴', 'Pasted'),
    ('已导出文件', 'File exported'),
    ('工具介绍', 'About'),
    ('功能一览', 'Features'),
    ('使用教程', 'How to Use'),
    ('常见问题', 'FAQ'),
    ('隐私说明', 'Privacy'),
    ('赞助支持', 'Support'),
    ('站点地图', 'Sitemap'),
    ('GitHub 仓库', 'GitHub Repo'),
    ('CSS 压缩', 'CSS Minify'),
    ('2026 年 9 月 20 日', 'Sep 20, 2026'),
    ('最后更新', 'Last updated'),
    ('输入', 'Input'),
    ('输出', 'Output'),
    ('粘贴', 'Paste'),
    ('清空', 'Clear'),
    ('下载', 'Download'),
    ('请按 Ctrl+V 手动粘贴', 'Press Ctrl+V to paste manually'),
    ('互转', 'Convert'),
]

# 精确片段替换（含 JS 代码 / 整行标记，优先级最高，先于字典执行）
EXACT = [
    # 页面级 title / 描述
    ('<title>CSS 压缩 · Markdown 互转 · 中英排版｜文本格式化工具箱</title>',
     '<title>CSS Minifier · Markdown Converter · CJK Typography | Text Formatter Toolbox</title>'),
    ('<meta name="description" content="免费的在线文本格式化工具箱：CSS/HTML 压缩与美化、Markdown 与 HTML 互转、段落整理、中英文之间自动加空格、标点全半角转换、URL 与 Base64 编解码。纯浏览器本地运行，内容不上传服务器，无需注册，可离线使用。">',
     '<meta name="description" content="Free online text formatter toolbox: CSS/HTML minify & beautify, Markdown & HTML conversion, paragraph cleanup, CJK-Latin spacing, full/half-width punctuation, URL & Base64 codecs. Runs 100% in your browser — nothing is uploaded.">'),
    ('<meta name="keywords" content="CSS压缩,CSS格式化,CSS美化,HTML压缩,HTML美化,Markdown转HTML,HTML转Markdown,中英文之间加空格,中英混排排版,中文标点转换,全角半角转换,在线文本格式化,文本处理工具,JSON美化,Base64编解码,URL编解码,开发者工具箱">',
     '<meta name="keywords" content="css minifier,css beautifier,html formatter,html minifier,markdown to html,html to markdown,cjk spacing,pangu spacing,full-width half-width,online text formatter,text tools,json formatter,base64 encode,url encoder,developer tools">'),
    ('<meta property="og:title" content="CSS 压缩 · Markdown 互转 · 中英排版｜文本格式化工具箱">',
     '<meta property="og:title" content="CSS Minifier · Markdown Converter · CJK Typography | Text Formatter Toolbox">'),
    ('<meta property="og:description" content="CSS/HTML 压缩美化、Markdown 互转、段落整理、中英排版加空格、全半角转换、Base64/URL 编解码。纯本地运行，数据不出浏览器。">',
     '<meta property="og:description" content="CSS/HTML minify & beautify, Markdown conversion, paragraph cleanup, CJK spacing, Base64/URL codecs. 100% local — data never leaves your browser.">'),
    ('<meta name="twitter:title" content="CSS 压缩 · Markdown 互转 · 中英排版｜文本格式化工具箱">',
     '<meta name="twitter:title" content="CSS Minifier · Markdown Converter · CJK Typography | Text Formatter Toolbox">'),
    ('<meta name="twitter:description" content="免费在线文本格式化工具，纯本地运行，内容不上传服务器。">',
     '<meta name="twitter:description" content="Free online text formatter. 100% local — nothing is uploaded.">'),
    ('<meta property="og:locale" content="zh_CN">',
     '<meta property="og:locale" content="en_US">'),
    ('<meta name="ai:summary" content="文本格式化工具箱是一个免费的纯前端在线文本处理工具，支持 CSS/HTML 压缩与美化、Markdown 与 HTML 互转、段落整理、中英文间距与标点全半角转换、URL/Base64/JSON 处理；所有计算在浏览器本地完成，文本不会上传到任何服务器。">',
     '<meta name="ai:summary" content="Text Formatter Toolbox is a free, pure front-end online text toolkit: CSS/HTML minify & beautify, Markdown & HTML conversion, paragraph cleanup, CJK-Latin spacing, full/half-width punctuation, URL/Base64/JSON codecs. All processing runs locally in the browser — text is never uploaded.">'),
    ('<meta name="application-name" content="文本格式化工具箱">',
     '<meta name="application-name" content="Text Formatter Toolbox">'),
    # canonical / og:url 指向 /en/
    ('<link rel="canonical" href="' + ROOT + '">',
     '<link rel="canonical" href="' + EN + '">'),
    ('<meta property="og:url" content="' + ROOT + '">',
     '<meta property="og:url" content="' + EN + '">'),
    # html lang
    ('<html lang="zh-CN"', '<html lang="en"'),
    # 语言切换按钮（英文版指回中文版）
    ('<a class="btn ghost" href="./en/" hreflang="en" aria-label="Switch to English version">English</a>',
     '<a class="btn ghost" href="../" hreflang="zh-CN" aria-label="切换到中文版">中文</a>'),
    # 快捷键提示整行
    ('<p class="footnote">按 <span class="kbd">Ctrl</span> + <span class="kbd">Enter</span> 快速执行当前工具的第一个操作</p>',
     '<p class="footnote">Press <span class="kbd">Ctrl</span> + <span class="kbd">Enter</span> to run the first action of the current tool</p>'),
    # 页脚标语与时间
    ('文本格式化工具箱 · 免费开源的在线 CSS / HTML / Markdown / 中英排版工具 · 纯浏览器本地运行，内容不上传',
     'Text Formatter Toolbox · Free & open-source online CSS / HTML / Markdown / CJK typography tools · Runs entirely in your browser, nothing is uploaded'),
    # JS 内动态文案
    ("toast(item.label + ' 完成')", "toast(item.label + ' done')"),
    ("return t.length + ' 字符 · ' + (t === '' ? 0 : t.split('\\n').length) + ' 行';",
     "return t.length + ' chars · ' + (t === '' ? 0 : t.split('\\n').length) + ' lines';"),
    # 相对资源路径（/en/ 下需要回根目录）
    ('href="favicon.svg"', 'href="../favicon.svg"'),
    ('href="icon-192.png"', 'href="../icon-192.png"'),
    ('href="manifest.webmanifest"', 'href="../manifest.webmanifest"'),
    ('href="llms.txt"', 'href="../llms.txt"'),
    ('href="sitemap.xml"', 'href="../sitemap.xml"'),
    ("register('sw.js')", "register('../sw.js')"),
    # typo 示例整行替换为英文语境（避免字典误伤「标点」二字）
    ("typo: '这是一段中英混排的text,包含English标点.com后面少了空格,and中文English之间没有空格.\\nprice is 1,200 dollars,thanks!the URL https://example.com/a?b=1&c=2 不受影响，代码块 `foo(a,b)` 也不受影响。',",
     "typo: 'This is a mixed CJK-Latin line,text with English punctuation.com missing a space,and no space between中文andEnglish.\\nprice is 1,200 dollars,thanks!the URL https://example.com/a?b=1&c=2 stays intact,code `foo(a,b)` stays intact too.',"),
]


def main():
    html = io.open(SRC, encoding='utf-8').read()

    # --- 结构级替换 ---
    # SEO 内容区
    i = html.index('<div class="seo">')
    j = html.index('<footer class="site-footer"')
    html = html[:i] + EN_SEO + html[j:]

    # JSON-LD
    html = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>',
                  lambda m: EN_JSONLD.replace('ENURL', EN).replace('ROOTURL', ROOT), html, count=1)

    # canonical 自动修正脚本
    html = re.sub(r'<script>\(function\(\)\{var O=[\s\S]*?\}\)\(\);</script>', EN_FIX, html, count=1)

    # --- 精确片段 ---
    for old, new in EXACT:
        if old not in html:
            print('  [warn] 未命中:', old[:60].replace('\n', ' '))
        html = html.replace(old, new)

    # --- 字典（长度降序） ---
    for old, new in sorted(PAIRS, key=lambda p: -len(p[0])):
        html = html.replace(old, new)

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    io.open(DST, 'w', encoding='utf-8', newline='\n').write(html)

    zh_left = re.findall(r'[\u4e00-\u9fff]{2,}', html)
    print('en/index.html written,', len(html), 'bytes')
    print('残留中文片段数:', len(zh_left))
    for s in sorted(set(zh_left))[:30]:
        print('  -', s)


if __name__ == '__main__':
    main()
