#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页表格爬虫工具
用于从网页中提取表格数据并保存为CSV文件
支持多种表格格式和动态内容
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import sys
import argparse
import time
import random
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class TableScraper:
    def __init__(self, use_selenium=False, headless=True):
        """
        初始化爬虫
        :param use_selenium: 是否使用Selenium（用于动态内容）
        :param headless: 是否使用无头浏览器
        """
        self.use_selenium = use_selenium
        self.driver = None
        
        # 设置请求头，模拟真实浏览器
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        if self.use_selenium:
            self._setup_selenium(headless)
    
    def _setup_selenium(self, headless=True):
        """设置Selenium WebDriver"""
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(f'--user-agent={self.headers["User-Agent"]}')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
            print("✅ Selenium WebDriver 初始化成功")
        except Exception as e:
            print(f"❌ Selenium 初始化失败: {e}")
            print("请确保已安装 Chrome 浏览器和 chromedriver")
            sys.exit(1)
    
    def scrape_with_requests(self, url):
        """使用requests库爬取静态表格"""
        try:
            print(f"🔍 正在使用 requests 爬取: {url}")
            
            # 添加随机延迟，避免被反爬
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tables = soup.find_all('table')
            
            if not tables:
                print("❌ 未找到表格元素")
                return []
            
            print(f"✅ 找到 {len(tables)} 个表格")
            return self._parse_tables(tables)
            
        except requests.RequestException as e:
            print(f"❌ 请求失败: {e}")
            return []
        except Exception as e:
            print(f"❌ 解析失败: {e}")
            return []
    
    def scrape_with_selenium(self, url, wait_time=10):
        """使用Selenium爬取动态表格"""
        try:
            print(f"🔍 正在使用 Selenium 爬取: {url}")
            
            self.driver.get(url)
            
            # 等待页面加载完成
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            
            # 获取页面源码
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            tables = soup.find_all('table')
            
            if not tables:
                print("❌ 未找到表格元素")
                return []
            
            print(f"✅ 找到 {len(tables)} 个表格")
            return self._parse_tables(tables)
            
        except TimeoutException:
            print("❌ 页面加载超时，未找到表格")
            return []
        except Exception as e:
            print(f"❌ Selenium 爬取失败: {e}")
            return []
    
    def _parse_tables(self, tables):
        """解析表格数据"""
        all_tables_data = []
        
        for i, table in enumerate(tables):
            print(f"📊 正在解析第 {i+1} 个表格...")
            
            table_data = []
            
            # 查找表头
            headers = []
            header_row = table.find('tr')
            if header_row:
                header_cells = header_row.find_all(['th', 'td'])
                headers = [cell.get_text(strip=True) for cell in header_cells]
            
            # 查找所有行
            rows = table.find_all('tr')
            for row_idx, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                if cells:
                    row_data = []
                    for cell in cells:
                        # 提取单元格文本，处理嵌套标签
                        text = cell.get_text(separator=' ', strip=True)
                        row_data.append(text)
                    
                    if row_data:  # 只添加非空行
                        table_data.append(row_data)
            
            if table_data:
                # 如果没有明确的表头，使用第一行作为表头
                if not headers and table_data:
                    headers = [f"列{j+1}" for j in range(len(table_data[0]))]
                
                all_tables_data.append({
                    'table_index': i + 1,
                    'headers': headers,
                    'data': table_data
                })
                print(f"✅ 表格 {i+1} 解析完成，共 {len(table_data)} 行数据")
            else:
                print(f"⚠️ 表格 {i+1} 无数据")
        
        return all_tables_data
    
    def save_to_csv(self, tables_data, base_filename="scraped_table"):
        """保存表格数据到CSV文件"""
        if not tables_data:
            print("❌ 没有数据可保存")
            return
        
        for table_info in tables_data:
            filename = f"{base_filename}_{table_info['table_index']}.csv"
            
            try:
                with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # 写入表头
                    if table_info['headers']:
                        writer.writerow(table_info['headers'])
                    
                    # 写入数据
                    writer.writerows(table_info['data'])
                
                print(f"💾 表格 {table_info['table_index']} 已保存到: {filename}")
                
            except Exception as e:
                print(f"❌ 保存文件失败: {e}")
    
    def save_to_excel(self, tables_data, filename="scraped_tables.xlsx"):
        """保存所有表格到Excel文件（多个sheet）"""
        if not tables_data:
            print("❌ 没有数据可保存")
            return
        
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for table_info in tables_data:
                    sheet_name = f"表格{table_info['table_index']}"
                    
                    # 创建DataFrame
                    if table_info['headers']:
                        df = pd.DataFrame(table_info['data'], columns=table_info['headers'])
                    else:
                        df = pd.DataFrame(table_info['data'])
                    
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            print(f"💾 所有表格已保存到: {filename}")
            
        except Exception as e:
            print(f"❌ 保存Excel文件失败: {e}")
    
    def scrape_table(self, url, output_format='csv', output_file=None):
        """主要的爬取方法"""
        print(f"🚀 开始爬取表格数据...")
        print(f"🔗 目标网址: {url}")
        
        # 首先尝试使用requests
        tables_data = self.scrape_with_requests(url)
        
        # 如果requests失败且启用了Selenium，则使用Selenium
        if not tables_data and self.use_selenium:
            print("🔄 requests方式未获取到数据，尝试使用Selenium...")
            tables_data = self.scrape_with_selenium(url)
        
        if not tables_data:
            print("❌ 未能获取到任何表格数据")
            return False
        
        # 保存数据
        if output_file is None:
            output_file = "scraped_table"
        
        if output_format.lower() == 'excel':
            self.save_to_excel(tables_data, f"{output_file}.xlsx")
        else:
            self.save_to_csv(tables_data, output_file)
        
        return True
    
    def close(self):
        """关闭WebDriver"""
        if self.driver:
            self.driver.quit()


def main():
    parser = argparse.ArgumentParser(description='网页表格爬虫工具')
    parser.add_argument('url', help='要爬取的网页URL')
    parser.add_argument('-s', '--selenium', action='store_true', 
                       help='使用Selenium爬取动态内容')
    parser.add_argument('-o', '--output', default='scraped_table',
                       help='输出文件名前缀（默认：scraped_table）')
    parser.add_argument('-f', '--format', choices=['csv', 'excel'], 
                       default='csv', help='输出格式（默认：csv）')
    parser.add_argument('--headless', action='store_false', 
                       help='使用有头浏览器（仅在使用Selenium时有效）')
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    scraper = TableScraper(use_selenium=args.selenium, headless=args.headless)
    
    try:
        # 执行爬取
        success = scraper.scrape_table(
            url=args.url,
            output_format=args.format,
            output_file=args.output
        )
        
        if success:
            print("🎉 表格爬取完成！")
        else:
            print("❌ 表格爬取失败")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断操作")
    except Exception as e:
        print(f"❌ 程序执行错误: {e}")
    finally:
        scraper.close()


if __name__ == "__main__":
    # 示例用法
    if len(sys.argv) == 1:
        print("📖 网页表格爬虫工具使用示例：")
        print("python web_scraper.py https://example.com/page-with-tables")
        print("python web_scraper.py https://example.com -s -f excel -o my_tables")
        print("\n参数说明：")
        print("-s, --selenium    使用Selenium爬取动态内容")
        print("-o, --output      指定输出文件名")
        print("-f, --format      指定输出格式（csv或excel）")
        print("--headless        显示浏览器窗口（仅Selenium模式）")
        sys.exit(0)
    
    main()