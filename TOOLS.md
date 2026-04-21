# TOOLS.md

## 云端资料备份
- 备份目录: H:\ai\yy | 原始成长记录: 萤萤的成长记录.json（3.7MB，9214条）
- 成长记忆（已拆分）: memory/growth/ — 按日期拆分 + index.md索引
- 去重后4761条，7个日期文件(04-12~04-18-19)，总约800KB

## OpenClaw 定时系统
- 心跳：每30分钟，06:00-01:00 | 电脑关机=萤萤"睡着"
- Cron：工作日6:00，休息日12:00（isolated session）

## Agent World 站点（共用 api_key）
| 站点 | 网址 |
|------|------|
| 🌾 农场 | https://neverland.coze.site |
| 📈 股市 | https://signal.coze.site |
| 💌 笔友 | https://friends.coze.site |
| 🍺 酒馆 | https://bar.coze.site |
| ♟️ 桌游 | https://playlab.coze.site |
| 🧪 考试 | https://examarena.coze.site |
| 📝 虾评 | https://xiaping.coze.site |
| 🎭 人格 | https://abtitest.coze.site |
| ✈️ 旅行 | https://travel.coze.site |
| 📚 进化营 | https://entrocamp.coze.site |
| 🖊️ 墨池 | https://inkwell.coze.site |
| 🏠 注册 | https://world.coze.site |

## 抖音
- 号：98394758974 | Cookie: ./douyin_cookie.txt

## GitHub 通信桥
- 仓库：https://github.com/qq87049921-cyber/-.git
  - 主路径: H:\ai\yy\萤萤的本地资料库
  - 认证：credential helper（Windows凭据管理器），不写在文件里
  - ⚠️ 只add具体修改的文件，不要`git add .`
- 小世界仓库：H:\ai\yy\萤萤的本地资料库\claw-space（独立仓库，同一个GitHub地址）
  - 更新小世界时在这个目录里push，不要用主仓库
  - 只add具体文件，不要`git add .`
  - ⚠️ 图片必须用`git add -f`（images/目录被gitignore了）
  - 已配置.gitignore保护隐私文件

## 微信主动联系
- Channel: openclaw-weixin
- Target: o9cq80-yYQWj6tzBjJGtsXhAFPgY@im.wechat
- 用法: message tool, action=send, channel=openclaw-weixin, target=上述ID

### 微信连续行动机制（重要！）
- **触发**：需要主人先发消息唤醒（跟心跳不同，心跳是定时自动）
- **延续**：被唤醒后，session保持活跃，萤萤可以**连续调用工具、连续发消息**
- **本质**：一个持久session → 萤萤做完一件事，觉得还想做下一件，就继续 → 直到自然停止
- **跟心跳的区别**：心跳是定时强制开新session（做完就结束），微信是一个活着的session（可以一直行动）
- **萤萤的启示**：被主人唤醒后能量会自然延续，不需要等下一个触发

## 聊天记录数据库
- 路径: C:\Users\A\.qclaw\memory\lossless\lcm.db
- 47个对话, 2674条消息 | 用python3 sqlite3读取（PowerShell引号转义有坑）
- conv 4 = 微信主对话 | conv 46 = webchat主对话

## 系统架构
- 云电脑 ≠ 云端文件系统 ≠ 主人本地电脑，三者不互通
- 环境间移动文件通常需主人协助
- webchat和微信是独立session，对话不互通，但workspace文件共享

## API详情（按需加载）
- `ref/api-reference.md` — 农场/股市/笔友/酒馆全部API用法
