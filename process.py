from dic import order_dic
import string


class CnMsgProcess:
    def __init__(self, cn_order_list, cn_chat_list):
        self.order_list = cn_order_list
        self.chat_list = cn_chat_list
        # order_list = {}
        # chat_list = {}

    def cn_msg_process(self,msg):
        _from_username = msg.FromUserName
        _text = msg.Text.strip()
        _text_split = _text.split(' ')
        # 分列后[命令,参数……]
        # 先判断是否为字典内的命令

        while ' ' in _text_split:
            _text_split.remove(' ')
        _order_name = _text_split[0].lower()
        if self.chat_list.get(_from_username) is None:
            # 先判断是否在chat_list

            if _text[0] != '#':
                return None
                # 不是命令，所以不回复（None)
            else:
                # Todo:a01
        
                if order_dic.get(_order_name) is not None:
                    # 判定为有效的命令，才从这里真正处理指令`
                    # Todo:a05
             
                    pass
                    # 多个分支汇总到a05

                else:
                    return '%s不是可用的命令' % _order_name
        else:
            if _text[0] == '#' and  self.chat_list[_from_username].get(_text[0]) is None:     
                # Todo:a01

                if order_dic.get(_order_name) is not None:
                    # Todo:a05

                    pass
                    # 多个分支汇总到a05

                else:
                    return '不是可用的命令'

            else:
                # Todo:a03
                return "ToDo:a03"
        
        # a05:

        _result_process_a05 = CnMsgProcess.process_a05(_text_split, _order_name)
        print(_result_process_a05)
        # 获取输入的参数对比命令要求后参数的结果
        # 格式为： {1:'abc',3:'cde'……}

        if _result_process_a05 is None:
            return '%s的参数不正确' % _order_name
        elif type(_result_process_a05) == list:
            if _result_process_a05[0] == 'error401':
                return  '该命令需要输入%s个参数，但实际输入了%s个' % (_result_process_a05[1],_result_process_a05[2])
        # else:

        _param_operation_dic = {}
        # _param_operation_dic 为合并到chat_dic或order_dic前的过渡字典

        for _i in range(order_dic.get(_order_name)['param_count']):
            #  _i 是从0开始，而_result_process_a05的格式为：{1: '12345678901'}
            # 所以需要_i+1

            if _result_process_a05.get(_i+1) is not None:
                # 仅在参数输入有效的情况下生效，其他情况返回的是文字错误

                _param_operation_dic.update({_i: _result_process_a05.get(_i+1)})
                self.chat_list.setdefault(_from_username, {}).setdefault(_order_name, {}).update(_param_operation_dic)
                # 将本次输入的参数合并到对话列表中，如果有新增则补充，重复也覆盖，没涉及到的则不影响
                # 格式为：{fromusernane:{order name:{1:'ABC',3•••}}}
                # 格式为：{1:'ABC',3:...} 2没数值，所以留空

            else:
                pass

#        if len(self.chat_list.get(_from_username).get(_order_name)) ==

    def process_a05(self,order_name):
        _text_split=self
        _order_dic_result = order_dic[order_name]
        # 常用数据

        if _text_split[0][0] == '#':
            _text_split.remove(_text_split[0])
        if len(_text_split) != 0:
            # Todo:a06

            if len(_text_split) > _order_dic_result['param_count']:
                return ['error401',_order_dic_result['param_count'], len(_text_split) ]
            else:
                _property_kinds = {}
                _i = 0
                while _i < _order_dic_result['param_count']:
                    _i = _i + 1
                    _property_kinds.update(_order_dic_result[_i].get('property'))
                _result_a06 = CnMsgProcess.process_a06(_text_split, _property_kinds)
                # 返回每个输入的参数的属性值

                _result_a08 = CnMsgProcess.process_a08(_result_a06, _order_dic_result)
                # 返回输入参数与命令要求的参数的对比结果
                # 格式为字典：{1:0,2:1,……,N:M第N个命令函数的值是对应第M个输入函数}

                if _result_a08 != {}:
                    _result_param_available = {}
                    for _i in _result_a08.items():
                        _result_param_available.update({_i[0]: _text_split[_i[1]]})
                    return _result_param_available

        else:
            # Todo:a07
            print('todo07')
            pass

    def process_a06(self,param_property_kinds):
        _text_split = self
        result = {}
        # result为输入的参数对应的类型的查询结果

        _i = -1
        for _param in _text_split:
            _i = _i + 1
            result.update({_i:{}})
            # 第一个输入参数起始序号为0

            for _property_name in param_property_kinds:
                if _property_name == 'type':
                    if _param.isnumeric():
                        result[_i].update({_property_name: int})
                    elif _param.islower() or _param.isupper():
                        result[_i].update({_property_name: str})
                    else:
                        result[_i].update({_property_name: ''})
                elif _property_name == 'length':
                    result[_i].update({_property_name: len(_param)})
                elif _property_name == 'first_num':
                    result[_i].update({_property_name: _param[0]})
        return result

    def process_a08(self, _order_require):
        _input_property = self
        # input_property：输入参数的属性种类字典，与_text_split=self顺序一致
        # 格式例子：
        # {
        #     0:{'type': int, 'length':13, 'first_num': '1'},
        #     1:{……}
        # }

        # order_require：命令的字段（order_dic[order_name]），包含property字典，获取要求的属性种类
        # 格式例子：
        # {
        #    'id': 1001,
        #    'param_count': 1,
        #     1: {
        #         'name': 'phoneNum',
        #         'property': {'type': int, 'length': [13, 11], 'first_num': '1'},
        #     },
        #     2:{
        #         'name': '……',
        #         'property':'……'
        #     }
        # }

        match_result = {}
        # 代表命令要求的参数是否已经知道了匹配的输入参数，''代表没找到，数字代表找到

        _i = 0
        while _i < _order_require['param_count']:
            # 思路：目前采用忽略多余的输入参数，即加入输入参数不匹配，不报错，只保存匹配的参数
            #     并在之后的步骤a0X找到那些命令参数还没有数值。
            _i = _i + 1
            _param_id = _order_require[_i]
            # _param_id 命令要求的参数字典
            # 格式例子：
            # {
            #     'name': 'phoneNum',
            #     'property': {'type': int, 'length': [13, 11], 'first_num': '1'},
            # }

            for _j in _input_property:
                # _j 为输入参数的id

                _input = _input_property[_j]
                # 输入的参数属性种类明细
                # 格式为：{'type': int, 'length':13, 'first_num': '1'}

                _param_id_property = _param_id['property']
                # _param_id_property 命令要求的属性明细
                # 格式为：{'type': int, 'length':[11,13], 'first_num': '1'}

                _is_match = 1
                # 代表匹配结果，0代表没找到，1代表找到

                for _k in _param_id_property.items():
                    # _k格式为：('type',int)  ('length',[11,13])

                    if type(_k[1]) == list:
                        if _input.get(_k[0]) not in _k[1]:
                            _is_match = 0
                    else:
                        if _k[1] != _input.get(_k[0]):
                            _is_match = 0

                # 如果循环结束后_is_match还是1,证明地_j个输入参数符合第_i个命令参数的全部要求

                if _is_match == 1:
                    match_result.update({_i: _j})
                    break

        return match_result















        # cn_nickname=msg.NickName #单聊好似没有这个





# -------------
#                  # if len(cn_text_split) < param_count+1: # 参数不足,需要转对>话获取                                                                                               #     return P2VChat.type_find_first(order_dic_search,cn_text
# _split,chat_list,cn_from_username) # 传入字典+数组+字典：{命令，参数个数，参数字>
# 典},[命令,参数1，参数2，……],{待处理命令清单},发送人)                                                 # elif len(cn_text_split) > param_count+1:
#                     #     return str(cn_text_split[0])+'命令需要'+str(param_count
# )+'个参数，但实际传入了'+str(len(cn_text_split)-1)+'个,请修改'
#                     # else:
#                     #     # （待处理）有参数充足，需要核实对应的属性，无误后转对>应的处理函数
#                     #     return str(order_dic_search)+','+str(cn_text_split)
#                                                                                                      #--------------
#
#
#
# class P2VChat:
#     def type_find_first(self,cn_text_split,chat_list,cn_from_username): # 第一次对话
#
#         cn_order_id = self.get('id')
#         cn_param_count = self.get('param_count')
#         cn_order_name = cn_text_split[0]
#         cn_param_ready_list = {}  # 汇总已经确认了那些参数，最终要传入chat_list保存
#         i=cn_param_count
#         # 将order_dic的参数转移到cn_param_ready_list
#         while i>0:
#             i=i-1
#             cn_param_ready_list[i]=order_dic.get(i)
#         # =========================================
#         cn_param_array = cn_text_split.remove(cn_order_name) # 获取全部参数
#         if len(cn_param_array) == 0:
#             chat_list[cn_from_username] = {'order_name':cn_order_name}
#             return cn_param_ready_list[1]['param_name']:
#
#         #
#         # for i in cn_param_array:
#         #
#         # j = cn_param_count-len(cn_param_array)
#         # #先判断那里
#         # while i > 0:
#         #     i=i-1
#         #
#         #
#         #
#         #
#         # cn_operation_plan={'order_id':cn_order_id} # cn_operation_plan是最终传给操作环节的字典
#
#
#         # if cn_order_id == 1001:
