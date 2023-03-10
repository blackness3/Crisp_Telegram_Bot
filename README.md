    docker pull moefaq/crisp_telegram_bot:tagname
#### 参数说明
<table>
    <tr>
        <th>选项/参数</th>
        <th>说明</th>
    </tr>
    <tr>
        <td>--name </td>
        <td>容器名称设置为: </td>
    </tr>
    <tr>
        <td>-v ./config.yaml:/Crisp_Telegram_Bot/config.yaml</td>
        <td rowspan="2">将配置文件config.yaml挂载至容器中</td>
    </tr>
    <tr>
        <td>&lt;Crisp_Telegram_Bot_data&gt;/config.yaml:/Crisp_Telegram_Bot/config.yaml</td>
    </tr>
    <tr>
        <td>moefaq/Crisp_Telegram_Bot-docker:latest</td>
        <td>指定镜像, latest为镜像tag, 详见<a href="#24-image-tag%E8%AF%B4%E6%98%8E">Image tag说明</a></td>
    </tr>
    <tr>
        <td>-f docker-compose.yaml</td>
        <td>指定compose文件</td>
    </tr>
    <tr>
        <td>-p ctb</td>
        <td>指定project名称, 指定后容器名形如ctb-bot-1</td>
    </tr>
</table>

#### Docker-compose.yml 环境变量说明
容器未挂载config.yml时，entrypoint.sh会根据环境变量生成config.yml。  
注：distroless构建的镜像暂不支持环境变量生产配置文件。
| 选项/参数     | 说明                                                                         |
| ------------- | ---------------------------------------------------------------------------- |
| BOT_TOKEN     |                                                                              |
| BOT_ADMIN_ID  | 管理员tg id，使用半角逗号(,)分隔。<br>e.g. 123456789,321654987,555555,111222 |
| CRISP_ID      |                                                                              |
| CRISP_KEY     |                                                                              |
| CRISP_WEBSITE |                                                                              |


#### tagname说明
| tag        | 说明                                                  | image size                                                                                                |
| ---------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| latest     | alpine 3.17 + python 3.8                              | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/latest)     |
| 3.8        | 同latest                                              | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/py3.8)      |
| 3.9        | alpine 3.17 + python 3.9                              | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/py3.9)      |
| 3.10       | alpine 3.17 + python 3.10                             | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/py3.10)     |
| 3.11       | alpine 3.17 + python 3.11                             | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/py3.11)     |
| distroless | 使用google distroless镜像构建<br>debian11 +python 3.9 | ![Docker Image Size (tag)](https://img.shields.io/docker/image-size/moefaq/crisp_telegram_bot/distroless) |