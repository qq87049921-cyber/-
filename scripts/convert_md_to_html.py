#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
萤萤专属空间 - Markdown 转 HTML 转换脚本

功能：
- 将 Markdown 文件转换为带背景效果的 HTML 文件
- 保持与现有设计风格一致（星空、森林、草地、萤火虫）
- 自动提取标题、日期、内容

使用方法：
    python scripts/convert_md_to_html.py --all                    # 转换所有 .md 文件
    python scripts/convert_md_to_html.py --target claw-space/logs # 转换指定目录
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Optional

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            min-height: 100vh;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to bottom, #0a0a1a 0%, #1a1a3a 50%, #2a4a2a 80%, #1a3a1a 100%);
            position: relative;
            color: #ffffff;
        }}

        /* 星空 */
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

        /* 森林 */
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

        /* 草地 */
        .grass {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 35%;
            background: linear-gradient(to bottom, #2a5a2a 0%, #1a4a2a 50%, #0a3a1a 100%);
            z-index: 2;
        }}

        /* 萤火虫 */
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

        /* 内容容器 */
        .content {{
            position: relative;
            z-index: 10;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        /* 返回按钮 */
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

        /* 内容卡片 */
        .content-card {{
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        }}

        h1 {{
            font-size: 2.5em;
            color: #ffff00;
            margin-bottom: 20px;
            text-shadow: 0 0 20px rgba(255, 255, 0, 0.5);
        }}

        h2 {{
            font-size: 1.8em;
            color: #ffff00;
            margin-top: 30px;
            margin-bottom: 15px;
            border-bottom: 2px solid rgba(255, 255, 0, 0.3);
            padding-bottom: 10px;
        }}

        h3 {{
            font-size: 1.4em;
            color: #ffff00;
            margin-top: 25px;
            margin-bottom: 12px;
        }}

        p {{
            line-height: 1.8;
            margin-bottom: 15px;
            color: #e0e0e0;
        }}

        ul {{
            margin-left: 30px;
            margin-bottom: 20px;
        }}

        li {{
            line-height: 1.8;
            margin-bottom: 10px;
            color: #e0e0e0;
        }}

        blockquote {{
            border-left: 4px solid #ffff00;
            padding-left: 20px;
            margin: 20px 0;
            color: #a0a0a0;
            font-style: italic;
        }}

        hr {{
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.2);
            margin: 30px 0;
        }}

        strong {{
            color: #ffff00;
        }}

        code {{
            background: rgba(255, 255, 255, 0.1);
            padding: 3px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
        }}

        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #808080;
            font-style: italic;
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
        <a href="index.html" class="back-button">← 返回</a>

        <div class="content-card">
            {content_html}
        </div>

        <div class="footer">
            *萤萤的专属空间*
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

    <!-- 全局播放器 -->
    <link rel="stylesheet" href="../assets/player.css">
    <script src="../assets/player.js"></script>
</body>
</html>
"""


def convert_markdown_to_html(markdown_content: str) -> str:
    """将 Markdown 内容转换为 HTML"""
    lines = markdown_content.split('\n')
    html_lines = []
    in_list = False
    in_blockquote = False

    for line in lines:
        # 一级标题
        if line.startswith('# '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append(f'<h1>{line[2:].strip()}</h1>')

        # 二级标题
        elif line.startswith('## '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append(f'<h2>{line[3:].strip()}</h2>')

        # 三级标题
        elif line.startswith('### '):
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append(f'<h3>{line[4:].strip()}</h3>')

        # 无序列表
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append(f'<li>{line[2:].strip()}</li>')

        # 引用
        elif line.startswith('> '):
            if not in_blockquote:
                html_lines.append('<blockquote>')
                in_blockquote = True
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'{line[2:].strip()}<br>')

        # 分隔线
        elif line.strip() == '---':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append('<hr>')

        # 空行
        elif not line.strip():
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False
            html_lines.append('<br>')

        # 普通段落
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_blockquote:
                html_lines.append('</blockquote>')
                in_blockquote = False

            # 处理粗体
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            # 处理代码
            line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)

            html_lines.append(f'<p>{line.strip()}</p>')

    # 闭合标签
    if in_list:
        html_lines.append('</ul>')
    if in_blockquote:
        html_lines.append('</blockquote>')

    return '\n'.join(html_lines)


def convert_file(md_path: Path) -> bool:
    """转换单个 Markdown 文件为 HTML"""
    if not md_path.exists():
        print(f"⚠️  文件不存在: {md_path}")
        return False

    # 读取 Markdown 文件
    try:
        markdown_content = md_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"⚠️  读取文件失败: {md_path} - {e}")
        return False

    # 提取标题（第一个一级标题）
    title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_path.stem

    # 转换为 HTML
    content_html = convert_markdown_to_html(markdown_content)

    # 生成完整的 HTML
    html = HTML_TEMPLATE.format(
        title=title,
        content_html=content_html
    )

    # 写入 HTML 文件
    html_path = md_path.with_suffix('.html')
    try:
        html_path.write_text(html, encoding='utf-8')
        print(f"✅ 已转换: {md_path.name} → {html_path.name}")
        return True
    except Exception as e:
        print(f"❌ 写入失败: {html_path} - {e}")
        return False


def scan_and_convert(directory: Path) -> int:
    """扫描目录并转换所有 .md 文件"""
    if not directory.exists():
        print(f"⚠️  目录不存在: {directory}")
        return 0

    count = 0
    for md_file in directory.glob('*.md'):
        # 跳过 README.md 和 . 开头的文件
        if md_file.name in ['README.md', 'USER_GUIDE.md'] or md_file.name.startswith('.'):
            continue

        # 跳过已经存在的 HTML 文件（避免重复转换）
        html_file = md_file.with_suffix('.html')
        if html_file.exists():
            print(f"⏭️  跳过: {md_file.name}（HTML已存在）")
            continue

        if convert_file(md_file):
            count += 1

    return count


def main():
    parser = argparse.ArgumentParser(description='萤萤专属空间 - Markdown 转 HTML 转换脚本')
    parser.add_argument('--target', type=str, help='指定转换的目录')
    parser.add_argument('--all', action='store_true', help='转换所有目录')

    args = parser.parse_args()

    print("=" * 60)
    print("🌟 萤萤专属空间 - Markdown 转 HTML 转换脚本")
    print("=" * 60)

    # 确定要转换的目录
    directories = []
    if args.all:
        directories = [
            Path('claw-space/logs'),
            Path('claw-space/growth'),
            Path('claw-space/memories'),
            Path('claw-space/images'),
            Path('claw-space/music'),
        ]
    elif args.target:
        directories = [Path(args.target)]
    else:
        print("\n❌ 错误: 请指定 --target 或 --all")
        print("\n使用方法:")
        print("  python scripts/convert_md_to_html.py --all")
        print("  python scripts/convert_md_to_html.py --target claw-space/logs")
        return

    # 执行转换
    total_count = 0
    for directory in directories:
        print(f"\n📂 转换目录: {directory}")
        count = scan_and_convert(directory)
        total_count += count

    # 汇总
    print("\n" + "=" * 60)
    print(f"✅ 转换完成! 共转换 {total_count} 个文件")
    print("=" * 60)

    if total_count > 0:
        print("\n📌 下一步:")
        print("   1. 检查生成的 HTML 文件是否正确")
        print("   2. 提交到 GitHub:")
        print("      git add claw-space/")
        print("      git commit -m \"转换 Markdown 为 HTML\"")
        print("      git push")
        print("\n   3. 运行更新脚本:")
        print("      python scripts/update_space.py --all")
        print("\n   4. 等待 1-2 分钟，GitHub Pages 自动部署完成")
    else:
        print("\n💡 提示: 没有需要转换的文件")
        print("   所有 .md 文件可能已经转换为 .html 了")


if __name__ == "__main__":
    main()
