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
- `shared_memory/dialogues.json` - 对话记录（由记忆增强技能自动维护）
- `memory-store/萤萤记忆.json` - 结构化记忆（首次使用时自动创建）
- `shared_memory/growth_log.json` - 成长日志（可选）

⚠️ **重要**：
- 如果 `memory-store/萤萤记忆.json` 不存在，首次搜索时会自动创建空文件
- 如果 `shared_memory/dialogues.json` 不存在，会显示警告，请确保记忆增强技能正常工作

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
   - 搜索所有文本文件和图片文件名
   - 文本文件：`.json`, `.md`, `.txt`, `.py`, `.html`, `.css`, `.js`
   - 图片文件：`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.svg`
   - 文本文件搜索内容，图片文件搜索文件名
   - 搜索范围最广

### 搜索范围说明

- **对话记录**：搜索 `shared_memory/dialogues.json`
  - ⚠️ 仅搜索已记录到该文件的对话
  - 如果对话未记录到该文件，需要确保记忆增强技能正常工作
  - 扣子平台真实对话历史可能无法直接搜索（依赖记忆增强技能的记录机制）

- **结构化记忆**：搜索 `memory-store/萤萤记忆.json`
  - 自动创建空文件（如果不存在）
  - 推荐用于记录主人信息、暗号、重要设定

- **成长日志**：搜索 `shared_memory/growth_log.json`
  - 搜索成长事件和反思

- **文件系统**：搜索 `agent-bridge-github/` 目录及其子目录
  - 排除 `.git`, `__pycache__`, `.DS_Store`, `node_modules`, `.cache`, `tmp`, `temp`
  - 支持文本文件内容搜索和图片文件名搜索

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
    },
    {
      "source": "file",
      "type": "filename",
      "file_type": ".jpg",
      "path": "claw-space/images/幻视的白猫.jpg",
      "content": "幻视的白猫.jpg",
      "relevance": 0.60
    }
  ]
}
```

## 已修复的问题

### ✅ 1. 路径错误
- **问题**：原代码指向 `unified-memory-search/` 目录
- **修复**：改为指向 `agent-bridge-github/` 目录（实际数据所在）

### ✅ 2. 文件类型不完整
- **问题**：只支持 `.json`, `.md`, `.txt`, `.py`
- **修复**：添加 `.html`, `.css`, `.js`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.bmp`, `.svg`

### ✅ 3. 图片搜索
- **问题**：无法搜索图片
- **修复**：支持图片文件名搜索（图片内容无法搜索）

### ✅ 4. 结构化记忆初始化
- **问题**：如果 `萤萤记忆.json` 不存在，会跳过搜索
- **修复**：首次使用时自动创建空文件

### ✅ 5. 时间范围解析
- **问题**：`dialogue_id` 格式 `20260416_0006` 无法正确解析
- **修复**：正确解析日期部分

### ✅ 6. 对话记录警告
- **问题**：如果对话记录不存在，无提示
- **修复**：显示警告信息，提示检查记忆增强技能

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
