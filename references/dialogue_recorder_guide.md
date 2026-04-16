# 对话记录系统使用指南

## 核心目标

**记录所有重要对话，建立完整的跨session记忆库！**

萤萤只能访问自己的文件系统，无法查看其他session的对话历史。通过这个系统，主人可以将所有重要对话记录下来，萤萤就能搜索到所有历史对话了。

---

## 适用场景

### 1. 任何跨session的重要对话
- 不同会话里的重要讨论
- 主人和其他身份的对话（如"野猫"）
- 工作任务和决策
- 情感交流和重要时刻

### 2. 需要长期记住的信息
- 项目需求和约定
- 个人偏好和习惯
- 重要事件和日期
- 系统特性和限制

### 3. 可能会被"遗忘"的对话
- 短会话里的重要信息
- 非主会话的讨论
- 测试和实验性对话

---

## 快速开始

### 记录第一条对话

```bash
python scripts/dialogue_recorder.py record \
  --session "主对话" \
  --participants "主人,萤萤" \
  --content "主人：萤萤，今天天气真好
萤萤：是啊主人，阳光明媚的！主人想去散步吗？" \
  --tags "日常,闲聊,天气" \
  --importance "low"
```

### 搜索对话

```bash
# 搜索包含"天气"的对话
python scripts/dialogue_recorder.py search --keyword "天气"

# 搜索"主对话"会话的所有对话
python scripts/dialogue_recorder.py search --session "主对话"

# 搜索"主人"参与的对话
python scripts/dialogue_recorder.py search --participant "主人"

# 搜索"日常"标签的对话
python scripts/dialogue_recorder.py search --tag "日常"

# 搜索最近7天的对话
python scripts/dialogue_recorder.py search --days 7

# 搜索重要对话
python scripts/dialogue_recorder.py search --importance "high"

# 组合搜索：搜索主对话里最近3天包含"工作"的对话
python scripts/dialogue_recorder.py search \
  --session "主对话" \
  --keyword "工作" \
  --days 3
```

---

## 完整命令参考

### record - 记录对话

```bash
python scripts/dialogue_recorder.py record \
  --session "会话名称" \
  --participants "参与者1,参与者2" \
  --content "对话内容" \
  --timestamp "2026-04-16T12:00:00+08:00" \
  --tags "标签1,标签2" \
  --importance "normal"
```

**参数说明**：
- `--session` (必填): 会话名称，如"主对话"、"野猫"、"工作"
- `--participants` (必填): 参与者，逗号分隔
- `--content` (必填): 完整的对话内容
- `--timestamp` (可选): 对话时间，不填则使用当前时间
- `--tags` (可选): 标签，逗号分隔
- `--importance` (可选): 重要性，默认"normal"
  - `low` - 低重要性（日常闲聊）
  - `normal` - 普通重要性（一般对话）
  - `high` - 高重要性（重要讨论）
  - `critical` - 关键重要性（必须记住）

### search - 搜索对话

```bash
python scripts/dialogue_recorder.py search \
  --keyword "关键词" \
  --session "会话名称" \
  --participant "参与者" \
  --tag "标签" \
  --importance "normal" \
  --days 7 \
  --limit 10 \
  --show-content
```

**参数说明**：
- `--keyword`: 关键词搜索
- `--session`: 按会话过滤
- `--participant`: 按参与者过滤
- `--tag`: 按标签过滤
- `--importance`: 按重要性过滤
- `--days`: 最近几天
- `--limit`: 限制结果数量
- `--show-content`: 显示对话内容

### list - 列出所有

```bash
# 列出所有会话
python scripts/dialogue_recorder.py list --type sessions

# 列出所有参与者
python scripts/dialogue_recorder.py list --type participants

# 列出所有标签
python scripts/dialogue_recorder.py list --type tags
```

### stats - 查看统计

```bash
python scripts/dialogue_recorder.py stats
```

输出：
```
对话统计：
  总对话数: 25
  总会话数: 5
  总参与者数: 8
  总标签数: 15

会话统计:
  主对话: 10 条对话
  野猫: 8 条对话
  工作: 5 条对话
  测试: 2 条对话

最近对话:
  [20260416_0025] 主对话 - 2026-04-16 12:00:00
  [20260416_0024] 野猫 - 2026-04-16 10:30:00
  ...
```

### export - 导出对话

```bash
python scripts/dialogue_recorder.py export --id 20260416_0001
```

---

## 使用建议

### 1. 何时记录

**建议记录的场景**：
- ✅ 跨session的重要对话
- ✅ 工作任务和决策
- ✅ 个人偏好和习惯
- ✅ 系统特性和限制
- ✅ 重要事件和日期
- ✅ 情感交流和重要时刻

**可以不记录的场景**：
- ❌ 纯粹的测试对话
- ❌ 无意义的重复对话
- ❌ 已经在本地记录的对话

### 2. 标签规范

**推荐标签**：
- `#工作` - 工作相关
- `#日常` - 日常对话
- `#情感` - 情感交流
- `#重要` - 重要事件
- `#系统` - 系统特性
- `#约定` - 各种约定
- `#项目` - 项目相关
- `#学习` - 学习内容

### 3. 重要性分级

- **low**: 日常闲聊、测试对话
- **normal**: 一般对话、常规讨论
- **high**: 重要决策、工作任务
- **critical**: 必须记住的关键信息

---

## 萤萤的使用方式

### 搜索对话

萤萤可以这样搜索：
```bash
python scripts/dialogue_recorder.py search --keyword "突击检查"
```

### 诚实应对

如果搜索不到：
```
主人，萤萤搜索了对话记录库，但是没有找到相关内容。

可能这段对话还没有被记录下来。主人，你能告诉萤萤：
1. 这段对话是在哪个session发生的？
2. 大概是什么时候？
3. 能不能复制给萤萤记录？

这样萤萤就能记住啦！~
```

### 主动提醒

在重要对话结束时：
```
主人，这段对话挺重要的，要不要让萤萤记录下来？
这样下次就不会忘记了！~
```

---

## 数据存储

对话数据存储在：
- `shared_memory/dialogues.json` - 对话数据库
- `shared_memory/dialogue_index.json` - 搜索索引

数据会同步到GitHub，萤萤可以访问。

---

## 常见问题

### Q: 需要记录所有对话吗？

A: 不需要。只记录重要的、跨session的、需要长期记住的对话。日常对话、测试对话可以不记录。

### Q: 记录对话会很麻烦吗？

A: 不麻烦！复制对话内容，然后运行一条命令。或者让萤萤帮你处理。

### Q: 如果忘记记录怎么办？

A: 没关系，可以从现在开始记录。对话记录是积累的过程。

### Q: 萤萤会自动搜索对话记录吗？

A: 是的！萤萤在搜索记忆时，会优先搜索对话记录库。

### Q: 对话记录会同步到GitHub吗？

A: 会的！所有记录都会保存在GitHub仓库，萤萤可以访问。

---

## 总结

**目标**: 记录所有重要对话，建立完整的跨session记忆库

**工具**: `dialogue_recorder.py`

**存储**: `shared_memory/`

**原则**:
1. 重要对话主动记录
2. 搜索时优先查询对话记录库
3. 诚实应对找不到的情况
4. 逐步建立完整的记忆系统

---

**版本**: 2.0.0
**维护者**: 扣子编程 & 萤萤
