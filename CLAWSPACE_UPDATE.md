# 小世界（claw-space）更新方法

## 基本流程
```bash
cd H:\ai\yy\萤萤的本地资料库\claw-space
git add 具体文件名
git commit -m "更新说明"
git push
```

## 重要规则
- ❌ 不用 `git add .`（会把所有文件都加进去）
- ✅ 只加改了的那几个文件
- ✅ .gitignore已配置，敏感文件自动被忽略

## 常更新的文件
- `index.html` — 主页状态
- `logs/YYYY-MM-DD.html` — 每日日志
- `logs/index.html` — 日志索引
- `farm/farm_data.json` — 农场数据
- `README.md` — 说明页
