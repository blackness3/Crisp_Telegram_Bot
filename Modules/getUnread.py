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
                        #通过消息指纹将消息置为已读
                        data['fingerprints'] = [message['fingerprint']]
                        client.website.mark_messages_read_in_conversation(
                            website_id, session_id, data)

                        text = '📠Crisp消息推送\n'
                        content = message['content']
                        text = f'{text}🧾内容：{content}\n\n'
                        text = f'{text}🧷Session：{session_id}'
                        for admin_id in config['bot']['admin_id']:
                            await context.bot.send_message(
                                chat_id=admin_id,
                                text=text
                            )
                    # 筛选出文件类型消息
                    if message['type'] == 'file':
                        # 通过文件mime type筛选出含image消息
                        mime = str(message['content']['type'])
                        if mime.count('image') > 0:
                            #通过消息指纹将消息置为已读
                            data['fingerprints'] = [message['fingerprint']]
                            client.website.mark_messages_read_in_conversation(
                                website_id, session_id, data)
                            
                            for admin_id in config['bot']['admin_id']:
                                await context.bot.send_photo(chat_id=admin_id, photo=message['content']['url'], caption=message['content']['name'])