#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class BaiduSearcher:
    """百度搜索类，用于搜索特定关键词并返回搜索结果链接"""
    
    # 常量定义
    BAIDU_URL = "https://www.baidu.com"
    SEARCH_BOX_ID = "kw"
    SEARCH_BUTTON_ID = "su"
    RESULT_LINKS_SELECTOR = "#content_left .result a"
    WAIT_TIME = 2  # 等待页面加载的时间（秒）
    MAX_RESULTS = 10  # 默认返回的最大结果数量
    
    def __init__(self, headless=False):
        """
        初始化搜索器
        
        Args:
            headless: 是否使用无头模式（不显示浏览器界面）
        """
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
            
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
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
    keyword = input("请输入要搜索的关键词: ")
    
    print(f"正在搜索 '{keyword}'...")
    
    # 使用with语句自动管理资源
    with BaiduSearcher(headless=False) as searcher:
        results = searcher.search(keyword)
        
        print(f"\n搜索 '{keyword}' 的结果:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   链接: {result['url']}")
            print()


if __name__ == "__main__":
    main() 