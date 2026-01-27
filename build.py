import os
import json
import re
import datetime

# 配置
POSTS_DIR = 'posts'
JSON_FILE = 'posts.json'

def parse_post(filename):
    filepath = os.path.join(POSTS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 正则提取 Front Matter (--- ... ---)
    metadata = {}
    front_matter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    
    body = content
    if front_matter_match:
        yaml_text = front_matter_match.group(1)
        body = content.replace(front_matter_match.group(0), '').strip() # 去掉头，只留正文
        
        # 解析 Key: Value
        for line in yaml_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                # 处理布尔值
                if value.lower() == 'true': value = True
                elif value.lower() == 'false': value = False
                metadata[key] = value

    # 2. 自动生成简介 (取前80字，去掉Markdown符号)
    clean_body = re.sub(r'[#*`\[\]()!>]', '', body).replace('\n', ' ')
    excerpt = clean_body[:80] + '...'

    # 3. 组装数据
    return {
        "title": metadata.get('title', filename.replace('.md', '')),
        "date": metadata.get('date', '2026-01-01'),
        "category": metadata.get('category', '默认'),
        "image": metadata.get('image', ''),
        "pinned": metadata.get('pinned', False),
        "excerpt": metadata.get('excerpt', excerpt),
        "file": f"{POSTS_DIR}/{filename}" # 浏览器点击时加载这个文件
    }

def main():
    posts = []
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

    # 遍历所有 md 文件
    files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.md')]
    
    print(f"🔍 发现 {len(files)} 篇文章，开始构建...")

    for filename in files:
        try:
            post = parse_post(filename)
            posts.append(post)
        except Exception as e:
            print(f"⚠️ 解析失败: {filename} - {e}")

    # 按日期倒序排列 (最新的在前)
    posts.sort(key=lambda x: x['date'], reverse=True)

    # 写入 JSON
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 成功生成 posts.json！包含 {len(posts)} 篇文章。")

if __name__ == "__main__":
    main()
