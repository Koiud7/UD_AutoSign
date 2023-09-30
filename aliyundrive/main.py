import os
import re
import requests

from aliyundrive import Aliyundrive


def main():
    token = os.environ["ALIYUNDRIVE_TOKEN"]
    
    ali = Aliyundrive()
    message_all = []

    result = ali.aliyundrive_check_in(token)
    message_all.append(str(result))

    title = '阿里云盘签到结果'
    message_all = '\n'.join(message_all)
    message_all = re.sub('\n+', '\n', message_all).rstrip('\n')

    send_to_telegram(message_all)
    print(message_all)


def send_to_telegram(message_all):  # 接收 email 和 message 参数
    if "TELEGRAM_BOT_TOKEN" in os.environ and "TELEGRAM_CHAT_ID" in os.environ:
        bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": f" {message_all}",
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Telegram 消息发送成功")
        else:
            print("Telegram 消息发送失败")
    else:
        print("未配置 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")

if __name__ == '__main__':
    main()
