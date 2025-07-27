#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的使用示例
演示如何使用TableScraper类
"""

from web_scraper import TableScraper

def example_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    # 要爬取的网页URL（这里使用一个包含表格的示例网站）
    url = "https://www.w3schools.com/html/html_tables.asp"
    
    # 创建爬虫实例（不使用Selenium）
    scraper = TableScraper(use_selenium=False)
    
    try:
        # 爬取表格并保存为CSV
        success = scraper.scrape_table(
            url=url,
            output_format='csv',
            output_file='example_tables'
        )
        
        if success:
            print("✅ 爬取成功！请查看生成的CSV文件")
        else:
            print("❌ 爬取失败")
            
    finally:
        scraper.close()

def example_selenium_usage():
    """使用Selenium的示例"""
    print("\n=== Selenium使用示例 ===")
    
    # 动态内容网站示例
    url = "https://www.w3schools.com/html/html_tables.asp"
    
    # 创建爬虫实例（使用Selenium）
    scraper = TableScraper(use_selenium=True, headless=True)
    
    try:
        # 爬取表格并保存为Excel
        success = scraper.scrape_table(
            url=url,
            output_format='excel',
            output_file='selenium_tables'
        )
        
        if success:
            print("✅ Selenium爬取成功！请查看生成的Excel文件")
        else:
            print("❌ Selenium爬取失败")
            
    finally:
        scraper.close()

def example_custom_url():
    """让用户输入URL的示例"""
    print("\n=== 自定义URL示例 ===")
    
    url = input("请输入要爬取的网页URL: ").strip()
    
    if not url:
        print("未输入URL，使用默认示例URL")
        url = "https://www.w3schools.com/html/html_tables.asp"
    
    print(f"正在爬取: {url}")
    
    # 先尝试requests方式
    scraper = TableScraper(use_selenium=False)
    
    try:
        success = scraper.scrape_table(
            url=url,
            output_format='csv',
            output_file='custom_tables'
        )
        
        if not success:
            print("requests方式失败，尝试使用Selenium...")
            scraper.close()
            
            # 使用Selenium重试
            scraper = TableScraper(use_selenium=True, headless=True)
            success = scraper.scrape_table(
                url=url,
                output_format='csv',
                output_file='custom_tables_selenium'
            )
        
        if success:
            print("✅ 爬取成功！")
        else:
            print("❌ 两种方式都失败了")
            
    finally:
        scraper.close()

if __name__ == "__main__":
    print("🚀 网页表格爬虫示例程序")
    print("=" * 50)
    
    # 运行示例
    try:
        # 基本使用
        example_basic_usage()
        
        # Selenium使用（需要Chrome和ChromeDriver）
        # example_selenium_usage()
        
        # 自定义URL
        # example_custom_url()
        
    except KeyboardInterrupt:
        print("\n⏹️ 用户中断程序")
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
    
    print("\n🎉 示例程序结束")