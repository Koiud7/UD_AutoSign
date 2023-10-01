import os
import time
import ddddocr
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def save_img(src, img_path):
    img = requests.get(src)
    with open(img_path, "wb") as f:
        f.write(img.content)

def get_captcha(driver):
    driver.save_screenshot('pic.png')
    pic = Image.open('pic.png')
    # 确定验证码的位置和大小
    captcha_region = (500, 660, 640, 710)  # 替换x、y、width、height为实际值
    # 根据确定的位置和大小截取验证码
    captcha_image = pic.crop(captcha_region)
    # 保存验证码图片
    captcha_image.save('result.png')
    
    # 初始化 DDDDORC 实例
    ocr = ddddocr.DdddOcr()

    # 识别验证码图片中的字符
    with open('result.png', 'rb') as image_file:
        img_bytes = image_file.read()
    result = ocr.classification(img_bytes)
    return result


def login(driver):
    try:
        # 输入用户名和密码
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        # 找到元素
        element = driver.find_element(By.XPATH, "//img[@width='120']")
        # 使用JavaScript模拟点击
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)
        # 等待验证码图片加载完成
        captcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "seccodeverify"))
        )

        # 获取验证码并填入表单
        captcha = get_captcha(driver)
        captcha_element.clear()
        captcha_element.send_keys(captcha)

        # 登录按钮元素
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "loginsubmit"))
        )
        # 使用JavaScript模拟点击
        driver.execute_script("arguments[0].click();", login_button)
        time.sleep(20)

        # 检查登录按钮是否仍然存在
        if not driver.find_elements(By.NAME, "loginsubmit"):
            # 登录按钮不存在，登录成功
            print("登录成功")
            return True
        else:
            # 登录按钮仍然存在，登录失败
            return False
    except Exception as e:
        # 发生异常，登录失败
        print(f"登录时发生异常: {str(e)}")
        return False


def sign_in(driver):
    # 等待页面加载完成
    global sign_flag, message
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/?is_agree=1']"))
    )
    # 点击同意按钮
    driver.find_element(By.CSS_SELECTOR, "a[href='/?is_agree=1']").click()
    # 检查是否存在点击签到的元素
    sign_elements = driver.find_elements(By.XPATH, "//img[@alt='点击签到']")
    if sign_elements:
        sign = sign_elements[0]
        sign.click()
        sign_flag = "签到成功"
    else:
        # 如果点击签到元素不存在，检查今日已签到元素
        today_signed_elements = driver.find_elements(By.XPATH, "//img[@alt='今日已签']")
        if today_signed_elements:
            sign = today_signed_elements[0]
            sign.click()
            sign_flag = "今日已签"
    wait = WebDriverWait(driver, 10)
    # 在当前网页获取当日签到积分
    rmb_element = wait.until(EC.presence_of_element_located((By.ID, "lxreward")))
    rmb = rmb_element.get_attribute("value")
    # 获取连续签到日期
    lianxudays_element = wait.until(EC.presence_of_element_located((By.ID, "lxdays")))
    lianxudays = lianxudays_element.get_attribute("value")
    # 获取总软妹币
    driver.get("https://moxing.love/home.php?mod=spacecp&ac=credit")
    total_rmb_xpath = "/html/body/div/div[2]/div[1]/div/ul[2]/li[3]"
    total_rmb_element = wait.until(EC.presence_of_element_located((By.XPATH, total_rmb_xpath)))
    total_rmb = total_rmb_element.text
    total_rmb = total_rmb.split("软妹币:")[1].strip()
    # 获取头衔
    driver.get("https://moxing.love/home.php?mod=spacecp&ac=usergroup")
    touxian_xpath = "/html/body/div/div[2]/div[1]/div/div[1]/table[2]/tbody[3]/tr/th"
    touxian_element = wait.until(EC.presence_of_element_located((By.XPATH, touxian_xpath)))
    touxian = touxian_element.text
    # 获取总积分
    total_jifen_xpath = "/html/body/div/div[2]/div[1]/div/div[1]/table[2]/tbody[1]/tr[2]/th/span"
    total_jifen_element = wait.until(EC.presence_of_element_located((By.XPATH, total_jifen_xpath)))
    total_jifen = total_jifen_element.text
    total_jifen = total_jifen.split("积分:")[1].strip()
    # 获取升级还需要的积分
    total_need_xpath = "/html/body/div/div[2]/div[1]/div/div[1]/div/table/tbody[1]/tr[1]/th/span"
    total_need_element = wait.until(EC.presence_of_element_located((By.XPATH, total_need_xpath)))
    total_need = total_need_element.text
    total_need = total_need.split("您升级到此用户组还需积分")[1].strip()

    text = f"签到软妹币:  {rmb}\n软妹币总数:  {total_rmb}\n连续签到天数:  {lianxudays}\n—————————————————\n当前头衔:  {touxian}\n总积分:  {total_jifen}\n升级剩余积分  {total_need}"
    message = f"*😈moxing论坛: {sign_flag}*\n\n```\n{text}\n```"

def close_browser(driver):
    driver.quit()


def send_to_telegram(msg):  
    if "TELEGRAM_BOT_TOKEN" in os.environ and "TELEGRAM_CHAT_ID" in os.environ:
        bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": msg,
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Telegram 消息发送成功")
        else:
            print("Telegram 消息发送失败")
    else:
        print("未配置 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID")

# def send_image_to_telegram(image_path):
#     token = os.environ["TELEGRAM_BOT_TOKEN"]
#     chat_id = os.environ["TELEGRAM_CHAT_ID"]
#     url = f"https://api.telegram.org/bot{token}/sendPhoto"
#     files = {'photo': open(image_path, 'rb')}
#     data = {'chat_id': chat_id}
#     response = requests.post(url, data=data, files=files)
#     return response

if __name__ == "__main__":
    username = os.environ["MOXING_USERNAME"]
    password = os.environ["MOXING_PSW"]
    img_path = os.path.join(os.getcwd(), "1.png")

    max_attempts = 5  # 设置最大执行次数
    attempts = 0  # 初始化计数器
    while attempts < max_attempts:
        # 初始化WebDriver并设置窗口大小
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--window-size=1200,960")
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_argument("--start-maximized")  # 最大化窗口
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://moxing.love/member.php?mod=logging&action=login")
        # 设置页面缩放级别为100%
        driver.execute_script("document.body.style.zoom='100%'")
        login_success = login(driver)

        if login_success:
            sign_in(driver)
            time.sleep(5)
            send_to_telegram(message)
            print(message)
            close_browser(driver)
            break
        else:
            # 给telegram发消息：登录失败，正在重试
            close_browser(driver)
            attempts += 1  # 递增计数器
            alarm1 = f"moxing登陆失败:验证码错误，已重试 {attempts} 次"
            send_to_telegram(alarm1)
            print(alarm1)

        if attempts >= max_attempts:
            alarm2 = f"警告:达到最大重登次数{max_attempts}次，不再重试"
            send_to_telegram(alarm2)
            print(alarm2)
            break
