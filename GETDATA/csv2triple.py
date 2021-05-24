
'''
将属性的csv文件转换为abox和tbox
'''
from GETDATA import *
import csv
col2int={
    'id':0,
    '属性':1,
    'domain':2,
    'range':3,
    'is_transitive':4,
    'is_symmetric':5,
    'is_functional':6,
    'inverseof':7,
    'inversefunctional':8,
    'sameas':9,
    'subpropertyof':10,
}
def getvalue(elem,name):
    return elem[col2int[name]]
rst_abox,rst_tbox=[],[]

name2id=dict()
with open(PROFILE_ROOT,'r',encoding='utf-8')as f:
    writer=csv.reader(f)
    for i,elem in enumerate(writer):
        if i==0:
            continue
        rst_abox.append((getvalue(elem,'id'),'name',getvalue(elem,'属性')))
        name2id[getvalue(elem,'属性')]=getvalue(elem,'id')

with open(PROFILE_ROOT, 'r', encoding='utf-8')as f:
    writer = csv.reader(f)
    for i,elem in enumerate(writer):
        if i==0:
            continue
        try:
            rst_tbox.append(((getvalue(elem,'id'),'rdfs:domain',getvalue(elem,'domain'))))
            rst_tbox.append(((getvalue(elem, 'id'), 'rdfs:range', getvalue(elem, 'range'))))
            if getvalue(elem,'is_transitive')==1:
                rst_tbox.append((getvalue(elem, 'id'), 'type','owl:transitiveproperty'))
            if getvalue(elem, 'is_symmetric') == 1:
                rst_tbox.append((getvalue(elem, 'id'), 'type', 'owl:symmetricproperty'))
            if getvalue(elem, 'is_functional') == 1:
                rst_tbox.append((getvalue(elem, 'id'), 'type', 'owl:functionalproperty'))
            if getvalue(elem, 'inverseof'):
                rst_tbox.append((getvalue(elem, 'id'), 'owl:inverseof',name2id[getvalue(elem,'inverseof')]))
            if getvalue(elem, 'inversefunctional') == 1:
                rst_tbox.append((getvalue(elem, 'id'), 'type', 'owl:inversefunctionalproperty'))
            if getvalue(elem, 'inverseof'):
                rst_tbox.append((getvalue(elem, 'id'), 'owl:sameas',name2id[getvalue(elem,'sameas')]))
            if getvalue(elem, 'subpropertyof'):
                rst_tbox.append((getvalue(elem, 'id'), 'rdfs:subpropertyof',name2id[getvalue(elem,'subpropertyof')]))
        except Exception as e:
            print(i,elem)
            print(e)
    print(rst_abox,rst_tbox)