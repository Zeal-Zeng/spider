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
def getiData(url = 'http://www.mafengwo.cn/i/7618004.html'):
    data = {}
    r = s.get(url)
    r.encoding='utf-8'
    b = BeautifulSoup(r.text)
    userinfo = json.loads(b.find('script', type='text/javascript').text.strip().split('=',1)[1].strip().rstrip(';'))
    author_name =  userinfo.get('author_name','')
    data['author_name'] = author_name

    avatar = userinfo.get('logo_120','')
    data['avatar'] = avatar
    try:
        day_time_people = dict([i.get('class')+[i.text.split('/',1)[1]] for i in b.find('div', class_='tarvel_dir_list clearfix').ul.children if not isinstance(i,str)])
        data.update(day_time_people)
    except:
        print('E!'+"day_time_people")
    article = [i for i in b.find('div', class_='va_con _j_master_content').contents if not isinstance(i,str)]
    contents = []
    for i in article:
        try:
            c = i.get('class')
            if '_j_note_content' in c:
                contents.append(i.text.strip())
                # pass
            elif 'add_pic' in c:
                contents.append('<img src="'+ i.img.get('data-rt-src').strip()+'"/>')
                # pass
            elif 'article_title' in c:
                contents.append("<h2>"+ i.h2.text.strip() +"</h2>")
                # pass
        except:
            print("airtile EEE!")
    content  = '\n'.join(contents)
    data['content'] = content

    b2 =BeautifulSoup(json.loads(s.get('http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?params={"iid":"%s"}'%userinfo['iid']).text)['data']['html'])
    try:
        time_view_like = [i.text for i in b2.find("div", class_='vc_time').contents if not isinstance(i, str)]
        time = time_view_like[0]
        data['time'] = time
        view,like = time_view_like[1].split('/',1)
        data['view'] = view
        data['like'] = like
    except:
        print("EEE! time_view_like")
    try:
        destination = b.find('a', class_='_j_mdd_stas').text
        data['destination'] = destination
    except:
        print("EEE! destination")
    try:
        b3 = BeautifulSoup(json.loads(s.get('http://pagelet.mafengwo.cn/note/pagelet/bottomReplyApi?params={"iid":"%s","page":"1"}'%userinfo['iid']).text)['data']['html'])
        replys = b3.findAll('div', class_='mfw-cmt _j_reply_item')
        reply_info =[]
        for reply in replys:
            reply_user_info = reply.find('div',class_="mcmt-info")
            reply_user_name = reply_user_info.a.get("title")
            reply_user_id = reply_user_info.a.get("href")
            reply_user_avatar = reply_user_info.img.get("src")
            reply_content = reply.find('p', class_='_j_reply_content').get("data-content")
            reply_time = reply.find('div', class_='time').text
            reply_info.append({'reply_user_name':reply_user_name,
                               'reply_user_id':reply_user_id,
                               'reply_user_avatar':reply_user_avatar,
                               'reply_content':reply_content,
                               'reply_time':reply_time})
        data['reply_info'] = reply_info
    except:
        print("EEE! reply_info")
    return  data



# 'http://www.mafengwo.cn/note/detail.php?iId=7542569&iPage=2'
# 'http://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?params={"type":0,"objid":0,"page":250,"ajax":1,"retina":0}'

# https://m.mafengwo.cn/note/index/more?mddid=0&iPage=2



# https://m.mafengwo.cn/poi/17506.html
# https://m.mafengwo.cn/jd/12703/gonglve.html?page=2&is_ajax=1
# https://m.mafengwo.cn/mdd/12703
# http://www.mafengwo.cn/mdd/



'http://www.mafengwo.cn/photo/poi/17506.html'
def getMddData(url='http://www.mafengwo.cn/poi/17506.html'):
    data = {}
    b = BeautifulSoup(s.get(url).text)
    h = json.loads(b.script.text.split('=', 1)[1].strip().rstrip(';'))
    data['title'] =  h['poiname']
    d = b.find('div', class_='mod mod-detail')
    dd = [i for i in d if not isinstance(i, str)]
    data['summary'] = dd[0].text
    o = [i for i in dd[1].contents if not isinstance(i, str)]
    for i in o :
        ii = [j.text for j in i if not isinstance(j, str)]
        data['ii[0]'] = ii[1]
    for x in d.findAll('dl'):
        data[x.dt.text]=x.dd.text
    comments_url = 'http://pagelet.mafengwo.cn/poi/pagelet/poiCommentListApi?params={"poi_id":"%d","page":1,"just_comment":1}'%h['poiid']
    json.loads(s.get(comments_url))['data']['html']
    cb = BeautifulSoup(json.loads(s.get(comments_url).text)['data']['html'])
    cb.find('div', class_='rev-list')






