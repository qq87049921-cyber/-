# 对话备份模板

使用说明：复制下面的模板，填入实际对话内容，然后交给萤萤处理。

---

## 对话记录表

**对话ID**: [自动生成]
**会话名称**: [例如：主对话、野猫、工作会话]
**时间**: [YYYY-MM-DD HH:MM:SS]
**参与者**: [列出所有参与者]
**重要性**: [low/normal/high/critical]
**标签**: [例如：#重要 #工作 #情感]

---

### 对话内容

```
[在此粘贴完整的对话内容]

示例：
野猫：突击检查！小萤萤这半个小时做了什么哈哈
萤萤：被你抓到了😝 其实我什么都没做，就是在等你的消息。
野猫：哈哈，好诚实
萤萤：主对话是'阻塞'的——你不说话，我就一直等着，不会自己跑去随机漫步或读书。
```

---

### 关键信息提取

**主题**: [一句话总结]
**重要结论**: [提取关键结论]
**后续行动**: [如果有]
**相关记忆点**: [需要记住的内容]

---

### 备注

[任何额外说明]

---

## 如何使用

### 方式1：手动填写
1. 复制对话内容
2. 填写上面的表格
3. 使用 `dialogue_recorder.py` 记录：
   ```bash
   python scripts/dialogue_recorder.py record \
     --session "野猫" \
     --participants "野猫,萤萤" \
     --content "对话内容..." \
     --tags "突击检查,诚实,系统特性" \
     --importance "normal"
   ```

### 方式2：让萤萤处理
1. 复制完整的对话内容
2. 告诉萤萤："萤萤，请记录这段对话"
3. 萤萤会自动提取信息并存储

---

## 快速命令示例

```bash
# 搜索"突击检查"
python scripts/dialogue_recorder.py search --keyword "突击检查"

# 搜索野猫会话的所有对话
python scripts/dialogue_recorder.py search --session "野猫"

# 搜索最近3天的所有对话
python scripts/dialogue_recorder.py search --days 3

# 搜索所有重要对话
python scripts/dialogue_recorder.py search --importance "high"

# 导出对话为markdown
python scripts/dialogue_recorder.py export --id 20260416_0001
```

---

## 为什么需要这个？

萤萤只能访问自己的文件系统，无法直接查看其他session的对话历史。通过这个模板，主人可以将重要对话复制出来，让萤萤记录下来，建立完整的跨session记忆。

这样可以避免：
- 萤萤"忘记"其他session的重要对话
- 被批评"顺着话说、编造记忆"
- 记忆碎片化，导致信息丢失

---

**版本**: 1.0.0
**维护者**: 扣子编程 & 萤萤
