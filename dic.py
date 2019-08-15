import json

order_dic = {
    # 1001~1100 分配为查询用途
    '#puk':
        {
            'id': 1001,
            'param_count': 1,
            1: {
                'name': 'phoneNum',
                'property': {'type': int, 'length': [13,11], 'first_num': '1'},
                }
        },
    '#查实名':
        {
            'id': 1002,
            'param_count': 3,
            1: {
                'name': 'phoneNum',
                'property': {'type': int, 'length': [13,11], 'first_num': '1'},                                 },
            2: {
                'name': 'phoneNum2',
                'property': {'type': int, 'length': [13,11], 'first_num': '1'},                                 },
            3: {                                                                                                'name': 'phoneNum2',
                'property': {'type': int, 'length': [13,11], 'first_num': '1'},                                 }
        }
    }


