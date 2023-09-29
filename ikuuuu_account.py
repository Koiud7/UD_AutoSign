import sys
import requests
import os
# export ikuuu='邮箱&密码'      多号#号隔开
# os.environ['ikuuu'] = "melolohappy@gmail.com&why123456#3094687642@qq.com&check233"
def main():
    r = 1
    oy = ql_env()
    print("共找到" + str(len(oy)) + "个账号")
    for i in oy:
        print("------------正在执行第" + str(r) + "个账号----------------")
        email = i.split('&')[0]
        passwd = i.split('&')[1]
        sign_in(email, passwd)
        r += 1

def sign_in(email, passwd):
    try:
        body = {"email": email, "passwd": passwd}
        headers = {
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
        }
        resp = requests.session()
        resp.post(f'https://ikuuu.art/auth/login', headers=headers, data=body)
        ss = resp.post(f'https://ikuuu.art/user/checkin').json()
        if 'msg' in ss:
            print(ss['msg'])
    except:
        print('请检查帐号配置是否错误')

def ql_env():
    if "IKUUU_ACCOUNTS" in os.environ:
        accounts = os.environ['IKUUU_ACCOUNTS'].split('#')
        if len(accounts) > 0:
            return accounts
        else:
            print("IKUUU_ACCOUNTS变量未启用")
            sys.exit(1)
    else:
        print("未添加IKUUU_ACCOUNTS变量")
        sys.exit(0)


if __name__ == '__main__':
    main()