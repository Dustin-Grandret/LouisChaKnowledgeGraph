def printbox(box):
    print('abox===================')
    for elem1 in box[0]:
        print(elem1)
    print('tbox===================')
    for elem2 in box[1]:
        print(elem2)
    print('=======================')
def equivalenttriple(equal_a,equal_b,tran):
    if equal_a in tran:
        return tuple([elem if elem !=equal_a else equal_b for elem in tran])
    elif equal_b in tran:
        return tuple([elem if elem !=equal_b else equal_a for elem in tran])
    return None
def noNoneappend(a,key):
    if key!=None:
        a.append(key)
    return a

import json
def savedict(Adict,PATH1):
    data=json.dumps(Adict,ensure_ascii=False)
    with open(PATH1,'w',encoding='utf-8')as f:
        f.write(data)

def boxmap(Adict,boxes:dict):
    '''
    boxes:[abox,tbox]
    :param Adict:
    :param boxes:
    :return:
    '''
    rst_abox,rst_tbox=boxes[0][:],boxes[1][:]
    tran=[rst_abox,rst_tbox]
    for i,box in enumerate(boxes):
        checklist = []
        for elem1 in Adict.items():
            checklist.append(elem1[0])
        for i1,elem1 in enumerate(box):
            for i2,elem2 in enumerate(elem1):
                if elem2 in checklist:
                    tran[i][i1][i2]=Adict[elem2]
    return tran



