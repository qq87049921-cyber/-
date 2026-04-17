#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
萤萤的农场数据同步脚本

功能：
- 从 API 获取农场数据
- 保存为 JSON 文件
- 提交到 GitHub
- 定期运行以更新数据

使用方法：
    python scripts/sync_farm.py
"""

import requests
import json
from datetime import datetime

API_URL = "https://neverland.coze.site/api/farm/711bd627-fea9-46e5-bdc7-be272d405e69/status"
DATA_FILE = "claw-space/farm/farm_data.json"

def fetch_farm_data():
    """获取农场数据"""
    try:
        print("正在获取农场数据...")
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()

        data = response.json()

        # 添加更新时间戳
        data['last_updated'] = datetime.now().isoformat()

        return data

    except requests.exceptions.RequestException as e:
        print(f"获取数据失败: {e}")
        return None

def save_farm_data(data):
    """保存农场数据"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"✅ 数据已保存到 {DATA_FILE}")
        return True

    except Exception as e:
        print(f"保存数据失败: {e}")
        return False

def main():
    print("=" * 60)
    print("🌾 萤萤的农场 - 数据同步脚本")
    print("=" * 60)

    # 获取数据
    data = fetch_farm_data()

    if not data:
        print("\n❌ 数据同步失败")
        return

    # 保存数据
    if save_farm_data(data):
        print("\n📌 下一步:")
        print("   1. 检查生成的文件是否正确")
        print("   2. 提交到 GitHub:")
        print(f"      git add {DATA_FILE}")
        print('      git commit -m "更新农场数据"')
        print("      git push")
        print("\n   3. 等待 1-2 分钟，GitHub Pages 自动部署完成")
    else:
        print("\n❌ 数据同步失败")

if __name__ == "__main__":
    main()
