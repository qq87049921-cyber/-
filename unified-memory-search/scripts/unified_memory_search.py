#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一记忆搜索工具

功能：
- 整合多种搜索方式和数据源
- 搜索对话记录、结构化记忆、成长日志、文件系统
- 支持关键词、模糊搜索、时间范围、正则表达式
- 返回按优先级排序的结果

使用方法：
    python scripts/unified_memory_search.py --keywords "白猫"
    python scripts/unified_memory_search.py --days 7
    python scripts/unified_memory_search.py --action summary
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import sys

# 数据源配置
# 指向 agent-bridge-github/ 目录（实际数据所在目录）
BASE_DIR = Path(__file__).parent.parent.parent

SOURCES = {
    'structured_memory': BASE_DIR / 'memory-store' / '萤萤记忆.json',
    'dialogues': BASE_DIR / 'shared_memory' / 'dialogues.json',
    'growth_log': BASE_DIR / 'shared_memory' / 'growth_log.json'
}

# 支持的文件类型
TEXT_FILE_TYPES = ['.json', '.md', '.txt', '.py', '.html', '.css', '.js']
IMAGE_FILE_TYPES = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.svg']

ALL_FILE_TYPES = TEXT_FILE_TYPES + IMAGE_FILE_TYPES


class UnifiedMemorySearch:
    """统一记忆搜索类"""

    def __init__(self):
        self.results = []

        # 初始化结构化记忆文件（如果不存在）
        self._init_structured_memory()

    def _init_structured_memory(self):
        """初始化结构化记忆文件"""
        memory_file = SOURCES['structured_memory']

        if not memory_file.exists():
            try:
                memory_file.parent.mkdir(parents=True, exist_ok=True)

                # 创建空的结构化记忆
                empty_memory = {
                    'owner': {},
                    'self': {},
                    'status': {},
                    'settings': {},
                    'last_updated': datetime.now().isoformat()
                }

                with open(memory_file, 'w', encoding='utf-8') as f:
                    json.dump(empty_memory, f, ensure_ascii=False, indent=2)

                print(f"✅ 已创建结构化记忆文件: {memory_file}")

            except Exception as e:
                print(f"❌ 创建结构化记忆文件失败: {e}")

    def search(self, **kwargs):
        """执行搜索"""
        action = kwargs.get('action')

        if action == 'summary':
            return self.get_summary()
        elif action == 'info':
            return self.get_info(kwargs.get('key'))
        else:
            return self.search_memory(**kwargs)

    def search_memory(self, **kwargs):
        """搜索记忆"""
        keywords = kwargs.get('keywords', [])
        days = kwargs.get('days')
        fuzzy = kwargs.get('fuzzy', False)
        regex = kwargs.get('regex')
        search_type = kwargs.get('type')
        importance = kwargs.get('importance')

        self.results = []

        # 1. 搜索结构化记忆（最高优先级）
        if not search_type or search_type in ['structured_memory', 'owner', 'self']:
            self.search_structured_memory(keywords, importance)

        # 2. 搜索对话记录
        if not search_type or search_type in ['dialogue', 'dialogues']:
            self.search_dialogues(keywords, days, fuzzy, regex, importance)

        # 3. 搜索成长日志
        if not search_type or search_type in ['growth', 'growth_log']:
            self.search_growth_log(keywords, days, importance)

        # 4. 搜索文件系统
        if not search_type or search_type == 'files':
            self.search_files(keywords, days, fuzzy, regex)

        # 按相关性排序
        self.results.sort(key=lambda x: x['relevance'], reverse=True)

        return {
            'total_results': len(self.results),
            'results': self.results
        }

    def search_structured_memory(self, keywords, importance):
        """搜索结构化记忆"""
        memory_file = SOURCES['structured_memory']

        if not memory_file.exists():
            return

        try:
            with open(memory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 搜索所有字段
            for key, value in data.items():
                if key == 'last_updated':
                    continue

                # 检查重要性
                if importance and not self.check_importance(value, importance):
                    continue

                # 检查关键词
                if self.match_keywords(value, keywords):
                    self.results.append({
                        'source': 'structured_memory',
                        'type': key,
                        'content': value,
                        'relevance': 1.0  # 结构化记忆优先级最高
                    })

        except Exception as e:
            print(f"搜索结构化记忆失败: {e}")

    def search_dialogues(self, keywords, days, fuzzy, regex, importance):
        """搜索对话记录"""
        dialogue_file = SOURCES['dialogues']

        if not dialogue_file.exists():
            print(f"⚠️ 对话记录文件不存在: {dialogue_file}")
            print(f"💡 请确保记忆增强技能正常工作")
            return

        try:
            with open(dialogue_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            dialogues = data.get('dialogues', {})

            for dialogue_id, dialogue in dialogues.items():
                # 检查时间范围
                if days and not self.check_time_range(dialogue_id, days):
                    continue

                content = dialogue.get('content', '')

                # 检查关键词
                if keywords:
                    if fuzzy:
                        if not any(kw in content for kw in keywords):
                            continue
                    elif regex:
                        if not re.search(regex, content):
                            continue
                    else:
                        if not all(kw in content for kw in keywords):
                            continue

                # 计算相关性
                relevance = 0.8
                if importance and dialogue.get('importance') == importance:
                    relevance += 0.1

                self.results.append({
                    'source': 'dialogues',
                    'id': dialogue_id,
                    'session': dialogue.get('session_name'),
                    'content': content,
                    'tags': dialogue.get('tags', []),
                    'relevance': relevance
                })

        except Exception as e:
            print(f"搜索对话记录失败: {e}")

    def search_growth_log(self, keywords, days, importance):
        """搜索成长日志"""
        growth_file = SOURCES['growth_log']

        if not growth_file.exists():
            return

        try:
            with open(growth_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            events = data.get('events', [])

            for event in events:
                # 检查时间范围
                if days and not self.check_time_range(event['timestamp'], days):
                    continue

                description = event.get('description', '')
                title = event.get('title', '')

                # 检查关键词
                if keywords:
                    content = f"{title} {description}"
                    if not any(kw in content for kw in keywords):
                        continue

                # 检查重要性
                if importance and event.get('impact') != importance:
                    continue

                self.results.append({
                    'source': 'growth_log',
                    'type': event.get('type'),
                    'title': title,
                    'content': description,
                    'timestamp': event.get('timestamp'),
                    'relevance': 0.7
                })

        except Exception as e:
            print(f"搜索成长日志失败: {e}")

    def search_files(self, keywords, days, fuzzy, regex):
        """搜索文件系统"""
        # 排除不需要搜索的目录
        exclude_dirs = {'.git', '__pycache__', '.DS_Store', 'node_modules', '.cache', 'tmp', 'temp'}

        for filepath in BASE_DIR.rglob("*"):
            if not filepath.is_file():
                continue

            # 排除特定目录
            if any(exclude_dir in filepath.parts for exclude_dir in exclude_dirs):
                continue

            # 检查文件类型
            if filepath.suffix.lower() not in ALL_FILE_TYPES:
                continue

            # 检查文件名
            if keywords and any(kw.lower() in filepath.name.lower() for kw in keywords):
                self.results.append({
                    'source': 'file',
                    'type': 'filename',
                    'file_type': filepath.suffix,
                    'path': str(filepath.relative_to(BASE_DIR)),
                    'content': filepath.name,
                    'relevance': 0.6
                })

            # 检查文件内容（仅文本文件）
            if filepath.suffix.lower() in TEXT_FILE_TYPES:
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    if keywords:
                        if fuzzy:
                            if any(kw in content for kw in keywords):
                                self.results.append({
                                    'source': 'file',
                                    'type': 'content',
                                    'path': str(filepath.relative_to(BASE_DIR)),
                                    'content': content[:200],
                                    'relevance': 0.5
                                })
                        elif regex:
                            match = re.search(regex, content)
                            if match:
                                self.results.append({
                                    'source': 'file',
                                    'type': 'content',
                                    'path': str(filepath.relative_to(BASE_DIR)),
                                    'content': match.group()[:200],
                                    'relevance': 0.5
                                })
                        else:
                            if all(kw in content for kw in keywords):
                                self.results.append({
                                    'source': 'file',
                                    'type': 'content',
                                    'path': str(filepath.relative_to(BASE_DIR)),
                                    'content': content[:200],
                                    'relevance': 0.5
                                })

                except Exception:
                    continue

    def get_summary(self):
        """获取记忆摘要"""
        summary = {}

        # 获取结构化记忆
        if SOURCES['structured_memory'].exists():
            with open(SOURCES['structured_memory'], 'r', encoding='utf-8') as f:
                data = json.load(f)
            summary['structured_memory'] = data

        # 获取最近的对话
        if SOURCES['dialogues'].exists():
            with open(SOURCES['dialogues'], 'r', encoding='utf-8') as f:
                data = json.load(f)
            dialogues = data.get('dialogues', {})
            recent_dialogues = sorted(dialogues.items(), key=lambda x: x[0], reverse=True)[:5]
            summary['recent_dialogues'] = [
                {'id': k, 'session': v.get('session_name'), 'preview': v.get('content', '')[:100]}
                for k, v in recent_dialogues
            ]
        else:
            summary['dialogues_note'] = "对话记录文件不存在，请确保记忆增强技能正常工作"

        return summary

    def get_info(self, key):
        """获取特定信息"""
        if not SOURCES['structured_memory'].exists():
            return {}

        with open(SOURCES['structured_memory'], 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data.get(key, {})

    def match_keywords(self, content, keywords):
        """检查是否匹配关键词"""
        if not keywords:
            return True

        content_str = json.dumps(content, ensure_ascii=False).lower()

        return all(kw.lower() in content_str for kw in keywords)

    def check_importance(self, content, importance):
        """检查重要性"""
        if isinstance(content, dict):
            return content.get('importance') == importance
        return False

    def check_time_range(self, timestamp, days):
        """检查是否在时间范围内"""
        try:
            # 处理 dialogue_id 格式：20260416_0006
            if isinstance(timestamp, str) and re.match(r'^\d{8}_\d{4}$', timestamp):
                # 解析日期部分：20260416 → 2026-04-16
                date_str = timestamp[:8]
                parsed_date = datetime.strptime(date_str, '%Y%m%d')
                timestamp = parsed_date

            elif isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

            elif isinstance(timestamp, (int, float)):
                timestamp = datetime.fromtimestamp(timestamp)

            cutoff = datetime.now() - timedelta(days=days)
            return timestamp >= cutoff

        except Exception as e:
            print(f"⚠️ 时间解析失败: {timestamp}, 错误: {e}")
            return True


def main():
    parser = argparse.ArgumentParser(description='统一记忆搜索工具')

    # 搜索方式
    parser.add_argument('--keywords', nargs='+', help='关键词列表')
    parser.add_argument('--fuzzy', action='store_true', help='模糊搜索')
    parser.add_argument('--regex', help='正则表达式')
    parser.add_argument('--days', type=int, help='搜索最近N天')

    # 过滤条件
    parser.add_argument('--type', help='按类型搜索')
    parser.add_argument('--importance', help='按重要性搜索')

    # 获取信息
    parser.add_argument('--action', choices=['summary', 'info'], help='操作类型')
    parser.add_argument('--key', help='信息键名')

    args = parser.parse_args()

    # 执行搜索
    searcher = UnifiedMemorySearch()

    if args.action:
        result = searcher.search(action=args.action, key=args.key)
    else:
        result = searcher.search(
            keywords=args.keywords,
            days=args.days,
            fuzzy=args.fuzzy,
            regex=args.regex,
            type=args.type,
            importance=args.importance
        )

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
