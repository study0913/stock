from bs4 import BeautifulSoup

html = """
<html>
<head><title>标题</title></head>
<body>
 <p class="title" name="dromouse"><b>标题</b></p>
 <div name="divlink">
  <p>
   <a href="http://example.com/1" class="sister" id="link1">链接1</a>
   <a href="http://example.com/2" class="sister" id="link2">链接2</a>
   <a href="http://example.com/3" class="sister" id="link3">链接3</a>
  </p>
 </div>
 <p></p>
 <div name='dv2'></div>
</body>
</html>
"""

soup = BeautifulSoup(html, 'lxml')

# 通过tag查找
print(soup.select('title'))  # [<title>标题</title>]
print(soup.title.string)
print(soup.a.string)
# 通过tag逐层查找
print(soup.select("html head title"))  # [<title>标题</title>]

# 通过class查找
print(soup.select('.sister'))
# [<a class="sister" href="http://example.com/1" id="link1">链接1</a>,
# <a class="sister" href="http://example.com/2" id="link2">链接2</a>,
# <a class="sister" href="http://example.com/3" id="link3">链接3</a>]


# 通过id查找
print(soup.select('#link1, #link2'))
# [<a class="sister" href="http://example.com/1" id="link1">链接1</a>,
# <a class="sister" href="http://example.com/2" id="link2">链接2</a>]


# 组合查找
print(soup.select('p #link1'))
# [<a class="sister" href="http://example.com/1" id="link1">链接1</a>]


# 查找直接子标签
print(soup.select("head > title"))
# [<title>标题</title>]
print(soup.select("p > #link1"))
# [<a class="sister" href="http://example.com/1" id="link1">链接1</a>]

print(soup.select("p > a:nth-of-type(2)"))
# [<a class="sister" href="http://example.com/2" id="link2">链接2</a>]
# nth-of-type 是CSS选择器


# 查找兄弟节点（向后查找）
print(soup.select("#link1 ~ .sister"))
# [<a class="sister" href="http://example.com/2" id="link2">链接2</a>,
# <a class="sister" href="http://example.com/3" id="link3">链接3</a>]

print(soup.select("#link1 + .sister"))
# [<a class="sister" href="http://example.com/2" id="link2">链接2</a>]


# 通过属性查找
print(soup.select('a[href="http://example.com/1"]'))

# ^ 以XX开头
print(soup.select('a[href^="http://example.com/"]'))

# * 包含
print(soup.select('a[href*=".com/"]'))

# 查找包含指定属性的标签
print(soup.select('[name]'))

# 查找第一个元素
print(soup.select_one(".sister"))

tds = soup.find_all('a')

for td in tds:
    print(td.string)