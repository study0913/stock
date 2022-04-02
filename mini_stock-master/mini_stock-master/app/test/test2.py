from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import re

# option = ChromeOptions()
# option.add_argument("--headless")
# option.add_argument("--no-sandbox")
#
# browser = Chrome(options=option)
#
# # 请求头
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
# url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/000725.phtml'
# browser.get(url)
#
# htmlData = browser.page_source
# print(htmlData)

#   保存为文件
# fileOb = open('result.html', 'w', encoding='utf-8')  # 打开一个文件，没有就新建一个
# fileOb.write(htmlData)
# fileOb.close()

#  读取本地文件
fileOb = open(r'result.html', 'r', encoding='utf-8')
htmlData = fileOb.read()
fileOb.close()
# print(htmlData)
# 7、用soup解析文 件
soup = BeautifulSoup(htmlData, 'lxml')

trs = soup.find('table', id='comInfo1').find_all('tr')
comInfo = []
for tr in trs:  # 循环所有行
    for td in tr.find_all('td')[1:2]:  # 在行中查找第2列，第3列的值
        comInfo.append(td.getText())
    for td in tr.find_all('td')[3:4]:  # 在行中查找第2列，第3列的值
        comInfo.append(td.getText())

# print(comInfo)  # 打印值

current_price = soup.select('#price')[0].getText()
# print(current_price)

hq = soup.select('#hq')[0].getText().replace('\n', '').replace('\r', '').replace('：', '')
# print(hq)
patten = r"总市值(\d+\.\d+)亿.*?市盈率TTM(\d+\.\d+)"
res = re.search(patten, hq)
if res:
    total_value = float(res.group(1))*1000000000
    pe_ratio = res.group(2)

# 构建字典
reg = re.search(r"(\d+)万元", comInfo[7])
# print(reg)
reg_capital = int(reg.group(1))*10000

stock = {'stock_name': comInfo[0],
         'stock_type': comInfo[2],
         'issue_price': comInfo[4],
         'reg_capital': reg_capital,
         'address': comInfo[21],
         'company_brief': comInfo[23],
         'total_value': total_value,
         'pe_ratio': pe_ratio,
         'current_price': current_price
         }

print(stock)
