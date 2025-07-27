#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版网页表格爬虫
快速从网页提取表格数据
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys

def scrape_tables(url, output_file="scraped_tables.csv"):
    """
    简化版表格爬取函数
    
    Args:
        url (str): 目标网页URL
        output_file (str): 输出CSV文件名
    """
    
    # 设置请求头，模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"正在获取网页: {url}")
        
        # 发送HTTP请求
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        # 解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有表格
        tables = soup.find_all('table')
        print(f"发现 {len(tables)} 个表格")
        
        if not tables:
            print("未发现任何表格")
            return
        
        # 提取第一个表格的数据（通常是主要表格）
        table = tables[0]
        data = []
        
        # 提取所有行
        rows = table.find_all('tr')
        
        for row in rows:
            # 提取单元格数据
            cells = row.find_all(['td', 'th'])
            row_data = []
            
            for cell in cells:
                # 获取单元格文本，去除多余空白
                cell_text = cell.get_text(strip=True)
                cell_text = ' '.join(cell_text.split())  # 处理换行和多余空格
                row_data.append(cell_text)
            
            # 添加非空行
            if row_data and any(cell.strip() for cell in row_data):
                data.append(row_data)
        
        # 保存为CSV文件
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        
        print(f"成功提取 {len(data)} 行数据")
        print(f"数据已保存到: {output_file}")
        
        # 显示前几行数据预览
        print("\n数据预览（前5行）:")
        for i, row in enumerate(data[:5]):
            print(f"第{i+1}行: {row}")
            
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except Exception as e:
        print(f"处理过程中出错: {e}")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法: python3 simple_table_scraper.py <网页URL> [输出文件名]")
        print("示例: python3 simple_table_scraper.py 'https://example.com/table-page' 'my_data.csv'")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "scraped_tables.csv"
    
    scrape_tables(url, output_file)

if __name__ == "__main__":
    main()