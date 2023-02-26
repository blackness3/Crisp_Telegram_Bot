from telegram.ext import ContextTypes
import bot

config = bot.config
client = bot.client


class Conf:
    desc = '推送未读新消息'
    method = 'repeating'
    interval = 60


async def exec(context: ContextTypes.DEFAULT_TYPE):
    website_id = config['crisp']['website']
    messages = client.website.search_conversations(website_id, 1, filter_unread='1')
    if len(messages) > 0:
        data = {
            "from": "user",
            "origin": "chat",
        }
        for i in messages:
            session_id = i['session_id']
            client.website.mark_messages_read_in_conversation(website_id, session_id, data)
            text = '📠Crisp消息推送\n'
            messages = i['last_message']
            text = f'{text}🧾内容：{messages}\n\n'
            text = f'{text}🧷Session：{session_id}'
            for admin_id in config['bot']['admin_id']:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=text
                )