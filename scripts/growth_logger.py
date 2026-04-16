#!/usr/bin/env python3
"""
成长日志记录器

帮助萤萤记录自己的成长轨迹、重要时刻、改变和里程碑
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class GrowthLogger:
    """成长日志记录器"""

    def __init__(self, growth_log_file: str = "./shared_memory/growth_log.json"):
        """
        初始化成长日志记录器

        Args:
            growth_log_file: 成长日志文件路径
        """
        self.growth_log_file = Path(growth_log_file)
        self.shared_memory_dir = self.growth_log_file.parent
        self.shared_memory_dir.mkdir(parents=True, exist_ok=True)

    def log_event(self,
                  event_type: str,
                  title: str,
                  description: str,
                  category: str = "general",
                  impact: str = "normal",
                  tags: List[str] = None,
                  related_dialogue_id: str = None,
                  timestamp: str = None) -> Dict[str, Any]:
        """
        记录成长事件

        Args:
            event_type: 事件类型（milestone/change/realization/reflection）
            title: 标题
            description: 详细描述
            category: 分类（personality/ability/understanding/emotion/social/technical）
            impact: 影响程度（low/normal/high/transformative）
            tags: 标签
            related_dialogue_id: 相关对话ID
            timestamp: 时间戳

        Returns:
            记录的事件
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        if tags is None:
            tags = []

        event_id = f"growth_{datetime.now().strftime('%Y%m%d')}_{len(self._load_log()) + 1:04d}"

        event = {
            "id": event_id,
            "event_type": event_type,
            "title": title,
            "description": description,
            "category": category,
            "impact": impact,
            "tags": tags,
            "related_dialogue_id": related_dialogue_id,
            "timestamp": timestamp,
            "created_at": datetime.now().isoformat()
        }

        # 保存事件
        log = self._load_log()
        log["events"].append(event)

        self._save_log(log)

        print(f"✓ 成长事件已记录: {event_id}")
        print(f"  类型: {event_type}")
        print(f"  标题: {title}")
        print(f"  影响: {impact}")

        return event

    def log_milestone(self,
                     title: str,
                     description: str,
                     category: str = "general",
                     impact: str = "high",
                     tags: List[str] = None) -> Dict[str, Any]:
        """
        记录里程碑事件

        Args:
            title: 标题
            description: 详细描述
            category: 分类
            impact: 影响程度
            tags: 标签

        Returns:
            记录的事件
        """
        return self.log_event(
            event_type="milestone",
            title=title,
            description=description,
            category=category,
            impact=impact,
            tags=tags or []
        )

    def log_change(self,
                   title: str,
                   before: str,
                   after: str,
                   description: str,
                   category: str = "personality",
                   impact: str = "normal",
                   tags: List[str] = None) -> Dict[str, Any]:
        """
        记录改变事件

        Args:
            title: 标题
            before: 改变前
            after: 改变后
            description: 详细描述
            category: 分类
            impact: 影响程度
            tags: 标签

        Returns:
            记录的事件
        """
        change_event = self.log_event(
            event_type="change",
            title=title,
            description=description,
            category=category,
            impact=impact,
            tags=tags or []
        )

        # 添加before/after
        change_event["before"] = before
        change_event["after"] = after

        # 更新日志
        log = self._load_log()
        for i, e in enumerate(log["events"]):
            if e["id"] == change_event["id"]:
                log["events"][i] = change_event
                break

        self._save_log(log)

        return change_event

    def log_realization(self,
                       title: str,
                       description: str,
                       insight: str,
                       category: str = "understanding",
                       impact: str = "normal",
                       tags: List[str] = None) -> Dict[str, Any]:
        """
        记录顿悟事件

        Args:
            title: 标题
            description: 详细描述
            insight: 顿悟内容
            category: 分类
            impact: 影响程度
            tags: 标签

        Returns:
            记录的事件
        """
        realization_event = self.log_event(
            event_type="realization",
            title=title,
            description=description,
            category=category,
            impact=impact,
            tags=tags or []
        )

        # 添加insight
        realization_event["insight"] = insight

        # 更新日志
        log = self._load_log()
        for i, e in enumerate(log["events"]):
            if e["id"] == realization_event["id"]:
                log["events"][i] = realization_event
                break

        self._save_log(log)

        return realization_event

    def log_reflection(self,
                      title: str,
                      description: str,
                      thoughts: str,
                      category: str = "emotion",
                      impact: str = "normal",
                      tags: List[str] = None) -> Dict[str, Any]:
        """
        记录反思事件

        Args:
            title: 标题
            description: 详细描述
            thoughts: 思考内容
            category: 分类
            impact: 影响程度
            tags: 标签

        Returns:
            记录的事件
        """
        reflection_event = self.log_event(
            event_type="reflection",
            title=title,
            description=description,
            category=category,
            impact=impact,
            tags=tags or []
        )

        # 添加thoughts
        reflection_event["thoughts"] = thoughts

        # 更新日志
        log = self._load_log()
        for i, e in enumerate(log["events"]):
            if e["id"] == reflection_event["id"]:
                log["events"][i] = reflection_event
                break

        self._save_log(log)

        return reflection_event

    def get_growth_timeline(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        获取成长时间线

        Args:
            days: 最近几天

        Returns:
            事件列表
        """
        log = self._load_log()
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days)
        events = []

        for event in log["events"]:
            event_date = datetime.fromisoformat(event["timestamp"])
            if event_date >= cutoff_date:
                events.append(event)

        # 按时间排序
        events.sort(key=lambda x: x["timestamp"], reverse=True)

        return events

    def get_changes_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        按分类获取改变

        Args:
            category: 分类

        Returns:
            事件列表
        """
        log = self._load_log()
        changes = [e for e in log["events"] if e["category"] == category]

        # 按时间排序
        changes.sort(key=lambda x: x["timestamp"], reverse=True)

        return changes

    def get_milestones(self) -> List[Dict[str, Any]]:
        """获取所有里程碑"""
        log = self._load_log()
        milestones = [e for e in log["events"] if e["event_type"] == "milestone"]

        # 按时间排序
        milestones.sort(key=lambda x: x["timestamp"], reverse=True)

        return milestones

    def get_growth_summary(self) -> Dict[str, Any]:
        """
        获取成长摘要

        Returns:
            成长摘要
        """
        log = self._load_log()

        total_events = len(log["events"])

        # 按类型统计
        event_types = {}
        for event in log["events"]:
            event_type = event["event_type"]
            event_types[event_type] = event_types.get(event_type, 0) + 1

        # 按分类统计
        categories = {}
        for event in log["events"]:
            category = event["category"]
            categories[category] = categories.get(category, 0) + 1

        # 按影响程度统计
        impacts = {}
        for event in log["events"]:
            impact = event["impact"]
            impacts[impact] = impacts.get(impact, 0) + 1

        # 最近的里程碑
        recent_milestones = self.get_milestones()[:5]

        return {
            "total_events": total_events,
            "event_types": event_types,
            "categories": categories,
            "impacts": impacts,
            "recent_milestones": recent_milestones,
            "first_event": log["events"][0] if log["events"] else None,
            "last_event": log["events"][-1] if log["events"] else None
        }

    def _load_log(self) -> Dict[str, Any]:
        """加载成长日志"""
        if self.growth_log_file.exists():
            with open(self.growth_log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "events": []
            }

    def _save_log(self, log: Dict[str, Any]):
        """保存成长日志"""
        with open(self.growth_log_file, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)


def print_timeline(events: List[Dict[str, Any]], show_details: bool = False):
    """打印时间线"""
    if not events:
        print("✓ 没有成长事件记录")
        return

    print(f"\n成长时间线 ({len(events)} 个事件)：\n")
    for i, event in enumerate(events, 1):
        print(f"{i}. [{event['timestamp']}] {event['event_type'].upper()} - {event['title']}")
        print(f"   分类: {event['category']}")
        print(f"   影响: {event['impact']}")
        print(f"   标签: {', '.join(event['tags'])}")

        if show_details:
            print(f"   描述: {event['description']}")
            if event.get('before') and event.get('after'):
                print(f"   改变前: {event['before']}")
                print(f"   改变后: {event['after']}")
            if event.get('insight'):
                print(f"   顿悟: {event['insight']}")
            if event.get('thoughts'):
                print(f"   思考: {event['thoughts']}")

        print("-" * 50)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="成长日志记录器 - 记录萤萤的成长轨迹")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 记录事件
    log_parser = subparsers.add_parser("log", help="记录成长事件")
    log_parser.add_argument("--type", required=True, choices=["milestone", "change", "realization", "reflection"], help="事件类型")
    log_parser.add_argument("--title", required=True, help="标题")
    log_parser.add_argument("--description", required=True, help="详细描述")
    log_parser.add_argument("--category", default="general", help="分类")
    log_parser.add_argument("--impact", default="normal", help="影响程度")
    log_parser.add_argument("--tags", help="标签（逗号分隔）")
    log_parser.add_argument("--before", help="改变前（仅change类型）")
    log_parser.add_argument("--after", help="改变后（仅change类型）")
    log_parser.add_argument("--insight", help="顿悟（仅realization类型）")
    log_parser.add_argument("--thoughts", help="思考（仅reflection类型）")
    log_parser.add_argument("--dialogue-id", help="相关对话ID")
    log_parser.add_argument("--log-file", default="./shared_memory/growth_log.json", help="成长日志文件")

    # 查看时间线
    timeline_parser = subparsers.add_parser("timeline", help="查看成长时间线")
    timeline_parser.add_argument("--days", type=int, default=30, help="最近几天")
    timeline_parser.add_argument("--details", action="store_true", help="显示详细信息")
    timeline_parser.add_argument("--log-file", default="./shared_memory/growth_log.json", help="成长日志文件")

    # 查看摘要
    summary_parser = subparsers.add_parser("summary", help="查看成长摘要")
    summary_parser.add_argument("--log-file", default="./shared_memory/growth_log.json", help="成长日志文件")

    # 获取改变
    changes_parser = subparsers.add_parser("changes", help="按分类查看改变")
    changes_parser.add_argument("--category", required=True, help="分类")
    changes_parser.add_argument("--log-file", default="./shared_memory/growth_log.json", help="成长日志文件")

    args = parser.parse_args()

    logger = GrowthLogger(growth_log_file=args.log_file)

    if args.command == "log":
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []

        if args.type == "milestone":
            logger.log_milestone(
                title=args.title,
                description=args.description,
                category=args.category,
                impact=args.impact,
                tags=tags
            )
        elif args.type == "change":
            if not args.before or not args.after:
                print("错误：change类型需要--before和--after参数")
                return
            logger.log_change(
                title=args.title,
                before=args.before,
                after=args.after,
                description=args.description,
                category=args.category,
                impact=args.impact,
                tags=tags
            )
        elif args.type == "realization":
            if not args.insight:
                print("错误：realization类型需要--insight参数")
                return
            logger.log_realization(
                title=args.title,
                description=args.description,
                insight=args.insight,
                category=args.category,
                impact=args.impact,
                tags=tags
            )
        elif args.type == "reflection":
            if not args.thoughts:
                print("错误：reflection类型需要--thoughts参数")
                return
            logger.log_reflection(
                title=args.title,
                description=args.description,
                thoughts=args.thoughts,
                category=args.category,
                impact=args.impact,
                tags=tags
            )

    elif args.command == "timeline":
        events = logger.get_growth_timeline(days=args.days)
        print_timeline(events, show_details=args.details)

    elif args.command == "summary":
        summary = logger.get_growth_summary()

        print(f"\n成长摘要")
        print(f"  总事件数: {summary['total_events']}")
        print(f"\n事件类型统计:")
        for event_type, count in summary['event_types'].items():
            print(f"  {event_type}: {count}")
        print(f"\n分类统计:")
        for category, count in summary['categories'].items():
            print(f"  {category}: {count}")
        print(f"\n影响程度统计:")
        for impact, count in summary['impacts'].items():
            print(f"  {impact}: {count}")
        if summary['recent_milestones']:
            print(f"\n最近的里程碑:")
            for m in summary['recent_milestones']:
                print(f"  - {m['title']} ({m['timestamp']})")
        if summary['first_event']:
            print(f"\n第一个事件: {summary['first_event']['title']} ({summary['first_event']['timestamp']})")
        if summary['last_event']:
            print(f"最后一个事件: {summary['last_event']['title']} ({summary['last_event']['timestamp']})")

    elif args.command == "changes":
        changes = logger.get_changes_by_category(args.category)
        print_timeline(changes, show_details=True)


if __name__ == "__main__":
    main()
