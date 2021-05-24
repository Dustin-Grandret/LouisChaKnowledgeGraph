from TI.rules import *
from TI.typeinference import typeInference
def test1(rule,args=[]):
    abox = [
        ('郭靖', '学习', '飞檐走壁'),
        ('黄蓉', '嫁给', '郭靖'),
        ('郭靖', '嫁给', 'asd')
    ]
    tbox = [
        ('学习', 'domain', '人类'),
        ('嫁给', 'domain', '女性'),
        ('学习', 'range', '武功'),
        ('嫁给', 'range', '男性'),
        ('嫁给', 'type', 'owl:transitiveproperty')
    ]
    abox,tbox=rule().run(args={
        'abox':abox,
        'tbox':tbox
    } if args == [] else args)
    print(list(set(abox)),list(set(tbox)))

def test2(args=[],is_show=False):
    rules=[
        rule1(),
        rule2(),
        rule3(),
        rule4(),
        rule5(),
        rule6(),
        rule7(),
        rule8(),
        rule9(),
        rule10(),
        rule11(),
        rule13(),
        rule_owl_1(),
        rule_owl_2(),
        rule_owl_4(),
        rule_owl_3(),
        rule_owl_5()
    ]
    typeInference_test=typeInference()
    typeInference_test.start(rules)
    abox = [
        ('我','吃','饭'),
        ('我','吃','米')
    ]
    tbox = [
        ('吃','owl:sameas','恰'),
        ('吃','owl:inverseof','被吃'),
        ('owl:inverseof','type','owl:symmetricproperty')
    ]
    abox,tbox=typeInference_test.TI(args={
        'abox': abox,
        'tbox': tbox}if args == [] else args)
    abox=list(set(abox))
    tbox = list(set(tbox))
    if is_show:
        printbox(list((abox,tbox)))
    return abox,tbox
if __name__ == '__main__':
    test1(rule2)
    test2()