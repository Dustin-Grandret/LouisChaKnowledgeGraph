import os
namedict=dict()
from includefile import *
with open(namelistroot, 'r', encoding='utf-8')as f:
    namedict = eval(f.read())

def _nobookappearance(args):
    for elem in namedict.keys():
        if args['data'].find(elem)!=-1:
            return False
    return True

def washhtml1():
    for elem in os.listdir(root):
        data=''
        with open(root+elem,'r',encoding='utf-8')as f:
            data=f.read()
        flag1=(data.find('金庸')==-1)
        flag2=_nobookappearance(args={
            'data':data
        })
        if (not flag1) or (not flag2):
            with open(saveroot+elem,'w',encoding='utf-8') as f:
                f.write(data)

def washhtml2():
    import html
    with open(testcsvroot,'r',encoding='utf-8')as f:
        a=html.unescape(f.read())
        import re

        a=re.sub(' ','',a)
        a=re.sub('<.*?>','',a)
        with open('../test_1.csv', 'w', encoding='utf-8')as f:
            f.write(a)

#washhtml1()
print(len(os.listdir(saveroot)))
washhtml2()
