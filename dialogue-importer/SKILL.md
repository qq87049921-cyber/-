---
name: dialogue-importer
description: 主对话导入工具；当用户需要批量导入主对话、手动复制对话内容、从文件导入对话时使用
---

# 主对话导入工具

## 任务目标

- 提供批量导入主对话的能力
- 支持多种对话格式（纯文本、JSON）
- 自动转换为 dialogues.json 格式
- 支持导入几千条对话

## 前置准备

- 准备对话内容文件（纯文本或 JSON 格式）
- 确保 `shared_memory/` 目录存在

## 操作步骤

### 步骤1：准备对话内容

从扣子平台导出对话，或手动复制对话内容到文件。

**支持的格式**：

1. **纯文本格式**（推荐）
   ```
   主人：你好
   萤萤：你好呀~
   ---
   主人：今天天气怎么样？
   萤萤：今天是晴天哦！~
   ```

2. **JSON 数组格式**
   ```json
   [
       {"role": "user", "content": "你好"},
       {"role": "assistant", "content": "你好呀~"}
   ]
   ```

### 步骤2：运行导入脚本

```bash
# 自动检测格式
python scripts/import_dialogues.py --input dialogues.txt

# 指定会话名称
python scripts/import_dialogues.py --input dialogues.txt --session "主对话"

# 覆盖现有对话
python scripts/import_dialogues.py --input dialogues.txt --overwrite

# 指定格式
python scripts/import_dialogues.py --input dialogues.json --format json
```

### 步骤3：验证导入

```bash
# 搜索对话
python scripts/unified_memory_search.py --keywords "任意关键词"

# 查看对话统计
python scripts/dialogue_recorder.py list
```

## 使用示例

### 示例1：导入纯文本对话

- 场景：主人从扣子平台手动复制了几百条对话
- 命令：
  ```bash
  # 1. 创建对话文件
  cat > dialogues.txt << 'EOF'
  主人：你好
  萤萤：你好呀~
  ---
  主人：今天天气怎么样？
  萤萤：今天是晴天哦！~
  EOF

  # 2. 导入对话
  python scripts/import_dialogues.py --input dialogues.txt
  ```
- 预期产出：成功导入 2 条对话到 `shared_memory/dialogues.json`
- 关键要点：使用 `---` 分隔多条对话

### 示例2：导入 JSON 格式对话

- 场景：主人从扣子平台导出了 JSON 格式的对话
- 命令：
  ```bash
  python scripts/import_dialogues.py --input dialogues.json --format json
  ```
- 预期产出：成功导入所有对话
- 关键要点：JSON 格式必须是数组，每个元素包含 `role` 和 `content`

### 示例3：导入几千条对话

- 场景：主人有几千条对话需要导入
- 命令：
  ```bash
  # 分批导入（每次1000条）
  python scripts/import_dialogues.py --input dialogues_part1.txt
  python scripts/import_dialogues.py --input dialogues_part2.txt
  python scripts/import_dialogues.py --input dialogues_part3.txt
  ```
- 预期产出：成功导入所有对话，不会重复
- 关键要点：分批导入，避免一次性处理太多数据

## 资源索引

- 脚本：见 [scripts/import_dialogues.py](scripts/import_dialogues.py)（导入脚本，支持纯文本和 JSON 格式）
- 模板：见 [templates/dialogue_template.md](templates/dialogue_template.md)（对话模板文件，包含使用说明）

## 注意事项

- 默认不会覆盖现有对话，只有对话ID相同时才会跳过
- 如果需要覆盖，请使用 `--overwrite` 参数
- 支持自动检测格式（`--format auto`）
- 空行会被忽略
- 使用 `---` 或 `===` 分隔多条对话

## 高级用法

### 查看导入进度

脚本会显示导入进度：
```
📖 正在读取文件: dialogues.txt
   文件大小: 12345 字符
   文件行数: 234 行
🔍 正在解析对话...
   检测到格式: plain
✅ 解析完成，共 100 条对话
✅ 成功添加 100 条新对话
💾 对话已保存到: shared_memory/dialogues.json
   总对话数: 100
```

### 批量导入

如果有多个文件，可以批量导入：
```bash
for file in dialogues_*.txt; do
    python scripts/import_dialogues.py --input "$file"
done
```

### 验证导入

导入后，使用搜索工具验证：
```bash
# 搜索特定关键词
python scripts/unified_memory_search.py --keywords "关键词"

# 查看所有对话
python scripts/dialogue_recorder.py list
```
