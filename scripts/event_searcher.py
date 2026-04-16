"""
增强版事件搜索工具

支持多种搜索方式：关键词、时间范围、模糊搜索、正则表达式
"""

import os
import re
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any


class EventSearcher:
    """事件搜索器"""

    def __init__(self, memory_file: str = None):
        """
        初始化搜索器

        Args:
            memory_file: 记忆文件路径
        """
        self.memory_file = memory_file
        self.memory = self._load_memory()

    def _load_memory(self) -> Dict[str, Any]:
        """加载记忆"""
        if self.memory_file and os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def search_by_keywords(self, keywords: List[str], exact_match: bool = False) -> List[Dict]:
        """
        关键词搜索

        Args:
            keywords: 关键词列表
            exact_match: 是否精确匹配

        Returns:
            匹配的结果列表
        """
        results = []

        # 搜索记忆文件
        if self.memory:
            memory_str = json.dumps(self.memory, ensure_ascii=False).lower()
            keyword_matches = []
            for keyword in keywords:
                if exact_match:
                    if keyword.lower() in memory_str.split():
                        keyword_matches.append(keyword)
                else:
                    if keyword.lower() in memory_str:
                        keyword_matches.append(keyword)

            if keyword_matches:
                results.append({
                    "source": "memory_file",
                    "matched_keywords": keyword_matches,
                    "content": self.memory
                })

        # 搜索其他文件
        base_dir = Path(".")
        for filepath in base_dir.rglob("*.json"):
            if "memory" in filepath.name.lower() or "对话" in filepath.name.lower():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    keyword_matches = []
                    for keyword in keywords:
                        if exact_match:
                            if re.search(r'\b' + re.escape(keyword) + r'\b', content, re.IGNORECASE):
                                keyword_matches.append(keyword)
                        else:
                            if keyword.lower() in content.lower():
                                keyword_matches.append(keyword)

                    if keyword_matches:
                        results.append({
                            "source": str(filepath),
                            "matched_keywords": keyword_matches,
                            "preview": self._get_preview(content, keywords)
                        })
                except Exception as e:
                    continue

        return results

    def search_by_time_range(self, days: int, keywords: List[str] = None) -> List[Dict]:
        """
        按时间范围搜索

        Args:
            days: 最近几天
            keywords: 可选的关键词过滤

        Returns:
            匹配的结果列表
        """
        results = []
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")

        base_dir = Path(".")
        for filepath in base_dir.rglob("*"):
            if filepath.is_file():
                # 检查文件修改时间
                mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                if mtime >= cutoff_date:
                    # 可选：过滤关键词
                    if keywords:
                        try:
                            with open(filepath, 'r', encoding='utf-8') as f:
                                content = f.read()

                            if all(kw.lower() in content.lower() for kw in keywords):
                                results.append({
                                    "source": str(filepath),
                                    "modified_time": mtime.strftime("%Y-%m-%d %H:%M:%S"),
                                    "preview": self._get_preview(content, keywords)
                                })
                        except Exception:
                            continue
                    else:
                        results.append({
                            "source": str(filepath),
                            "modified_time": mtime.strftime("%Y-%m-%d %H:%M:%S")
                        })

        return sorted(results, key=lambda x: x["modified_time"], reverse=True)

    def fuzzy_search(self, query: str) -> List[Dict]:
        """
        模糊搜索

        Args:
            query: 查询文本

        Returns:
            匹配的结果列表
        """
        results = []
        query_lower = query.lower()

        base_dir = Path(".")
        for filepath in base_dir.rglob("*.json"):
            if "memory" in filepath.name.lower() or "对话" in filepath.name.lower():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().lower()

                    # 模糊匹配：计算相似度
                    similarity = self._calculate_similarity(query_lower, content)
                    if similarity > 0.3:  # 30% 相似度阈值
                        results.append({
                            "source": str(filepath),
                            "similarity": similarity,
                            "preview": self._get_preview(content, query.split())
                        })
                except Exception:
                    continue

        return sorted(results, key=lambda x: x["similarity"], reverse=True)

    def search_with_regex(self, pattern: str) -> List[Dict]:
        """
        正则表达式搜索

        Args:
            pattern: 正则表达式

        Returns:
            匹配的结果列表
        """
        results = []

        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as e:
            print(f"正则表达式错误: {e}")
            return []

        base_dir = Path(".")
        for filepath in base_dir.rglob("*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                matches = regex.findall(content)
                if matches:
                    results.append({
                        "source": str(filepath),
                        "matches": matches[:5],  # 只显示前 5 个匹配
                        "preview": self._get_preview(content, matches[:3])
                    })
            except Exception:
                continue

        return results

    def _get_preview(self, content: str, keywords: List[str], context_length: int = 100) -> str:
        """获取预览"""
        content_lower = content.lower()
        for keyword in keywords:
            keyword_lower = keyword.lower()
            pos = content_lower.find(keyword_lower)
            if pos != -1:
                start = max(0, pos - context_length // 2)
                end = min(len(content), pos + len(keyword) + context_length // 2)
                return "..." + content[start:end] + "..."
        return content[:context_length] + "..."

    def _calculate_similarity(self, query: str, content: str) -> float:
        """计算相似度"""
        query_words = set(query.split())
        content_words = set(content.split())

        if not query_words:
            return 0.0

        # 计算交集比例
        intersection = query_words & content_words
        return len(intersection) / len(query_words)

    def search_recent_events(self, hours: int = 24) -> List[Dict]:
        """
        搜索最近的事件

        Args:
            hours: 最近几小时

        Returns:
            事件列表
        """
        return self.search_by_time_range(days=hours / 24)


def print_results(results: List[Dict]):
    """打印结果"""
    if not results:
        print("✓ 没有找到匹配的结果")
        return

    print(f"\n找到 {len(results)} 个结果：\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. 来源: {result.get('source', '未知')}")
        for key, value in result.items():
            if key != 'source':
                print(f"   {key}: {value}")
        print("-" * 50)


def main():
    """命令行入口"""
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

    args = parser.parse_args()

    searcher = EventSearcher(memory_file=args.memory_file)

    if args.action == "keywords":
        if not args.keywords:
            print("错误: --keywords 参数必填")
            return
        keywords = [k.strip() for k in args.keywords.split(",")]
        results = searcher.search_by_keywords(keywords, exact_match=args.exact)
        print_results(results)

    elif args.action == "time":
        if not args.days:
            print("错误: --days 参数必填")
            return
        results = searcher.search_by_time_range(days=args.days)
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
