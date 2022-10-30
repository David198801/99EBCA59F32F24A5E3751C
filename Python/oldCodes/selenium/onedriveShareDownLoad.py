from selenium import webdriver
import time

passwordSwitch = True
password = "shen-nai"

options = webdriver.ChromeOptions()
options.binary_location = r"D:\Program Files\Chrome-bin\chrome.exe"
browser = webdriver.Chrome(chrome_options=options)

browser.get(r'https://jxjjxy-my.sharepoint.com/:f:/g/personal/kgky11vn_t_odmail_cn/ElZc7F-XMztHlMnOVNNBTZIBAVYUZz_GTSoRjMIBsGX6Kg?e=60h1W8')

#找到密码输入框，填入密码并点击验证
if passwordSwitch:
    inputElement = browser.find_element_by_id("txtPassword")
    inputElement.send_keys(password)
    browser.find_element_by_id("btnSubmitPassword").click()

dirElementContainerList = browser.find_elements_by_class_name("ms-List-cell")

for dirElementContainer in dirElementContainerList[:1]:
    buttonElement = dirElementContainer.find_elements_by_tag_name("button")[0]
    buttonElement.click()

    dirElementContainerList1 = browser.find_elements_by_class_name("ms-List-cell")
    for i in dirElementContainerList1:
        buttonElement1 = dirElementContainer.find_elements_by_tag_name("button")[0]
        print(buttonElement1.text)


# # browser.quit()