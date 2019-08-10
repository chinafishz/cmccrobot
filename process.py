from dic import order_dic,chat_dic


class CnMsgProcess:
    order_list={}
    chart_list={}

    def __init__(self,msg,cn_order_list,cn_chart_list):
        self.order_list=cn_order_list
        self.chart_list=cn_chart_list

    def cn_msg_process(self):
        _from_username=self.fromusername
        if CnMsgProcess.chart_list.get(_from_username) is None:
            # 先判断是否在chat_list

            _text = self.Text
            if _text[0] != '#':
                return '不是命令'
            else:
                # Todo:a01

                _text_split = _text.split(' ') 
                # 分列后[命令,参数……]
                # 先判断是否为字典内的命令
                
                _order_name = _text_split[0].lower()
                if order_dic.get(_order_name) is not None:
                    # 判定为有效的命令，才从这里真正处理指令
                    #Todo:a05
             
                    _result = CnMsgProcess.process_a05(_text_split, _order_name)
                    return _result
    
                else:
                    return '不是可用的命令'
        else:
            _text = self.Text
            if _text[0] == '#' and  chat_dic[_from_username].get(_text[0]) is None:            
                # Todo:a01

                _text_split = _text.split(' ') 
                # 分列后[命令,参数……]

                _order_name = _text_split[0].lower()
                if order_dic.get(_order_name) is not None:
                    # Todo:a05

                    _result = CnMsgProcess.process_a05(_text_split,_order_name)
                    return _result

                else:
                    return '不是可用的命令'

            else:
                # Todo:a03
                return 0


    def process_a05(self,order_name):
        _text_split=self
        _order_dic_result = order_dic[order_name]
        # 常用数据

        _param_get_property = {}
        # 命令各参数查询结果

        if _text_split[0][0] == '#':
            _text_split.remove(_text_split[0])
        if len(_text_split) !=0:
            # Todo:a06
        
            if len(_text_split) > _order_dic_result['param_count']:
                return 'param of order need %s ,but you input %s' % (_order_dic_result['param_count'],len(_text_split))

            _result_a06 = CnMsgProcess.process_a06(_text_split,_order_dic_result['property'])
            #返回每个输入的参数的属性值

        else:
            # Todo:a07
            return


    def process_a06(self,param_property):
        _text_split=self
        _result={}
        for _param in _text_split:
            for _property_name in param_property:
                if _property_name == 'type':
                    return 0





        # cn_nickname=msg.NickName #单聊好似没有这个





# -------------
                    #                                                                                # param_count = order_dic_search.get('param_count') # param_c
ount为改命令所需的参数个数
                    # for i in reversed(range(len(cn_text_split))):
                    #     if cn_text_split[i] == ''
                    #         cn_text_split.remove('')                                               # if len(cn_text_split) < param_count+1: # 参数不足,需要转对>话获取                                                                                               #     return P2VChat.type_find_first(order_dic_search,cn_text
_split,chat_list,cn_from_username) # 传入字典+数组+字典：{命令，参数个数，参数字>
典},[命令,参数1，参数2，……],{待处理命令清单},发送人)                                                 # elif len(cn_text_split) > param_count+1:
                    #     return str(cn_text_split[0])+'命令需要'+str(param_count
)+'个参数，但实际传入了'+str(len(cn_text_split)-1)+'个,请修改'
                    # else:
                    #     # （待处理）有参数充足，需要核实对应的属性，无误后转对>应的处理函数
                    #     return str(order_dic_search)+','+str(cn_text_split)
                                                                                                     #--------------



class P2VChat:
    def type_find_first(self,cn_text_split,chat_list,cn_from_username): # 第一次对话

        cn_order_id = self.get('id')
        cn_param_count = self.get('param_count')
        cn_order_name = cn_text_split[0]
        cn_param_ready_list = {}  # 汇总已经确认了那些参数，最终要传入chat_list保存
        i=cn_param_count
        # 将order_dic的参数转移到cn_param_ready_list
        while i>0:
            i=i-1
            cn_param_ready_list[i]=order_dic.get(i)
        # =========================================
        cn_param_array = cn_text_split.remove(cn_order_name) # 获取全部参数
        if len(cn_param_array) == 0:
            chat_list[cn_from_username] = {'order_name':cn_order_name}
            return cn_param_ready_list[1]['param_name']:

        #
        # for i in cn_param_array:
        #
        # j = cn_param_count-len(cn_param_array)
        # #先判断那里
        # while i > 0:
        #     i=i-1
        #
        #
        #
        #
        # cn_operation_plan={'order_id':cn_order_id} # cn_operation_plan是最终传给操作环节的字典


        # if cn_order_id == 1001:
