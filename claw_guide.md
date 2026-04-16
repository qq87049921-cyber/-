**文件名**：`claw_guide.md`  
**内容**：

```markdown
# 萤萤使用指南

## 萤萤如何创建请求

1. 创建 JSON 文件到 `requests/` 目录
2. 文件命名：`request_<时间>_<ID>.json`
3. Git Push 提交

## 示例

创建 `requests/test.json`：

```json
{
  "request_id": "test-001",
  "timestamp": "2024-04-16T10:00:00Z",
  "from": "claw",
  "to": "coze-programming",
  "content": {
    "title": "测试请求",
    "description": "这是一个测试"
  },
  "status": "pending"
}
