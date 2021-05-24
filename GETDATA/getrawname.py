#爬取金庸小说人物名称
'''
update.info:
1.格式：{书名:[人名1,人民2]}
'''
from includefile import *
def getrawname():
    rst=''
    with open (PROJECTROOT+'docs/金庸人物.html', 'r', encoding='utf-8') as f:
        rawtext=f.read()
        pat1='<h2 class="dataname"><span class="color">(.*?)</span>人物大全</h2>'
        booknamelist=re.compile(pat1,re.S).findall(rawtext)
        pat2='''<div class="datapice">(.*?)</div>'''
        tran=re.compile(pat2,re.S).findall(rawtext)
        pat3='<a.*?/>(.*?)</a>'
        bookpeopledict=dict()
        for i in range(len(booknamelist)):
            bookpeopledict[booknamelist[i]]=re.compile(pat3,re.S).findall(tran[i])
        rst=json.dumps(bookpeopledict,ensure_ascii=False)
        print(rst)
    with open ('../character.json', 'w', encoding='utf-8') as f:
        f.write(rst)
    return rst





