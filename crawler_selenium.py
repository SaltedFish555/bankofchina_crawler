from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


import requests
from bs4 import BeautifulSoup
import json
import sys



re_type=requests.get('https://www.11meigui.com/tools/currency')
soup_type=BeautifulSoup(re_type.text,'html.parser')
tbodys=soup_type.find_all('tbody')[1:] # 第0个是冗余的欧洲信息，删去
type_dict={}
for tbody in tbodys:
    trs=tbody.find_all('tr')[2:] 
    for tr in trs:
        tds=tr.find_all('td')
        k=tds[4].text.strip()
        v=tds[1].text.strip()
        type_dict[k]=v
        
        
# with open('type.json','w') as f: # 可以存为json文件，以后就可以直接读文件了
#     json.dump(type_dict,f,ensure_ascii=False,indent=2)




if len(sys.argv) != 3:
    print("输入有误")
    sys.exit(1)

date_info=sys.argv[1]
date=f'{date_info[:4]}-{date_info[4:6]}-{date_info[6:8]}' # 修改日期字符串的格式

type_date_info=sys.argv[2]
type=type_dict[type_date_info] # 把货币代号转化为货币名





driver=webdriver.Edge()
driver.get("https://www.boc.cn/sourcedb/whpj/")

erectDate=driver.find_element(By.NAME,'erectDate')
erectDate.send_keys("2021-12-30")

nothing=driver.find_element(By.NAME,'nothing')
nothing.send_keys("2021-12-30")


pjname=driver.find_element(By.NAME,'pjname')
# 模拟点击这个下拉框，让其可见
actions = ActionChains(driver)
actions.move_to_element(pjname)
actions.click()
actions.perform()

# 获取所有选项
options=pjname.find_elements(By.TAG_NAME,'option')

# 将获取选项下标与文本之间的映射字典
options_dict={}
for i,option in enumerate(options):
    options_dict[option.text]=i

# 使用 Select 类选择选项
select = Select(pjname)
select.select_by_index(options_dict['美元'])

# 找到按钮元素
search_button = driver.find_element(By.XPATH, '//input[@class="search_btn" and @style="float:right;margin-righth:26px;" and @type="button" and @onclick="executeSearch()"]')
# 模拟点击按钮
search_button.click()

html=driver.page_source
# print(html)

sleep(1) # 等待一秒保证页面跳转完成







soup=BeautifulSoup(html,"html.parser")

# 找到价格表
table=soup.find('table',{'cellpadding': '0', 'align': 'left', 'cellspacing': '0', 'width': '100%'})
tr=table.find_all('tr')[1] # 第0个tr是表头，后面的才是这一天内各个时间点发布的价位,这里取第1个
td=tr.find_all('td')[1] # 类似地，第0个是表头(货币名)，后面的才是价位，这里取第1个

print(td.text.strip())

