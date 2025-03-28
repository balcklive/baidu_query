#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class BaiduSearcher:
    """百度搜索类，用于搜索特定关键词并返回搜索结果链接"""
    
    # 常量定义
    BAIDU_URL = "https://www.baidu.com"
    SEARCH_BOX_ID = "kw"
    SEARCH_BUTTON_ID = "su"
    RESULT_LINKS_SELECTOR = "#content_left .result a"
    WAIT_TIME = 2  # 等待页面加载的时间（秒）
    MAX_RESULTS = 10  # 默认返回的最大结果数量
    
    # 支持的浏览器类型
    BROWSER_CHROME = "chrome"
    BROWSER_FIREFOX = "firefox"
    BROWSER_EDGE = "edge"
    
    def __init__(self, browser_type=BROWSER_FIREFOX, headless=False):
        """
        初始化搜索器
        
        Args:
            browser_type: 浏览器类型，支持 "chrome", "firefox", "edge"
            headless: 是否使用无头模式（不显示浏览器界面）
        """
        self.browser_type = browser_type.lower()
        self.driver = None
        
        # 根据不同的浏览器类型初始化WebDriver
        if self.browser_type == self.BROWSER_CHROME:
            self._init_chrome_driver(headless)
        elif self.browser_type == self.BROWSER_FIREFOX:
            self._init_firefox_driver(headless)
        elif self.browser_type == self.BROWSER_EDGE:
            self._init_edge_driver(headless)
        else:
            raise ValueError(f"不支持的浏览器类型: {browser_type}，请使用 'chrome', 'firefox' 或 'edge'")
    
    def _init_chrome_driver(self, headless):
        """初始化Chrome浏览器驱动"""
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
            
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        try:
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                options=options
            )
        except Exception as e:
            print(f"Chrome浏览器初始化失败: {e}")
            print("尝试使用Firefox浏览器...")
            self.browser_type = self.BROWSER_FIREFOX
            self._init_firefox_driver(headless)
    
    def _init_firefox_driver(self, headless):
        """初始化Firefox浏览器驱动"""
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        
        try:
            self.driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=options
            )
        except Exception as e:
            print(f"Firefox浏览器初始化失败: {e}")
            print("尝试使用Edge浏览器...")
            self.browser_type = self.BROWSER_EDGE
            self._init_edge_driver(headless)
    
    def _init_edge_driver(self, headless):
        """初始化Edge浏览器驱动"""
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        
        # 添加自定义用户数据目录
        import tempfile
        user_data_dir = os.path.join(tempfile.gettempdir(), f"edge_user_data_{int(time.time())}")
        options.add_argument(f"--user-data-dir={user_data_dir}")
        
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )
    
    def search(self, keyword, max_results=None):
        """
        搜索关键词并返回结果链接
        
        Args:
            keyword: 要搜索的关键词
            max_results: 返回的最大结果数量，默认为类中定义的常量
            
        Returns:
            包含搜索结果链接的列表，每个结果为字典，包含标题和URL
        """
        if not self.driver:
            raise Exception("浏览器驱动未初始化")
            
        if max_results is None:
            max_results = self.MAX_RESULTS
            
        # 打开百度首页
        self.driver.get(self.BAIDU_URL)
        
        # 查找搜索框并输入关键词
        search_box = self.driver.find_element(By.ID, self.SEARCH_BOX_ID)
        search_box.clear()
        search_box.send_keys(keyword)
        
        # 点击搜索按钮
        search_button = self.driver.find_element(By.ID, self.SEARCH_BUTTON_ID)
        search_button.click()
        
        # 等待页面加载
        time.sleep(self.WAIT_TIME)
        
        # 获取搜索结果
        result_elements = self.driver.find_elements(By.CSS_SELECTOR, self.RESULT_LINKS_SELECTOR)
        
        results = []
        for element in result_elements[:max_results]:
            try:
                title = element.text
                url = element.get_attribute("href")
                if title and url:
                    results.append({
                        "title": title,
                        "url": url
                    })
            except Exception as e:
                print(f"提取结果时出错: {e}")
        
        return results
    
    def close(self):
        """关闭浏览器并释放资源"""
        if self.driver:
            self.driver.quit()
            
    def __enter__(self):
        """支持使用with语句"""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开with代码块时自动关闭浏览器"""
        self.close()


def main():
    """主函数，用于演示使用方法"""
    # 获取浏览器类型
    print("支持的浏览器类型:")
    print("1. Chrome")
    print("2. Firefox")
    print("3. Edge")
    browser_choice = input("请选择浏览器类型 (默认: Firefox): ")
    
    if browser_choice == "1":
        browser_type = BaiduSearcher.BROWSER_CHROME
    elif browser_choice == "3":
        browser_type = BaiduSearcher.BROWSER_EDGE
    else:
        browser_type = BaiduSearcher.BROWSER_FIREFOX
    
    keyword = input("请输入要搜索的关键词: ")
    
    print(f"正在使用 {browser_type} 浏览器搜索 '{keyword}'...")
    
    # 使用with语句自动管理资源
    with BaiduSearcher(browser_type=browser_type, headless=False) as searcher:
        results = searcher.search(keyword)
        
        print(f"\n搜索 '{keyword}' 的结果:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   链接: {result['url']}")
            print()


if __name__ == "__main__":
    main() 