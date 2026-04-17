---
name: unified-memory-search
description: 统一记忆搜索工具；当用户需要搜索历史对话、重要信息、暗号、设定等任何记忆内容时使用
dependency:
  python:
    - requests>=2.28.0
---

# 统一记忆搜索

## 任务目标

- 提供统一的记忆搜索入口
- 整合多种搜索方式和数据源
- 确保重要信息不会被遗漏
- 支持多种搜索策略

## 前置准备

确保以下目录和文件存在：
- `shared_memory/dialogues.json` - 对话记录
- `memory-store/萤萤记忆.json` - 结构化记忆（可选）
- `shared_memory/growth_log.json` - 成长日志（可选）

## 搜索策略

### 搜索优先级

1. **第一优先：结构化记忆**
   - 搜索 `memory-store/萤萤记忆.json`
   - 包含主人信息、重要设定、暗号等
   - 搜索速度快，命中率高

2. **第二优先：对话记录**
   - 搜索 `shared_memory/dialogues.json`
   - 包含所有对话历史
   - 搜索全面，但速度较慢

3. **第三优先：成长日志**
   - 搜索 `shared_memory/growth_log.json`
   - 包含成长事件和反思
   - 适合搜索成长相关内容

4. **第四优先：文件系统**
   - 搜索所有文本文件
   - 包含 markdown、json、txt 等
   - 搜索范围最广

## 操作步骤

### 基本搜索

```bash
# 关键词搜索
python scripts/unified_memory_search.py --keywords "白猫"

# 多关键词搜索
python scripts/unified_memory_search.py --keywords "主人" "暗号"

# 模糊搜索
python scripts/unified_memory_search.py --keywords "检查" --fuzzy

# 正则表达式搜索
python scripts/unified_memory_search.py --regex "萤萤.*检查"
```

### 时间范围搜索

```bash
# 搜索最近7天
python scripts/unified_memory_search.py --days 7

# 搜索特定日期范围
python scripts/unified_memory_search.py --start-date "2026-04-10" --end-date "2026-04-20"

# 搜索最近30天的关键词
python scripts/unified_memory_search.py --days 30 --keywords "农场"
```

### 高级搜索

```bash
# 按类型搜索
python scripts/unified_memory_search.py --keywords "主人" --type dialogue
python scripts/unified_memory_search.py --keywords "农场" --type growth

# 按重要性搜索
python scripts/unified_memory_search.py --keywords "暗号" --importance high

# 组合搜索
python scripts/unified_memory_search.py --keywords "主人" --days 30 --fuzzy
```

### 获取记忆摘要

```bash
# 获取完整记忆摘要
python scripts/unified_memory_search.py --action summary

# 获取主人信息
python scripts/unified_memory_search.py --action info --key owner

# 获取当前状态
python scripts/unified_memory_search.py --action info --key status
```

## 使用示例

### 示例1：搜索重要暗号

- 场景：主人问"我们的暗号是什么？"
- 命令：`python scripts/unified_memory_search.py --keywords "暗号" --importance high`
- 预期产出：找到"白猫"暗号

### 示例2：搜索最近的对话

- 场景：主人问"我们昨天聊了什么？"
- 命令：`python scripts/unified_memory_search.py --days 1 --type dialogue`
- 预期产出：显示最近一天的对话摘要

### 示例3：模糊搜索

- 场景：主人问"萤萤还记得那个检查的事吗？"
- 命令：`python scripts/unified_memory_search.py --keywords "检查" --fuzzy`
- 预期产出：找到包含"检查"的所有对话

### 示例4：获取记忆摘要

- 场景：萤萤"醒来"时需要恢复上下文
- 命令：`python scripts/unified_memory_search.py --action summary`
- 预期产出：显示完整记忆摘要（主人信息、当前状态、重要设定）

## 资源索引

- 脚本：见 [scripts/unified_memory_search.py](scripts/unified_memory_search.py)（统一搜索核心脚本）
- 参考：见 [references/memory-schema.md](references/memory-schema.md)（记忆格式定义）

## 注意事项

- ⭐ **这是唯一的记忆搜索工具，删除或禁用其他搜索工具**
- ⭐ **每次搜索会依次检查多个数据源，确保不遗漏**
- ⭐ **重要信息会优先显示在结果中**
- ⭐ **如果搜索不到结果，会尝试扩大搜索范围**

## 搜索结果格式

搜索结果按优先级排序：

```json
{
  "total_results": 10,
  "results": [
    {
      "source": "structured_memory",
      "type": "owner",
      "content": {
        "name": "野猫",
        "nickname": "主人",
        "secret_code": "白猫"
      },
      "relevance": 0.95
    },
    {
      "source": "dialogues",
      "id": "20260416_0006",
      "session": "主对话",
      "content": "暗号记住了：白猫！🐱✨",
      "relevance": 0.90
    }
  ]
}
```

## 最佳实践

### 搜索策略

1. **优先使用关键词搜索**（精确、快速）
2. **找不到时使用模糊搜索**（扩大范围）
3. **再找不到使用时间范围搜索**（查找历史）
4. **最后使用正则表达式**（复杂模式）

### 记录重要信息

发现重要信息后，立即记录到结构化记忆：

```bash
python scripts/memory_manager.py --action update \
  --memory-file memory-store/萤萤记忆.json \
  --new-info '{"owner": {"secret_code": "白猫"}}'
```

### 定期更新

- 每次对话结束后，记录重要内容
- 每天更新一次记忆摘要
- 定期整理和归档旧对话
