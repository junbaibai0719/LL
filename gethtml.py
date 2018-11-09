import requests
import re
import json

import usesqlit

url = {
    '':'https://blog.csdn.net/',
    'newarticles':'https://blog.csdn.net/nav/newarticles',
    'news':'https://blog.csdn.net/nav/news',
    'ai':'https://blog.csdn.net/nav/ai',
    'cloud':'https://blog.csdn.net/nav/cloud',
    'db':'https://blog.csdn.net/nav/db',
    'career':'https://blog.csdn.net/nav/career',
    'game':'https://blog.csdn.net/nav/game',
    'engineering':'https://blog.csdn.net/nav/engineering',
    'web':'https://blog.csdn.net/nav/web',
    'mobile':'https://blog.csdn.net/nav/mobile',
    'iot':'https://blog.csdn.net/nav/iot',
    'ops':'https://blog.csdn.net/nav/ops',
    'fund':'https://blog.csdn.net/nav/fund',
    'lang':'https://blog.csdn.net/nav/lang',
    'arch':'https://blog.csdn.net/nav/arch',
    'avi':'https://blog.csdn.net/nav/avi',
    'sec':'https://blog.csdn.net/nav/sec',
    'other':'https://blog.csdn.net/nav/other'
}
offset_url = 'https://blog.csdn.net/api/articles?type=more&category={cla}&shown_offset={offset}'

#匹配article url的正则
rurl = '"(https://blog.csdn.net/.*?/article/.*?/[0-9]{8})"'
rurll = '"url":"(https://blog.csdn.net/.*?/article/.*?/[0-9]{8})'
#匹配博客内容的正则
rtitle = '<title>(.+)</title>'
rcontent = '>(.+)</p'
#编译正则
com_rurl = re.compile(rurl)
com_rurll = re.compile(rurll)
com_rtitle = re.compile(rtitle)
com_rcontent = re.compile(rcontent)


#获取博客文章的url
def get_atcurl(htmltext):
    goturl = re.findall(com_rurl, htmltext)
    goturl.extend(re.findall(com_rurll, htmltext.replace('\\', '')))
    goturl = set(goturl)
    goturl = list(goturl)
    return goturl

#获取shown_offset
def get_offset(htmltext):
    offset = []
    jn = json.loads(htmltext)
    list = jn['articles']
    tempurl = 'https://blog.csdn.net/api/articles?type=more&category=newarticles&shown_offset={}'
    for i in list:
        shown_offset = i['shown_offset']
        url = tempurl.format(shown_offset)
        offset.append((shown_offset,0))
    return  offset


def get_atc_content(url):
    #发出get请求,获取网页的html文本
    response = requests.get(url)
    htmltext = response.text
    #获取标题
    title = re.findall(com_rtitle,htmltext)
    #获取博客文本内容
    content = ''.join(re.findall(com_rcontent,htmltext))
    contention = re.split('<.*?>',content)
    articlefile = open('./temparticle.txt','w+',encoding='utf-8')
    articlefile.write(''.join(title))
    for i in contention:
        articlefile.write(i)
        articlefile.write('\n')
    articlefile.close()
    #获取html里的其他博客文章url
    goturl = get_atcurl(htmltext)
    return goturl

if __name__ == '__main__':
    response = requests.get('https://blog.csdn.net/shuishen520/article/details/83861996')
    url = get_atcurl(response.text)
    print(url)
    print(url.__len__())
    mysql = usesqlit.MySql('mydb.db')
    mysql.url_save(url)
    # 读一次，访问一次，再读一次
    mysql.url_read()
    urlm = mysql.url_access()
    mysql.set_url_acce(urlm[0][0])
    mysql.url_read()
    get_atc_content('https://blog.csdn.net/shuishen520/article/details/83861996')
