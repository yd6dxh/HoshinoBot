from hoshino.typing import CQEvent
from hoshino.util import FreqLimiter, filt_message

from .. import chara
from . import sv

CN_NUM_SIMPLE = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
}

def chinese_to_digit(star_text: str) -> int | None:
    return CN_NUM_SIMPLE.get(star_text, None)

lmt = FreqLimiter(5)

@sv.on_suffix('是谁')
@sv.on_prefix('谁是')
async def whois(bot, ev: CQEvent):
    name = ev.message.extract_plain_text().strip()
    if not name:
        return
    id_ = chara.name2id(name)
    confi = 100
    guess = False
    if id_ == chara.UNKNOWN:
        id_, guess_name, confi = chara.guess_id(name)
        guess = True
    c = chara.fromid(id_)

    if confi < 60:
        return

    uid = ev.user_id
    if not lmt.check(uid):
        await bot.finish(ev, f'兰德索尔花名册冷却中(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)

    lmt.start_cd(uid, 120 if guess else 0)
    if guess:
        name = filt_message(name)
        msg = f'兰德索尔似乎没有叫"{name}"的人...\n角色别称补全计划: github.com/Ice9Coffee/LandosolRoster'
        await bot.send(ev, msg)
        msg = f'您有{confi}%的可能在找{guess_name} {await c.get_icon_cqcode()} {c.name}'
        await bot.send(ev, msg)
    else:
        msg = f'{await c.get_icon_cqcode()} {c.name}'
        await bot.send(ev, msg, at_sender=True)

@sv.on_rex(r'^查(询|找|看)\s*([一二三四五六1-6])星(卡面|立绘)\s*(.+)$')
async def query_card(bot, ev: CQEvent):
    uid = ev.user_id
    if not lmt.check(uid):
        await bot.finish(ev, f'兰德索尔花名册冷却中(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)
    lmt.start_cd(uid)
    
    match = ev['match']
    star = match.group(2) 
    star_digit = chinese_to_digit(star) if not star.isdigit() else int(star)
    name = match.group(4).strip() 
    
    c = chara.fromname(name, star=int(star_digit))
    if c.id == chara.UNKNOWN:
        msg = f'未知角色'
        if uid not in bot.config.SUPERUSERS:
            lmt.start_cd(uid, 120)
            msg += '\n非管理员2分钟内仅能查询一次'
        await bot.send(ev, msg, at_sender=True)
        return
    
    await bot.send(ev, await c.get_card_cqcode())

@sv.on_rex(r'^查(询|找|看)\s*([1-6])星头像\s*(.+)$')
async def query_icon(bot, ev: CQEvent):
    uid = ev.user_id
    if not lmt.check(uid):
        await bot.finish(ev, f'兰德索尔花名册冷却中(剩余 {int(lmt.left_time(uid)) + 1}秒)', at_sender=True)
    lmt.start_cd(uid)
    
    match = ev['match']
    star = match.group(2) 
    star_digit = chinese_to_digit(star) if not star.isdigit() else int(star)
    name = match.group(4).strip() 
    
    c = chara.fromname(name, star=int(star_digit))
    if c.id == chara.UNKNOWN:
        msg = f'未知角色'
        if uid not in bot.config.SUPERUSERS:
            lmt.start_cd(uid, 60)
            msg += '\n非管理员2分钟内仅能查询一次'
        await bot.send(ev, msg, at_sender=True)
        return
    
    await bot.send(ev, await c.get_icon_cqcode())