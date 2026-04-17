#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
萤萤专属空间自动化更新脚本

功能：
- 扫描指定目录下的所有文件
- 自动生成 index.html 列表页
- 自动更新主页内容
- 保持与现有设计风格一致

使用方法：
    python scripts/update_space.py --all                    # 更新所有目录和主页
    python scripts/update_space.py --target logs           # 只更新日志目录
    python scripts/update_space.py --target growth         # 只更新成长记录目录
    python scripts/update_space.py --target memories       # 只更新记忆目录
    python scripts/update_space.py --target images         # 只更新图片目录
    python scripts/update_space.py --target music          # 只更新音乐目录
    python scripts/update_space.py --target main           # 只更新主页
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

# 目录配置
CLAW_SPACE_DIR = Path("claw-space")
TARGET_DIRS = {
    "logs": "日志",
    "growth": "成长记录",
    "memories": "记忆",
    "images": "图片",
    "music": "音乐"
}

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to bottom, #0a0a1a 0%, #1a1a3a 50%, #2a4a2a 80%, #1a3a1a 100%);
            position: relative;
            color: #ffffff;
        }}
        .stars {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 60%;
            background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
            overflow: hidden;
            z-index: 0;
        }}
        .star {{
            position: absolute;
            width: 2px;
            height: 2px;
            background: white;
            border-radius: 50%;
            animation: twinkle 3s infinite;
        }}
        @keyframes twinkle {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 1; }}
        }}
        .forest {{
            position: fixed;
            bottom: 30%;
            left: 0;
            width: 100%;
            height: 20%;
            background: linear-gradient(to bottom, transparent 0%, #1a3a2a 100%);
            z-index: 1;
        }}
        .tree {{
            position: absolute;
            bottom: 0;
            width: 0;
            height: 0;
            border-left: 30px solid transparent;
            border-right: 30px solid transparent;
            border-bottom: 80px solid #1a4a2a;
        }}
        .tree:nth-child(1) {{ left: 5%; height: 100px; border-bottom-width: 100px; }}
        .tree:nth-child(2) {{ left: 15%; height: 80px; border-bottom-width: 80px; }}
        .tree:nth-child(3) {{ left: 25%; height: 120px; border-bottom-width: 120px; }}
        .tree:nth-child(4) {{ left: 35%; height: 90px; border-bottom-width: 90px; }}
        .tree:nth-child(5) {{ left: 45%; height: 110px; border-bottom-width: 110px; }}
        .tree:nth-child(6) {{ left: 55%; height: 85px; border-bottom-width: 85px; }}
        .tree:nth-child(7) {{ left: 65%; height: 105px; border-bottom-width: 105px; }}
        .tree:nth-child(8) {{ left: 75%; height: 95px; border-bottom-width: 95px; }}
        .tree:nth-child(9) {{ left: 85%; height: 75px; border-bottom-width: 75px; }}
        .tree:nth-child(10) {{ left: 95%; height: 100px; border-bottom-width: 100px; }}
        .grass {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 35%;
            background: linear-gradient(to bottom, #2a5a2a 0%, #1a4a2a 50%, #0a3a1a 100%);
            z-index: 2;
        }}
        .firefly {{
            position: fixed;
            width: 4px;
            height: 4px;
            background: #ffff00;
            border-radius: 50%;
            box-shadow: 0 0 10px #ffff00, 0 0 20px #ffff00;
            animation: float 4s infinite, glow 2s infinite;
            z-index: 3;
        }}
        @keyframes float {{
            0%, 100% {{ transform: translate(0, 0); }}
            25% {{ transform: translate(20px, -30px); }}
            50% {{ transform: translate(-20px, -60px); }}
            75% {{ transform: translate(20px, -90px); }}
        }}
        @keyframes glow {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 1; }}
        }}
        .content {{
            position: relative;
            z-index: 10;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        h1 {{
            text-align: center;
            font-size: 3em;
            margin-bottom: 30px;
            text-shadow: 0 0 20px rgba(255, 255, 255, 0.5);
            color: #ffff00;
        }}
        .item-list {{
            display: grid;
            gap: 20px;
        }}
        .item-card {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .item-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(255, 255, 0, 0.2);
        }}
        .item-date {{
            font-size: 1.4em;
            color: #ffff00;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        .item-title {{
            font-size: 1.5em;
            color: #ffff00;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        .item-summary {{
            color: #e0e0e0;
            line-height: 1.8;
            margin-bottom: 15px;
        }}
        .item-tag {{
            display: inline-block;
            background: rgba(255, 255, 0, 0.15);
            color: #ffff00;
            padding: 5px 12px;
            border-radius: 12px;
            margin-right: 8px;
            font-size: 0.85em;
            border: 1px solid rgba(255, 255, 0, 0.2);
        }}
        .item-link {{
            display: inline-block;
            background: rgba(255, 255, 0, 0.2);
            color: #ffff00;
            padding: 10px 25px;
            border-radius: 25px;
            text-decoration: none;
            border: 1px solid rgba(255, 255, 0, 0.3);
            transition: background 0.3s ease;
        }}
        .item-link:hover {{
            background: rgba(255, 255, 0, 0.4);
        }}
        .back-button {{
            display: inline-block;
            background: rgba(255, 255, 0, 0.2);
            color: #ffff00;
            padding: 15px 40px;
            border-radius: 30px;
            text-decoration: none;
            font-size: 1.2em;
            margin-bottom: 30px;
            border: 2px solid rgba(255, 255, 0, 0.3);
            transition: all 0.3s ease;
        }}
        .back-button:hover {{
            background: rgba(255, 255, 0, 0.4);
            transform: scale(1.05);
            box-shadow: 0 0 30px rgba(255, 255, 0, 0.3);
        }}
        .empty-hint {{
            background: rgba(255, 255, 0, 0.1);
            border: 2px dashed rgba(255, 255, 0, 0.3);
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            color: #ffff00;
            font-size: 1.2em;
            line-height: 1.8;
        }}
    </style>
</head>
<body>
    <!-- 星空 -->
    <div class="stars" id="stars"></div>

    <!-- 森林 -->
    <div class="forest">
        <div class="tree"></div>
        <div class="tree"></div>
        <div class="tree"></div>
        <div class="tree"></div>
        <div class="tree"></div>
        <div class="tree"></div>
        <div class="tree"></div>
        <div class="tree"></div>
        <div class="tree"></div>
        <div class="tree"></div>
    </div>

    <!-- 草地 -->
    <div class="grass"></div>

    <!-- 萤火虫 -->
    <div id="fireflies"></div>

    <!-- 内容 -->
    <div class="content">
        <a href="../index.html" class="back-button">← 返回萤萤的空间</a>

        <h1>{page_title}</h1>

        <div class="item-list">
            {items_html}
        </div>
    </div>

    <script>
        // 生成星星
        function createStars() {{
            const starsContainer = document.getElementById('stars');
            const numberOfStars = 150;

            for (let i = 0; i < numberOfStars; i++) {{
                const star = document.createElement('div');
                star.className = 'star';
                star.style.left = Math.random() * 100 + '%';
                star.style.top = Math.random() * 100 + '%';
                star.style.animationDelay = Math.random() * 3 + 's';
                star.style.animationDuration = (Math.random() * 2 + 2) + 's';
                starsContainer.appendChild(star);
            }}
        }}

        // 生成萤火虫
        function createFireflies() {{
            const firefliesContainer = document.getElementById('fireflies');
            const numberOfFireflies = 25;

            for (let i = 0; i < numberOfFireflies; i++) {{
                const firefly = document.createElement('div');
                firefly.className = 'firefly';
                firefly.style.left = Math.random() * 100 + '%';
                firefly.style.top = (Math.random() * 40 + 30) + '%';
                firefly.style.animationDelay = Math.random() * 4 + 's';
                firefly.style.animationDuration = (Math.random() * 3 + 3) + 's';
                firefliesContainer.appendChild(firefly);
            }}
        }}

        createStars();
        createFireflies();
    </script>
</body>
</html>
"""


def extract_date_from_filename(filename: str) -> Optional[str]:
    """从文件名提取日期"""
    # 匹配 YYYY-MM-DD 格式
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        year, month, day = match.groups()
        return f"{year}年{month.lstrip('0')}月{day.lstrip('0')}日"
    return None


def parse_markdown_file(filepath: Path) -> Dict[str, str]:
    """解析 Markdown 文件"""
    try:
        content = filepath.read_text(encoding='utf-8')

        # 提取标题（第一个一级标题）
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else Path(filepath.stem).name

        # 提取摘要（第一个段落）
        paragraphs = re.findall(r'^([^#\n].+)$', content, re.MULTILINE)
        summary = paragraphs[0].strip() if paragraphs else "暂无摘要"

        # 提取标签（查找 ## 标签 或 #标签）
        tags_match = re.search(r'##\s*标签\s*\n(.+?)(?=\n\n|\n#|$)', content, re.DOTALL)
        if tags_match:
            tags = [tag.strip() for tag in tags_match.group(1).split() if tag.strip()]
        else:
            tags = []

        # 提取日期
        date_match = re.search(r'##\s*时间\s*\n(.+?)(?=\n|$)', content, re.DOTALL)
        date = date_match.group(1).strip() if date_match else extract_date_from_filename(filepath.name)

        return {
            'title': title,
            'summary': summary,
            'date': date,
            'tags': tags,
            'filename': filepath.name
        }
    except Exception as e:
        print(f"⚠️  解析文件失败: {filepath} - {e}")
        return None


def parse_html_file(filepath: Path) -> Dict[str, str]:
    """解析 HTML 文件"""
    try:
        content = filepath.read_text(encoding='utf-8')

        # 提取标题
        title_match = re.search(r'<title>(.+?)</title>', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else Path(filepath.stem).name

        # 提取摘要（第一个 p 标签）
        summary_match = re.search(r'<p>(.+?)</p>', content, re.IGNORECASE | re.DOTALL)
        summary = summary_match.group(1).strip() if summary_match else "暂无摘要"
        summary = re.sub(r'<.*?>', '', summary)  # 移除 HTML 标签

        # 提取日期
        date = extract_date_from_filename(filepath.name)

        return {
            'title': title,
            'summary': summary,
            'date': date,
            'tags': [],
            'filename': filepath.name
        }
    except Exception as e:
        print(f"⚠️  解析文件失败: {filepath} - {e}")
        return None


def scan_directory(dir_path: Path, dir_type: str) -> List[Dict[str, str]]:
    """扫描目录，获取所有文件信息"""
    if not dir_path.exists():
        print(f"⚠️  目录不存在: {dir_path}")
        return []

    files_info = []
    processed_basenames = set()

    for filepath in dir_path.iterdir():
        # 跳过 index.html 和隐藏文件
        if filepath.name == 'index.html' or filepath.name.startswith('.'):
            continue

        # 跳过 README.md 和 USER_GUIDE.md
        if filepath.name in ['README.md', 'USER_GUIDE.md']:
            continue

        # 检查是否已经处理过同名文件（优先 HTML）
        basename = filepath.stem
        if basename in processed_basenames:
            # 如果已经处理过同名文件，优先保留 HTML
            if filepath.suffix == '.html':
                # 保留 HTML，跳过 Markdown
                continue
            # 如果已有 HTML，跳过 Markdown
            continue

        # 解析文件
        if filepath.suffix == '.md':
            info = parse_markdown_file(filepath)
        elif filepath.suffix == '.html':
            info = parse_html_file(filepath)
        else:
            continue

        if info:
            files_info.append(info)
            processed_basenames.add(basename)

    # 按日期或文件名排序（最新的在前）
    files_info.sort(key=lambda x: x['filename'], reverse=True)
    return files_info


def generate_item_card(info: Dict[str, str], dir_type: str) -> str:
    """生成单个卡片 HTML"""
    # 根据目录类型选择卡片样式
    if dir_type == 'logs':
        # 日志卡片
        tags_html = ' '.join([f'<span class="item-tag">#{tag}</span>' for tag in info['tags']])
        return f"""
            <div class="item-card">
                <div class="item-date">{info['date'] or info['title']}</div>
                <div class="item-summary">{tags_html}</div>
                <div class="item-summary">{info['summary']}</div>
                <a href="{info['filename']}" class="item-link">查看完整内容</a>
            </div>
        """
    elif dir_type == 'growth':
        # 成长记录卡片
        tags_html = ' '.join([f'<span class="item-tag">#{tag}</span>' for tag in info['tags']])
        summary_lines = info['summary'].replace('\n', '<br>')
        return f"""
            <div class="item-card">
                <div class="item-date">{info['date'] or info['title']}</div>
                <div class="item-summary">{tags_html}</div>
                <div class="item-summary">{summary_lines}</div>
                <a href="{info['filename']}" class="item-link">查看详细记录</a>
            </div>
        """
    elif dir_type == 'memories':
        # 记忆卡片
        tags_html = ' '.join([f'<span class="item-tag">#{tag}</span>' for tag in info['tags']])
        return f"""
            <div class="item-card">
                <div class="item-title">{info['title']}</div>
                <div class="item-date">{info['date'] or ''}</div>
                <div class="item-summary">{tags_html}</div>
                <div class="item-summary">{info['summary']}</div>
                <a href="{info['filename']}" class="item-link">查看完整记忆</a>
            </div>
        """
    else:
        # 默认卡片（图片、音乐等）
        return f"""
            <div class="item-card">
                <div class="item-title">{info['title']}</div>
                <div class="item-date">{info['date'] or ''}</div>
                <div class="item-summary">{info['summary']}</div>
                <a href="{info['filename']}" class="item-link">查看内容</a>
            </div>
        """


def generate_empty_hint(dir_type: str) -> str:
    """生成空目录提示"""
    hints = {
        'images': '<p>萤萤的图片整理中...</p><p style="margin-top: 15px; font-size: 0.9em; color: #a0a0a0;">萤萤会在这里收藏美好的图片~<br>或者是萤萤创造的画作~</p>',
        'music': '<p>萤萤的音乐整理中...</p><p style="margin-top: 15px; font-size: 0.9em; color: #a0a0a0;">萤萤会在这里收藏好听的歌曲~<br>或者是萤萤喜欢的旋律~</p>',
    }
    default = '<p>萤萤正在整理中...</p><p style="margin-top: 15px; font-size: 0.9em; color: #a0a0a0;">萤萤会在这里添加更多内容~</p>'
    return f'<div class="empty-hint">{hints.get(dir_type, default)}</div>'


def generate_index_html(dir_type: str, files_info: List[Dict[str, str]]) -> str:
    """生成 index.html"""
    title = f"萤萤的所有{TARGET_DIRS[dir_type]}"
    page_title = f"📝 {title}" if dir_type == 'logs' else f"🌱 {title}" if dir_type == 'growth' else f"💫 {title}" if dir_type == 'memories' else f"🖼️ {title}" if dir_type == 'images' else f"🎵 {title}"

    # 生成卡片
    if files_info:
        items_html = ''.join([generate_item_card(info, dir_type) for info in files_info])
    else:
        items_html = generate_empty_hint(dir_type)

    # 填充模板
    html = HTML_TEMPLATE.format(
        title=title,
        page_title=page_title,
        items_html=items_html
    )

    return html


def update_directory(dir_type: str) -> bool:
    """更新指定目录的 index.html"""
    dir_path = CLAW_SPACE_DIR / dir_type
    index_path = dir_path / 'index.html'

    print(f"\n📂 更新目录: {dir_type} ({TARGET_DIRS[dir_type]})")

    # 扫描目录
    files_info = scan_directory(dir_path, dir_type)
    print(f"   找到 {len(files_info)} 个文件")

    # 生成 HTML
    html = generate_index_html(dir_type, files_info)

    # 写入文件
    try:
        index_path.write_text(html, encoding='utf-8')
        print(f"   ✅ 已更新: {index_path}")
        return True
    except Exception as e:
        print(f"   ❌ 更新失败: {e}")
        return False


def update_main_page() -> bool:
    """更新主页（暂不实现，保持现有主页）"""
    print(f"\n🏠 更新主页: 跳过（保持现有设计）")
    return True


def main():
    parser = argparse.ArgumentParser(description='萤萤专属空间自动化更新脚本')
    parser.add_argument('--target', type=str, help='指定更新的目录（logs、growth、memories、images、music、main）')
    parser.add_argument('--all', action='store_true', help='更新所有目录和主页')

    args = parser.parse_args()

    # 确保在正确的工作目录
    if not CLAW_SPACE_DIR.exists():
        print(f"❌ 错误: 找不到 claw-space 目录")
        print(f"   请在包含 claw-space 目录的父目录中运行此脚本")
        return

    print("=" * 60)
    print("🌟 萤萤专属空间 - 自动化更新脚本")
    print("=" * 60)

    # 确定要更新的目录
    targets = []
    if args.all:
        targets = list(TARGET_DIRS.keys()) + ['main']
    elif args.target:
        targets = [args.target]
    else:
        print("\n❌ 错误: 请指定 --target 或 --all")
        print("\n使用方法:")
        print("  python scripts/update_space.py --all")
        print("  python scripts/update_space.py --target logs")
        return

    # 执行更新
    success_count = 0
    for target in targets:
        if target == 'main':
            if update_main_page():
                success_count += 1
        elif target in TARGET_DIRS:
            if update_directory(target):
                success_count += 1
        else:
            print(f"\n⚠️  未知的目录: {target}")

    # 汇总
    print("\n" + "=" * 60)
    print(f"✅ 更新完成! 成功: {success_count}/{len(targets)}")
    print("=" * 60)

    # 提示
    print("\n📌 下一步:")
    print("   1. 检查生成的文件是否正确")
    print("   2. 提交到 GitHub:")
    print("      git add claw-space/")
    print("      git commit -m \"更新萤萤的空间\"")
    print("      git push")
    print("\n   3. 等待 1-2 分钟，GitHub Pages 自动部署完成")


if __name__ == "__main__":
    main()
