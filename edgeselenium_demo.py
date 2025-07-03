import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1. 让用户选择要打开的网页
file_name = input("请输入要打开的网页文件名（如 html.html 或 zhongzhouxian4.html）：").strip()
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
if not os.path.exists(file_path):
    print("文件不存在，请检查文件名！")
    exit(1)
url = f'file:///{file_path.replace(os.sep, "/")}'

options = webdriver.EdgeOptions()
options.add_experimental_option('detach', True)
driver = webdriver.Edge(options=options)
driver.get(url)
time.sleep(2)

# 2. 针对不同网页，执行不同跳转逻辑
if file_name == "html.html":
    nav_map = {
        "首页": "首页",
        "环保活动": "环保活动",
        "减碳小贴士": "减碳小贴士",
        "环保留言板": "环保留言板"
    }
    while True:
        command = input("请输入指令（如：打开环保活动，打开首页，输入exit退出）：")
        if command.strip() == "exit":
            break
        found = False
        for key in nav_map:
            if key in command:
                try:
                    btn = driver.find_element(By.LINK_TEXT, nav_map[key])
                    btn.click()
                    print(f"已自动跳转到{key}板块！")
                    found = True
                    break
                except Exception as e:
                    print(f"未找到'{key}'按钮，或点击失败：", e)
                    found = True
                    break
        if not found:
            print("未识别指令，请输入如'打开环保活动'、'打开首页'等。")
elif file_name == "zhongzhouxian4.html":
    # 支持的主板块和地标
    section_map = {
        "概述": "overview",
        "中轴线地图": "map",
        "地标建筑": "landmarks",
        "现代建筑": "modern"
    }
    # 地标id列表（部分示例，可补充）
    landmark_ids = [
        "永定门", "先农坛", "天坛", "正阳门", "天安门广场", "天安门", "外金水桥", "端门", "故宫", "太庙", "社稷坛", "景山", "万宁桥", "钟鼓楼", "鸟巢", "水立方"
    ]
    nav_map = {
        "概述": "概述",
        "中轴线地图": "中轴线地图",
        "地标建筑": "地标建筑",
        "现代建筑": "现代建筑"
    }
    while True:
        command = input("请输入指令（如：跳转到天坛，跳转到现代建筑，跳转到概述，输入exit退出）：")
        if command.strip() == "exit":
            break
        found = False
        # 导航栏跳转
        for key in nav_map:
            if key in command:
                try:
                    btn = driver.find_element(By.LINK_TEXT, nav_map[key])
                    btn.click()
                    print(f"已自动跳转到{key}板块！")
                    found = True
                    break
                except Exception as e:
                    pass
        # 主板块跳转（通过id）
        for key, section_id in section_map.items():
            if key in command:
                driver.execute_script(f"document.getElementById('{section_id}').scrollIntoView();")
                print(f"已跳转到{key}板块！")
                found = True
                break
        # 地标跳转
        for landmark in landmark_ids:
            if landmark in command:
                driver.execute_script(f"document.getElementById('{landmark}').scrollIntoView();")
                print(f"已跳转到{landmark}！")
                found = True
                break
        if not found:
            print("未识别指令，请输入如'跳转到天坛'、'跳转到现代建筑'、'跳转到概述'等。")
else:
    print("暂不支持该网页的自动跳转功能。")

print("即将关闭浏览器...")
driver.quit()