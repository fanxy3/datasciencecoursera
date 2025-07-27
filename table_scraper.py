#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页表格爬虫工具
用于从网页中提取表格数据并保存为CSV文件
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import sys
import time
import random
from urllib.parse import urljoin, urlparse
import csv

class TableScraper:
    def __init__(self, url, headers=None, delay=1):
        """
        初始化爬虫
        
        Args:
            url (str): 目标网页URL
            headers (dict): 请求头
            delay (int): 请求间隔时间（秒）
        """
        self.url = url
        self.delay = delay
        
        # 设置默认请求头，模拟浏览器访问
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def fetch_page(self):
        """
        获取网页内容
        
        Returns:
            BeautifulSoup: 解析后的网页内容
        """
        try:
            print(f"正在获取网页: {self.url}")
            
            # 添加随机延迟，避免被反爬
            time.sleep(random.uniform(0.5, self.delay))
            
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            # 尝试检测编码
            response.encoding = response.apparent_encoding
            
            print(f"网页获取成功，状态码: {response.status_code}")
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.exceptions.RequestException as e:
            print(f"获取网页失败: {e}")
            return None
    
    def find_tables(self, soup):
        """
        查找网页中的所有表格
        
        Args:
            soup (BeautifulSoup): 网页解析对象
            
        Returns:
            list: 表格元素列表
        """
        tables = soup.find_all('table')
        print(f"发现 {len(tables)} 个表格")
        return tables
    
    def extract_table_data(self, table, table_index=0):
        """
        提取表格数据
        
        Args:
            table: 表格元素
            table_index (int): 表格索引
            
        Returns:
            list: 表格数据，每行为一个列表
        """
        data = []
        
        # 查找表头
        headers = []
        header_row = table.find('tr')
        if header_row:
            for th in header_row.find_all(['th', 'td']):
                headers.append(th.get_text(strip=True))
        
        # 如果没有找到表头，使用默认列名
        if not headers:
            # 通过第一行数据确定列数
            first_row = table.find('tr')
            if first_row:
                col_count = len(first_row.find_all(['td', 'th']))
                headers = [f'列{i+1}' for i in range(col_count)]
        
        data.append(headers)
        
        # 提取数据行
        rows = table.find_all('tr')[1:] if table.find_all('tr') else []
        
        for row in rows:
            cells = row.find_all(['td', 'th'])
            row_data = []
            
            for cell in cells:
                # 处理单元格内容，去除多余空白
                cell_text = cell.get_text(separator=' ', strip=True)
                # 处理换行符和多余空格
                cell_text = ' '.join(cell_text.split())
                row_data.append(cell_text)
            
            # 只添加非空行
            if any(cell.strip() for cell in row_data):
                data.append(row_data)
        
        print(f"表格 {table_index + 1}: 提取了 {len(data)-1} 行数据，{len(headers)} 列")
        return data
    
    def save_to_csv(self, data, filename):
        """
        将数据保存为CSV文件
        
        Args:
            data (list): 表格数据
            filename (str): 输出文件名
        """
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(data)
            print(f"数据已保存到: {filename}")
        except Exception as e:
            print(f"保存CSV文件失败: {e}")
    
    def save_to_excel(self, all_tables_data, filename):
        """
        将所有表格数据保存为Excel文件
        
        Args:
            all_tables_data (list): 所有表格的数据
            filename (str): 输出文件名
        """
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                for i, data in enumerate(all_tables_data):
                    if data:
                        df = pd.DataFrame(data[1:], columns=data[0])
                        sheet_name = f'表格{i+1}'
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"数据已保存到: {filename}")
        except Exception as e:
            print(f"保存Excel文件失败: {e}")
    
    def scrape(self, output_format='csv', output_file=None):
        """
        执行爬取任务
        
        Args:
            output_format (str): 输出格式 ('csv' 或 'excel')
            output_file (str): 输出文件名
        """
        # 获取网页内容
        soup = self.fetch_page()
        if not soup:
            return
        
        # 查找表格
        tables = self.find_tables(soup)
        if not tables:
            print("未发现任何表格")
            return
        
        # 提取所有表格数据
        all_tables_data = []
        for i, table in enumerate(tables):
            print(f"\n处理表格 {i + 1}...")
            data = self.extract_table_data(table, i)
            all_tables_data.append(data)
        
        # 保存数据
        if not output_file:
            domain = urlparse(self.url).netloc
            output_file = f"{domain}_tables"
        
        if output_format.lower() == 'excel':
            self.save_to_excel(all_tables_data, f"{output_file}.xlsx")
        else:
            # 如果只有一个表格，保存为单个CSV
            if len(all_tables_data) == 1:
                self.save_to_csv(all_tables_data[0], f"{output_file}.csv")
            else:
                # 多个表格，分别保存
                for i, data in enumerate(all_tables_data):
                    self.save_to_csv(data, f"{output_file}_table_{i+1}.csv")

def main():
    """
    主函数，处理命令行参数
    """
    parser = argparse.ArgumentParser(description='网页表格爬虫工具')
    parser.add_argument('url', help='目标网页URL')
    parser.add_argument('-o', '--output', help='输出文件名（不含扩展名）')
    parser.add_argument('-f', '--format', choices=['csv', 'excel'], default='csv',
                        help='输出格式 (默认: csv)')
    parser.add_argument('-d', '--delay', type=float, default=1.0,
                        help='请求延迟时间（秒，默认: 1.0）')
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    scraper = TableScraper(args.url, delay=args.delay)
    
    # 执行爬取
    scraper.scrape(output_format=args.format, output_file=args.output)

if __name__ == "__main__":
    main()