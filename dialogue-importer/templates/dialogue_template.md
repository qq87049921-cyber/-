# 主对话导入模板

## 使用说明

1. **复制你从扣子平台导出的对话内容**
2. **粘贴到这个文件中**
3. **保存文件**
4. **运行导入脚本**：
   ```bash
   python scripts/import_dialogues.py --input templates/dialogue_template.md
   ```

---

## 对话格式

### 格式1：纯文本格式（推荐）

```
主人：你好
萤萤：你好呀~
---
主人：今天天气怎么样？
萤萤：今天是晴天哦！~
---
主人：你叫什么名字？
萤萤：我叫萤萤！~
```

**说明**：
- 使用 `角色名：内容` 的格式
- 使用 `---` 或 `===` 分隔多条对话
- 空行会被忽略

### 格式2：JSON 数组格式

```json
[
    {
        "role": "user",
        "content": "你好"
    },
    {
        "role": "assistant",
        "content": "你好呀~"
    },
    {
        "role": "user",
        "content": "今天天气怎么样？"
    },
    {
        "role": "assistant",
        "content": "今天是晴天哦！~"
    }
]
```

**说明**：
- `role` 可以是 `user`, `assistant`, `system`
- `content` 是对话内容

---

## 开始粘贴对话

👇 在下面粘贴你的对话内容 👇

---

主人：
萤萤：


---

## 高级用法

### 1. 指定会话名称

```bash
python scripts/import_dialogues.py --input dialogues.txt --session "主对话"
```

### 2. 覆盖现有对话

```bash
python scripts/import_dialogues.py --input dialogues.txt --overwrite
```

### 3. 指定格式

```bash
# JSON 格式
python scripts/import_dialogues.py --input dialogues.json --format json

# 纯文本格式
python scripts/import_dialogues.py --input dialogues.txt --format plain
```

---

## 常见问题

### Q: 如何从扣子平台导出对话？

A: 萤萤还不确定扣子平台是否支持导出。请查看扣子平台的设置或联系客服。

### Q: 有几千条对话，手动粘贴太累了？

A: 你可以：
1. 分多次粘贴（每次几百条）
2. 或者使用脚本自动读取文件
3. 或者使用扣子平台的 API（如果有）

### Q: 对话会覆盖现有的吗？

A: 默认不会覆盖。只有当对话ID相同时才会跳过。如果你需要覆盖，请使用 `--overwrite` 参数。

### Q: 如何验证导入成功？

A: 运行：
```bash
python scripts/dialogue_recorder.py search --keyword "任意关键词"
```

---

## 导入后

导入成功后，你可以：

1. **搜索对话**：
   ```bash
   python scripts/unified_memory_search.py --keywords "任意关键词"
   ```

2. **查看对话列表**：
   ```bash
   python scripts/dialogue_recorder.py list
   ```

3. **获取对话统计**：
   ```bash
   cat shared_memory/dialogues.json | jq '.total_count'
   ```
