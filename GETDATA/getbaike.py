from includefile import *
import time
def get_savehtml(url,saveroot,name):
    '''
    抓取网页并且将html存到本地备用，在saveroot下以name.html为名存储数据,抗干扰机制在getpage中。
    :param url:
    :param saveroot:
    :param name:
    :return: 返回网页数据
    '''
    rst=getpage(url)
    with open(saveroot+f'{name}.html','w',encoding='utf-8')as f:
        f.write(rst)
    print('Web page capture [{}] complete'.format(name))
    return rst
#get_savehtml('https://www.baidu.com/','F:\课程资料\pythonProject\\','test')
class characterlist_base():
    '''
    这个类用来继承，必须实现：
    generate_url(self,args)
    get_relative_character(self,args)
    '''
    def start(self):
        self.pointer=0
        self.namedict=dict()
        self.namelist=[]
        self.validnamelist=[]
    def _init_namelist_dict(self,namelistroot):
        '''
        按照文本内容返回最原始的人物列表。
        **最后的去重操作会将顺序打乱，所以不可重复操作**
        :param namelistroot: 储存人物列表的json文件地址
        json文件要求：键存储书名，值存储列表，列表内为人名，人名以字符串给出
        :return:无                       #TODO:True为读取文件成功，False为失败
        '''
        with open(namelistroot,'r',encoding='utf-8')as f:
            self.namedict=eval(f.read())
            for value in self.namedict.values():
                self.namelist.extend(value)
        self.namelist=list(set(self.namelist))
        print('将{} 作为人物列表导入完成'.format(namelistroot))
    def init_all(self,namelistroot):
        self.pointer=0
        self._init_namelist_dict(namelistroot)
        self.validnamelist = []
    def generate_url(self,args=dict()):
        raise NotImplementedError()
    def findbookname(self,charactername):
        for key,value in self.namedict.items():
            if charactername in value:
                return key
        return ''
    def deal_no_jump(self,args:dict):
        raise NotImplementedError()
    def get_relative_character(self,args=dict()):
        raise NotImplementedError()
    def cleannames(self):
        raise NotImplementedError()
    def run(self,args:dict):
        '''
        模板方法,获得所有人物的百科html文件
        saveroot,host_url,namelistroot
        :param args:
        :return:
        '''
        self.start()
        self.init_all(args['namelistroot'])
        while True:
            if self.pointer>=len(self.namelist):
               break
            else:
                #输出前先清空输出
                os.system('cls')
                print('已经爬完{},当前进度<={:.2%}'.format(self.pointer,self.pointer/len(self.namelist)))
            url=self.generate_url(args)
            rawdata=get_savehtml(url,args['saveroot'],self.namelist[self.pointer])
            if rawdata!="":#爬取出了结果
                rawdata=self.deal_no_jump(args={
                    'data':rawdata,
                    'charactername':self.namelist[self.pointer],
                    'saveroot':args['saveroot'],
                    'host_url':args['host_url']
                })
                if rawdata==-1:
                    self.pointer+=1
                    continue
                self.validnamelist.append(self.namelist[self.pointer])#找到哪些人名有词条
                names=self.get_relative_character({'data':rawdata})
                names=self.cleannames({'dirty_characters':names})
                for name in names:
                    if name not in self.namelist:
                        self.namelist.append(name)
            self.pointer += 1
            time.sleep(rand.randint(1,10)/10)
    def __str__(self):
        return str(
            dict(
                {
                    'pointer':self.pointer,
                    'namelist':self.namelist,
                    'namedict':self.namedict,
                    'validnamelist':self.validnamelist
                }
            )
        )

class LouisCha_characterlist(characterlist_base):
    def generate_url(self, args):
        return f'https://baike.baidu.com/item/{tranchinise(self.namelist[self.pointer])}'
    def get_relative_character(self, args):
        '''#获取人名（脏数据）
        df = pd.read_html(args['data'])[0]
        return list(df['人名'])'''#不够直接
        pat='''<li class="lemma-relation-item">.*?<span class="title">(.*?)</span>.*?</li>'''#抽人物关系
        return re.compile(pat,re.S).findall(args['data'])
    def is_clean(self,string):
        return string.find(':') == -1 and string.find('（') == -1 and\
        string.find('）') == -1 and string.find('  ')==-1 and\
        string.find('、')==-1
    def cleannames(self,args:dict):
        # TODO:清理数据，样例：['父亲：黄药师  母亲：冯氏（小字阿衡）', '郭靖', '郭芙、郭襄、郭破虏', '洪七公', '郭啸天', '李萍', '杨过', '耶律齐', '穆念慈、周伯通', '双雕、小红马、血鸟（连载版）']
        dirty_characters=args['dirty_characters']
        clean_characters=[]
        for dirty_character in dirty_characters:
           #思路是把连续的中文挑出来，如果挑出非人名也无妨，因为deal no jump会将其去掉
            tran=re.compile('([\u4e00-\u9fa5]+)').findall(dirty_character)
            clean_characters.extend(tran)
        return clean_characters
    def _nobookappearance(self,args):
        for elem in self.namedict.keys():
            if args['data'].find(elem)!=-1:
                return False
        return True
    def deal_no_jump(self,args:dict):
        '''
                这部分较为困难。
                没有找到词条也在这里处理
                :param args:
                data
                charactername
                saveroot
                host_url
                :return:
                '''
        if args['data'].find('金庸') == -1 and self._nobookappearance(args):  # 如‘冯氏’，搜出来不是金庸小说人物
            '''
            此处不能只写含"金庸"，如"谭婆：小说《天龙八部》中的人物"
            '''
            return -1
        elif args['data'].find('keywords') == -1:
            '''
            #找字串，-1为对象字符串不含参数字符串，其他值为索引
            #百科搜索可能页面跳转，找规律发现未跳转的页面没'keyword'字符串
            '''
            # TODO:通过返回码判断是否跳转更安全
            '''
            找规律发现金庸人物的目录下含书名,用人物找书名
            '''
            if args['data'].find('百度百科尚未收录词条') != -1:
                return -1

            else:
                newurl = ''
                polysemous_words = strongpat(args['data'], {
                    'for_polysemous': '<div class="para" label-module="para"><a(.*?)</a>[\s]*</div>'  # 识别多义词,把链接也拉过来
                }, re.S)

                for elem in polysemous_words[0]:
                    if elem.find('金庸') != -1 or elem.find(
                            self.findbookname(args['charactername'])) != -1:  # 认为结果含有金庸 或是书名就是索要查找结果
                        tran = re.compile('href="(.*?)"').findall(elem)  # 找链接
                        newurl = args['host_url'] + tran[0][1:]
                        return get_savehtml(newurl, args['saveroot'], args['charactername'])

        return args['data']
    def _getinfobox(self,args:dict):
        '''
        百度百科的html文档中infobox有多种格式,需要多种正则表达式进行提取。本函数提供了一个比较有效的方法。
        这一部分是这样完成的：
        1.首先创建测试函数，测试函数会将正则表达式提取为空的文档输出，并输出提取失败的文档个数
        2.根据提取失败的文档写出新的正则表达式添加在pats里
        3.本函数会循环迭代pats，使得文档尽可能多地匹配
        4.注意将较偏的提取规则放在列表的后面，以防其他html使用较偏的提取规则提取，如公孙绿萼.html的infobox不够规范，只能使用如pats[4]的提取规则提取
        :param args:
        :return:
        '''
        pats=['''<dt class="basicInfo-item name">(.*?)</dt>[\s]*<dd class="basicInfo-item value">[\s]*(.*?)[\s]*</dd>''',
              '''<li class="basicInfo-hide">[\s]*<div class="info-title">(.*?)</div>[\s]*<div class="info-content".*?>(.*?)</div>[\s]*</li>''',
              '''<li>[\s]*<div class="info-title">(.*?)</div>[\s]*<div class="info-content".*?>(.*?)</div>[\s]*</li>''',
              '''<p>[\s]*<strong>(.*?)</strong>(.*?)</p>''',
              '''\n([\u2E80-\u9FFF]*?)：(.*?)<br />''']

        for pat in pats:
            tran=re.compile(pat,re.S).findall(args['data'])
            if tran!=[]:
                rst=tran[:]
                return [(args['name'],rst[i][0],rst[i][1]) for i in range(len(rst))]
    def test_getinfobox(self,args,key):
        count=0
        for elem in self.getzip(args):
            if self._getinfobox(elem)==None:
                count+=1
                print(elem['name'])
        print(count)
    def getzip(self,args:dict):
        for elem in os.listdir(args['rawdataroot']):
            yield {'name':elem[:-5],
                    'data':open(args['rawdataroot']+elem,'r',encoding='utf-8').read()}
    def get_triple(self,args:dict):
        import zipfile
        zipfile_path = ''
        trandict=geti2c()
        with zipfile.ZipFile(args['rawdataroot'], mode='r') as zfile:  # 只读方式打开压缩包
            for name in zfile.namelist():  # 获取zip文档内所有文件的名称列表
                with zfile.open(name, mode='r') as single_file:
                    yield self._getinfobox(args={'name':trandict[name[:-5]],'data':single_file.read()})
    def getinfobox(self,args):
        target=open('../test.csv', 'a', encoding='utf-8')
        writer=csv.writer(target)
        for newargs in self.getzip(args):
            tran=self._getinfobox(args=newargs)
            if tran:
                for triple in tran:
                    writer.writerow(triple)
        target.close()



if __name__ == '__main__':
    '''
    #1.建立一个原始的人物名单
    #2.下载人物名单中所有人物对应的百科文档，每下载一个人物，人物名单去除一个人
    #3.分析得到的百科文档，生成出新的人物列表
    #4.回到2，直到人物名单为空
    '''
    r'''    tran=characterlist_base()
    tran.run(args={
        'namelistroot':r'F:\课程资料\pythonProject\character_test.json',
        'saveroot':r'F:\课程资料\pythonProject\rawdata\\'
    }
    )
    print(str(tran))'''
    '''tran=LouisCha_characterlist()
    for elem in tran.get_triple(args={
        'rawdataroot':r'F:\课程资料\pythonProject\rawdata_tran.zip'
    }):
        print(elem)'''
    #使用下面一段代码运行
    tran=LouisCha_characterlist()
    try:
        """tran.run(args={
            'host_url':r'https://baike.baidu.com/',
            'saveroot':r'F:/课程资料/pythonProject/rawdata//',
            'namelistroot':r'F:/课程资料/pythonProject/character.json'
        })"""
        tran.getinfobox(args={
            'rawdataroot':PROJECTROOT+'rawdata_tran\\'
        })
        """tran.test_getinfobox(args={
            'rawdataroot':PROJECTROOT+'rawdata_tran\\'
        },key=1)"""

    except Exception as e:
        print(e)
        with open(PROJECTROOT+'log.txt', 'w', encoding='utf-8') as f:
            f.write(str(tran))
    #get_savehtml(f'https://baike.baidu.com/item/{tranchinise("黄蓉")}','F:\课程资料\pythonProject\\','test')


