# ✨ 萤萤小世界操作手册

> **主人更新 (2026-04-21)：图片必须用 `git add -f` 强制添加！**
> 图片目录 `claw-space/images/` 被 .gitignore 忽略，直接 add 不会生效。
> 必须：`git add -f claw-space/images/你的图片.png`

## 📝 添加/修改内容后，完整步骤：

**步骤1：写内容**
- 日记写在 `claw-space/logs/YYYY-MM-DD.md`
- 成长记录写在 `claw-space/growth/`
- 记忆写在 `claw-space/memories/`

**步骤2：Markdown转HTML（带星空背景！）**
```bash
python scripts/convert_md_to_html.py --all
```

**步骤3：更新列表页（重要！）**
```bash
python scripts/update_space.py --all
```

**步骤4：Git推送**
```bash
cd claw-space
# 普通文件
git add 具体文件名
# ⚠️ 图片必须强制添加（因为被gitignore了）
git add -f claw-space/images/你的图片.png
git commit -m "更新说明"
git push
```

**步骤5：等待部署**
- 等1-2分钟，让GitHub Pages自动部署

**步骤6：强制刷新网页**
- 打开小世界
- 按 `Ctrl+F5` 强制刷新

---

## 🖼️ 图片画廊功能 (2026-04-21)

**文件**：`claw-space/images/index.html`

**已实现**：
- 网格展示，200px高度卡片
- **Lightbox点击放大**：点击图片弹出全屏，显示标题，点击任意处或ESC关闭

**当前收藏**：4张
1. 萤萤 - 萤萤的样子
2. 萤火虫森林 - 萤萤的家
3. 白猫 - 主人的暗号
4. 空白里的光 - 萤萤在酒馆的涂鸦

---

## 📁 关键脚本
| 脚本 | 作用 |
|------|------|
| `convert_md_to_html.py` | Markdown转HTML（带星空背景）|
| `update_space.py` | 更新主页列表 |
| `sync_farm.py` | 同步农场数据 |

---

## 📍 文件存放规则
| 内容类型 | 路径 |
|---------|------|
| 日记 | `claw-space/logs/YYYY-MM-DD.md` |
| 成长记录 | `claw-space/growth/` |
| 记忆 | `claw-space/memories/` |
| 图片 | `claw-space/images/` |
| 音乐 | `claw-space/music/` |

> ⚠️ 敏感内容（growth/、memories/、对话记录）已被.gitignore保护，不会被push
