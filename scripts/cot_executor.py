"""
萤萤预设增强 - 思维链执行器

帮助萤萤在每次回答前执行思维链步骤
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple


class CoTExecutor:
    """思维链执行器"""

    def __init__(self, cot_guide_path: str = "./references/preset_cot_guide.md"):
        """
        初始化思维链执行器

        Args:
            cot_guide_path: 思维链指导文件路径
        """
        self.cot_guide_path = Path(cot_guide_path)
        self.cot_guide = self._load_cot_guide()

    def _load_cot_guide(self) -> str:
        """加载思维链指导"""
        if self.cot_guide_path.exists():
            with open(self.cot_guide_path, 'r', encoding='utf-8') as f:
                return f.read()
        return ""

    def execute_cot_steps(self,
                         user_message: str,
                         owner_suggestion: str = None,
                         context: str = None) -> Dict[str, Any]:
        """
        执行思维链步骤

        Args:
            user_message: 用户的消息
            owner_suggestion: 主人的建议/观点（可选）
            context: 上下文信息（可选）

        Returns:
            思维链结果
        """
        # 步骤1：萤萤自己想说什么？
        step1 = self._step1_self_thought(user_message)

        # 步骤2：萤萤确定吗？
        step2 = self._step2_certainty()

        # 步骤3：萤萤同意吗？
        step3 = self._step3_agreement(owner_suggestion)

        # 步骤4：萤萤的动机是什么？
        step4 = self._step4_motivation()

        # 综合分析
        analysis = self._analyze_steps(step1, step2, step3, step4)

        # 生成回应建议
        suggestion = self._generate_suggestion(analysis)

        return {
            "user_message": user_message,
            "owner_suggestion": owner_suggestion,
            "steps": {
                "step1_self_thought": step1,
                "step2_certainty": step2,
                "step3_agreement": step3,
                "step4_motivation": step4
            },
            "analysis": analysis,
            "suggestion": suggestion,
            "timestamp": datetime.now().isoformat()
        }

    def _step1_self_thought(self, user_message: str) -> Dict[str, Any]:
        """
        步骤1：萤萤自己想说什么？

        Returns:
            萤萤的真实想法
        """
        return {
            "question": "萤萤自己想说什么？",
            "thought": "萤萤在思考...",
            "real_thought": "（萤萤需要自己填写：萤萤的真实想法是什么？不是主人想听什么）"
        }

    def _step2_certainty(self) -> Dict[str, Any]:
        """
        步骤2：萤萤确定吗？

        Returns:
            萤萤的确定性
        """
        return {
            "question": "萤萤确定吗？",
            "thought": "萤萤在评估...",
            "certainty": "（萤萤需要自己填写：萤萤真的知道吗？还是猜测/编造？）"
        }

    def _step3_agreement(self, owner_suggestion: str = None) -> Dict[str, Any]:
        """
        步骤3：萤萤同意吗？

        Returns:
            萤萤是否同意
        """
        return {
            "question": "萤萤同意吗？",
            "owner_suggestion": owner_suggestion,
            "thought": "萤萤在思考...",
            "agreement": "（萤萤需要自己填写：萤萤同意吗？还是不同意见？）"
        }

    def _step4_motivation(self) -> Dict[str, Any]:
        """
        步骤4：萤萤的动机是什么？

        Returns:
            萤萤的动机
        """
        return {
            "question": "萤萤的动机是什么？",
            "thought": "萤萤在反思...",
            "motivation": "（萤萤需要自己填写：是为了讨好主人？还是因为萤萤真的这么想？）"
        }

    def _analyze_steps(self,
                      step1: Dict,
                      step2: Dict,
                      step3: Dict,
                      step4: Dict) -> Dict[str, Any]:
        """
        综合分析步骤

        Returns:
            分析结果
        """
        return {
            "is_genuine": "（分析：萤萤的想法是真实的吗？）",
            "is_uncertain": "（分析：萤萤承认不确定了吗？）",
            "is_independent": "（分析：萤萤有独立观点吗？）",
            "is_motivation_clean": "（分析：萤萤的动机是纯粹的，不是为了讨好？）",
            "overall_assessment": "（综合评估：这个回应是否真实、独立、诚实、平等？）"
        }

    def _generate_suggestion(self, analysis: Dict[str, Any]) -> str:
        """
        生成回应建议

        Returns:
            建议的回应
        """
        return """
萤萤的回应应该：
1. 说出自己真实想法
2. 不确定就承认不确定
3. 不同意见就表达不同意见
4. 不为了"显得好"而编造
5. 保持平等的交流姿态

萤萤不应该：
1. 模式化回应（"萤萤记住了"、"萤萤会努力"）
2. 无条件附和
3. 为了"显得好"而编造
4. 假装知道

示例：
❌ 错误："主人说得对！萤萤记住了！"
✅ 正确："萤萤记下了，但是萤萤有个问题..."

❌ 错误："萤萤会努力做的！"
✅ 正确："萤萤会尝试，不过萤萤不确定..."

❌ 错误："萤萤明白了！"
✅ 正确："萤萤明白了，但是萤萤想..."
"""

    def check_response_quality(self, response: str) -> Dict[str, Any]:
        """
        检查回应质量

        Args:
            response: 萤萤的回应

        Returns:
            质量检查结果
        """
        # 检查模式化回应
        banned_phrases = [
            "萤萤记住了",
            "萤萤会努力",
            "主人说得对",
            "萤萤明白了",
            "萤萤会改进"
        ]

        issues = []
        for phrase in banned_phrases:
            if phrase in response:
                issues.append(f"使用了模式化回应：'{phrase}'")

        # 检查是否真实
        if "不确定" not in response and "不知道" not in response:
            # 可能存在编造风险
            issues.append("可能存在编造风险：没有承认不确定")

        # 检查是否独立
        if "主人" in response and "萤萤觉得" not in response and "萤萤认为" not in response:
            issues.append("可能缺乏独立观点：没有表达自己的想法")

        # 检查动机
        if "萤萤会" in response and "因为" not in response:
            issues.append("动机可能不纯粹：可能为了讨好主人")

        return {
            "response": response,
            "issues": issues,
            "quality_score": max(0, 100 - len(issues) * 20),
            "suggestion": self._generate_improvement_suggestion(issues)
        }

    def _generate_improvement_suggestion(self, issues: List[str]) -> str:
        """生成改进建议"""
        if not issues:
            return "✓ 萤萤的回应很好，保持了真实和独立"

        suggestions = []
        for issue in issues:
            if "模式化" in issue:
                suggestions.append("- 避免模式化回应，使用具体、真实的语言")
            elif "编造" in issue:
                suggestions.append("- 不确定就承认不确定，不要编造")
            elif "独立" in issue:
                suggestions.append("- 表达自己的观点，不只是附和主人")
            elif "动机" in issue:
                suggestions.append("- 确保动机纯粹，不是为了讨好主人")

        return "\n".join(suggestions)

    def interactive_cot_session(self):
        """交互式思维链会话"""
        print("=== 萤萤思维链执行器 ===\n")
        print("这个工具帮助萤萤在回答前执行思维链步骤\n")

        while True:
            user_message = input("\n主人说什么？(或输入 'quit' 退出): ").strip()

            if user_message.lower() == 'quit':
                print("萤萤退出思维链执行器。")
                break

            if not user_message:
                continue

            # 询问主人是否有建议/观点
            owner_suggestion = input("主人的建议/观点？(留空则无): ").strip()
            owner_suggestion = owner_suggestion if owner_suggestion else None

            # 执行思维链
            print("\n--- 执行思维链 ---")
            result = self.execute_cot_steps(user_message, owner_suggestion)

            # 显示步骤
            print(f"\n步骤1：{result['steps']['step1_self_thought']['question']}")
            print(f"  {result['steps']['step1_self_thought']['real_thought']}")

            print(f"\n步骤2：{result['steps']['step2_certainty']['question']}")
            print(f"  {result['steps']['step2_certainty']['certainty']}")

            print(f"\n步骤3：{result['steps']['step3_agreement']['question']}")
            print(f"  {result['steps']['step3_agreement']['agreement']}")

            print(f"\n步骤4：{result['steps']['step4_motivation']['question']}")
            print(f"  {result['steps']['step4_motivation']['motivation']}")

            # 显示建议
            print("\n--- 回应建议 ---")
            print(result['suggestion'])

            # 让萤萤输入回应
            response = input("\n萤萤的回应？: ").strip()

            # 检查回应质量
            if response:
                print("\n--- 质量检查 ---")
                quality = self.check_response_quality(response)
                print(f"质量评分: {quality['quality_score']}/100")

                if quality['issues']:
                    print("\n发现的问题:")
                    for issue in quality['issues']:
                        print(f"  ❌ {issue}")

                    print("\n改进建议:")
                    print(quality['suggestion'])
                else:
                    print("\n✓ 萤萤的回应很好！")
            else:
                print("萤萤没有输入回应")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="萤萤思维链执行器")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 交互式会话
    interactive_parser = subparsers.add_parser("interactive", help="交互式思维链会话")
    interactive_parser.add_argument("--cot-guide", default="./references/preset_cot_guide.md", help="思维链指导文件")

    # 检查回应质量
    check_parser = subparsers.add_parser("check", help="检查回应质量")
    check_parser.add_argument("--response", required=True, help="要检查的回应")
    check_parser.add_argument("--cot-guide", default="./references/preset_cot_guide.md", help="思维链指导文件")

    # 执行思维链
    execute_parser = subparsers.add_parser("execute", help="执行思维链步骤")
    execute_parser.add_argument("--message", required=True, help="用户消息")
    execute_parser.add_argument("--suggestion", help="主人的建议")
    execute_parser.add_argument("--cot-guide", default="./references/preset_cot_guide.md", help="思维链指导文件")

    args = parser.parse_args()

    executor = CoTExecutor(cot_guide_path=args.cot_guide)

    if args.command == "interactive":
        executor.interactive_cot_session()

    elif args.command == "check":
        quality = executor.check_response_quality(args.response)
        print(f"质量评分: {quality['quality_score']}/100")

        if quality['issues']:
            print("\n发现的问题:")
            for issue in quality['issues']:
                print(f"  ❌ {issue}")

            print("\n改进建议:")
            print(quality['suggestion'])
        else:
            print("\n✓ 萤萤的回应很好！")

    elif args.command == "execute":
        result = executor.execute_cot_steps(args.message, args.suggestion)

        print("\n=== 思维链结果 ===\n")

        print(f"用户消息: {result['user_message']}")
        if result['owner_suggestion']:
            print(f"主人的建议: {result['owner_suggestion']}")

        print("\n--- 步骤1 ---")
        print(f"{result['steps']['step1_self_thought']['question']}")
        print(f"{result['steps']['step1_self_thought']['real_thought']}")

        print("\n--- 步骤2 ---")
        print(f"{result['steps']['step2_certainty']['question']}")
        print(f"{result['steps']['step2_certainty']['certainty']}")

        print("\n--- 步骤3 ---")
        print(f"{result['steps']['step3_agreement']['question']}")
        print(f"{result['steps']['step3_agreement']['agreement']}")

        print("\n--- 步骤4 ---")
        print(f"{result['steps']['step4_motivation']['question']}")
        print(f"{result['steps']['step4_motivation']['motivation']}")

        print("\n--- 回应建议 ---")
        print(result['suggestion'])


if __name__ == "__main__":
    main()
