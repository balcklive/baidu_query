#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import csv
import time
from datetime import datetime
from baidu_search import BaiduSearcher

# 常量定义
RESULTS_DIR = "search_results"  # 结果保存目录
KEYWORDS_FILE = "keywords.txt"  # 关键词文件路径
DEFAULT_MAX_RESULTS = 10  # 每个关键词的默认最大结果数
DELAY_BETWEEN_SEARCHES = 3  # 每次搜索之间的延迟时间（秒）
CSV_OUTPUT = "batch_results.csv"  # CSV输出文件
JSON_OUTPUT = "batch_results.json"  # JSON输出文件

def load_keywords(filepath):
    """
    从文件加载关键词列表
    
    Args:
        filepath: 关键词文件路径
        
    Returns:
        关键词列表
    """
    # 如果文件不存在，创建一个示例文件
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("Python教程\n人工智能\n数据分析\n机器学习\n深度学习")
        print(f"已创建示例关键词文件: {filepath}")
    
    # 读取关键词
    with open(filepath, 'r', encoding='utf-8') as f:
        keywords = [line.strip() for line in f if line.strip()]
    
    return keywords

def save_all_to_csv(all_results, filepath):
    """
    将所有搜索结果保存到一个CSV文件
    
    Args:
        all_results: 所有关键词的搜索结果
        filepath: 保存路径
    """
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(["关键词", "序号", "标题", "URL", "搜索时间"])
        
        # 写入数据行
        for keyword, results in all_results.items():
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for i, result in enumerate(results, 1):
                writer.writerow([
                    keyword,
                    i, 
                    result['title'], 
                    result['url'],
                    timestamp
                ])
    
    print(f"所有结果已保存到CSV文件: {filepath}")

def save_all_to_json(all_results, filepath):
    """
    将所有搜索结果保存到一个JSON文件
    
    Args:
        all_results: 所有关键词的搜索结果
        filepath: 保存路径
    """
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "keywords": {}
    }
    
    for keyword, results in all_results.items():
        data["keywords"][keyword] = results
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"所有结果已保存到JSON文件: {filepath}")

def get_browser_type():
    """获取用户选择的浏览器类型"""
    print("支持的浏览器类型:")
    print("1. Chrome")
    print("2. Firefox (推荐)")
    print("3. Edge")
    browser_choice = input("请选择浏览器类型 (默认: Firefox): ")
    
    if browser_choice == "1":
        return BaiduSearcher.BROWSER_CHROME
    elif browser_choice == "3":
        return BaiduSearcher.BROWSER_EDGE
    else:
        return BaiduSearcher.BROWSER_FIREFOX

def main():
    # 创建保存目录（如果不存在）
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    
    # 获取浏览器类型
    browser_type = get_browser_type()
    
    # 加载关键词
    keywords = load_keywords(KEYWORDS_FILE)
    print(f"已加载 {len(keywords)} 个关键词: {', '.join(keywords)}")
    
    # 获取最大结果数
    max_results_input = input(f"请输入每个关键词要返回的最大结果数量 (默认: {DEFAULT_MAX_RESULTS}): ")
    max_results = int(max_results_input) if max_results_input.isdigit() else DEFAULT_MAX_RESULTS
    
    # 是否使用无头模式
    headless_input = input("是否使用无头模式（不显示浏览器窗口）? (y/n, 默认: y): ")
    headless = headless_input.lower() != 'n'
    
    print(f"开始批量搜索 {len(keywords)} 个关键词，每个关键词最多返回 {max_results} 条结果...")
    print(f"使用 {browser_type} 浏览器，{'使用' if headless else '不使用'}无头模式")
    
    all_results = {}
    
    # 使用with语句自动管理资源
    with BaiduSearcher(browser_type=browser_type, headless=headless) as searcher:
        for i, keyword in enumerate(keywords, 1):
            print(f"\n[{i}/{len(keywords)}] 正在搜索 '{keyword}'...")
            
            try:
                results = searcher.search(keyword, max_results=max_results)
                all_results[keyword] = results
                
                print(f"  已找到 {len(results)} 条搜索结果")
                
                # 每个关键词单独保存
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename_base = f"{keyword}_{timestamp}".replace(" ", "_")
                
                # 保存到单独的JSON文件
                json_path = os.path.join(RESULTS_DIR, f"{filename_base}.json")
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "keyword": keyword,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "results": results
                    }, f, ensure_ascii=False, indent=2)
                
                # 防止请求过于频繁
                if i < len(keywords):
                    print(f"  等待 {DELAY_BETWEEN_SEARCHES} 秒后继续...")
                    time.sleep(DELAY_BETWEEN_SEARCHES)
                
            except Exception as e:
                print(f"  搜索 '{keyword}' 时出错: {e}")
    
    # 保存所有结果
    if all_results:
        # 保存到CSV文件
        csv_path = os.path.join(RESULTS_DIR, CSV_OUTPUT)
        save_all_to_csv(all_results, csv_path)
        
        # 保存到JSON文件
        json_path = os.path.join(RESULTS_DIR, JSON_OUTPUT)
        save_all_to_json(all_results, json_path)
        
        print(f"\n批量搜索完成，共处理 {len(keywords)} 个关键词，结果已保存到 {RESULTS_DIR} 目录")
    else:
        print("\n批量搜索未返回任何结果")


if __name__ == "__main__":
    main() 