"""
generate_posts.py
放到博客根目录，和 index.html 同级，运行后自动生成新格式的 posts.json

使用方法：
    python generate_posts.py

依赖：无需安装任何库，Python 3 自带
"""

import os
import json
import re

POSTS_DIR = "posts"       # md 文件所在文件夹
OUTPUT_FILE = "posts.json"  # 输出文件


def parse_front_matter(filepath, filename):
    """读取 md 文件，解析 Front Matter，返回元数据字典"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    metadata = {
        "file": filename,
        "title": filename.replace(".md", ""),
        "date": "2026-01-01",
        "category": "默认",
        "image": "https://picsum.photos/seed/default/800/500",
        "excerpt": "",
        "pinned": False,
    }

    # 匹配 --- 包裹的 Front Matter
    match = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", text)
    if match:
        yaml_block = match.group(1)
        body = text[match.end():]

        for line in yaml_block.split("\n"):
            if ":" not in line:
                continue
            key, *rest = line.split(":")
            key = key.strip()
            value = ":".join(rest).strip()

            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False

            if key:
                metadata[key] = value
    else:
        body = text

    # 自动生成摘要（取正文前 80 个字）
    clean_body = re.sub(r"[#*`\[\]()!>\-]", "", body)
    clean_body = re.sub(r"\s+", " ", clean_body).strip()
    metadata["excerpt"] = clean_body[:80] + "..." if len(clean_body) > 80 else clean_body

    return metadata


def main():
    if not os.path.isdir(POSTS_DIR):
        print(f"❌ 找不到 {POSTS_DIR}/ 文件夹，请确认脚本放在博客根目录")
        return

    md_files = [f for f in os.listdir(POSTS_DIR) if f.endswith(".md")]

    if not md_files:
        print(f"❌ {POSTS_DIR}/ 里没有找到任何 .md 文件")
        return

    posts = []
    for filename in md_files:
        filepath = os.path.join(POSTS_DIR, filename)
        try:
            meta = parse_front_matter(filepath, filename)
            posts.append(meta)
            print(f"✅ {filename}  →  {meta['title']}")
        except Exception as e:
            print(f"⚠️  {filename} 解析失败：{e}")

    # 按日期倒序排列
    posts.sort(key=lambda p: p["date"], reverse=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 完成！共处理 {len(posts)} 篇文章，已写入 {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
