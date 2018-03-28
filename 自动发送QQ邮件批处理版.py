from selenium import webdriver
import time
import sys
browser = webdriver.Firefox()  # 坑0：firefox需要下载geckodriver.exe
browser.get("https://mail.qq.com/")

# 点击账户密码登录按钮
browser.switch_to.frame("login_frame")  # 坑1:登录窗口在框架（frame）中，需要先进入这个框架
element = browser.find_element_by_id("switcher_plogin")  # 坑2：如果用class_name，后台登录qq和未登录的class_name有区别
element.click()

# 输入账号
uElement = browser.find_element_by_id("u")
uElement.send_keys("youremail@qq.com")

# 输入密码
pElement = browser.find_element_by_id("p")
pElement.send_keys("emailpasswd")

# 登录邮箱
loginElement = browser.find_element_by_class_name("login_button")
loginElement.click()
time.sleep(2)  # 坑2.5： 浏览器跳转页面延迟较长时可以设置一个延时以便新的页面加载出来后再执行后续代码

# 点击写信按钮

browser.switch_to.default_content()  # 坑3：进入某个框架后不能对主文档元素进行操作，如果需要，则应切换至主文档
composeElement = browser.find_element_by_id("composebtn")
composeElement.click()

# 填入正文内容
time.sleep(1)
browser.switch_to.frame("mainFrame")
letter = sys.argv[2]
letterElement = browser.find_element_by_xpath("/html/body")
letterElement.send_keys(letter)

# 填写主题
# time.sleep(0.5)
# subject = "来自DG的邮件"
# subElement = browser.find_element_by_id("subject")
# subElement.send_keys(subject)

# 填入收件人地址
time.sleep(0.5)
mailTo = sys.argv[1]
addElements = browser.find_element_by_id("toAreaCtrl")
addElement = addElements.find_element_by_tag_name("input")  # 坑4：input标签无法直接定位（xpath可以），需要二次定位
addElement.send_keys(mailTo)

# 发送邮件
sendElement = browser.find_element_by_name("sendbtn")
sendElement.click()

# 确认发送
time.sleep(1)
browser.switch_to.default_content()
# 坑5：如果发送时没有输入主题，会弹出窗口确认是否发送。检测handle没有变更，所以直接在原主文档进行操作
try:
    yesElement = browser.find_element_by_id("QMconfirm_QMDialog_confirm")
    yesElement.click()
    browser.quit()
except:
    browser.quit()
"""
使用sys模块加上bat批处理的方式可以帮助我们更方便的使用这个脚本。
此程序有一点安全性的问题，你的个人邮箱和密码都暴露在代码中很容易泄露，我的解决方案是另写一个密码保管的文件，以字典形式储存代码，然后把这个密码保管的文件作为模块导入进来。
其实在定位的过程中我发现很多时候selenium定位元素会比较难，需要多重定位，用xpath的方法会比较简单一点。
"""
