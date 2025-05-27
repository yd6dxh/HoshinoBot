import os
from hoshino import Service
from hoshino.modules.priconne import chara
from hoshino.typing import CQEvent

from . import _pcr_data

sv = Service("priconne_character_guide", bundle="pcr娱乐", help_="""
图鉴 角色名 —— 查询角色信息
图鉴 角色ID —— 通过ID查询角色信息
""".strip())

@sv.on_prefix("图鉴")
async def character_info(bot, ev: CQEvent):
    name = ev.message.extract_plain_text().strip()
    if not name:
        return

    # 尝试解析为角色 ID
    if name.isdigit():
        char_id = int(name)
    else:
        char_id = chara.name2id(name)

    if char_id == chara.UNKNOWN or char_id not in _pcr_data.CHARA_PROFILE:
        await bot.finish(ev, "未找到该角色信息，请检查输入的角色名或ID。")

    profile = _pcr_data.CHARA_PROFILE[char_id]
    c = chara.fromid(char_id)

    # 格式化返回信息
    info_text = (
        f"{await c.get_icon_cqcode()}{profile['名字']}\n"
        f"公会：{profile['公会']}\n"
        f"生日：{profile['生日']}\n"
        f"年龄：{profile['年龄']}岁\n"
        f"身高：{profile['身高']}\n"
        f"体重：{profile['体重']}\n"
        f"血型：{profile['血型']}\n"
        f"种族：{profile['种族']}\n"
        f"喜好：{profile['喜好']}\n"
        f"声优：{profile['声优']}\n"
    )

    await bot.send(ev, info_text)
