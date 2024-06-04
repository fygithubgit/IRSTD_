import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

num = 0  # 计数器，记录已下载图片数量
max_images = 4000  # 最大下载图片数量

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
}

# 使用Selenium启动浏览器
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 设置窗口大小，确保可以加载更多图片
driver.set_window_size(1920, 1080)

# 图片页面的url
url = 'https://www.bing.com/images/search?q=%E9%9A%90%E7%90%83%E8%8F%8C%E5%9B%BE%E7%89%87&form=IQFRML&first=1'
driver.get(url)

pachong_picture_path = r'D:\DAIMA\BasicIRSTD-main\images'
if not os.path.exists(pachong_picture_path):
    os.mkdir(pachong_picture_path)


def download_image(img_url, num):
    try:
        picture = requests.get(img_url, headers=headers, timeout=10)  # 设置超时
        if picture.status_code == 200:
            file_name = os.path.join(pachong_picture_path, f'image{num}.jpg')  # 给下载下来的图片命名。加数字，是为了名字不重复
            with open(file_name, "wb") as f:  # 以二进制写入的方式打开图片
                f.write(picture.content)  # 往图片里写入爬下来的图片内容
            print(f'Successfully downloaded {file_name}')
        else:
            print(f'Failed to download {img_url} - status code: {picture.status_code}')
    except Exception as e:
        print(f'Failed to download {img_url} - {e}')


# 记录已经下载过的图片URL，避免重复下载
downloaded_urls = set()

while num < max_images:
    # 向下滚动页面，加载更多图片
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)  # 等待页面加载

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 查找所有img标签
    img_tags = soup.find_all('img')

    for img_tag in img_tags:
        img_url = img_tag.get('src')
        if img_url and img_url.startswith('http') and img_url not in downloaded_urls:
            num += 1  # 数字加1，这样图片名字就不会重复了
            download_image(img_url, num)
            downloaded_urls.add(img_url)

            if num >= max_images:
                break

driver.quit()
print('Download completed.')
