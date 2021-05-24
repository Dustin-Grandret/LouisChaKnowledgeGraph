
class Rule_basic():
    def _run(self, args):
        '''
        接口说明：
        0.类命名规则：rule数字，数字对应ppt中rdf后面数字
        派生类请单独写在一个文件中，本文件下的类作为例子。
        1.在本函数中需要完成的工作：根据给定三元组组成的列表（abox，tbox），按照当前函数所执行的规则编写输出两个新三元组组成的列表的接口。两个新三
        元组分别为abox和tbox。新三元组中不包含原三元组列表的内容。不需要去重。
        2.本函数执行的操作是按照当前规则，将生成的三元组全部输出
        :param args: [
        参数规定：
        'tbox':tbox,
        'abox':abox
        可以按照 rule数字_参数名 添加新键，命名规则保证不重名
        ]
        trule[0]:头，trule[1]:边，trule[2]:尾
        arule[0]:头，arule[1]:边，arule[2]:尾

        迭代器命名建议：trule对应tbox的迭代器，arule对应abox的迭代器。

        :return:返回值建议命名为rst_abox,rst_tbox

        type 省略前缀
        3.TODO:本函数所完成的逻辑规则(需填写)
        '''
        raise NotImplementedError()

    def run(self, args):
        raw_rst_abox, raw_rst_tbox = self._run(args)
        rst_abox, rst_tbox = [], []
        for elem in raw_rst_abox:
            if elem not in args['abox']:
                rst_abox.append(elem)
        for elem in raw_rst_tbox:
            if elem not in args['tbox']:
                rst_tbox.append(elem)
        return rst_abox, rst_tbox