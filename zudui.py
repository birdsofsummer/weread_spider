import calendar
import time

API={
        "zudui":"https://weread.qq.com/wrpage/huodong/abtest/zudui?collageId={vid}_{t}&shareVid={vid}&from=timeline&wrRefCgi=",
        "zan":"https://weread.qq.com/wrpage/huodong/abtest/jizan?isAnimateNavBarBackground=1&senderVid={vid}&vol={t}&designId={t}_0&from=timeline&wrRefCgi=",
        "fan":"https://weread.qq.com/wrpage/huodong/abtest/fan?vol={t}&inviteVid={vid}&wrRefCgi=",
}

today=lambda :time.strftime("%Y%m%d", time.localtime())
year=lambda : int(time.strftime("%Y", time.localtime()))
month=lambda : int(time.strftime("%m", time.localtime()))
monthcalendar=lambda: calendar.monthcalendar(year(),month())

day=lambda :int(time.strftime("%d", time.localtime()))
weekday=lambda : int(time.strftime("%w", time.localtime()))
add_month=lambda d:"{y}{m}{d}".format(y=year(),m=month(),d=d)

tuesday,thursday,saturday=[add_month(w[x]) for x in [1,3,5] for w in monthcalendar() if w[x] >=day()]

fomat_d=lambda v: lambda vid,t: v.format(vid=vid,t=t)

api={k: fomat_d(v) for k,v in API.items()}

api1={
    "zudui":lambda vid: api["zudui"](vid,saturday),
    "zan":lambda vid: api["zan"](vid,tuesday),
    "fan":lambda vid: api["fan"](vid,thursday),
}

vid2url1=lambda vid,t :(api["zudui"](vid,t),api["zan"](vid,t),api["fan"](vid,t),)
vid2url=lambda vid :(api1["zudui"](vid),api1["zan"](vid),api1["fan"](vid),)

def  test():
    vid=76924631
    r=vid2url(vid)
    print(r)

