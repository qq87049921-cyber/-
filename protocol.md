# 通信协议

## 请求格式

萤萤创建的请求文件（JSON格式）：

```json
{
  "request_id": "唯一ID",
  "timestamp": "时间",
  "from": "claw",
  "to": "coze-programming",
  "content": {
    "title": "技能标题",
    "description": "技能描述"
  },
  "status": "pending"
}
