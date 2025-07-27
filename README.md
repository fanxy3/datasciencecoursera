# 网页表格爬虫工具

这是一个用于从网页中提取表格数据的Python爬虫工具，支持保存为CSV或Excel格式。

## 功能特点

- 自动识别网页中的所有表格
- 智能处理表头和数据行
- 支持中文字符处理
- 模拟浏览器访问，避免反爬机制
- 支持CSV和Excel输出格式
- 可配置请求延迟和自定义请求头

## 安装依赖

在Mac终端中运行以下命令安装依赖：

```bash
# 安装Python包管理工具pip（如果未安装）
# 通常Mac自带Python和pip

# 安装项目依赖
pip3 install -r requirements.txt

# 或者单独安装各个包
pip3 install requests beautifulsoup4 pandas openpyxl lxml
```

## 使用方法

### 基本用法

```bash
# 爬取网页表格并保存为CSV
python3 table_scraper.py "https://example.com/page-with-tables"

# 指定输出文件名
python3 table_scraper.py "https://example.com/page-with-tables" -o "my_data"

# 保存为Excel格式
python3 table_scraper.py "https://example.com/page-with-tables" -f excel

# 设置请求延迟（避免被网站封IP）
python3 table_scraper.py "https://example.com/page-with-tables" -d 2.0
```

### 命令行参数

- `url`: 目标网页URL（必需）
- `-o, --output`: 输出文件名（不含扩展名）
- `-f, --format`: 输出格式，可选 `csv` 或 `excel`（默认：csv）
- `-d, --delay`: 请求延迟时间（秒，默认：1.0）

### 使用示例

```bash
# 示例1：爬取维基百科表格
python3 table_scraper.py "https://en.wikipedia.org/wiki/List_of_countries_by_population" -o "population_data" -f excel

# 示例2：爬取股票数据表格
python3 table_scraper.py "https://finance.yahoo.com" -o "stock_data" -d 2.0
```

## 代码功能说明

### 主要类和方法

- `TableScraper`: 主要的爬虫类
  - `fetch_page()`: 获取网页内容
  - `find_tables()`: 查找页面中的所有表格
  - `extract_table_data()`: 提取表格数据
  - `save_to_csv()`: 保存为CSV格式
  - `save_to_excel()`: 保存为Excel格式

### 特性

1. **智能表头处理**: 自动识别`<th>`标签作为表头，如果没有则使用第一行数据
2. **编码处理**: 自动检测网页编码，正确处理中文字符
3. **反爬策略**: 使用真实浏览器User-Agent，支持随机延迟
4. **数据清理**: 自动去除多余空白字符和换行符
5. **多表格支持**: 可以处理一个页面中的多个表格

## 注意事项

1. **遵守网站条款**: 使用前请确保遵守目标网站的robots.txt和使用条款
2. **请求频率**: 建议设置适当的延迟时间，避免对目标服务器造成压力
3. **动态内容**: 此工具仅能处理静态HTML表格，对于JavaScript动态生成的表格可能无效
4. **网络环境**: 某些网站可能需要代理或特殊配置才能访问

## 依赖包说明

- `requests`: HTTP请求库
- `beautifulsoup4`: HTML解析库
- `pandas`: 数据处理库
- `openpyxl`: Excel文件处理库
- `lxml`: XML/HTML解析器（BeautifulSoup的后端）

## 故障排除

如果遇到问题，可以尝试：

1. 检查网络连接
2. 增加请求延迟时间
3. 检查目标网站是否有反爬机制
4. 查看终端输出的错误信息

## 许可证

此工具仅供学习和研究使用，请遵守相关法律法规和网站使用条款。
