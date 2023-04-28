from telegram.ext import ContextTypes
import bot
import socketio
import requests
import json
import base64

# def someting
config = bot.config
client = bot.client
website_id = config["crisp"]["website"]

query = {}
conversationMetasDict = {}  # {session_id : metas}


class Conf:
    desc = "推送未读新消息"
    method = "events"
    enable = False

if config['crisp']['msgapi'] == 'rtm':
    Conf.enable = True 

def getKey(content: str):
    if len(config["autoreply"]) > 0:
        for x in config["autoreply"]:
            keyword = x.split("|")
            for key in keyword:
                if key in content:
                    return True, config["autoreply"][x]
    return False, ""


# Store crisp conversation metas
def storeCrispConversationMetas(session_id):
    metas = client.website.get_conversation_metas(website_id, session_id)
    conversationMetasDict[session_id] = metas


# Create socketio client instance
sioEvents = [
    "message:send",
    "session:set_data"
]

sioAuthenticateTier = {
    "tier": "plugin",
    "username": config["crisp"]["id"],
    "password": config["crisp"]["key"],
    "events": sioEvents,
}
sio = socketio.AsyncClient(reconnection_attempts=5, logger=True)


# Meow!
def getCrispConnectEndpoints():
    url = "https://api.crisp.chat/v1/plugin/connect/endpoints"

    authtier = base64.b64encode(
        (config["crisp"]["id"] + ":" + config["crisp"]["key"]).encode("utf-8")
    ).decode("utf-8")
    payload = ""
    headers = {"X-Crisp-Tier": "plugin", "Authorization": "Basic " + authtier}
    response = requests.request("GET", url, headers=headers, data=payload)
    endPoint = json.loads(response.text).get("data").get("socket").get("app")
    return endPoint


def sendTextMessageBuilder(message):
    session_id = message["session_id"]
    metas = conversationMetasDict.get(session_id)
    text = "📠<b>Crisp消息推送</b>\n"
    if len(metas["email"]) > 0:
        email = metas["email"]
        text = f"{text}📧<b>电子邮箱</b>：{email}\n"
    if len(metas["data"]) > 0:
        if "Plan" in metas["data"]:
            Plan = metas["data"]["Plan"]
            text = f"{text}🪪<b>使用套餐</b>：{Plan}\n"
        if "UsedTraffic" in metas["data"] and "AllTraffic" in metas["data"]:
            UsedTraffic = metas["data"]["UsedTraffic"]
            AllTraffic = metas["data"]["AllTraffic"]
            text = f"{text}🗒<b>流量信息</b>：{UsedTraffic} / {AllTraffic}\n"
    content = message["content"]
    text = f"{text}🧾<b>消息内容</b>：{content}\n"
    # 自动回复判定
    result, autoreply = getKey(message["content"])
    if result is True:
        text = f"{text}💡<b>自动回复</b>：{autoreply}\n"
        query = {
            "type": "text",
            "content": autoreply,
            "from": "operator",
            "origin": "chat",
        }
        client.website.send_message_in_conversation(website_id, session_id, query)
    # Session打个码
    text = f"{text}\n🧷<b>Session</b>：<tg-spoiler>{session_id}</tg-spoiler>"
    return text


def sendImageMessageBuilder(message):
    session_id = message["session_id"]
    text = "📠<b>Crisp消息推送</b>\n"
    # Session打个码
    text = f"{text}\n🧷<b>Session</b>：<tg-spoiler>{session_id}</tg-spoiler>"
    return text


async def sendTextMessage(message):
    session_id = message["session_id"]
    text = sendTextMessageBuilder(message)
    for admin_id in config["bot"]["admin_id"]:
        await callbackContext.bot.send_message(
            chat_id=admin_id, text=text, parse_mode="HTML"
        )
    client.website.mark_messages_read_in_conversation(
        website_id,
        session_id,
        {"from": "user", "origin": "chat", "fingerprints": [message["fingerprint"]]},
    )


async def sendImageMessage(message):
    session_id = message["session_id"]
    text = sendImageMessageBuilder(message)
    for admin_id in config["bot"]["admin_id"]:
        await callbackContext.bot.send_photo(
            chat_id=admin_id,
            photo=message["content"]["url"],
            caption=text,
            parse_mode="HTML",
        )
    client.website.mark_messages_read_in_conversation(
        website_id,
        session_id,
        {"from": "user", "origin": "chat", "fingerprints": [message["fingerprint"]]},
    )

# Send all unread message.
async def sendAllUnread():
    conversations = client.website.search_conversations(
        website_id, 1, filter_unread='1')
    if len(conversations) > 0:
        query = {}
        for conversation in conversations:
            session_id = conversation['session_id']
            messages = client.website.get_messages_in_conversation(website_id, session_id, query)
            if conversationMetasDict.get(session_id) == None:
                storeCrispConversationMetas(session_id)
            for message in messages:
                if len(message['read']) == 0:
                    if message["type"] == "text":
                        await sendTextMessage(message)
                    elif message["type"] == "file" and str(message["content"]["type"]).count("image") > 0:
                        await sendImageMessage(message)
                    else:
                        print("Unhandled Message Type : ", message["type"])

# Def Event Handlers
@sio.on("connect")
async def connect():
    await sio.emit("authentication", sioAuthenticateTier)


@sio.on("unauthorized")
async def unauthorized(data):
    pass
    print('Unauthorized: ', data)

@sio.on("session:set_data")
async def updateMetasDataNode(data):
    for key in data.get('data'):
        conversationMetasDict[data['session_id']]['data'][key]=data['data'][key]
    pass

@sio.on("message:send")
async def messageForward(data):
    session_id = data["session_id"]
    try:
        if conversationMetasDict.get(session_id) == None:
            storeCrispConversationMetas(session_id)
        if data["type"] == "text":
            await sendTextMessage(data)
        elif data["type"] == "file" and str(data["content"]["type"]).count("image") > 0:
            await sendImageMessage(data)
        else:
            print("Unhandled Message Type : ", data["type"])
    except Exception as err:
        print(err)

@sio.event
async def connect_error():
    print("The connection failed!")


@sio.event
async def disconnect():
    print("Disconnected from server.")


# Connecting to Crisp RTM(WSS) Server
async def start_server():
    await sio.connect(
        getCrispConnectEndpoints(),
        transports="websocket",
        wait_timeout=10,
    )
    await sio.wait()


# _(:з」∠)_
async def exec(context: ContextTypes.DEFAULT_TYPE):
    global callbackContext
    callbackContext = context
    await sendAllUnread()
    await start_server()
