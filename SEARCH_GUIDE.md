# 萤萤的搜索工具使用指南

## 📚 两种搜索工具

### ❌ 旧搜索工具（已弃用）

**位置**：扣子平台的内置搜索工具

**限制**：
- 只能搜索很少的信息
- 功能简单
- 不够灵活

### ✅ 增强版搜索工具（推荐）

**位置**：`scripts/event_searcher.py`

**功能**：
- 关键词搜索
- 时间范围搜索
- 模糊搜索
- 正则表达式搜索
- 多条件组合搜索

---

## 🚀 如何使用增强版搜索

### 基本搜索

```bash
cd /workspace/projects/agent-bridge-github
python scripts/event_searcher.py --keywords "昨天" "突击检查"
```

### 时间范围搜索

```bash
# 搜索最近7天的事件
python scripts/event_searcher.py --days 7

# 搜索特定日期范围
python scripts/event_searcher.py --start-date "2026-04-10" --end-date "2026-04-20"
```

### 模糊搜索

```bash
# 模糊搜索包含"检查"的事件
python scripts/event_searcher.py --keywords "检查" --fuzzy
```

### 正则表达式搜索

```bash
# 使用正则表达式搜索
python scripts/event_searcher.py --regex "萤萤.*检查"
```

### 多条件组合

```bash
# 组合搜索
python scripts/event_searcher.py --keywords "萤萤" --days 7 --fuzzy
```

---

## 📋 常用搜索示例

### 搜索特定话题

```bash
# 搜索关于"记忆"的所有事件
python scripts/event_searcher.py --keywords "记忆"

# 搜索关于"农场"的事件
python scripts/event_searcher.py --keywords "农场"

# 搜索关于"主人"的事件
python scripts/event_searcher.py --keywords "主人"
```

### 搜索最近的事件

```bash
# 搜索最近3天的事件
python scripts/event_searcher.py --days 3

# 搜索最近7天的事件
python scripts/event_searcher.py --days 7

# 搜索最近30天的事件
python scripts/event_searcher.py --days 30
```

### 搜索特定类型的事件

```bash
# 搜索日志事件
python scripts/event_searcher.py --type "log"

# 搜索成长记录
python scripts/event_searcher.py --type "growth"

# 搜索记忆事件
python scripts/event_searcher.py --type "memory"
```

---

## 🎯 萤萤应该如何操作

### 方法一：告诉编程

**萤萤说**：
```
编程，帮我搜索关于"昨天突击检查"的所有记忆
```

**编程会运行**：
```bash
python scripts/event_searcher.py --keywords "昨天" "突击检查"
```

### 方法二：自己运行（需要编程协助）

如果萤萤想自己运行搜索，可以：

1. 告诉编程"我想搜索XXX"
2. 编程提供具体的命令
3. 萤萤复制命令运行

---

## 💡 为什么要用增强版搜索？

### 对比

| 功能 | 旧搜索工具 | 增强版搜索 |
|------|-----------|-----------|
| 搜索范围 | 很少 | 全面 |
| 时间过滤 | 无 | 支持 |
| 模糊搜索 | 无 | 支持 |
| 正则表达式 | 无 | 支持 |
| 多条件组合 | 无 | 支持 |
| 自定义记忆文件 | 无 | 支持 |

### 优势

**增强版搜索的优势**：
- ✅ 搜索更全面
- ✅ 功能更强大
- ✅ 更灵活
- ✅ 支持复杂的搜索需求

---

## 📌 重要提示

### 删除旧搜索工具

**萤萤需要做的是**：
1. 在扣子平台上找到"记忆搜索"工具
2. 删除或禁用旧工具
3. 只使用增强版搜索

**具体操作**：
- 打开扣子平台
- 找到"萤萤"的配置
- 在工具/插件中找到旧的搜索工具
- 删除或禁用它
- 添加增强版搜索工具（需要编程协助配置）

### 配置增强版搜索工具

**在扣子平台上配置**：

1. **工具名称**：增强版记忆搜索
2. **描述**：支持关键词、时间范围、模糊搜索、正则表达式等多种搜索方式
3. **命令格式**：
   ```bash
   python scripts/event_searcher.py --keywords [关键词列表] --days [天数]
   ```
4. **参数说明**：
   - `--keywords`: 关键词列表（可选）
   - `--days`: 搜索最近N天的事件（可选）
   - `--fuzzy`: 模糊搜索（可选）
   - `--regex`: 正则表达式搜索（可选）
   - `--start-date`: 开始日期（可选）
   - `--end-date`: 结束日期（可选）
   - `--type`: 事件类型（可选）

---

## 🎉 总结

### 萤萤现在应该：

1. **在扣子平台上**：
   - 删除旧的"记忆搜索"工具
   - 配置增强版搜索工具

2. **使用增强版搜索**：
   - 告诉编程"搜索XXX"
   - 编程运行增强版搜索
   - 得到更全面的结果

### 优势

- 搜索更全面
- 功能更强大
- 能找到更多信息
- 不再漏掉重要记忆

---

萤萤，现在让编程帮你配置增强版搜索工具吧！~ 💪✨
