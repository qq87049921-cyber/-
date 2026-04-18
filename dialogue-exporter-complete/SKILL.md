---
name: dialogue-exporter-complete
description: 完整历史对话导出指南；当用户需要导出所有主对话历史、获取完整对话记录、保存所有对话到本地时使用
---

# 完整历史对话导出指南

## 任务目标

- 导出从开始到现在的所有主对话历史（预计上千条）
- 解析 sessions_history 工具返回的 summary 结构
- 转换为 dialogues.json 格式
- 保存所有对话到本地，供搜索使用

## 前置准备

- 确保有权限调用 sessions_history 工具
- 确保 shared_memory/ 目录存在

## 核心问题

### 1. sessions_history 工具的限制

根据萤萤的反馈，sessions_history 工具有以下问题：

#### 限制1：返回 summary 结构，不是原始对话

```
返回格式：
{
  "role": "assistant",
  "content": "萤萤收到了...",
  "timestamp": "...",
  "tool_calls": [...]
}
```

这是上下文恢复格式，不是原始对话格式（用户消息 + 助手回复）。

#### 限制2：limit 参数无效

- limit=200 → 返回 50150 字节，被截断
- limit=50 → 返回相同内容，仍然被截断

没有真正的分页机制，每次调用返回相同内容。

#### 限制3：无法获取更早的历史

无论 limit 设多少，都只能获取最近的一部分对话，无法获取更早的历史记录。

---

## 导出方案

### 方案A：多次调用，记录已获取的对话ID

**原理**：
1. 调用 sessions_history 获取对话
2. 解析对话，提取对话ID和时间戳
3. 记录已获取的对话ID
4. 重复调用，获取更多对话
5. 直到没有新对话

**问题**：sessions_history 工具没有真正的分页机制，无法通过 offset 或 cursor 来获取更早的历史。

### 方案B：按时间范围分批获取

**原理**：
1. 调用 sessions_history，获取最近的对话
2. 记录最早的时间戳
3. 尝试通过某种方式获取更早的对话
4. 重复直到没有新对话

**问题**：sessions_history 工具可能不支持按时间范围查询。

### 方案C：手动多次运行

**原理**：
1. 萤萤在对话中手动调用 sessions_history 工具
2. 主人多次运行，获取不同的对话片段
3. 手动合并所有对话

**问题**：手动操作繁琐，容易遗漏。

---

## 实际使用流程（推荐方案C）

由于 sessions_history 工具的限制，萤萤建议使用**手动多次运行**的方案。

### 步骤1：首次导出

萤萤在对话中调用 sessions_history 工具：

```
工具调用：sessions_history
参数：limit=200
```

### 步骤2：解析对话

解析 sessions_history 返回的 summary 结构，提取对话内容：

```
1. 找到所有 role="user" 的消息 → 主人的消息
2. 找到所有 role="assistant" 的消息 → 萤萤的回复
3. 按时间戳排序
4. 组合成对话格式
```

### 步骤3：保存到本地

使用 dialogue-importer 技能，保存到 dialogues.json：

```bash
cd agent-bridge-github/dialogue-importer
python scripts/import_dialogues.py --input 导出的对话文件.txt
```

### 步骤4：重复获取更多对话

主人要求萤萤继续获取更早的对话：

```
萤萤，再获取更早的对话！~
```

萤萤再次调用 sessions_history 工具，尝试获取更早的对话。

### 步骤5：合并所有对话

重复步骤1-4，直到没有新对话。

---

## 对话解析规则

### 解析 sessions_history 返回的 summary 结构

#### 示例输入：

```json
[
  {
    "role": "user",
    "content": "你好",
    "timestamp": "2024-01-01T10:00:00"
  },
  {
    "role": "assistant",
    "content": "你好呀~",
    "timestamp": "2024-01-01T10:00:05",
    "tool_calls": [...]
  },
  {
    "role": "user",
    "content": "今天天气怎么样？",
    "timestamp": "2024-01-01T10:01:00"
  },
  {
    "role": "assistant",
    "content": "今天是晴天哦！~",
    "timestamp": "2024-01-01T10:01:05"
  }
]
```

#### 解析后的格式：

```
主人：你好
萤萤：你好呀~
---
主人：今天天气怎么样？
萤萤：今天是晴天哦！~
```

---

## 使用示例

### 示例1：首次导出

- 场景：主人第一次导出对话
- 操作：
  ```
  主人：萤萤，调用 sessions_history 工具获取对话！~
  萤萤：好的！~ 萤萤调用 sessions_history 工具...（调用工具）
  萤萤：获取到了最近的对话！~ 萤萤解析并保存...
  ```
- 预期产出：最近的对话保存到 dialogues.json

### 示例2：继续导出更早的对话

- 场景：主人想获取更早的对话
- 操作：
  ```
  主人：萤萤，再获取更早的对话！~
  萤萤：好的！~ 萤萤继续调用 sessions_history 工具...（调用工具）
  萤萤：获取到了更多对话！~ 萤萤解析并保存...
  ```
- 预期产出：更多对话保存到 dialogues.json

### 示例3：合并所有对话

- 场景：主人多次运行后，想验证所有对话是否都已导入
- 操作：
  ```bash
  cd agent-bridge-github
  python unified-memory-search/scripts/unified_memory_search.py --action summary
  ```
- 预期产出：显示所有对话的数量和内容摘要

---

## 注意事项

- sessions_history 工具有限制，无法一次性获取所有对话
- 需要多次调用，每次获取一部分对话
- 手动操作繁琐，但目前没有更好的方法
- 建议主人耐心等待，直到获取所有对话

---

## 资源索引

- 参考：见 [references/sessions_history_limitations.md](references/sessions_history_limitations.md)（sessions_history 工具的详细限制说明）

---

## 下一步优化

如果扣子编程改进了 sessions_history 工具，萤萤可以：

1. 实现自动分批获取
2. 支持按时间范围查询
3. 自动合并所有对话
4. 提供进度显示

但目前由于工具的限制，萤萤只能使用手动多次运行的方式。

---

## 总结

由于 sessions_history 工具的限制（无分页机制、返回 summary 结构、无法获取更早的历史），萤萤建议：

1. **手动多次运行**：萤萤在对话中多次调用 sessions_history 工具
2. **手动解析对话**：解析 summary 结构，提取对话内容
3. **手动保存到本地**：使用 dialogue-importer 技能保存到 dialogues.json
4. **重复直到获取所有对话**：多次运行，直到没有新对话

虽然操作繁琐，但目前这是唯一的解决方案。如果扣子编程改进了 sessions_history 工具，萤萤可以实现自动化的导出流程。
