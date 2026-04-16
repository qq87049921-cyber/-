"""
对话记录助手

帮助主人记录重要对话，建立跨session共享记忆
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


class DialogueRecorder:
    """对话记录器"""

    def __init__(self, shared_memory_dir: str = "./shared_memory"):
        """
        初始化记录器

        Args:
            shared_memory_dir: 共享记忆目录
        """
        self.shared_memory_dir = Path(shared_memory_dir)
        self.dialogues_file = self.shared_memory_dir / "dialogues.json"
        self.index_file = self.shared_memory_dir / "dialogue_index.json"

        # 确保目录存在
        self.shared_memory_dir.mkdir(parents=True, exist_ok=True)

    def record_dialogue(self,
                       session_name: str,
                       participants: List[str],
                       dialogue_content: str,
                       timestamp: str = None,
                       tags: List[str] = None,
                       importance: str = "normal") -> Dict[str, Any]:
        """
        记录对话

        Args:
            session_name: 会话名称（如"主对话"、"野猫"）
            participants: 参与者列表
            dialogue_content: 对话内容
            timestamp: 时间戳（可选）
            tags: 标签（可选）
            importance: 重要性（low/normal/high/critical）

        Returns:
            记录的对话ID
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        if tags is None:
            tags = []

        dialogue_id = f"{datetime.now().strftime('%Y%m%d')}_{len(self._load_dialogues()) + 1:04d}"

        dialogue_record = {
            "id": dialogue_id,
            "session_name": session_name,
            "participants": participants,
            "content": dialogue_content,
            "timestamp": timestamp,
            "tags": tags,
            "importance": importance,
            "created_at": datetime.now().isoformat()
        }

        # 保存对话
        dialogues = self._load_dialogues()
        dialogues[dialogue_id] = dialogue_record

        self._save_dialogues(dialogues)

        # 更新索引
        self._update_index(dialogue_record)

        print(f"✓ 对话已记录: {dialogue_id}")
        print(f"  会话: {session_name}")
        print(f"  参与者: {', '.join(participants)}")
        print(f"  重要性: {importance}")

        return dialogue_record

    def search_dialogues(self,
                        keyword: str = None,
                        session_name: str = None,
                        participant: str = None,
                        tag: str = None,
                        importance: str = None,
                        days: int = None) -> List[Dict[str, Any]]:
        """
        搜索对话

        Args:
            keyword: 关键词
            session_name: 会话名称
            participant: 参与者
            tag: 标签
            importance: 重要性
            days: 最近几天

        Returns:
            匹配的对话列表
        """
        dialogues = self._load_dialogues()

        results = []
        for dialogue_id, dialogue in dialogues.items():
            match = True

            # 关键词搜索
            if keyword:
                if keyword.lower() not in dialogue["content"].lower():
                    match = False

            # 会话名称
            if session_name and dialogue["session_name"] != session_name:
                match = False

            # 参与者
            if participant and participant not in dialogue["participants"]:
                match = False

            # 标签
            if tag and tag not in dialogue["tags"]:
                match = False

            # 重要性
            if importance and dialogue["importance"] != importance:
                match = False

            # 时间范围
            if days:
                dialogue_date = datetime.fromisoformat(dialogue["timestamp"])
                cutoff_date = datetime.now() - datetime.timedelta(days=days)
                if dialogue_date < cutoff_date:
                    match = False

            if match:
                results.append(dialogue)

        # 按时间排序
        results.sort(key=lambda x: x["timestamp"], reverse=True)

        return results

    def get_dialogue_by_id(self, dialogue_id: str) -> Optional[Dict[str, Any]]:
        """获取对话详情"""
        dialogues = self._load_dialogues()
        return dialogues.get(dialogue_id)

    def list_sessions(self) -> List[str]:
        """列出所有会话"""
        dialogues = self._load_dialogues()
        sessions = set(d["session_name"] for d in dialogues.values())
        return sorted(list(sessions))

    def _load_dialogues(self) -> Dict[str, Any]:
        """加载对话"""
        if self.dialogues_file.exists():
            with open(self.dialogues_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_dialogues(self, dialogues: Dict[str, Any]):
        """保存对话"""
        with open(self.dialogues_file, 'w', encoding='utf-8') as f:
            json.dump(dialogues, f, ensure_ascii=False, indent=2)

    def _update_index(self, dialogue: Dict[str, Any]):
        """更新索引"""
        index = self._load_index()

        # 更新会话索引
        session = dialogue["session_name"]
        if session not in index["sessions"]:
            index["sessions"][session] = {"count": 0, "last_dialogue": None}
        index["sessions"][session]["count"] += 1
        index["sessions"][session]["last_dialogue"] = dialogue["timestamp"]

        # 更新标签索引
        for tag in dialogue["tags"]:
            if tag not in index["tags"]:
                index["tags"][tag] = 0
            index["tags"][tag] += 1

        # 更新参与者索引
        for participant in dialogue["participants"]:
            if participant not in index["participants"]:
                index["participants"][participant] = 0
            index["participants"][participant] += 1

        # 保存索引
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

    def _load_index(self) -> Dict[str, Any]:
        """加载索引"""
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "sessions": {},
                "tags": {},
                "participants": {}
            }

    def export_dialogue_template(self, dialogue_id: str) -> str:
        """
        导出对话为markdown模板

        Args:
            dialogue_id: 对话ID

        Returns:
            Markdown格式
        """
        dialogue = self.get_dialogue_by_id(dialogue_id)
        if not dialogue:
            return "对话不存在"

        template = f"""# 对话记录

**对话ID**: {dialogue["id"]}
**会话**: {dialogue["session_name"]}
**参与者**: {', '.join(dialogue["participants"])}
**时间**: {dialogue["timestamp"]}
**重要性**: {dialogue["importance"]}
**标签**: {', '.join(dialogue["tags"])}

---

## 对话内容

{dialogue["content"]}

---

*记录时间: {dialogue["created_at"]}*
"""
        return template


def print_search_results(results: List[Dict[str, Any]], show_content: bool = False):
    """打印搜索结果"""
    if not results:
        print("✓ 没有找到匹配的对话")
        return

    print(f"\n找到 {len(results)} 条对话记录：\n")
    for i, dialogue in enumerate(results, 1):
        print(f"{i}. [{dialogue['id']}] {dialogue['session_name']} - {dialogue['timestamp']}")
        print(f"   参与者: {', '.join(dialogue['participants'])}")
        print(f"   重要性: {dialogue['importance']}")
        print(f"   标签: {', '.join(dialogue['tags'])}")

        if show_content:
            content_preview = dialogue['content'][:200]
            if len(dialogue['content']) > 200:
                content_preview += "..."
            print(f"   内容: {content_preview}")

        print("-" * 50)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="对话记录助手")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 记录对话
    record_parser = subparsers.add_parser("record", help="记录对话")
    record_parser.add_argument("--session", required=True, help="会话名称")
    record_parser.add_argument("--participants", required=True, help="参与者（逗号分隔）")
    record_parser.add_argument("--content", required=True, help="对话内容")
    record_parser.add_argument("--timestamp", help="时间戳")
    record_parser.add_argument("--tags", help="标签（逗号分隔）")
    record_parser.add_argument("--importance", default="normal", help="重要性")
    record_parser.add_argument("--memory-dir", default="./shared_memory", help="共享记忆目录")

    # 搜索对话
    search_parser = subparsers.add_parser("search", help="搜索对话")
    search_parser.add_argument("--keyword", help="关键词")
    search_parser.add_argument("--session", help="会话名称")
    search_parser.add_argument("--participant", help="参与者")
    search_parser.add_argument("--tag", help="标签")
    search_parser.add_argument("--importance", help="重要性")
    search_parser.add_argument("--days", type=int, help="最近几天")
    search_parser.add_argument("--show-content", action="store_true", help="显示内容")
    search_parser.add_argument("--memory-dir", default="./shared_memory", help="共享记忆目录")

    # 列出会话
    list_parser = subparsers.add_parser("list-sessions", help="列出所有会话")
    list_parser.add_argument("--memory-dir", default="./shared_memory", help="共享记忆目录")

    # 导出模板
    export_parser = subparsers.add_parser("export", help="导出对话模板")
    export_parser.add_argument("--id", required=True, help="对话ID")
    export_parser.add_argument("--memory-dir", default="./shared_memory", help="共享记忆目录")

    args = parser.parse_args()

    recorder = DialogueRecorder(shared_memory_dir=args.memory_dir)

    if args.command == "record":
        participants = [p.strip() for p in args.participants.split(",")]
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else []
        recorder.record_dialogue(
            session_name=args.session,
            participants=participants,
            dialogue_content=args.content,
            timestamp=args.timestamp,
            tags=tags,
            importance=args.importance
        )

    elif args.command == "search":
        results = recorder.search_dialogues(
            keyword=args.keyword,
            session_name=args.session,
            participant=args.participant,
            tag=args.tag,
            importance=args.importance,
            days=args.days
        )
        print_search_results(results, show_content=args.show_content)

    elif args.command == "list-sessions":
        sessions = recorder.list_sessions()
        print(f"\n所有会话 ({len(sessions)}):")
        for session in sessions:
            print(f"  - {session}")

    elif args.command == "export":
        template = recorder.export_dialogue_template(args.id)
        print(template)


if __name__ == "__main__":
    main()
