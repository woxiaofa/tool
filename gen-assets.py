# -*- coding: utf-8 -*-
"""生成 OG 社交分享图与 PWA 图标（含中文字体渲染）"""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "C:/Windows/Fonts"


def load(name, size):
    for f in name:
        p = os.path.join(FONT_DIR, f)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


REG = load(["msyh.ttc", "msyh.ttf", "simhei.ttf"], 10)
BOLD = load(["msyhbd.ttc", "msyh.ttc", "simhei.ttf"], 10)

WHITE = (255, 255, 255, 255)
SOFT = (199, 210, 254, 255)


def gradient(size, c1, c2, vertical=True):
    w, h = size
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    n = h if vertical else w
    for i in range(n):
        t = i / max(1, n - 1)
        color = tuple(round(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        if vertical:
            d.line([(0, i), (w, i)], fill=color)
        else:
            d.line([(i, 0), (i, h)], fill=color)
    return img


def rounded_mask(size, radius_ratio=0.18):
    w, h = size
    m = Image.new("L", (w * 4, h * 4), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], radius=int(min(w, h) * radius_ratio * 4), fill=255)
    return m.resize(size, Image.LANCZOS)


def make_og(path):
    W, H = 1200, 630
    img = gradient((W, H), (79, 70, 229), (99, 102, 241))
    d = ImageDraw.Draw(img, "RGBA")

    # 右下装饰圆环
    d.ellipse([860, 150, 1300, 590], outline=(255, 255, 255, 40), width=60)
    d.ellipse([980, 30, 1180, 230], outline=(255, 255, 255, 30), width=40)

    f_badge = ImageFont.truetype(FONT_DIR + "/msyhbd.ttc", 30) if os.path.exists(FONT_DIR + "/msyhbd.ttc") else BOLD
    f_title = ImageFont.truetype(FONT_DIR + "/msyhbd.ttc", 82) if os.path.exists(FONT_DIR + "/msyhbd.ttc") else BOLD
    f_sub = ImageFont.truetype(FONT_DIR + "/msyh.ttc", 34) if os.path.exists(FONT_DIR + "/msyh.ttc") else REG
    f_tag = ImageFont.truetype(FONT_DIR + "/msyh.ttc", 27) if os.path.exists(FONT_DIR + "/msyh.ttc") else REG

    # 顶部徽章
    d.rounded_rectangle([80, 92, 372, 152], radius=30, fill=(255, 255, 255, 46))
    d.text((110, 102), "免费 · 开源 · 纯本地运行", font=f_badge, fill=WHITE)

    # 主标题
    d.text((78, 196), "文本格式化工具箱", font=f_title, fill=WHITE)
    d.line([(84, 316), (330, 316)], fill=(255, 255, 255, 200), width=7)

    # 副标题
    d.text((78, 348), "CSS / HTML 压缩美化  ·  Markdown 与 HTML 互转", font=f_sub, fill=SOFT)
    d.text((78, 398), "段落整理  ·  中英排版加空格  ·  JSON / URL / Base64", font=f_sub, fill=SOFT)

    # 标签胶囊
    tags = ["CSS 压缩", "HTML 格式化", "Markdown", "中英留白", "全半角", "Base64"]
    x = 80
    for t in tags:
        tw = d.textlength(t, font=f_tag) + 40
        d.rounded_rectangle([x, 464, x + tw, 516], radius=26, fill=(255, 255, 255, 38))
        d.text((x + 20, 473), t, font=f_tag, fill=WHITE)
        x += tw + 14

    # 底部提示
    d.text((78, 552), "打开即用，无需注册  —  输入内容不会离开你的浏览器", font=f_tag, fill=SOFT)

    img.save(path, "PNG")
    print("og-image.png ->", path)


def make_icon(size, path, maskable=False):
    pad = int(size * 0.16) if maskable else 0
    inner = size - pad * 2
    radius = int(inner * 0.22)
    bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    # 圆角渐变底
    box_size = inner
    if maskable:
        box = Image.new("RGBA", (size, size), (79, 70, 229, 255))
        bg = box
    else:
        g = gradient((box_size, box_size), (99, 102, 241), (79, 70, 229))
        g.putalpha(rounded_mask((box_size, box_size), 0.22))
        bg.paste(g, (0, 0), g)

    d = ImageDraw.Draw(bg)
    cx, cy = size / 2, size / 2
    unit = size / 64.0
    cl = size - 2 * pad
    s = cl / 64.0

    def bar(x, y, w, h, op=255):
        d.rounded_rectangle([pad + x * s, pad + y * s, pad + (x + w) * s, pad + (y + h) * s],
                            radius=(h * s) / 2, fill=(255, 255, 255, op))

    if maskable:
        # maskable 版本：内容收紧到安全区（80% 直径）
        bar(15, 22, 22, 5, 255)
        bar(15, 32, 30, 5, 255)
        bar(15, 42, 16, 5, 255)
        bar(21, 52, 24, 5, 165)
    else:
        bar(13, 17, 30, 4.6, 255)
        bar(13, 27, 38, 4.6, 255)
        bar(13, 37, 22, 4.6, 255)
        bar(21, 47, 30, 4.6, 165)
        d.arc([41.5 * s - 8.5 * s, 38 * s - 8.5 * s, 41.5 * s + 8.5 * s, 38 * s + 8.5 * s],
              start=0, end=360, fill=(255, 255, 255, 242), width=max(2, int(4.2 * s)))
        d.line([(44 * s, 40.5 * s), (54 * s, 50.5 * s)], fill=(255, 255, 255, 230), width=max(2, int(4.2 * s)))

    bg.save(path, "PNG")
    print(f"icon {size} -> {path}")


if __name__ == "__main__":
    make_og(os.path.join(BASE, "og-image.png"))
    make_icon(192, os.path.join(BASE, "icon-192.png"))
    make_icon(512, os.path.join(BASE, "icon-512.png"))
    make_icon(512, os.path.join(BASE, "icon-maskable-512.png"), maskable=True)
