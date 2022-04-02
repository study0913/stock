from urllib import request, parse
from bs4 import BeautifulSoup

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/000725.phtml'
requests = request.Request(url=url, headers=headers)
response = request.urlopen(requests)

htmlData = response.read().decode('gbk', 'ignore')
# print(htmlData)
#   保存为文件
# fileOb = open('result.html', 'w', encoding='utf-8')  # 打开一个文件，没有就新建一个
# fileOb.write(htmlData)
# fileOb.close()

# 7、用soup解析文 件
soup = BeautifulSoup(htmlData, 'lxml')
# soup.prettify()
# print(soup.title)
# print(soup.title.name)
# print(soup.title.parent.name)
# print(soup.p.attrs)
# print(soup.title.string)

# name = soup.find_all('table')
# print(name[3])


trs = soup.find('table', id='comInfo1').find_all('tr')
for tr in trs:  # 循环所有行
    for td in tr.find_all('td')[0:2]:  # 在行中查找第2列，第3列的值
        print(td.getText())  # 打印值
