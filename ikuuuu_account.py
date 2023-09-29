import sys
import requests
import os

def main():
    r = 1
    oy = ql_env()
    print("共找到" + str(len(oy)) + "个账号")
    for i in oy:
        print("------------正在执行第" + str(r) + "个账号----------------")
        email = i.split('&')[0]
        passwd = i.split('&')[1]
        result = sign_in(email, passwd)
        send_to_telegram(result)
        r += 1

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

def send_to_telegram(message):
    if "TELEGRAM_BOT_TOKEN" in os.environ and "TELEGRAM_CHAT_ID" in os.environ:
        bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": email+":"+message,
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Telegram 消息发送成功")
        else:
            print("Telegram 消息发送失败")
    else:
        print(TELEGRAM_BOT_TOKEN)
        print(TELEGRAM_CHAT_ID)
        print(email)
        print(password)
        print("未配置 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")

if __name__ == '__main__':
    main()
