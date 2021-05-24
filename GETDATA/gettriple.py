from TI import *
import re
import csv


def printdict(argdict):
    print('|===============================')
    for i,v in argdict.items():
        print(f'{i}:{v}')
    print('Length:'+f'{len(argdict)}')
    print('|===============================')
def dataread(PATH,need_clean_blank=False):
    data = ''
    with open(DATAFILE + PATH, 'r', encoding='utf-8') as f:
        data = f.read()
    if need_clean_blank:
        data=re.sub('''

''', '\n', data)
    return data
def datawrite(PATH,data):
    with open(DATAFILE+PATH,'w',encoding='utf-8')as f:
        f.write(data)
def tripleread(PATH,need_clean_blank=False,is_show=False):
    with open(DATAFILE+PATH,'r',encoding='utf-8')as f:
        reader=csv.reader(f)
        triplelist=[tuple(row) for row in reader]
    if need_clean_blank:
        triplelist=list(set(triplelist))
    if is_show:
        print(triplelist)
    return triplelist
def triplewrite(PATH,rst):
    rst=list(set([tuple(row) for row in rst]))
    with open(DATAFILE+PATH,'w',encoding='utf-8')as f:
        writer=csv.writer(f)
        writer.writerows(rst)
    data=dataread(PATH)
    datawrite(PATH,re.sub('''

''', '\n', data))

def havevalue(a):
    return a and a!='' and a!='None'
#本程序完成对事实的抽取。
#从csv文件中抽取出tbox，并且确定命名映射，存储在本地json文件中
'''
1.将csv文件中的编号换成中文名
2.确定csv文件中对应的映射规则
3.确定类和人物属性
4.根据规则取出tbox
'''
#1.

#初期转换csv格式
def s1():
    data=dataread('class_1.csv')
    data=re.sub(',,,,,,,,,','',data)
    datawrite('class_1.csv',data)

#生成编号与名称的映射表
def s2(PATH='class_1.csv',is_show=False):
    pointerdict=dict()
    with open (DATAFILE+PATH,'r',encoding='utf-8')as f:
        a=csv.reader(f)
        for elem in a:
            pointerdict[elem[0]]=elem[1]
    if is_show:
        printdict(pointerdict)
    return pointerdict
#将properties_1.scv文件中的编号替换成类名
data=''
#整理数据,将properties_1.scv文件中的编号替换成类名
def s3(PATH1='properties_1.csv',PATH2='properties_2.csv',pointerdict=s2()):
    data=dataread(PATH1)
    tran=data[:]
    for i,v in pointerdict.items():
        tran=re.sub(i,v,tran)
    datawrite(PATH2,tran)

#将所有类名，属性名打印
def s3_1(PATH1,PATH2):
    with open(DATAFILE+PATH1,'r',encoding='utf-8')as f:
        data=csv.reader(f)
        names=[row[1] for row in data]
        script=''
        for i,name in enumerate(names):
            script+=str(name)+' '
            if i%10==0:
                script+='\n'
        datawrite(PATH2,script)

#根据属性表生成三元组
def s4(PATH1='properties_2.csv',PATH2='properties_3.csv'):
    triplelist=tripleread(PATH1)
    rst=[]

    for i,elem in enumerate(triplelist):
        if i==0:
            continue
        for j in range(1,len(elem)):
            head=elem[1]
            if havevalue(elem[2]):
                rst.append((head,TI_DOMAIN,elem[2]))
            if havevalue(elem[3]):
                rst.append((head, TI_RANGE, elem[3]))
            if elem[4]==str(1):
                rst.append((head, TYPE, TI_TRANSITIVE))
            if elem[5]==str(1):
                rst.append((head, TYPE, TI_SYMMETRIC))
            if elem[6]==str(1):
                rst.append((head, TYPE, TI_FUNCTIONAL))
            if havevalue(elem[7]):
                rst.append((head, TI_INVERSE, elem[7]))
            if elem[8]==str(1):
                rst.append((head, TYPE, TI_INVERSEFUNCTIONAL))
            if havevalue(elem[9]):
                rst.append((head, TI_SAMEAS, elem[9]))
            if havevalue(elem[10]):
                rst.append((head,TI_SUBPROPERTY, elem[10]))
            if elem[11]=='关系':
                rst.append((head,TI_TYPE, TI_RELATION_1))
            if elem[11]=='属性':
                rst.append((head,TI_TYPE, TI_PROPERTY_1))
    rst=list(set(rst))
    triplewrite(PATH2,rst)

#将kg三元组内容转存
def s5_0(PATH1='kg三元组04_13.csv',PATH2='kg三元组04_13_1.csv'):
    triplewrite(PATH2,tripleread(PATH1))
#转换csv文件编码，去掉无效字符
def s5(PATH='kg三元组04_13_1.csv'):
    tran=dataread(PATH,need_clean_blank=True)
    tran = re.sub('：', '', tran)
    tran = re.sub('主要成就1', '主要成就', tran)
    tran = re.sub('主要成就2', '主要成就', tran)
    tran = re.sub('主要成就3', '主要成就', tran)
    tran = re.sub('及其衍生作品', '', tran)

    tran=re.sub('金庸武侠小说','',tran)

    datawrite(PATH,tran)
    triplewrite(PATH,tripleread(PATH))

#三元组将有分隔符的化为多条三元组
def s6(PATH='kg三元组04_13_1.csv'):
    rst=[]
    triples=tripleread(PATH)
    splitflags=',，，、/→\n'
    for elem in triples:
        is_change=False
        for splitflag in splitflags:
            if splitflag in elem[1]:
                tran=elem[1].split(splitflag)
                for elem2 in tran:
                    rst.append((elem[0],elem2,elem[2]))
                is_change=True
        for splitflag in splitflags:
            if splitflag in elem[2]:
                tran = elem[2].split(splitflag)
                for elem2 in tran:
                    rst.append((elem[0], elem[1],elem2))
                is_change = True
        if not is_change:
            rst.append(elem)




    triplewrite(PATH,rst)

def s6_2(PATH='kg三元组04_13_1.csv'):
    rst = []
    triples = tripleread(PATH)
    #消除()和“”
    for elem in triples:
        is_change = False
        if '(' in elem[2]:
            tran=re.compile('(.*?)\((.*?)\)(.*?)').findall(elem[2])
            for elem2 in tran:
                rst.append((elem[0], elem2, elem[2]))
            is_change = True
        if not is_change:
            rst.append(elem)

    triplewrite(PATH, rst)
def s6_3(PATH='kg三元组04_13_1.csv'):
    tran=tripleread(PATH)
    rst=[]
    for elem in tran:
        rst.append((elem[0],elem[1],re.sub('\n','',elem[2])))
    triplewrite(PATH,rst)
#检查无效字符
def s6_1(PATH='kg三元组04_13_1.csv'):
    triples=tripleread(PATH)
    #测试
    flags=[]
    for elem in triples:
        for elem2 in elem:
            tran=re.compile('([^\u4e00-\u9fa5A-za-z0-9）~]+?)').findall(elem2)
            if len(tran)>0:
                flags.extend(tran)
    print(list(set(flags)))

def s7(PATH1='properties_2.csv',PATH2='kg三元组04_13_1.csv',PATH3='kg三元组04_13_2.csv'):
    #生成目前已有属性：
    properties=[row[1] for row in tripleread(PATH1)]
    rst=[]
    for row in tripleread(PATH2):
        if row[1] in properties and row[2]!='':
           rst.append(row)
    triplewrite(PATH3,rst)

#生成abox,tbox
def s8(PATH1='kg三元组04_13_2.csv',PATH2='properties_3.csv'):
    abox,tbox=[],[]
    for row in tripleread(PATH1):
        if havevalue(row[0]) and havevalue(row[1]) and havevalue(row[2]):
            abox.append(tuple(row))
    for row in tripleread(PATH2):
        if havevalue(row[0]) and havevalue(row[1]) and havevalue(row[2]):
            tbox.append(tuple(row))
    return list(set(abox)),list(set(tbox))

#类别推断步骤1：规则推理

def s9(PATH1='abox_test.csv',PATH2='tbox_test.csv'):
    abox, tbox = s8()
    abox,tbox=test2(args={
        'abox':abox,
        'tbox':tbox
    })
    triplewrite(PATH1,abox)
    triplewrite(PATH2, tbox)


#根据json文件抽取出csv文件中的abox
#分别将abox和tbox存储在本地文件中

#分离relation和property便于可视化
def s10(PATH1='aboxwithproperty.csv',PATH2='aboxwithrelation.csv'):
    test = get_RELATION_PROPERTY()
    abox, tbox = s8()
    rst_property_box, rst_relation_box = test._run(
        args={
            'abox': abox,
            'tbox': tbox
        }
    )
    triplewrite(PATH1,rst_property_box)
    triplewrite(PATH2,rst_relation_box)

def generate_disjoint(PATH1='class_1.csv',PATH2='class_2.csv'):
    triples=tripleread(PATH1)
    triples=[triple[1] for triple in triples]
    data=''
    for elem in triples:
        data+=','+elem
    for i,elem in enumerate(triples):
        data+='\n'+elem+',a'*(i+1)
    datawrite(PATH2,data)
def getdisjoint(PATH1,PATH2,rst_abox):
    triples = tripleread(PATH1)
    triples = [triple[1] for triple in triples]
    from tqdm import tqdm
    for i,elem in tqdm(enumerate(tripleread(PATH2))):
        for j,elem2 in enumerate(elem):
            if elem2==str(1):
                rst_abox.append(
                    (triples[i-1],TI_DISJOINT,triples[j-1])
                )
    return rst_abox
def s11(PATH,PATH2):
    box=tripleread(PATH)
    rst=[]
    for elem in box:
        flag=True
        for elem1 in elem:
            for splitflag in ',，，、/→\n':
                if splitflag in elem1:
                    flag=False
        if not flag:
            continue
        rsttran=[]
        for elem1 in elem:
            tran=elem1[:]
            tran=re.sub('等$','',tran)
            tran=re.sub('「','',tran)
            tran = re.sub('」', '', tran)
            rsttran.append(tran)
        rst.append(rsttran)
    triplewrite(PATH2,rst)
if __name__ == '__main__':
    #generate_disjoint()
    #s11('abox_test.csv','abox_test_1.csv')
    #s11('tbox_test.csv', 'tbox_test_1.csv')
    abox=tripleread('abox_test.csv')
    tbox = tripleread('tbox_test.csv')
    tbox.extend(getdisjoint('class_1.csv','class_3.csv',[]))
    test=rule_check_1()
    printbox(test.run(args={
        'abox':abox,
        'tbox':tbox
    }))