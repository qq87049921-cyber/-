#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版事件搜索工具 - 扩展版

支持搜索：
- 文本文件内容：.json, .md, .txt, .py, .html, .css, .js
- 图片文件名：.jpg, .jpeg, .png, .gif, .webp
- 所有文件名
"""

import os
import re
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any


class EventSearcher:
    """事件搜索器 - 扩展版"""

    TEXT_EXTENSIONS = {'.json', '.md', '.txt', '.py', '.html', '.css', '.js', '.xml', '.yaml', '.yml'}
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}

    def __init__(self, memory_file: str = None, base_dir: str = None):
        self.memory_file = memory_file
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.memory = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        if self.memory_file and os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def search_by_keywords(self, keywords: List[str], exact_match: bool = False) -> List[Dict]:
        """关键词搜索 - 扩展版"""
        results = []

        # 1. 搜索记忆文件
        if self.memory:
            memory_str = json.dumps(self.memory, ensure_ascii=False).lower()
            for keyword in keywords:
                if keyword.lower() in memory_str:
                    results.append({
                        'source': 'memory_file',
                        'file': self.memory_file,
                        'keyword': keyword,
                        'type': 'memory'
                    })

        # 2. 搜索所有文件
        for filepath in self.base_dir.rglob("*"):
            if not filepath.is_file():
                continue

            filename_lower = filepath.name.lower()

            # 搜索文本文件内容
            if filepath.suffix.lower() in self.TEXT_EXTENSIONS:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read().lower()
                        for keyword in keywords:
                            if keyword.lower() in content:
                                context = self._extract_context(content, keyword.lower())
                                results.append({
                                    'source': 'file_content',
                                    'file': str(filepath.relative_to(self.base_dir)),
                                    'keyword': keyword,
                                    'context': context,
                                    'type': 'content'
                                })
                                break
                except:
                    pass

            # 搜索文件名（包括图片）
            for keyword in keywords:
                if keyword.lower() in filename_lower:
                    file_type = 'image' if filepath.suffix.lower() in self.IMAGE_EXTENSIONS else 'filename'
                    results.append({
                        'source': 'filename',
                        'file': str(filepath.relative_to(self.base_dir)),
                        'keyword': keyword,
                        'type': file_type
                    })
                    break

        return results

    def search_by_time_range(self, days: int = 7, keywords: List[str] = None) -> List[Dict]:
        """时间范围搜索"""
        results = []
        cutoff_time = datetime.now() - timedelta(days=days)

        for filepath in self.base_dir.rglob("*"):
            if not filepath.is_file():
                continue

            mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
            if mtime < cutoff_time:
                continue

            result = {
                'source': 'time_search',
                'file': str(filepath.relative_to(self.base_dir)),
                'modified': mtime.strftime('%Y-%m-%d %H:%M:%S'),
                'type': 'recent_file'
            }

            if keywords:
                matched = False
                filename_lower = filepath.name.lower()
                for kw in keywords:
                    if kw.lower() in filename_lower:
                        matched = True
                        result['keyword'] = kw
                        result['match_type'] = 'filename'
                        break

                if not matched and filepath.suffix.lower() in self.TEXT_EXTENSIONS:
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            for kw in keywords:
                                if kw.lower() in content:
                                    matched = True
                                    result['keyword'] = kw
                                    result['match_type'] = 'content'
                                    break
                    except:
                        pass

                if matched:
                    results.append(result)
            else:
                results.append(result)

        results.sort(key=lambda x: x['modified'], reverse=True)
        return results

    def fuzzy_search(self, query: str) -> List[Dict]:
        """模糊搜索"""
        results = []
        query_lower = query.lower()

        for filepath in self.base_dir.rglob("*"):
            if not filepath.is_file():
                continue

            if query_lower in filepath.name.lower():
                file_type = 'image' if filepath.suffix.lower() in self.IMAGE_EXTENSIONS else 'filename'
                results.append({
                    'source': 'fuzzy_search',
                    'file': str(filepath.relative_to(self.base_dir)),
                    'match_type': 'filename',
                    'type': file_type
                })

            if filepath.suffix.lower() in self.TEXT_EXTENSIONS:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        similarity = self._calculate_similarity(query, content)
                        if similarity > 0.1:
                            results.append({
                                'source': 'fuzzy_search',
                                'file': str(filepath.relative_to(self.base_dir)),
                                'similarity': f'{similarity:.2%}',
                                'type': 'content'
                            })
                except:
                    pass

        return results

    def search_with_regex(self, pattern: str) -> List[Dict]:
        """正则表达式搜索"""
        results = []
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            return results

        for filepath in self.base_dir.rglob("*"):
            if not filepath.is_file():
                continue

            if regex.search(filepath.name):
                results.append({
                    'source': 'regex_search',
                    'file': str(filepath.relative_to(self.base_dir)),
                    'match_type': 'filename',
                    'type': 'filename'
                })

            if filepath.suffix.lower() in self.TEXT_EXTENSIONS:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        matches = regex.findall(content)
                        if matches:
                            results.append({
                                'source': 'regex_search',
                                'file': str(filepath.relative_to(self.base_dir)),
                                'matches': matches[:5],
                                'type': 'content'
                            })
                except:
                    pass

        return results

    def _extract_context(self, content: str, keyword: str, context_length: int = 100) -> str:
        pos = content.find(keyword)
        if pos != -1:
            start = max(0, pos - context_length // 2)
            end = min(len(content), pos + len(keyword) + context_length // 2)
            return "..." + content[start:end] + "..."
        return content[:context_length] + "..."

    def _calculate_similarity(self, query: str, content: str) -> float:
        query_words = set(query.split())
        content_words = set(content.split())
        if not query_words:
            return 0.0
        intersection = query_words & content_words
        return len(intersection) / len(query_words)

    def search_recent_events(self, hours: int = 24) -> List[Dict]:
        return self.search_by_time_range(days=hours / 24)


def print_results(results: List[Dict]):
    if not results:
        print("✓ 没有找到匹配的结果")
        return
    print(f"\n找到 {len(results)} 个结果：\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. 类型: {result.get('type', '未知')}")
        print(f"   文件: {result.get('file', '未知')}")
        if 'keyword' in result:
            print(f"   关键词: {result['keyword']}")
        if 'context' in result:
            print(f"   上下文: {result['context'][:80]}...")
        if 'modified' in result:
            print(f"   修改时间: {result['modified']}")
        print("-" * 50)


def main():
    parser = argparse.ArgumentParser(description="增强版事件搜索工具")
    parser.add_argument("--action", required=True,
                        choices=["keywords", "time", "fuzzy", "regex", "recent"],
                        help="搜索类型")
    parser.add_argument("--keywords", help="关键词（逗号分隔）")
    parser.add_argument("--exact", action="store_true", help="精确匹配")
    parser.add_argument("--days", type=int, help="搜索最近几天")
    parser.add_argument("--hours", type=int, help="搜索最近几小时")
    parser.add_argument("--query", help="模糊搜索查询")
    parser.add_argument("--regex", help="正则表达式")
    parser.add_argument("--memory-file", help="记忆文件路径")
    parser.add_argument("--base-dir", help="搜索的基础目录")

    args = parser.parse_args()

    base_dir = args.base_dir or os.getcwd()
    searcher = EventSearcher(memory_file=args.memory_file, base_dir=base_dir)

    if args.action == "keywords":
        if not args.keywords:
            print("错误: --keywords 参数必填")
            return
        keywords = [k.strip() for k in args.keywords.split(",")]
        results = searcher.search_by_keywords(keywords, exact_match=args.exact)
        print_results(results)

    elif args.action == "time":
        days = args.days or 7
        keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else None
        results = searcher.search_by_time_range(days=days, keywords=keywords)
        print_results(results)

    elif args.action == "fuzzy":
        if not args.query:
            print("错误: --query 参数必填")
            return
        results = searcher.fuzzy_search(args.query)
        print_results(results)

    elif args.action == "regex":
        if not args.regex:
            print("错误: --regex 参数必填")
            return
        results = searcher.search_with_regex(args.regex)
        print_results(results)

    elif args.action == "recent":
        hours = args.hours or 24
        results = searcher.search_recent_events(hours=hours)
        print_results(results)


if __name__ == "__main__":
    main()
