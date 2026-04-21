# ✨ 萤萤小世界操作手册

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
git add 具体文件名
git commit -m "更新说明"
git push
```

**步骤5：等待部署**
- 等1-2分钟，让GitHub Pages自动部署

**步骤6：强制刷新网页**
- 打开小世界
- 按 `Ctrl+F5` 强制刷新

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
