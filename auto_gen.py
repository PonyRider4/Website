import os
import json
import re

# 配置
POSTS_DIR = 'posts'
JSON_FILE = 'posts.json'

def parse_post(filename):
    filepath = os.path.join(POSTS_DIR, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 提取 Front Matter (--- ... ---)
    metadata = {}
    front_matter_match = re.search(r^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    
    if front_matter_match:
        yaml_text = front_matter_match.group(1)
        # 简单的解析 key: value
        for line in yaml_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        # 移除 Front Matter，剩下的就是正文
        body = content.replace(front_matter_match.group(0), '').strip()
    else:
        # 如果没写头部信息，就用默认值
        metadata = {
            'title': filename.replace('.md', ''),
            'date': '2026-01-01',
            'category': '未分类',
            'image': 'https://picsum.photos/800/500', # 默认图
            'pinned': 'false'
        }
        body = content.strip()

    # 2. 自动生成简介 (取正文前 100 字)
    # 去掉 Markdown 符号
    clean_body = re.sub(r'[#*`\[\]()]', '', body) 
    excerpt = clean_body[:80] + '...' if len(clean_body) > 80 else clean_body

    return {
        "title": metadata.get('title'),
        "date": metadata.get('date'),
        "category": metadata.get('category'),
        "image": metadata.get('image'),
        "pinned": metadata.get('pinned', 'false').lower() == 'true',
        "excerpt": excerpt,
        "file": f"{POSTS_DIR}/{filename}"
    }

def main():
    posts = []
    # 扫描 posts 文件夹
    if not os.path.exists(POSTS_DIR):
        print(f"❌ 错误：找不到 {POSTS_DIR} 文件夹")
        return

    # 按文件名排序（或者按时间，这里默认按文件名倒序，你可以改）
    files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.md')], reverse=True)

    for i, filename in enumerate(files):
        try:
            post = parse_post(filename)
            post['id'] = i + 1  # 自动生成 ID
            posts.append(post)
            print(f"✅ 解析成功: {filename}")
        except Exception as e:
            print(f"⚠️ 解析失败 {filename}: {e}")

    # 写入 JSON
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    print(f"\n🎉 成功生成 {len(posts)} 篇文章配置！")

if __name__ == "__main__":
    main()