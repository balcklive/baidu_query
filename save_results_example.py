#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import os
from datetime import datetime
from baidu_search import BaiduSearcher

# 常量定义
RESULTS_DIR = "search_results"  # 结果保存目录
DEFAULT_KEYWORD = "Python教程"  # 默认搜索关键词
DEFAULT_MAX_RESULTS = 20  # 默认最大结果数

def save_to_json(results, keyword, filepath):
    """
    将搜索结果保存为JSON文件
    
    Args:
        results: 搜索结果列表
        keyword: 搜索关键词
        filepath: 保存路径
    """
    data = {
        "keyword": keyword,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到JSON文件: {filepath}")

def save_to_csv(results, keyword, filepath):
    """
    将搜索结果保存为CSV文件
    
    Args:
        results: 搜索结果列表
        keyword: 搜索关键词
        filepath: 保存路径
    """
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(["序号", "标题", "URL", "关键词", "搜索时间"])
        
        # 写入数据行
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for i, result in enumerate(results, 1):
            writer.writerow([
                i, 
                result['title'], 
                result['url'], 
                keyword,
                timestamp
            ])
    
    print(f"结果已保存到CSV文件: {filepath}")

def main():
    # 创建保存目录（如果不存在）
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
    
    # 获取用户输入的关键词，如果为空则使用默认值
    keyword = input(f"请输入要搜索的关键词 (默认: {DEFAULT_KEYWORD}): ")
    if not keyword:
        keyword = DEFAULT_KEYWORD
    
    # 获取最大结果数
    max_results_input = input(f"请输入要返回的最大结果数量 (默认: {DEFAULT_MAX_RESULTS}): ")
    max_results = int(max_results_input) if max_results_input.isdigit() else DEFAULT_MAX_RESULTS
    
    print(f"正在搜索 '{keyword}'，最多返回 {max_results} 条结果...")
    
    # 使用with语句自动管理资源
    with BaiduSearcher(headless=False) as searcher:
        results = searcher.search(keyword, max_results=max_results)
        
        if not results:
            print("未找到搜索结果。")
            return
        
        # 打印结果
        print(f"\n已找到 {len(results)} 条搜索结果:")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   链接: {result['url']}")
            print()
        
        # 生成文件名（使用关键词和时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"{keyword}_{timestamp}".replace(" ", "_")
        
        # 保存结果
        json_path = os.path.join(RESULTS_DIR, f"{filename_base}.json")
        csv_path = os.path.join(RESULTS_DIR, f"{filename_base}.csv")
        
        save_to_json(results, keyword, json_path)
        save_to_csv(results, keyword, csv_path)


if __name__ == "__main__":
    main() 