'''ROOT=R'F:\课程资料\20-21长学期2课程\数据挖掘\新建文件夹\train\\'
NAME=R'000e04d6-d6ef-442f-b070-4309493221ba.json'
data=''
with open(ROOT+NAME,'r',encoding='utf-8')as f:
    tran=f.read()
    data=eval(tran)
import re
tran=[]
for i,elem in enumerate(data):
    tran.extend(re.compile(' [A-Za-z]+? ').findall(elem['text']))

def firsthigh(a):
    if a[i] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        return True
for i,elem in enumerate(tran):
    if firsthigh(tran[i]):
        flag=False
        j=i+1
        rst=[]
        while(flag and j<len(tran)):
            if firsthigh(tran[j]):
                pass
print(list(set(tran)))
'''
import random
def MonteCarloIntergrity(function,a,b,n):
    return sum([function(random.uniform(a,b)) for i in range(n)])/n*(b-a)

import math
def func1(x):
    return math.exp(-(x**2))
def func2(x):
    return x**2
def func3(x):
    return x*math.sin(x)

def SymmetricDifference(function,x,h):
    return (function(x+h)-function(x-h))/2/h

def func4(x):
    return 2*x+1
if False:
    for i in range(8):
        h=0.1**i
        print('h:{}'.format(h))
        print(SymmetricDifference(func4,6,h))

class OptimalStopping():
    def observation(self,curlist,t):
        return max(curlist[0:t+1])
        pass
    def decay(self,curlist,alpha='None'):
        if alpha!='None':
            pass
        return curlist
    def OptimalStopping_test(self,curlist,t,alpha):
        curlist=self.decay(curlist,alpha)
        observe=self.observation(curlist,t)
        for i in range(t+1,len(curlist)-1):
            if curlist[i]>=observe:
                return i
        return len(curlist)
    def getlist(self,a,b,n):
        return [random.uniform(a,b) for i in range(n)]
    def getObtimalStopping(self,a,b,length,n,alpha):
        rst=[]
        for i in range(n):
            tran=[self.OptimalStopping_test(self.getlist(a,b,length),j,alpha) for j in range(length)]
            rst.append(tran.index(max(tran)))
        print(rst)
        print(sum(rst)/len(rst))
        tran1=list(set(rst))
        tran2=[rst.count(x) for x in tran1]
        print(tran2.index(max(tran2)))
        print(tran1)
        print(tran2)


test=OptimalStopping()
test.getObtimalStopping(1,10,5,5000,'None')