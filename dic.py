import json

order_dic = {
    '#sms':
        {
            'id': 1,
            'param_count': 2,
            'system': '4a',
            'actual_order': '#4a_sms',
            1: {
                'name': '4A登陆验证码',
                'property': {'type': int, 'length': 6},
            },
            2: {
                'name': 'loginForm码',
                'property': {'type': int, 'length': [19, 20]},
            }
        },
    '#iot':
        {
            'id': 2,
            'param_count': 1,
            'system': '4a',
            'actual_order': '#4a_iot',
            1: {
                'name': '登陆iot',
                'property': {'type': str},
            }
        },
    # 1001~1100 分配为查询用途
    '#puk':
        {
            'id': 1001,
            'param_count': 1,
            'system': 'iot',
            'actual_order':'#puk',
            1: {
                'name': '物联网号码',
                'property': {'type': int, 'length': [13,11], 'first_num': '1'},
                }
        },
    '#查校验码':
        {
            'id': 1001,
            'actual_order': '#puk',
            'param_count': 1,
            'system': 'iot',

            1: {
                'name': '物联网号码',
                'property': {'type': int, 'length': [13, 11], 'first_num': '1'},
            }
        },
    '#查实名':
        {
            'id': 1002,
            'param_count': 1,
            'system': 'iot',
            'actual_order':'puk',
            1: {
                'name': '物联网号码',
                'property': {'type': int, 'length': [13,11], 'first_num': '1'}
            }

        },
    '#查状态':
        {
            'id': 1003,
            'param_count': 1,
            'system': 'iot',
            1: {
                'name': '物联网号码',
                'property': {'type': int, 'length': [13,11], 'first_num': '1'}
            }

        }
    }


