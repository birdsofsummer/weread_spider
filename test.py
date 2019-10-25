from spider import *


def test1():
    r=get(API['me'])
    print(r)

def test2():
    VID=get_vid(COOKIE)
    u=API['books']+str(VID)
    r=get(u)
    print(r)
    return r


