header = {
#     ':authority':'www.mafengwo.cn',
# ':method':'GET',
# ':path':'/sales/0-0-0-0-0-0-0-0.html?group=4',
# ':scheme':'https',
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'accept-encoding':'gzip, deflate, br',
'accept-language':'en-US,en;q=0.8',
'cache-control':'max-age=0',
'referer':'http://www.mafengwo.cn/',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


import requests
import json
from bs4 import BeautifulSoup
s = requests.session()
s.headers = header
def getData(url = 'http://www.mafengwo.cn/i/7618004.html'):
    r = s.get(url)
    r.encoding='utf-8'
    b = BeautifulSoup(r.text)
    userinfo = json.loads(b.find('script', type='text/javascript').text.strip().split('=',1)[1].strip().rstrip(';'))
    author_name =  userinfo.get('author_name','')
    avatar = userinfo.get('logo_120','')
    day_time_people = dict([i.get('class')+[i.text.split('/',1)[1]] for i in b.find('div', class_='tarvel_dir_list clearfix').ul.children if not isinstance(i,str)])
    article = [i for i in b.find('div', class_='va_con _j_master_content').contents if not isinstance(i,str)]
    for i in article:
        c = i.get('class')
        if '_j_note_content' in c:
            i.text
            # pass
        elif 'add_pic' in c:
            i.img.get('data-rt-src')
            # pass
        elif 'article_title' in c:
            i.h2.text
            # pass
