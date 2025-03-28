# 百度搜索爬虫工具

这是一个简单的Python工具，使用Selenium和浏览器自动化在百度上搜索关键词并获取搜索结果。

## 功能特点

- 在百度搜索指定关键词
- 提取搜索结果的标题和链接
- 支持有头/无头模式运行
- 使用上下文管理器自动管理浏览器资源
- **支持多种浏览器**：Chrome、Firefox、Edge

## 安装要求

1. Python 3.6+
2. 至少安装以下浏览器之一:
   - Google Chrome
   - Mozilla Firefox (推荐)
   - Microsoft Edge
3. 以下Python包（可通过requirements.txt安装）:
   - selenium
   - webdriver-manager

## 安装步骤

1. 克隆或下载本仓库
2. 安装依赖包:

```bash
pip install -r requirements.txt
```

## 使用方法

直接运行脚本:

```bash
python baidu_search.py
```

程序会提示选择浏览器类型，然后输入要搜索的关键词，自动打开相应浏览器，在百度上搜索该关键词，并返回搜索结果的标题和链接。

## 在代码中使用

```python
from baidu_search import BaiduSearcher

# 创建搜索器实例
# browser_type可以是"chrome"、"firefox"或"edge"
# headless=True表示无头模式（不显示浏览器窗口）
with BaiduSearcher(browser_type="firefox", headless=True) as searcher:
    # 搜索"Python教程"并获取结果
    results = searcher.search("Python教程")
    
    # 处理结果
    for result in results:
        print(f"标题: {result['title']}")
        print(f"链接: {result['url']}")
```

## 注意事项

- 确保安装了至少一种支持的浏览器
- 如果Chrome浏览器初始化失败，程序会自动尝试使用Firefox，然后是Edge
- 网络连接可能会影响搜索结果
- 百度页面结构变化可能导致选择器失效，需要相应更新 