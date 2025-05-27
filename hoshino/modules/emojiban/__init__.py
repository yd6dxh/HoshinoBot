from hoshino import Service, R, util
from hoshino.typing import CQEvent
import re

sv = Service('emojiban', enable_on_default=True)

# 设置需要拦截的表情（这里以QQ默认表情“[捂脸]”为例，可以添加更多）
BANNED_EMOJIS = ['[哦]']  # 自行添加想屏蔽的
MUTE_SECONDS = 86400  # 禁言时间（单位：秒）

@sv.on_message()
async def ban_on_emoji(bot, ev: CQEvent):
    # 检查是否是群消息
    if not ev.message_type == 'group':
        return

    # 遍历所有禁止表情
    for emoji in BANNED_EMOJIS:
        if emoji in str(ev.message):
            try:
                await bot.set_group_ban(
                    group_id=ev.group_id,
                    user_id=ev.user_id,
                    duration=MUTE_SECONDS
                )
                await bot.send(ev, f'检测到禁用表情“{emoji}”，禁言{MUTE_SECONDS}秒。')
                break
            except Exception as e:
                sv.logger.error(f'禁言失败: {e}')
print("emojiban 插件已加载")

