from dic import order_dic


class CnMsgProcess:
    def cn_msg_process(self,cn_from_username,chat_list):
        if chat_list.get[cn_from_username] is None:  # 先判断是否在chat_list
            cn_text = self.Text
            if cn_text[0] != '#':
                return '不是命令'
            else:
                cn_text_split = cn_text.split(' ') # cn_text_temp 为msg.text分列后[命令,参数……]
                # 先判断是否为字典内的命令
                order_dic_search = order_dic.get(cn_text_split[0].lower())#返还一个字典，第一个为指令代码，第二个为次指令需要有几个参数
                if order_dic_search is not None: # 判定为有效的命令，才从这里真正处理指令
                    param_count = order_dic_search.get('param_count') # param_count为改命令所需的参数个数
                    for i in reversed(range(len(cn_text_split))):
                        if cn_text_split[i] == '':
                            cn_text_split.remove('')
                    if len(cn_text_split) < param_count+1: # 参数不足,需要转对话获取
                        return P2VChat.cn_chat_find(order_dic_search,cn_text_split,chat_list)#传入字典+数组+字典：{命令，参数个数，参数字典},[命令,参数1，参数2，……],{待处理命令清单})
                    elif len(cn_text_split) > param_count+1:
                        return str(cn_text_split[0])+'命令需要'+str(param_count)+'个参数，但实际传入了'+str(len(cn_text_split)-1)+'个,请修改'
                    else:
                        # （待处理）有参数充足，需要核实对应的属性，无误后转对应的处理函数
                        return str(order_dic_search)+','+str(cn_text_split)
                elif order_dic_search is None:
                    return '不是字典里的命令'

        # cn_nickname=msg.NickName #单聊好似没有这个


class P2VChat:
    def type_find(self,cn_text_split,chat_list):
        cn_order_id = self.get('id')
        cn_param_count = self.get('param_count')
        cn_param_array = cn_text_split.remove(cn_text_split[0]) # 获取全部参数
        cn_param_ready_list = {}  # 汇总意见确认了那些参数，最终要传入chat_list保存
        i = cn_param_count
        while i > 0:
            i=i-1




        cn_operation_plan={'order_id':cn_order_id} # cn_operation_plan是最终传给操作环节的字典


        # if cn_order_id == 1001:
