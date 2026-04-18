#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主对话导入工具

功能：
- 从文本文件或模板文件导入对话
- 自动转换为 dialogues.json 格式
- 支持批量导入（几千条对话）
- 自动生成对话ID

使用方法：
    python scripts/import_dialogues.py --input dialogues.txt
    python scripts/import_dialogues.py --input dialogues.txt --session "主对话"
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


class DialogueImporter:
    """对话导入器"""

    def __init__(self, memory_dir: str = "./shared_memory"):
        """初始化导入器"""
        self.memory_dir = Path(memory_dir)
        self.dialogues_file = self.memory_dir / "dialogues.json"

        # 确保目录存在
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def load_dialogues(self) -> Dict[str, Any]:
        """加载现有对话"""
        if self.dialogues_file.exists():
            with open(self.dialogues_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                "type": "dialogue_database",
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "total_count": 0,
                "dialogues": {}
            }

    def parse_plain_text(self, content: str, session_name: str = "主对话") -> List[Dict[str, Any]]:
        """
        解析纯文本对话

        支持的格式：
        1. 角色名：内容
        2. [时间] 角色名：内容
        3. --- （分隔符，多条对话）

        示例：
        主人：你好
        萤萤：你好呀~
        ---
        主人：今天天气怎么样？
        萤萤：今天是晴天哦！~
        """
        dialogues = []
        current_dialogue = []
        dialogue_count = 0

        for line in content.split('\n'):
            line = line.strip()

            # 跳过空行
            if not line:
                continue

            # 分隔符，结束当前对话
            if line == '---' or line == '===':
                if current_dialogue:
                    dialogue_count += 1
                    dialogue_content = '\n'.join(current_dialogue)
                    dialogues.append({
                        "id": f"{datetime.now().strftime('%Y%m%d')}_{dialogue_count:04d}",
                        "session_name": session_name,
                        "participants": ["主人", "萤萤"],
                        "content": dialogue_content,
                        "timestamp": datetime.now().isoformat(),
                        "tags": [],
                        "importance": "normal",
                        "created_at": datetime.now().isoformat()
                    })
                    current_dialogue = []
                continue

            # 解析对话行
            # 格式：角色名：内容
            match = re.match(r'^([^:：]+)[:：](.+)$', line)
            if match:
                role = match.group(1).strip()
                content = match.group(2).strip()
                current_dialogue.append(f"{role}：{content}")
            else:
                # 不是对话行，直接添加
                current_dialogue.append(line)

        # 添加最后一条对话
        if current_dialogue:
            dialogue_count += 1
            dialogue_content = '\n'.join(current_dialogue)
            dialogues.append({
                "id": f"{datetime.now().strftime('%Y%m%d')}_{dialogue_count:04d}",
                "session_name": session_name,
                "participants": ["主人", "萤萤"],
                "content": dialogue_content,
                "timestamp": datetime.now().isoformat(),
                "tags": [],
                "importance": "normal",
                "created_at": datetime.now().isoformat()
            })

        return dialogues

    def parse_json_array(self, content: str) -> List[Dict[str, Any]]:
        """
        解析 JSON 数组格式

        格式：
        [
            {
                "role": "user",
                "content": "你好"
            },
            {
                "role": "assistant",
                "content": "你好呀~"
            }
        ]
        """
        dialogues = []
        dialogue_count = 0

        try:
            messages = json.loads(content)

            current_dialogue = []
            for msg in messages:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")

                if role == "user":
                    current_dialogue.append(f"主人：{content}")
                elif role == "assistant":
                    current_dialogue.append(f"萤萤：{content}")
                elif role == "system":
                    current_dialogue.append(f"系统：{content}")

            if current_dialogue:
                dialogue_count += 1
                dialogue_content = '\n'.join(current_dialogue)
                dialogues.append({
                    "id": f"{datetime.now().strftime('%Y%m%d')}_{dialogue_count:04d}",
                    "session_name": "主对话",
                    "participants": ["主人", "萤萤"],
                    "content": dialogue_content,
                    "timestamp": datetime.now().isoformat(),
                    "tags": [],
                    "importance": "normal",
                    "created_at": datetime.now().isoformat()
                })

        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
            return []

        return dialogues

    def import_dialogues(self, input_file: str, format: str = "auto", session_name: str = "主对话", overwrite: bool = False):
        """
        导入对话

        Args:
            input_file: 输入文件路径
            format: 文件格式（auto/json/plain）
            session_name: 会话名称
            overwrite: 是否覆盖现有对话
        """
        input_path = Path(input_file)

        if not input_path.exists():
            print(f"❌ 文件不存在: {input_file}")
            return

        # 读取文件
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"📖 正在读取文件: {input_file}")
        print(f"   文件大小: {len(content)} 字符")
        print(f"   文件行数: {len(content.split(chr(10)))} 行")

        # 自动检测格式
        if format == "auto":
            if content.strip().startswith('['):
                format = "json"
            else:
                format = "plain"
            print(f"   检测到格式: {format}")

        # 解析对话
        print(f"🔍 正在解析对话...")
        if format == "json":
            dialogues = self.parse_json_array(content)
        elif format == "plain":
            dialogues = self.parse_plain_text(content, session_name)
        else:
            print(f"❌ 不支持的格式: {format}")
            return

        print(f"✅ 解析完成，共 {len(dialogues)} 条对话")

        if len(dialogues) == 0:
            print(f"❌ 没有解析到对话，请检查文件格式")
            return

        # 加载现有对话
        data = self.load_dialogues()
        existing_dialogues = data.get('dialogues', {})

        if not overwrite:
            # 检查是否有重复
            existing_ids = set(existing_dialogues.keys())
            new_ids = set(d['id'] for d in dialogues)
            overlap = existing_ids & new_ids

            if overlap:
                print(f"⚠️ 发现 {len(overlap)} 条重复对话")
                print(f"   重复ID: {', '.join(overlap)}")

            # 只添加新的对话
            count = 0
            for dialogue in dialogues:
                if dialogue['id'] not in existing_ids:
                    existing_dialogues[dialogue['id']] = dialogue
                    count += 1

            print(f"✅ 成功添加 {count} 条新对话")
        else:
            # 覆盖现有对话
            for dialogue in dialogues:
                existing_dialogues[dialogue['id']] = dialogue

            print(f"✅ 成功导入 {len(dialogues)} 条对话（覆盖模式）")

        # 更新统计数据
        data['total_count'] = len(existing_dialogues)
        data['last_updated'] = datetime.now().isoformat()

        # 保存对话
        with open(self.dialogues_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"💾 对话已保存到: {self.dialogues_file}")
        print(f"   总对话数: {data['total_count']}")

        # 显示前3条对话预览
        print(f"\n📋 前3条对话预览:")
        for i, dialogue in enumerate(dialogues[:3], 1):
            print(f"   {i}. [{dialogue['id']}] {dialogue['session_name']}")
            print(f"      {dialogue['content'][:100]}...")


def main():
    parser = argparse.ArgumentParser(description='主对话导入工具')

    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--format', '-f', choices=['auto', 'json', 'plain'], default='auto', help='文件格式')
    parser.add_argument('--session', '-s', default='主对话', help='会话名称')
    parser.add_argument('--overwrite', '-o', action='store_true', help='覆盖现有对话')
    parser.add_argument('--memory-dir', '-m', default='./shared_memory', help='共享记忆目录')

    args = parser.parse_args()

    # 执行导入
    importer = DialogueImporter(memory_dir=args.memory_dir)
    importer.import_dialogues(
        input_file=args.input,
        format=args.format,
        session_name=args.session,
        overwrite=args.overwrite
    )


if __name__ == "__main__":
    main()
