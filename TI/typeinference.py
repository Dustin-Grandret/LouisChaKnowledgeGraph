class typeInference():
    def start(self,rules):
        self.IE=rules
        pass
    def retranslate(self):
        pass
    def TI(self,args):
        rst_abox,rst_tbox=args['abox'],args['tbox']
        counter=1
        import time
        timer=[]
        curtime=time.time()
        while(True):
            new_abox,new_tbox=[],[]
            for rule in self.IE :
                tran=rule.run(args={
                    'abox':rst_abox,
                    'tbox':rst_tbox
                })
                new_abox.extend(tran[0])
                new_tbox.extend(tran[1])

            if len(new_abox)==0 and len(new_tbox)==0:
                break
            rst_abox.extend(new_abox)
            rst_tbox.extend(new_tbox)
            #外层去重
            rst_abox=list(set([tuple(elem) for elem in rst_abox]))
            rst_tbox = list(set([tuple(elem) for elem in rst_tbox]))
            tran=time.time()-curtime
            timer.append(tran)
            print('第{}次迭代,消耗时间:{:.2f}s'.format(counter,tran))
            counter+=1
        print('总耗时:{:.2f}s'.format(sum(timer)))
        return rst_abox, rst_tbox
