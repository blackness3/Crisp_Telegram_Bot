#!/bin/sh

conver_to_array(){
    eval BOT_ADMIN_ID_env=$1
    eval IFS=","
    str=""
    for admin_id in ${BOT_ADMIN_ID_env};do
        str="$str    - ${admin_id}\n"
    done
    result=`echo -e "${str}"`
}

if [ ! -e "/Crisp_Telegram_Bot/config.yml" ]; then
    conver_to_array ${BOT_ADMIN_ID}
    cat > /Crisp_Telegram_Bot/config.yml << EOF
bot:
  token: ${BOT_TOKEN}
  admin_id:
${result}
crisp:
  id: ${CRISP_ID}
  key: ${CRISP_KEY}
  website: ${CRISP_WEBSITE}
EOF
fi
exec "$@"