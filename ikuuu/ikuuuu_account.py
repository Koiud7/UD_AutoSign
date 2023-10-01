import sys
import requests
import os

def main():
    r = 1
    oy = ql_env()
    messages = []  # Create an empty list to collect messages
    for i in oy:
        print("------------正在执行第" + str(r) + "个账号----------------")
        email = i.split('&')[0]
        passwd = i.split('&')[1]
        result = sign_in(email, passwd)
        messages.append(f"账户：{email}\n{result}")  # Add the message to the list
        r += 1
    send_to_telegram(messages)  # Pass the list of messages to send_to_telegram

def sign_in(email, passwd):
    try:
        body = {"email" : email,"passwd" : passwd,}
        headers = {'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
        resp = requests.session()
        resp.post(f'https://ikuuu.art/auth/login', headers=headers, data=body)
        ss = resp.post(f'https://ikuuu.art/user/checkin').json()
        if 'msg' in ss:
            return ss['msg']
        else:
            return '未知错误'
    except Exception as e:
        return f'请检查帐号配置是否错误：{str(e)}'

def ql_env():
    if "IKUUU_ACCOUNTS" in os.environ:
        token_list = os.environ['IKUUU_ACCOUNTS'].split('#')
        if len(token_list) > 0:
            return token_list
        else:
            print("IKUUU_ACCOUNTS变量未启用")
            sys.exit(1)
    else:
        print("未添加IKUUU_ACCOUNTS变量")
        sys.exit(0)

def send_to_telegram(messages):
    if "TELEGRAM_BOT_TOKEN" in os.environ and "TELEGRAM_CHAT_ID" in os.environ:
        bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]
        text = "\n—————————————————\n".join(messages)  # Join the messages with separator
        formatted_message = f"🚀 ikuuu自动签到完成\n\n{html.escape(text)}"  # 转义文本以防止链接
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": formatted_message,
            "parse_mode": "HTML",
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
