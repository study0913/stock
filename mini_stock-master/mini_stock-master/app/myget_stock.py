from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
import re
import efinance as ef
import numpy as np


# 从新浪网站获取股票基本信息
def get_stock_info(stock_code):
    option = ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--no-sandbox")
    # 可能需要手动添加路径
    browser = Chrome("chromedriver.exe")
    #browser = Chrome(options=option)
    #
    # # 请求头
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'}
    url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_CorpInfo/stockid/' + stock_code + '.phtml'
    browser.get(url)

    html_data = browser.page_source
    # print(html_data)

    soup = BeautifulSoup(html_data, 'lxml')

    trs = soup.find('table', id='comInfo1').find_all('tr')
    #  解析表格，将值一栏构成一个列表
    com_info = []
    for tr in trs:  # 循环所有行
        for td in tr.find_all('td')[1:2]:  # 在行中查找第2列，第3列的值
            com_info.append(td.getText())
        for td in tr.find_all('td')[3:4]:  # 在行中查找第2列，第3列的值
            com_info.append(td.getText())

    # print(comInfo)  # 打印值

    current_price = soup.select('#price')[0].getText()

    stock_name = soup.select('#stockName')[0].getText()
    stock_name = re.search(r"(.*?)[(]", stock_name).group(1)
    print(stock_name)

    hq = soup.select('#hq')[0].getText().replace('\n', '').replace('\r', '').replace('：', '')
    # print(hq)
    patten = r"总市值(\d+\.\d+)亿.*?市盈率TTM(\d+\.\d+)"
    res = re.search(patten, hq)
    if res:
        total_value = float(res.group(1)) * 1000000000
        pe_ratio = res.group(2)

    # 将字符转为数字
    reg = re.search(r"(\d+)万元", com_info[7])
    # print(reg)
    reg_capital = int(reg.group(1)) * 10000

    # 构建字典
    stock = {'stock_code': stock_code,
             'stock_name': stock_name,
             'company_name': com_info[0],
             'stock_type': com_info[2],
             'issue_price': com_info[4],
             'reg_capital': reg_capital,
             'address': com_info[21],
             'company_brief': com_info[23].replace('\xa0', '').replace('\n', '').replace('\r', ''),
             'total_value': total_value,
             'pe_ratio': pe_ratio,
             'current_price': current_price
             }
    print(stock)
    return stock


# 从新浪网站根据股票代码获取股票实时行情
def get_rt_hq(code):
    stock_code = code
    df = ef.stock.get_realtime_quotes()
    data = df.loc[df['股票代码'] == stock_code]
    data.columns = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    train_data = np.array(data)  # 先将数据框转换为数组
    train_data_list = train_data.tolist()  # 其次转换为列表
    return train_data_list[0]  # 以数组形式打出来方便看
