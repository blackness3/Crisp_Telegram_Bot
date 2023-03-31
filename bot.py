import logging
import yaml
import sys
import re

from telegram import __version__ as TG_VER
from telegram import Update
from crisp_api import Crisp

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This bot is not compatible with your current PTB version {TG_VER}. To upgrade use this command:"
        f"pip3 install python-telegram-bot --upgrade --pre"
    )
from telegram.ext import Application, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.getLogger(__name__)

VERSION = "2.0"

try:
    f = open('config.yml', 'r', encoding='utf-8')
    config = yaml.safe_load(f)
    if 'autoreply' not in config:
        with open("config.yml", "w", encoding="utf-8") as f:
            config['autoreply'] = {'在吗|你好': '欢迎使用客服系统，请等待客服回复你~'}
            print(config)
            yaml.dump(config, f, allow_unicode=True)
except FileNotFoundError as error:
    print('没有找到 config.yml，请复制 config.yml.example 并重命名为 config.yml')
    sys.exit(0)

try:
    client = Crisp()
    client.set_tier("plugin")
    client.authenticate(config['crisp']['id'], config['crisp']['key'])
    client.plugin.get_connect_account()
    client.website.get_website(config['crisp']['website'])
except Exception as error:
    print('无法连接 Crisp 服务，请确认 Crisp 配置项是否正确')
    sys.exit(0)

try:
    token = config['bot']['token']
    #proxy = 'http://127.0.0.1:7890'
    app = Application.builder().token(token).build()
    #app = Application.builder().token(token).proxy_url(proxy).get_updates_proxy_url(proxy).build()
except Exception as error:
    print('无法启动 Telegram Bot，请确认 Bot Token 是否正确，或者是否能连接 Telegram 服务器')
    sys.exit(0)


async def onReply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    website_id = config['crisp']['website']
    if msg.reply_to_message.text is not None:
        session_id = re.search(
            'session_\w{8}(-\w{4}){3}-\w{12}', msg.reply_to_message.text).group()
    elif msg.reply_to_message.caption is not None:
        session_id = re.search(
            'session_\w{8}(-\w{4}){3}-\w{12}', msg.reply_to_message.caption).group()
    query = {
        "type": "text",
        "content": msg.text,
        "from": "operator",
        "origin": "chat"
    }
    client.website.send_message_in_conversation(website_id, session_id, query)


def main():
    try:
        app.add_handler(MessageHandler(filters.REPLY & filters.TEXT, onReply))
        # 导入任务文件夹
        import Modules
        for i in Modules.content:
            mods = getattr(Modules, i)
            Conf = mods.Conf
            if Conf.method == 'repeating':
                app.job_queue.run_repeating(
                    mods.exec, interval=Conf.interval, name=i)
        # 启动 Bot
        app.run_polling(drop_pending_updates=True)
    except Exception as error:
        print(error)
        sys.exit(0)


if __name__ == "__main__":
    main()
