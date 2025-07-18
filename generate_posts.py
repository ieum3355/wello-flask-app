import json
import os

# 설정
POSTS_FILE = "posts.json"
POSTS_DIR = "templates/posts"
APP_FILE = "app.py"

# 1. HTML 포스트 파일 생성
def generate_post_html(slug, title, content):
    html = f"""{{% extends "layout.html" %}}
{{% block content %}}
<div class="p-4 bg-white rounded shadow-sm">
  <h2 class="fw-bold mb-3">{title}</h2>
  {content}
</div>
{{% endblock %}}"""
    with open(os.path.join(POSTS_DIR, f"{slug}.html"), "w", encoding="utf-8") as f:
        f.write(html)

# 2. app.py의 posts 리스트 갱신
def update_app_py(posts_data):
    with open(APP_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_posts_code = "    posts = [\n"
    for post in posts_data:
        new_posts_code += f'        {{"title": "{post["title"]}", "slug": "{post["slug"]}"}},\n'
    new_posts_code += "    ]\n"

    with open(APP_FILE, "w", encoding="utf-8") as f:
        inside_posts = False
        for line in lines:
            if line.strip().startswith("posts = ["):
                inside_posts = True
                f.write(new_posts_code)
            elif inside_posts and line.strip().startswith("]"):
                inside_posts = False
            elif not inside_posts:
                f.write(line)

# 실행
if __name__ == "__main__":
    with open(POSTS_FILE, "r", encoding="utf-8") as f:
        posts = json.load(f)

    for post in posts:
        generate_post_html(post["slug"], post["title"], post["content"])

    update_app_py(posts)
    print("✅ 포스트 HTML과 app.py 자동 생성 완료!")
