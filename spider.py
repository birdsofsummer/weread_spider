import sqlite3
import json
import os
import requests

IP="10.4.17.60" #adb
API={
   "user_info":"https://i.weread.qq.com/user/profile?gender=1&signature=1&vDesc=1&location=1&totalReadingTime=1&currentReadingTime=1&finishedBookCount=1&followerCount=1&followingCount=1&buyCount=1&reviewCount=1&reviewLikedCount=1&sameFollowing=1&reviewCommentedCount=1&likeBookCount=1&isFollowing=1&isFollower=1&isBlackMe=1&isInBlackList=1&bookReviewCount=1&noteBookCount=1&exchangedMoney=1&recentReadingBooks=1&booklistCount=1&booklistCollectCount=1&articleBookId=1&articleCount=1&articleDraftCount=1&articleReadCount=1&articleSubscribeCount=1&articleWordCount=1&audioCount=1&audioListenCount=1&audioLikedCount=1&audioCommentedCount=1&totalLikedCount=1&mpAccount=1&canExchange=1&isSubscribing=1&hideMe=1&wechatFriendCount=1&wechatFriendSubscribeCount=1&userVid=",
    #76924631
    "me":"https://i.weread.qq.com/friend/ranking?mine=1",
    "rank":"https://i.weread.qq.com/friend/ranking",
    "friendCommon":"https://i.weread.qq.com/shelf/friendCommon?userVid=",
    "books":"https://i.weread.qq.com/shelf/friendCommon?userVid=",
    "notebooks":"https://i.weread.qq.com/user/notebooks",
    "book_info":"https://i.weread.qq.com/book/info?bookId=",
    "bestbookmarks":"https://i.weread.qq.com/book/bestbookmarks?bookId=",
    "bookmarklist":"https://i.weread.qq.com/book/bookmarklist?bookId=",
    "chapterInfos":"https://i.weread.qq.com/book/chapterInfos",
    # post {"bookIds":["%d"],"synckeys":[0]}
   "flip":"https://weread.qq.com/wrpage/flip/card?vol=20191022&isAnimateNavBarBackground=1",
}

def get_cookie_file(ip=IP,path="."):
 #   import uiautomator2 as u2
 #   d = u2.connect(ip)
    cookie_file="/data/data/com.tencent.mm/app_x5webview/X5Cookies"
    os.popen("adb connect {}".format(ip))
    os.popen("adb pull {} {}".format(cookie_file,path))

def query(cookie_file="./X5Cookies",table="cookies"):
    conn = sqlite3.connect(cookie_file)
    c = conn.cursor()
    cursor = c.execute("PRAGMA table_info([{}])".format(table))
    k=[row for row in cursor]
    kk=tuple(row[1] for row in k)
    cursor = c.execute("SELECT *  from {}".format(table))
    r=[row for row in cursor]
    return [dict(zip(kk,x)) for x in r]

def get_cookie(cookie_file="X5Cookies"):
    if 'X5Cookies' not in [c for (a,b,c) in os.walk(".")][0]:get_cookie_file()
    return query()


def serialize_cookie(z=[]):
    return "; ".join(["=".join([x['name'],x['value']]) for x in z])

def get_cookie1():
    return serialize_cookie(get_cookie(IP))

def parse_cookie(c):
     return dict(x.split("=",1)  for x in c.split("; "))

def get_vid(c):
    v=parse_cookie(c)["wr_vid"]
    return int(v)

"""
   weread_url="https://weread.qq.com/wrpage/flip/card?vol=20191022&isAnimateNavBarBackground=1"
1. 微信聊天界面打开这个页面
2. adb连手机拿到微信的cookie文件
   也可电脑 https://x.weread.qq.com/
   扫码取出cookie手动粘贴
3. 解析cookie
4. 构造headers
"""

#COOKIE='wr_logined=1; wr_vid=76924631; wr_skey=L5PgUrvM; wr_avatar=http%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FQ0j4TwGTfTIsDBY64FCTjUwibjibBY0uPpm8ZHaibdDrBWhnGYoel8Y3S7gG2PKeClAwPAslakciaN0grb3xENby9A%2F132; wr_name=%E5%B0%8F%E8%88%9F%E4%BB%8E%E6%AD%A4%E9%80%9D; wr_logined=1'

COOKIE=get_cookie1()

def gen_headers(c=COOKIE):
    headers={
        'Host': 'i.weread.qq.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        "Cookie":c,
    }
    return headers



def get(url,params={}):
    headers=gen_headers()
    r = requests.get(url,params=params,headers=headers)
    data={}
    if r.ok:
        data = r.json()
    else:
        raise Exception(r.text)
    return data

def post(url,data='',params={}):
    headers=gen_headers()
    r = requests.post(url,params=params,data=data,headers=headers,verify=False)
    d={}
    if r.ok:
        d= r.json()
    else:
        raise Exception(r.text)
    return d

