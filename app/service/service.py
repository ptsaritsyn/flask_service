from hashlib import sha256
import requests
import json
import datetime
import time
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Service:

    def __init__(self, amount, currency, description):
        self.amount = amount
        self.currency = currency
        self.description = description
        self.payway = "payeer_rub"
        self.method = None
        self.headers = {'Content-Type': 'application/json'}
        self.shop_id = '5'
        self.shop_order_id = int(time.time())
        self.url = None
        self.__sign = None
        self.__secret_key = 'SecretKey01'

# Get data by method
    def get_method_data(self):
        method_list = {
            'bill': {
                        "payer_currency": self.currency,
                        "shop_amount": self.amount,
                        "shop_currency": self.currency,
                        "shop_id": self.shop_id,
                        "shop_order_id": self.shop_order_id,
                        "sign": self.__sign
                    },
            'invoice': {
                            "amount": self.amount,
                            "currency": self.currency,
                            "payway": self.payway,
                            "shop_id": self.shop_id,
                            "shop_order_id": self.shop_order_id,
                            "sign": self.__sign
                        }
        }

        if self.method in method_list:
            return method_list[self.method]

        return {}

# Get data after server response and send to next url
    def send_method_data(self, method_data):
        session = requests.Session()
        res = session.post(self.url, json=method_data, headers=self.headers)
        data = json.loads(res.content)

        return data

# Create sign using sha256 algorithm
    def generate_sign(self, **kwargs):
        sort_dict = {}
        concat_str = ''

        for key in sorted(kwargs):
            sort_dict.update({key: kwargs[key]})
            concat_str += '{}{}'.format(kwargs[key], ':')

        str_result = '{}{}'.format(concat_str[:-1], self.__secret_key)
        str_result = bytes(str_result, encoding='utf-8')
        self.__sign = sha256(str_result).hexdigest()

        return self.__sign

# Write log with current data
    def write_log(self, file_name='logger.log'):
        datetime_obj = datetime.datetime.now()
        with open(BASE_DIR+'/service/logs/'+file_name, 'a') as f:
            s = 'валюта:{},сумма:{},время отправки:{},описание:{},идентификатор:{}\n'.format(self.currency,
                                                                                             self.amount,
                                                                                             datetime_obj,
                                                                                             self.description,
                                                                                             self.shop_order_id)
            f.write(s)
