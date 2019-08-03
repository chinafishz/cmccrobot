import json

order_dic={
    # 1001~1100 分配为查询用途
    '#puk':
        {'id': 1001,
            'param_count': 1,
            1: {'param_name': 'phoneNum','param_type': int},
         },
    '#查实名':
        {
            'id': 1002,
            'param_count': 1,
            1: {'param_name': '电话号码', 'param_type': int},
        }
}