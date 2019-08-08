from dic import order_dic,chat_dic


class CnMsgProcess:
    order_list=''
    chart_list=''
    
    def __init__(self,msg,cn_order_list,cn_chart_list):
        order_list=cn_order_list
        chart_list=cn_chart_list

    def cn_msg_process(self):
        _from_username=self.fromusername
        if chat_list.get(_from_username) is None: 
            # 先判断是否在chat_list

            __text = self.Text
            if __text[0] != '#':
                return '不是命令'
            else:
                __text_split = __text.split(' ') 
                # 分列后[命令,参数……]
                # 先判断是否为字典内的命令
                
                if  order_dic.get(__text_split[0].lower()) is not None:
                    # 判定为有效的命令，才从这里真正处理指令
                    
                    # -------------
                    #
                    # param_count = order_dic_search.get('param_count') # param_count为改命令所需的参数个数
                    # for i in reversed(range(len(cn_text_split))):
                    #     if cn_text_split[i] == ''
                    #         cn_text_split.remove('')
                    # if len(cn_text_split) < param_count+1: # 参数不足,需要转对话获取
                    #     return P2VChat.type_find_first(order_dic_search,cn_text_split,chat_list,cn_from_username) # 传入字典+数组+字典：{命令，参数个数，参数字典},[命令,参数1，参数2，……],{待处理命令清单},发送人)
                    # elif len(cn_text_split) > param_count+1:
                    #     return str(cn_text_split[0])+'命令需要'+str(param_count)+'个参数，但实际传入了'+str(len(cn_text_split)-1)+'个,请修改'
                    # else:
                    #     # （待处理）有参数充足，需要核实对应的属性，无误后转对应的处理函数
                    #     return str(order_dic_search)+','+str(cn_text_split)


                    #--------------

                elif __order_dic_search is None:
                    return '不是可用的命令'
        else:
            _text=self.Text
            if _text[0] == '#' and  chat_dic[_from_username].get(_text[0]) is None:
                __text_split = __text.split(' ') 
                # 分列后[命令,参数……]

                __order_dic_search = order_dic.get(__text_split[0].lower())
            else:


        # cn_nickname=msg.NickName #单聊好似没有这个




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
