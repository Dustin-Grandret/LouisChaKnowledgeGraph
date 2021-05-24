from TI.rule_basic import Rule_basic
from TI.util import *

TYPE='rdfs:type'

TI_TYPE='rdfs:type'
TI_DATATYPE='rdfs:datatype'
TI_PROPERTY='rdf:property'
TI_DOMAIN='rdfs:domain'
TI_RANGE='rdfs:range'
TI_RESOURCE='rdfs:resource'
TI_CLASS='rdfs:class'
TI_SUBPROPERTY='rdfs:subpropertyof'
TI_SUBCLASS='rdfs:subclassof'
TI_LITERAL='rdfs:literal'
TI_TRANSITIVE='owl:transitiveproperty'
TI_INVERSEFUNCTIONAL='owl:inversefunctionalproperty'
TI_SYMMETRIC='owl:symmetricproperty'
TI_SAMEAS='owl:sameas'
TI_FUNCTIONAL='owl:functionalproperty'
TI_INVERSE='owl:inverseof'

TI_DISJOINT='owl:disjoint'
TI_RELATION_1='RELATION'
TI_PROPERTY_1='PROPERTY'

TI_DISJOINT_ERROR='error:disjointerror'
'''
标准：
type|->rdfs:type
rdf,rdfs,owl标记及其内容全部小写。
rdfs:type
'''
class rule1(Rule_basic):
    '''
    1.TODO:本函数所完成的逻辑规则(需填写)
    若uay，那么a是TI_PROPERTY
    '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            rst_tbox.append((trule[1],TI_TYPE,TI_PROPERTY))
        for trule in args['abox']:
            rst_tbox.append((trule[1],TI_TYPE,TI_PROPERTY))
        return rst_abox,rst_tbox


class rule2(Rule_basic):
    '''
    3.TODO:本函数所完成的逻辑规则(需填写)
    若t TI_DOMAIN c1 且 a t b 可推理出 a TI_TYPE c1
    '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            if trule[1]==TI_DOMAIN:
                for arule in args['abox']:
                    if arule[1]==trule[0]:
                        rst_abox.append((arule[0],TI_TYPE,trule[2]))
        return rst_abox,rst_tbox
class rule3(Rule_basic):
    '''
        3.TODO:本函数所完成的逻辑规则(需填写)
        若t TI_RANGE  c1 且 a t b 可推理出 b TI_TYPE c1
        '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            if trule[1]==TI_RANGE:
                for arule in args['abox']:
                    if arule[1]==trule[0]:
                        rst_abox.append((arule[2],TI_TYPE,trule[2]))
        return rst_abox,rst_tbox

#CHANGE
class rule4(Rule_basic):
    '''
    4.TODO:本函数所完成的逻辑规则(需填写)
    若uay，那么u和y是TI_RESOURCE
    '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            rst_tbox.append((trule[0],TI_TYPE,TI_RESOURCE))
            rst_tbox.append((trule[2],TI_TYPE,TI_RESOURCE))
        for trule in args['abox']:
            rst_tbox.append((trule[0],TI_TYPE,TI_RESOURCE))
            rst_tbox.append((trule[2],TI_TYPE,TI_RESOURCE))
        return rst_abox,rst_tbox


# In[2]:


class rule5(Rule_basic):
    '''
    5.TODO:本函数所完成的逻辑规则(需填写)
    若a TI_SUBPROPERTY b,b TI_SUBPROPERTY c 则 a TI_SUBPROPERTY c
    '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            if trule[1]==TI_SUBPROPERTY:
                for trule2 in args['tbox']:

                    if trule2[0]==trule[2] and trule2[1]==TI_SUBPROPERTY:
                        rst_tbox.append((trule[0],TI_SUBPROPERTY,trule2[2]))
        return rst_abox,rst_tbox


# In[4]:


class rule6(Rule_basic):
    '''
    6.TODO:本函数所完成的逻辑规则(需填写)
    若a的 TI_TYPE 是一个TI_PROPERTY,那么a是自身的TI_SUBPROPERTY
    '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            if trule[1]==TI_TYPE and trule[2]==TI_PROPERTY:
                rst_tbox.append((trule[0],TI_SUBPROPERTY,trule[0]))
        return rst_abox,rst_tbox


# In[5]:


class rule7(Rule_basic):
    '''
    7.TODO:本函数所完成的逻辑规则(需填写)
    若a是b的子属性，uay 则uby
    '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            if trule[1]==TI_SUBPROPERTY:
                for trule2 in args['tbox']:
                    if trule2[1]==trule[0]:
                        rst_tbox.append((trule2[0],trule[2],trule2[2]))
        return rst_abox,rst_tbox


# In[6]:


class rule8(Rule_basic):
    '''
    8.TODO:本函数所完成的逻辑规则(需填写)
    若u的类别是class,那么u是resource的子类
    '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            if trule[1]==TI_TYPE and trule[2]==TI_CLASS:
                rst_tbox.append((trule[0],TI_SUBCLASS,TI_RESOURCE))
        return rst_abox,rst_tbox


# In[11]:


class rule9(Rule_basic):
    '''
    9.TODO:本函数所完成的逻辑规则(需填写)
    若u是x的子类，v是TI_TYPE u,则v是TI_TYPEx
    '''
    def _run(self, args):
        rst_abox,rst_tbox=[],[]
        for trule in args['tbox']:
            if trule[1]==TI_SUBCLASS:
                for trule2 in args['tbox']:
                    if trule2[1]==TI_TYPE and trule2[2]==trule[0]:
                        rst_tbox.append((trule2[0],TI_TYPE,trule[2]))
        return rst_abox,rst_tbox



class rule10(Rule_basic):
    '''
        10.TODO:本函数所完成的逻辑规则(需填写)
        若 C,TI_TYPE,TI_CLASS 可推理出 C TI_SUBCLASS C
        '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            if trule[1] == TI_TYPE and trule[2] == TI_CLASS:
                rst_tbox.append((trule[0], TI_SUBCLASS, trule[0]))
        return rst_abox, rst_tbox


class rule11(Rule_basic):
    '''
        11.TODO:本函数所完成的逻辑规则(需填写)
        若u TI_SUBCLASS v. v TI_SUBCLASS x 可推理出 u TI_SUBCLASS x.
        '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            if trule[1] == TI_SUBCLASS:
                for trule_ in args['tbox']:
                    if trule_[1] == TI_SUBCLASS and trule[2] == trule_[0]:
                        rst_abox.append((trule[0], TI_SUBCLASS, trule_[2]))
        return rst_abox, rst_tbox


class rule13(Rule_basic):
    '''
        13.TODO:本函数所完成的逻辑规则(需填写)
        若 u TI_TYPE TI_DATATYPE 可推理出 u TI_SUBCLASS TI_LITERAL
        '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            if trule[1] == TI_TYPE and trule[2] == TI_DATATYPE:
                rst_tbox.append((trule[0], TI_SUBCLASS, TI_LITERAL))
        return rst_abox, rst_tbox

class rule_owl_1(Rule_basic):
    '''
            3.TODO:本函数所完成的逻辑规则(需填写)
            为属性增加TRANSITIVE性质，xRy且yRz推得xRz
            '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            if trule[1] == TYPE and trule[2]==TI_TRANSITIVE:
                for arule1 in args['abox']:
                    if arule1[1] == trule[0]:#xRy
                        for arule2 in args['abox']:
                            if arule2[1]==trule[0] and arule1[2]==arule2[0]:
                                rst_abox.append((arule1[0], trule[0], arule2[2]))
                for trule1 in args['tbox']:
                    if trule1[1] == trule[0]:#xRy
                        for trule2 in args['tbox']:
                            if trule2[1]==trule[0] and trule1[2]==trule2[0]:
                                rst_tbox.append((trule1[0], trule[0], trule2[2]))

        return rst_abox, rst_tbox
class rule_owl_2(Rule_basic):
    '''
            3.TODO:本函数所完成的逻辑规则(需填写)
            为属性增加SYMMETRIC性质，xRy有yRx
            '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:

            if trule[1] == TYPE and trule[2]==TI_SYMMETRIC:
                for arule1 in args['abox']:
                    if arule1[1] == trule[0]:#xRy
                        rst_abox.append((arule1[2], trule[0], arule1[0]))
                for trule1 in args['tbox']:
                    if trule1[1] == trule[0]:#xRy
                        rst_tbox.append((trule1[2], trule[0], trule1[0]))
        return rst_abox, rst_tbox
class rule_owl_3(Rule_basic):
    '''
            3.TODO:本函数所完成的逻辑规则(需填写)
            为属性增加FUNCTIONAL性质，xRy且xRz有x==z
            '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            if trule[1] == TYPE and trule[2]==TI_FUNCTIONAL:
                for arule1 in args['abox']:
                    if arule1[1]==trule[0]:
                        for arule2 in args['abox']:
                            if arule2[0]==arule1[0] and arule2[1]==trule[0]:
                                rst_abox.append((arule1[2],TI_SAMEAS,arule2[2]))
                for trule1 in args['tbox']:
                    if trule1[1] == trule[0]:
                        for trule2 in args['tbox']:
                            if trule2[0] == trule1[0] and trule2[1] == trule[0]:
                                rst_tbox.append((trule1[2],TI_SAMEAS, trule2[2]))
        return rst_abox, rst_tbox
class rule_owl_4(Rule_basic):
    '''
                3.TODO:本函数所完成的逻辑规则(需填写)
                TI_SAMEAS
                '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            if trule[1]==TI_SAMEAS:
                for arule in args['abox']:
                    noNoneappend(rst_abox,equivalenttriple(trule[0],trule[2],arule))
                for trule2 in args['tbox']:
                    noNoneappend(rst_tbox, equivalenttriple(trule[0], trule[2], trule2))
        return rst_abox, rst_tbox
class rule_owl_5(Rule_basic):
    '''
                3.TODO:本函数所完成的逻辑规则(需填写)
                TI_INVERSE a TI_INVERSE d, b a c =>c d b
                '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            if trule[1]==TI_INVERSE:
                for arule in args['abox']:
                    if arule[1]==trule[0]:
                        rst_abox.append((arule[2],trule[2],arule[0]))
                for trule1 in args['tbox']:
                    if trule1[1]==trule[0]:
                        rst_tbox.append((trule1[2],trule[2],trule1[0]))

        return rst_abox, rst_tbox
class rule_owl_6(Rule_basic):
    '''
            3.TODO:本函数所完成的逻辑规则(需填写)
            为属性增加INVERSEFUNCTIONAL性质，xRy且zRy有x==z
            '''

    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            if trule[1] == TYPE and trule[2]==TI_INVERSEFUNCTIONAL:
                for arule1 in args['abox']:
                    if arule1[1]==trule[0]:
                        for arule2 in args['abox']:
                            if arule2[2]==arule1[2] and arule2[1]==trule[0]:
                                rst_abox.append((arule1[0],TI_SAMEAS,arule2[0]))
                for trule1 in args['tbox']:
                    if trule1[1] == trule[0]:
                        for trule2 in args['tbox']:
                            if trule2[2] == trule1[2] and trule2[1] == trule[0]:
                                rst_tbox.append((trule1[0],TI_SAMEAS, trule2[0]))
        return rst_abox, rst_tbox


class rule_ti_1(Rule_basic):
    #解析并集
    def _run(self, args):
        rst_abox, rst_tbox = [], []
        for trule in args['tbox']:
            for elem in trule:
                pass
        return rst_abox, rst_tbox

#独立规则:将事实中的关系和属性分离
class get_RELATION_PROPERTY(Rule_basic):
    def _run(self, args):
        rst_property_box, rst_relation_box = [], []
        for trule in args['tbox']:
            if trule[1] == TI_TYPE and trule[2]==TI_PROPERTY_1:
                for arule1 in args['abox']:
                    if arule1[1]==trule[0]:
                        rst_property_box.append(arule1)
            if trule[1] == TI_TYPE and trule[2]==TI_RELATION_1:
                for arule1 in args['abox']:
                    if arule1[1]==trule[0]:
                        rst_relation_box.append(arule1)
        return rst_property_box, rst_relation_box



class Rule_check_basic(Rule_basic):
    '''
    rule_check规则禁止改动规则
    '''

    def getfactids(self,box):
        return [(*fact,factid) for factid, fact in enumerate(box)]
    def _translate_args(self,args):
        rst_box = args['abox'][:]
        rst_box.extend(args['tbox'])
        self.rst_original_box = self.getfactids(rst_box)
    def _run_tran(self):
        raise  NotImplementedError()
    def _run(self,args):
        self._translate_args(args)
        return self._run_tran()



class rule_check_1(Rule_check_basic):
    '''对于类A和类B,若A和B不相交且存在a使得a属于A且a属于B，
    则返回一条标识错误的三元组('序列号','DISJOINTERROR','ainA_ainB')
    rule_check规则禁止改动规则
    '''
    def _run_tran(self):
        rst_assertion_box= []
        rst_original_box=self.rst_original_box[:]
        #找所有含type的语句
        tran1,tran2=[],[]
        for elem in rst_original_box:
            if elem[1]==TI_TYPE:
                tran1.append(elem)
            if elem[1]==TI_DISJOINT:
                tran2.append(elem)
        #分析type语句
        for elem1 in tran2:
            for elem2 in tran1:
                if elem2[2]==elem1[0]:
                    for elem3 in tran1:
                        if elem3[0]==elem2[0] and elem3[2]==elem1[2]:
                            errorsrcipt=f'{elem3[0]} in {elem1[0]} and {elem1[2]},{elem1[0]} disjointwith {elem1[2]}'
                            rst_assertion_box.extend(
                                [
                                    (elem1[3],TI_DISJOINT_ERROR,errorsrcipt),
                                    (elem2[3], TI_DISJOINT_ERROR, errorsrcipt),
                                    (elem3[3], TI_DISJOINT_ERROR, errorsrcipt),
                                ]
                            )
        return  rst_original_box,rst_assertion_box

DATAFILE=r'F:\课程资料\pythonProject\triples\\'
import csv
import re
def tripleread(PATH,need_clean_blank=False,is_show=False):
    with open(DATAFILE+PATH,'r',encoding='utf-8')as f:
        reader=csv.reader(f)
        triplelist=[tuple(row) for row in reader]
    if need_clean_blank:
        triplelist=list(set(triplelist))
    if is_show:
        print(triplelist)
    return triplelist
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
def triplewrite(PATH,rst,is_random=False):
    if is_random:
        rst=list(set([tuple(row) for row in rst]))
    with open(DATAFILE+PATH,'w',encoding='utf-8')as f:
        writer=csv.writer(f)
        writer.writerows(rst)
    data=dataread(PATH)
    datawrite(PATH,re.sub('''

''', '\n', data))

def getdisjointfile(PATH1,PATH2,PATH3):
    a=tripleread(PATH1)
    b = tripleread(PATH2)
    a.extend(b)
    triplewrite(PATH3,a)

def getrdf(PATH1,PATH2,PATH3,PATH4):
    '''

    :param PATH1:名称映射字典
    :param PATH2: 最终rdf存储位置
    :param PATH3: abox位置
    :param PATH4: tbox位置
    :return:
    '''
    def _strcompare(a:str,b:str):
        if a<b:
            return -1
        elif a==b:
            return 0
        else:
            return 1
    def _tuplecompare(a:tuple,b:tuple):
        for i in range(3):
            if a[i]!=b[i]:
                return _strcompare(a[i],b[i])
        return 0
    def _bubbleSort(args:dict,issave=False,SAVEROOT='bubblesort.csv',isload=True):
        from tqdm import tqdm
        if isload:
            return tripleread(SAVEROOT)
        all_tuples = args['abox']
        all_tuples.extend(args['tbox'])
        all_tuples = list(set(all_tuples))
        """冒泡排序"""

        for i in tqdm(range(1, len(all_tuples))):
            for j in range(0, len(all_tuples) - i):
                if all_tuples[j][0] >= all_tuples[j + 1][0]:
                    temp = all_tuples[j]
                    all_tuples[j], all_tuples[j + 1] = all_tuples[j + 1], temp
        if issave:
            triplewrite(SAVEROOT,all_tuples)
        return all_tuples
        if isload:
            return tripleread(SAVEROOT)
        all_tuples = args['abox']
        all_tuples.extend(args['tbox'])
        all_tuples = list(set(all_tuples))
        '''选择排序'''

        for i in range(len(all_tuples)):
            tran=i
            minelem=all_tuples[i]
            for j in range(i,len(all_tuples)):
                if _tuplecompare(minelem,all_tuples[j]):#all_tuples[j]比minelem小
                    tran=j
                    minelem=all_tuples[j]


        if issave:
            triplewrite(SAVEROOT,all_tuples)
        return all_tuples
    def _boxmap(Adict:dict, boxes: list):
        '''
        boxes:[abox,tbox]
        :param Adict:
        :param boxes:
        :return:映射好的abox,tbox
        '''
        rst_abox=[list(row) for row in boxes[0]]
        rst_tbox = [list(row) for row in boxes[1]]
        tran = [rst_abox, rst_tbox]
        for i, box in enumerate(boxes):
            checklist = []
            for elem1 in Adict.items():
                checklist.append(elem1[0])
            for i1, elem1 in enumerate(box):
                for i2, elem2 in enumerate(elem1):
                    if elem2 in checklist:
                        tran[i][i1][i2] = 'entity:e{}'.format(Adict[elem2])
        return tran
    def _getstat(box, index):
        return (index==0 or box[index][0] != box[index - 1][0], index==len(box) - 1 or box[index][0] != box[index + 1][0])
    def _getid2name():
        return eval(open(DATAFILE+'id2name.txt','r',encoding='utf-8').read())
    def _getrdf(sorted_box, PATH2):
        id2name=_getid2name()
        script = ''
        # 生成前缀信息
        script = '@prefix entity: <http://kg_21_22//entity#> .\n\n'
        idlist=[curid[0] for curid in id2name.items()]
        for i, elem in enumerate(sorted_box):
            tran = _getstat(sorted_box, index=i)
            if tran[0] == 1:  # 第一次出现
                script += '''entity:{}
	relation:name "{}" ;\n'''.format(
                    re.sub('entity:','',elem[0]),
                    id2name[re.sub('entity:e','',elem[0])
                    ]if re.sub('entity:e','',elem[0]) in idlist else elem[0]
                )
            script += '''	{} {} {}\n'''.format(
                elem[1],
                elem[2],
                '.' if tran[1] == 1 else ';'
            )
        datawrite(PATH2, script)



    #读取aboxtbox，混合并排序
    all_triples=_bubbleSort(args={
        'abox':tripleread(PATH3),
        'tbox': tripleread(PATH4),
    })
    dictdata=dataread(PATH1)
    dictdata=eval(dictdata)
    #做字到URI的映射
    tran=_boxmap(dictdata,[all_triples,[]])
    tran=tran[0]
    _getrdf(tran,PATH2)
def cleansame(abox,tbox):#完成同义消歧
    for i,arule in enumerate(abox):
        for j,elem1 in enumerate(arule):
            if elem1==TI_SAMEAS:
                for i1,arule1 in enumerate(abox):
                    for j1, elem11 in enumerate(arule1):
                        if elem11 == arule[0]:
                            arule1[j1]=arule[2]
                for i1, trule1 in enumerate(tbox):
                    for j1, elem11 in enumerate(trule1):
                        if elem11 == arule[0]:
                            trule1[j1] = arule[2]
    #删除重复词，原来的sameas用于为实体添加别名
    rst_abox=list(set(abox))
    rst_tbox = list(set(tbox))
    return rst_abox,rst_tbox

def prettyrdf(PATH,PATH2):
    data=dataread(PATH)
    #0-3508
    script='''@prefix entity: <http://kg_21_22//entity#> .

'''
    for i in range(3509):
        tran=re.compile('''(entity:e{}.*?\.)'''.format(i),re.S).findall(data)
        script+=tran[0]+'\n'
    datawrite(PATH2,script)
if __name__ == '__main__':
    prettyrdf('FINAL.rdf','金庸小说人物知识图谱.rdf')