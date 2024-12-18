from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# 设置 Chrome 浏览器选项
chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')

# 启动浏览器
service = Service(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)
url = "https://ce.fudan.edu.cn"
driver.get(url)

# 等待页面完全加载
time.sleep(5)

try:
    # 等待登录按钮出现并点击
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#idcheckloginbtn"))
    )
    print("找到登录按钮")
    login_button.click()
    print("点击了登录按钮")
    
    # 等待链接所在的按钮出现并点击
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "body > div.nav > div > div.navRollInfo > div > div:nth-child(3)"))
    )
    print("找到指定按钮")
    button.click()
    print("点击了按钮")
    
    # 使用显式等待，等待表格加载
    try:
        print("当前页面URL:", driver.current_url)
        
        # 检查是否有iframe
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"找到 {len(iframes)} 个iframe")
        
        # 切换到第一个iframe
        target_iframe = iframes[0]
        driver.switch_to.frame(target_iframe)
        print("成功切换到目标iframe")
                
        page_num = 1
        all_data = []  # 存储所有页面的数据
        headers = None  # 存储表头
        
        while True:  # 循环处理每一页
            print(f"\n正在处理第 {page_num} 页...")
            # 等待页面加载完成
            time.sleep(20)
            
            # 尝试查找表格
            tables = driver.find_elements(By.TAG_NAME, "table")
            if not tables:
                print("未找到表格，可能已经是最后一页")
                break
            
            table = tables[0]  # 使用第一个表格
            print("找到表格")
            
            # 获取表头数据（只在第一页获取）
            if headers is None:
                headers = []
                header_row = table.find_element(By.TAG_NAME, "tr")
                header_cells = header_row.find_elements(By.TAG_NAME, "td")
                for cell in header_cells:
                    header_text = cell.text.strip()
                    if header_text:  # 只添加非空的表头
                        headers.append(header_text)
                print(f"找到表头: {headers}")
                
                if not headers:
                    print("未找到有效的表头，可能已经是最后一页")
                    break
            
            # 获取表格数据行
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # 跳过第一行（表头）
            print(f"找到 {len(rows)} 行数据")
            
            # 提取数据并去重
            page_data_dict = {}  # 使用字典来去重
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                row_data = []
                for col in cols:
                    cell_text = col.text.strip()
                    if '查看详情' in cell_text:
                        cell_text = '查看详情'
                    row_data.append(cell_text)
                
                if any(row_data) and len(row_data) == len(headers):
                    key = (row_data[0], row_data[1], row_data[6])
                    if key not in page_data_dict:
                        page_data_dict[key] = row_data
            
            # 将当前页的数据添加到总数据中
            all_data.extend(page_data_dict.values())
            
            # 保存当前页数据（如果需要）
            filename = f'data_2023/output_page_{page_num}.csv'
            with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  # 写入表头
                writer.writerows(page_data_dict.values())  # 写入数据
            print(f"第 {page_num} 页数据已保存到 {filename}")
            
            # 尝试点击下一页
            try:
                if page_num == 1:  # 第一页
                    # 查找所有页码链接
                    page_links = driver.find_elements(By.CSS_SELECTOR, "div.turn.pager.blue a")
                    for link in page_links:
                        if link.text.strip() == "2":  # 找到第2页的链接
                            link.click()
                            print("点击第2页")
                            page_num += 1
                            time.sleep(5)  # 等待页面加载
                            break
                else:  # 第二页及以后
                    # 查找所有页码链接
                    page_links = driver.find_elements(By.CSS_SELECTOR, "div.turn.pager.blue a")
                    next_page_num = str(page_num + 1)
                    for link in page_links:
                        if link.text.strip() == next_page_num:
                            link.click()
                            print(f"点击第{next_page_num}页")
                            page_num += 1
                            time.sleep(5)  # 等待页面加载
                            break
                    else:  # 如果没有找到下一页按钮
                        print("没有下一页了")
                        break
            except Exception as e:
                print(f"点击下一页时出错: {str(e)}")
                print("可能已经是最后一页")
                break
        
        # 所有页面处理完毕后，合并数据并去重
        if all_data:
            # 使用字典去重
            final_data_dict = {}
            for row in all_data:
                key = (row[0], row[1], row[6])  # 使用学期、选课序号和任课教师作为键
                if key not in final_data_dict:
                    final_data_dict[key] = row
            
            # 转换为列表并排序
            sorted_data = sorted(final_data_dict.values(), key=lambda x: (x[0], x[1], x[6]))
            
            # 保存最终的合并数据
            with open('output_all.csv', 'w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  # 写入表头
                writer.writerows(sorted_data)  # 写入所有数据
            print("\n所有数据已合并保存到 output_all.csv")
            print(f"总共处理了 {page_num} 页，��并后共有 {len(sorted_data)} 条记录")

    except Exception as e:
        print(f"发生错误: {str(e)}")
        print("\n调试信息:")
        print("当前URL:", driver.current_url)
        print("页面源码预览:", driver.page_source[:500])

except Exception as e:
    print(f"发生错误: {str(e)}")
    print("当前页面 URL:", driver.current_url)
    print("页面源代码:", driver.page_source[:500])  # 打印前500个字符的页面源代码
finally:
    driver.quit()