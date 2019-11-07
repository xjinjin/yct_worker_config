# -*- coding:utf-8 -*-

# Auther:xujinjin
# Date: 2019/9/6 9:20

# 配置好odoo服务端，获取数据库数据.
# 输入url,返回处理代码
from xmlrpc import client

class url_code():
    def __init__(self):
        self.server_url = 'http://192.168.1.240:8069'
        self.db_name = 'test'
        self.model = 'test.test'
        self.username = 'admin'
        self.password = 'admin'
    def url2code(self,url):
        no_query_url = url.split('?')[0]
        search_domain = [('url', '=', no_query_url)]                            # Domains:条件
        common = client.ServerProxy('%s/xmlrpc/2/common' % self.server_url)     # 连接
        user_id = common.authenticate(self.db_name, self.username, self.password, {})  # 认证
        models = client.ServerProxy('%s/xmlrpc/2/object' % self.server_url)     # 数据库接口，需要认证后才能使用
        url_ids = models.execute_kw(self.db_name, user_id, self.password, self.model, 'search',
                                    [search_domain])                            # 搜索，满足条件的id  []
        # print(url_ids)  未知url则url_ids=[]
        if not url_ids:
            # 如果是未知的url，存入postgresql。
            # 这个flow怎么处理？存在队列中，给出方案，在处理
            return 'unkown url'
        else:
            url_code = models.execute_kw(self.db_name, user_id, self.password, self.model, 'read',
                                         [url_ids, ['code']])   # 读数据，根据id返回记录[{}]
            url_code = url_code[0]['code']                      # 数据格式取值  type=str
            return url_code

if __name__ == '__main__':
    # 使用方式
    to_server = 'http://yct.sh.gov.cn/yct_other/tax/saveInputTax3?q=odoo'
    res_code_str = url_code().url2code(to_server)
    print(res_code_str)

# to_server = 'http://yct.sh.gov.cn/yct_other/tax/saveInputTax3?q=odoo'
# no_query_url = to_server.split('?')[0]
#
# server_url = 'http://192.168.1.240:8069'
# db_name = 'test'
# model = 'test.test'
# username = 'admin'
# password = 'admin'
#
# search_domain = [('url', '=', no_query_url)]  # Domains:条件
# common = client.ServerProxy('%s/xmlrpc/2/common' % server_url)  # 连接
# user_id = common.authenticate(db_name, username, password, {})  # 认证
# models = client.ServerProxy('%s/xmlrpc/2/object' % server_url)  # 数据库接口，需要认证后才能使用
# url_ids = models.execute_kw(db_name, user_id, password, model, 'search',
#                             [search_domain])  # 搜索，满足条件的id  []
# # print(url_ids)
# if not url_ids:
#     print('unkown url')
# else:
#     # 如果是未知的url，存入postgresql。
#     # 这个flow怎么处理？存在队列中，给出方案，在处理
#     url_code = models.execute_kw(db_name, user_id, password, model, 'read',
#                                  [url_ids, ['code']])  # 读数据，根据id返回记录[{}]
#     url_code = url_code[0]['code']
#     print(url_code)