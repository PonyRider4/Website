import os
import json
import time

# 配置
POSTS_DIR = 'posts'
JSON_FILE = 'posts.json'
IMAGE_DIR = 'images'

def get_posts():
    posts = []
    # 遍历 posts 文件夹
    for i, filename in enumerate(os.listdir(POSTS_DIR)):
        if filename.endswith('.md'):
            # 这里简单演示：你可以扩展去读取 Markdown 里的 Frontmatter 信息
            post = {
                "id": i + 1,
                "title": filename.replace('.md', ''), # 默认用文件名做标题
                "excerpt": "这是自动生成的简介...",
                "date": time.strftime("%Y-%m-%d"), # 默认今天
                "category": "默认分类",
                "image": f"{IMAGE_DIR}/cover{i%5+1}.jpg", # 随机分配封面
                "file": f"{POSTS_DIR}/{filename}",
                "pinned": False
            }
            posts.append(post)
    return posts

if __name__ == "__main__":
    data = get_posts()
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 成功更新 {len(data)} 篇文章到 {JSON_FILE}")
