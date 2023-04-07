- [Crisp Telegram Bot via Python](#crisp-telegram-bot-via-python)
  - [现有功能](#现有功能)
  - [常规使用](#常规使用)
  - [申请 Telegram Bot Token](#申请-telegram-bot-token)
  - [申请 Crisp 以及 MarketPlace 插件](#申请-crisp-以及-marketplace-插件)
  - [Docker部署](#docker部署)
    - [1. 安装Docker](#1-安装docker)
    - [2. 部署容器](#2-部署容器)
      - [2.1 下载compose文件](#21-下载compose文件)
      - [2.2 使用环境变量进行配置](#22-使用环境变量进行配置)
      - [2.3 运行容器](#23-运行容器)
    - [3. 环境变量说明](#3-环境变量说明)
    - [4. tagname说明](#4-tagname说明)
  - [特别说明](#特别说明)

# Crisp Telegram Bot via Python

一个简单的项目，让 Crisp 客服系统支持透过 Telegram Bot 来快速回复
快速反馈群：[https://t.me/v2board_python_bot](https://t.me/v2board_python_bot)

Python 版本需求 >= 3.8

## 现有功能
- 基于Crisp客服系统
- 自动推送文字、图片到指定聊天
- 自动基于关键词回复对应内容
- 支持回复后推送回对应客户

## 常规使用
```
# apt install git 如果你没有git的话
git clone https://github.com/DyAxy/Crisp_Telegram_Bot.git
# 进程常驻可参考 screen 或 nohup
# 你需要安装好 pip3 的包管理
cd Crisp_Telegram_Bot
pip3 install -r requirements.txt
cp config.yml.example config.yml
nano config.yml
# 编辑 line 3 为你的Bot Token
# 编辑 line 4、5 为信息发送的聊天ID
# 编辑 line 7 为你的 Crisp Marketplace 插件 ID
# 编辑 line 8 为你的 Crisp Marketplace 插件秘钥
# 编辑 line 9 为你的 Crisp 网站ID
# 编辑 line 11 为自动关键词回复，你可以复制成多行，每个关键词用 `|` 隔开即可，在 `:` 后输入自动回复内容
python3 bot.py
```

## 申请 Telegram Bot Token

1. 私聊 [https://t.me/BotFather](https://https://t.me/BotFather)
2. 输入 `/newbot`，并为你的bot起一个**响亮**的名字
3. 接着为你的bot设置一个username，但是一定要以bot结尾，例如：`v2board_bot`
4. 最后你就能得到bot的token了，看起来应该像这样：`123456789:gaefadklwdqojdoiqwjdiwqdo`

## 申请 Crisp 以及 MarketPlace 插件
1. 注册 [https://app.crisp.chat/initiate/signup](https://app.crisp.chat/initiate/signup)
2. 完成注册后，网站ID在浏览器中即可找到，看起来应该像这样：`https://app.crisp.chat/settings/website/12345678-1234-1234-1234-1234567890ab/`
3. 其中 `12345678-1234-1234-1234-1234567890ab` 就是网站ID
4. 前往 MarketPlace， 需要重新注册账号 [https://marketplace.crisp.chat/](https://marketplace.crisp.chat/)
5. 点击 New Plugin，选择 Private，输入名字以及描述。会获得开发者ID和Key，可能会不够用。
6. 需要Production Key，点击 Ask a production token，再点击Add a Scope。
7. 需要 2 条**read**和**write**权限：`website:conversation:sessions` 和 `website:conversation:messages`
8. 保存后即可获得ID和Key，此时点击右上角 Install Plugin on Website 即可。

## Docker部署
### 1. 安装Docker  
详细方法参详Linux发行版Wiki 或 [Docker Docs](https://docs.docker.com/desktop/get-started/)  

### 2. 部署容器
#### 2.1 下载compose文件
    curl -JL https://github.com/DyAxy/Crisp_Telegram_Bot/raw/master/docker-compose.yml.example -o docker-compose.yml
#### 2.2 使用环境变量进行配置
编辑docker-compose.yml文件，按照自己的情况将参数值填写到environment下的各项当中。  
同时保持volumes相关内容处于注释状态。
详细说明见[2.4 环境变量说明](#3-环境变量说明)
#### 2.3 运行容器
    docker compose -f docker-compose.yml up

### 3. 环境变量说明
容器未挂载config.yml时，entrypoint.sh会根据环境变量生成config.yml。  
注：distroless构建的镜像暂不支持环境变量生产配置文件。
| 选项/参数     | 说明                                                                                                              |
| ------------- | ----------------------------------------------------------------------------------------------------------------- |
| BOT_TOKEN     |                                                                                                                   |
| BOT_ADMIN_ID  | 管理员tg id，使用半角逗号(,)分隔。<br>e.g. 123456789,321654987,555555,111222                                      |
| CRISP_ID      | Crisp Marketplace 插件 ID                                                                                         |
| CRISP_KEY     | Crisp Marketplace 插件秘钥                                                                                        |
| CRISP_WEBSITE | Crisp 网站ID                                                                                                      |
| BOT_AUTOREPLY | 自动回复设置，详见[常规使用](#常规使用)，新增的时候整行复制往下写。<br>注："\0"是留着给entrypoint转义用的，别删。 |


### 4. tagname说明
| tag    | 说明                      | image size                                                                                            |
| ------ | ------------------------- | ----------------------------------------------------------------------------------------------------- |
| latest | alpine 3.17 + python 3.8  | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/latest) |
| 3.8    | 同latest                  | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/py3.8)  |
| 3.9    | alpine 3.17 + python 3.9  | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/py3.9)  |
| 3.10   | alpine 3.17 + python 3.10 | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/py3.10) |
| 3.11   | alpine 3.17 + python 3.11 | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/py3.11) |

## 特别说明
某些v2board自定义主题没有向crisp push data，需要用户自行实现，详见[crisp Chatbox Web SDK](https://docs.crisp.chat/guides/chatbox-sdks/web-sdk/)  
本项目包含一个v2board的示例: [v2board.js](/Assistant/JavaScript/v2board.js)