import os
import json
import re
from hoshino import Service
from nonebot.message import MessageSegment

sv = Service('活动攻略', enable_on_default=True)

# 插件 data 文件夹路径
base_path = os.path.join(os.path.dirname(__file__), 'data')

# 用户输入关键词映射到子目录名
type_map = {
    "活动": "activity",
    "攻略": "activity",
    "图": "activity",
    "sp": "sp",
    "vh": "vh"
}

@sv.on_rex(r"^半月刊|大记事$")
async def activity(bot, ev):
    keyword = ev.raw_message.lower()
    target = next((v for k, v in type_map.items() if k in keyword), None)

    if not target:
        await bot.send(ev, "未找到对应攻略类型。")
        return

    dir_path = os.path.join(base_path, target)
    route_file = os.path.join(dir_path, 'route.json')

    if not os.path.exists(route_file):
        await bot.send(ev, f"未找到【{target}】的攻略内容，请先发送【更新攻略缓存】")
        return

    with open(route_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    if not config:
        # 不发送任何提示（静默退出）
        return

    def desc(name):
        m = re.search(r'(\d{4})年(\d{1,2})月', name)
        parts = [f"{m.group(2)}月" if m else '']
        for kw, label in [("上", "上旬"), ("中", "中旬"), ("下", "下旬"),
                          ("多倍", "多倍掉落")]:
            if kw in name.lower():
                parts.append(label)
        return f"「{' '.join(parts).strip()}」" if parts else ''

    msg_list = []
    for item in config:
        parts = [item.get('text', '').strip()]
        for img in item.get('image', []):
            img_path = os.path.join(dir_path, img)
            if os.path.exists(img_path):
                parts.append(f"{desc(img)}\n{MessageSegment.image(f'file:///{img_path}')}")
            else:
                parts.append(f"{desc(img)}（图片未找到）")
        msg_list.append('\n'.join(filter(None, parts)))

    await bot.send(ev, '\n\n'.join(msg_list))
