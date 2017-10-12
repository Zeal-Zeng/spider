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

def getReviewUrls():
    all_reviews_urls = []
    for i in range(1,251):
        reviews_urls=[]
        b = BeautifulSoup(json.loads(s.get('http://pagelet.mafengwo.cn/note/pagelet/recommendNoteApi?params={"type":0,"objid":0,"page":%d,"ajax":1,"retina":0}'%i).text)['data']['html'])
        print(i)
        for j in b.findAll('div',class_='tn-item clearfix'):
            reviews_urls.append(j.a.get("href")+'\n')
        all_reviews_urls+=reviews_urls
        with open('review_urls.txt','a') as f:
            f.writelines(reviews_urls)
    return  all_reviews_urls
def getReviewUrls2():
    all_reviews_urls = set()
    i=6000
    l=len(all_reviews_urls)
    while(True):
        print(i)
        b = BeautifulSoup(json.loads(s.get('http://www.mafengwo.cn/ajax/ajax_article.php?start=%d'%i).text)['html'])
        reviews_urls = set(i.get("href")+'\n' for i in b.findAll('a'))
        all_reviews_urls|=reviews_urls
        with open('review_urls_2.txt','a') as f:
            f.writelines(reviews_urls)
        i+=1
        ll=len(all_reviews_urls)
        if(ll>l):
            pass
        else:
            break

    return all_reviews_urls
    with open('review_urls_2_all.txt','w') as f:
            f.writelines(all_reviews_urls)

# getReviewUrls2()
# with open('review_urls_2.txt') as f:
#     with open('review_urls_2_distinct.txt', 'a')as f2:
#         f2.writelines(set(f.readlines()))
def getmdd():
    url='http://www.mafengwo.cn/mdd/'
    b = BeautifulSoup(s.get(url).text)
    mdds = [j.rstrip('.html').lstrip('/travel-scenic-spot/mafengwo/')+'\n' for j in list(set([i.get('href') for i in  b.findAll('a')])) if j and j.startswith('/travel-scenic-spot/mafengwo/')]
    with open('mdds.txt','w')as f:
        f.writelines(mdds)
# getmdd()

def getJDUrl():
    # url ='http://www.mafengwo.cn/jd/%s/gonglve.html'
    with open('mdds.txt') as f:
        mdds = f.readlines()

    url ='http://www.mafengwo.cn/ajax/router.php'
    data = {
        'sAct': 'KMdd_StructWebAjax|GetPoisByTag',
        'iMddid': '10065',
        'iTagId': '0',
        'iPage': '2'}
    import json
    for mdd in mdds:
        data['iMddid'] = mdd.strip()
        i=0
        while(True):
            i+=1
            print(i)
            data['iPage']='%d'%i
            l = json.loads(s.post(url, data=data).text)['data']['list']
            if not l:
                break
            with open('jd.txt','a') as f:
                f.writelines([i.get('href').rstrip('.html').lstrip('/poi/')+'\n' for i in BeautifulSoup(l).findAll('a')])

getJDUrl()
