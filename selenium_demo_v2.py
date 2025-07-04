import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class UniversalWebNavigator:
    def __init__(self, browser_type="chrome"):
        """初始化通用网页导航器"""
        self.browser_type = browser_type.lower()
        self.driver = None
        self.navigation_elements = {}
        self.clickable_elements = {}
        self.scrollable_elements = {}
        
    def setup_driver(self):
        """设置浏览器驱动"""
        if self.browser_type == "chrome":
            options = webdriver.ChromeOptions()
            options.add_experimental_option('detach', True)
            self.driver = webdriver.Chrome(options=options)
        elif self.browser_type == "edge":
            options = webdriver.EdgeOptions()
            options.add_experimental_option('detach', True)
            self.driver = webdriver.Edge(options=options)
        else:
            raise ValueError("不支持的浏览器类型，请使用 'chrome' 或 'edge'")
    
    def analyze_page(self, url):
        """分析网页，提取可导航的元素"""
        print("正在分析网页结构...")
        
        # 等待页面加载
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 1. 查找导航链接
        self._find_navigation_links()
        
        # 2. 查找可点击元素
        self._find_clickable_elements()
        
        # 3. 查找可滚动到的元素
        self._find_scrollable_elements()
        
        # 4. 保存分析结果
        self._save_analysis()
        
        print(f"分析完成！发现 {len(self.navigation_elements)} 个导航元素，"
              f"{len(self.clickable_elements)} 个可点击元素，"
              f"{len(self.scrollable_elements)} 个可滚动元素")
    
    def _find_navigation_links(self):
        """查找导航链接"""
        # 常见的导航选择器
        nav_selectors = [
            "nav a", "header a", ".nav a", ".navigation a", ".menu a",
            "ul li a", ".navbar a", ".nav-menu a", ".nav-item a"
        ]
        
        for selector in nav_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.text.strip():
                        text = element.text.strip()
                        self.navigation_elements[text] = {
                            'type': 'link',
                            'element': element,
                            'selector': selector
                        }
            except Exception:
                continue
    
    def _find_clickable_elements(self):
        """查找可点击的元素"""
        # 查找按钮、链接等可点击元素
        clickable_selectors = [
            "button", "a", "[onclick]", "[role='button']", ".btn", ".button"
        ]
        
        for selector in clickable_selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed() and element.text.strip():
                        text = element.text.strip()
                        if text not in self.navigation_elements:
                            self.clickable_elements[text] = {
                                'type': 'clickable',
                                'element': element,
                                'selector': selector
                            }
            except Exception:
                continue
    
    def _find_scrollable_elements(self):
        """查找可滚动到的元素（有ID的元素）"""
        try:
            # 查找所有有ID的元素
            elements_with_id = self.driver.find_elements(By.CSS_SELECTOR, "[id]")
            for element in elements_with_id:
                element_id = element.get_attribute("id")
                if element_id and element.is_displayed():
                    # 尝试获取元素的文本内容作为显示名称
                    display_name = element.text.strip() or element_id
                    self.scrollable_elements[display_name] = {
                        'type': 'scrollable',
                        'id': element_id,
                        'element': element
                    }
        except Exception:
            pass
    
    def _save_analysis(self):
        """保存分析结果到文件"""
        analysis_data = {
            'navigation_elements': list(self.navigation_elements.keys()),
            'clickable_elements': list(self.clickable_elements.keys()),
            'scrollable_elements': list(self.scrollable_elements.keys())
        }
        
        with open('page_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis_data, f, ensure_ascii=False, indent=2)
    
    def execute_command(self, command):
        """执行用户命令"""
        command_lower = command.lower()
        
        # 1. 尝试导航链接
        for nav_text in self.navigation_elements:
            if nav_text.lower() in command_lower:
                try:
                    self.navigation_elements[nav_text]['element'].click()
                    print(f"已点击导航链接：{nav_text}")
                    return True
                except Exception as e:
                    print(f"点击导航链接失败：{e}")
                    return True
        
        # 2. 尝试可点击元素
        for clickable_text in self.clickable_elements:
            if clickable_text.lower() in command_lower:
                try:
                    self.clickable_elements[clickable_text]['element'].click()
                    print(f"已点击元素：{clickable_text}")
                    return True
                except Exception as e:
                    print(f"点击元素失败：{e}")
                    return True
        
        # 3. 尝试滚动到元素
        for scrollable_text in self.scrollable_elements:
            if scrollable_text.lower() in command_lower:
                try:
                    element_id = self.scrollable_elements[scrollable_text]['id']
                    self.driver.execute_script(f"document.getElementById('{element_id}').scrollIntoView();")
                    print(f"已滚动到：{scrollable_text}")
                    return True
                except Exception as e:
                    print(f"滚动到元素失败：{e}")
                    return True
        
        return False
    
    def show_available_commands(self):
        """显示可用的命令"""
        print("\n=== 可用的导航命令 ===")
        
        if self.navigation_elements:
            print("导航链接：")
            for nav in self.navigation_elements:
                print(f"  - 点击 {nav}")
        
        if self.clickable_elements:
            print("可点击元素：")
            for clickable in self.clickable_elements:
                print(f"  - 点击 {clickable}")
        
        if self.scrollable_elements:
            print("可滚动到的元素：")
            for scrollable in self.scrollable_elements:
                print(f"  - 滚动到 {scrollable}")
        
        print("\n示例命令：")
        print("  - '点击首页'")
        print("  - '滚动到关于我们'")
        print("  - '点击登录按钮'")
        print("  - 'exit' 退出程序")
    
    def run(self, url):
        """运行导航器"""
        try:
            self.setup_driver()
            self.driver.get(url)
            time.sleep(2)
            
            # 分析页面
            self.analyze_page(url)
            
            # 显示可用命令
            self.show_available_commands()
            
            # 主循环
            while True:
                command = input("\n请输入命令：").strip()
                if command.lower() == "exit":
                    break
                
                if not self.execute_command(command):
                    print("未找到匹配的元素，请尝试其他命令或查看可用命令列表。")
                    print("输入 'help' 查看可用命令，输入 'exit' 退出。")
                elif command.lower() == "help":
                    self.show_available_commands()
        
        except Exception as e:
            print(f"发生错误：{e}")
        finally:
            if self.driver:
                print("即将关闭浏览器...")
                self.driver.quit()

def main():
    """主函数"""
    print("=== 通用网页导航器 ===")
    
    # 选择浏览器类型
    browser = input("请选择浏览器类型 (chrome/edge，默认chrome): ").strip() or "chrome"
    
    # 选择要打开的网页
    choice = input("请选择要打开的网页：\n1. 本地HTML文件\n2. 网络URL\n请输入选择 (1/2): ").strip()
    
    if choice == "1":
        # 本地文件
        file_name = input("请输入要打开的网页文件名（如 html.html 或 zhongzhouxian4.html）：").strip()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), file_name))
        if not os.path.exists(file_path):
            print("文件不存在，请检查文件名！")
            return
        url = f'file:///{file_path.replace(os.sep, "/")}'
    elif choice == "2":
        # 网络URL
        url = input("请输入网页URL：").strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
    else:
        print("无效选择！")
        return
    
    # 创建并运行导航器
    navigator = UniversalWebNavigator(browser)
    navigator.run(url)

if __name__ == "__main__":
    main() 