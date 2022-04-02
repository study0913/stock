import requests
from lxml import etree
import json

# 获取网页源代码
r = requests.get('http://ipwhois.cnnic.cn/bns/query/Query/ipwhoisQuery.do?queryOption=ipv4&txtquery=8.8.8.8')

# 使用xpath对爬取的源代码进行处理
dom_tree = etree.HTML(r.content)
links = dom_tree.xpath("/html/body/center[1]/table[1]/tr/td/font")

# 取出links的单行、双行的数据
res1 = [i.text for i in links[::2]]
res2 = [i.text for i in links[1::2]]

# 把两行数据组合成在一起
result = tuple(zip(res1, res2))

print(result)
# 使用json格式保存到文件中
json.dump(result, open('xpath_get.txt', 'w', encoding='utf-8'), ensure_ascii=False)
