# 网页表格爬虫工具

一个功能强大的Python工具，用于从网页中提取表格数据并保存为CSV或Excel文件。支持静态和动态网页内容。

## 功能特性

- 🔍 **智能表格检测**: 自动识别网页中的所有表格
- 📊 **多格式输出**: 支持CSV和Excel格式
- 🚀 **双重爬取模式**: 
  - `requests + BeautifulSoup`: 适用于静态表格（快速）
  - `Selenium`: 适用于动态加载的表格
- 🛡️ **反爬虫保护**: 模拟真实浏览器行为
- 📝 **智能编码**: 自动处理中文字符编码
- ⚡ **错误恢复**: 自动重试和降级处理

## 安装依赖

### 1. 安装Python包

```bash
pip install -r requirements.txt
```

### 2. 安装Chrome浏览器和ChromeDriver（仅在使用Selenium时需要）

**在Mac上安装：**

```bash
# 安装Chrome浏览器
brew install --cask google-chrome

# 安装ChromeDriver
brew install chromedriver
```

**或者手动安装：**
1. 下载 [Chrome浏览器](https://www.google.com/chrome/)
2. 下载对应版本的 [ChromeDriver](https://chromedriver.chromium.org/)
3. 将ChromeDriver添加到系统PATH中

## 使用方法

### 基本用法

```bash
# 爬取静态表格（推荐先尝试此方法）
python web_scraper.py https://example.com/page-with-tables

# 爬取动态表格（使用Selenium）
python web_scraper.py https://example.com -s

# 保存为Excel格式
python web_scraper.py https://example.com -f excel

# 自定义输出文件名
python web_scraper.py https://example.com -o my_data
```

### 高级用法

```bash
# 完整参数示例
python web_scraper.py https://example.com \
    --selenium \
    --format excel \
    --output company_data \
    --headless

# 查看帮助
python web_scraper.py -h
```

### 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `url` | - | 要爬取的网页URL（必需） | - |
| `--selenium` | `-s` | 使用Selenium爬取动态内容 | False |
| `--output` | `-o` | 输出文件名前缀 | scraped_table |
| `--format` | `-f` | 输出格式（csv/excel） | csv |
| `--headless` | - | 显示浏览器窗口（仅Selenium） | True |

## 代码示例

### 简单使用

```python
from web_scraper import TableScraper

# 创建爬虫实例
scraper = TableScraper()

# 爬取表格
success = scraper.scrape_table("https://example.com")

# 清理资源
scraper.close()
```

### 高级使用

```python
from web_scraper import TableScraper

# 使用Selenium模式
scraper = TableScraper(use_selenium=True, headless=True)

try:
    # 爬取并保存为Excel
    success = scraper.scrape_table(
        url="https://example.com",
        output_format="excel",
        output_file="my_tables"
    )
    
    if success:
        print("爬取成功！")
    else:
        print("爬取失败")
        
finally:
    scraper.close()
```

## 输出文件说明

### CSV格式
- 每个表格保存为单独的CSV文件
- 文件命名格式：`{filename}_{table_index}.csv`
- 使用UTF-8编码，支持中文

### Excel格式
- 所有表格保存在一个Excel文件中
- 每个表格作为单独的工作表
- 工作表命名：`表格1`、`表格2`等

## 常见问题

### Q: 为什么爬取失败？
A: 可能的原因：
1. 网站有反爬虫保护 → 尝试使用 `-s` 参数
2. 表格是动态加载的 → 使用Selenium模式
3. 网络连接问题 → 检查网络连接

### Q: 如何处理需要登录的网站？
A: 可以修改代码中的headers或使用Selenium手动登录后再爬取。

### Q: 表格数据不完整怎么办？
A: 
1. 尝试使用Selenium模式（`-s`参数）
2. 增加等待时间
3. 检查是否需要滚动页面加载更多内容

### Q: ChromeDriver版本不匹配怎么办？
A: 确保ChromeDriver版本与Chrome浏览器版本匹配，或使用以下命令更新：
```bash
brew upgrade chromedriver
```

## 技术细节

### 支持的表格类型
- 标准HTML `<table>` 元素
- 带有 `<thead>`、`<tbody>`、`<tfoot>` 的表格
- 使用 `<th>` 和 `<td>` 的表格
- 动态生成的表格（需要Selenium）

### 字符编码处理
- 自动检测网页编码
- 输出文件使用UTF-8编码
- CSV文件包含BOM标记，确保Excel正确显示中文

### 错误处理
- 网络超时自动重试
- 优雅的错误降级（requests → Selenium）
- 详细的错误信息输出

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
