from telegram.ext import ContextTypes
import bot

config = bot.config
client = bot.client


class Conf:
    desc = '推送未读新消息'
    method = 'repeating'
    interval = 60


def getKey(content: str):
    if len(config['autoreply']) > 0:
        for x in config['autoreply']:
            keyword = x.split('|')
            for key in keyword:
                if key in content:
                    return True, config['autoreply'][x]
    return False, ''


async def exec(context: ContextTypes.DEFAULT_TYPE):
    website_id = config['crisp']['website']
    conversations = client.website.search_conversations(
        website_id, 1, filter_unread='1')
    if len(conversations) > 0:
        data = {
            "from": "user",
            "origin": "chat",
            "fingerprints": []
        }
        query = {

        }
        for conversation in conversations:
            session_id = conversation['session_id']
            # Crisp api docs: Returns the last batch of messages. 这个last batch到底能有多少我没整明白.
            messages = client.website.get_messages_in_conversation(
                website_id, conversation['session_id'], query)
            for message in messages:
                # read长度为0时该条消息未读
                if len(message['read']) == 0:
                    # 筛选出文本消息
                    if message['type'] == 'text':
                        # 通过消息指纹将消息置为已读
                        data['fingerprints'] = [message['fingerprint']]
                        client.website.mark_messages_read_in_conversation(
                            website_id, session_id, data)
                        text = '📠<b>Crisp消息推送</b>\n'
                        content = message['content']
                        text = f'{text}🧾<b>消息内容</b>：{content}\n'
                        # 自动回复判定
                        result, autoreply = getKey(message['content'])
                        if result is True:
                            text = f'{text}💡<b>自动回复</b>：{autoreply}\n'
                            query = {
                                "type": "text",
                                "content": autoreply,
                                "from": "operator",
                                "origin": "chat"
                            }
                            client.website.send_message_in_conversation(
                                website_id, session_id, query)
                        # Session打个码
                        text = f'{text}\n🧷<b>Session</b>：<tg-spoiler>{session_id}</tg-spoiler>'
                        for admin_id in config['bot']['admin_id']:
                            await context.bot.send_message(
                                chat_id=admin_id,
                                text=text,
                                parse_mode='HTML'
                            )
                    # 筛选出文件类型消息
                    if message['type'] == 'file':
                        # 通过文件mime type筛选出含image消息
                        mime = str(message['content']['type'])
                        if mime.count('image') > 0:
                            # 通过消息指纹将消息置为已读
                            data['fingerprints'] = [message['fingerprint']]
                            client.website.mark_messages_read_in_conversation(
                                website_id, session_id, data)

                            text = '📠<b>Crisp消息推送</b>\n'
                            # Session打个码
                            text = f'{text}\n🧷<b>Session</b>：<tg-spoiler>{session_id}</tg-spoiler>'
                            for admin_id in config['bot']['admin_id']:
                                await context.bot.send_photo(
                                    chat_id=admin_id,
                                    photo=message['content']['url'],
                                    caption=text,
                                    parse_mode='HTML'
                                )
