from py2neo import Graph,Node,Relationship
from analysis import *
import numpy as np
import pandas as pd
import random

util = PermisionAnalysisUtil('../result/')
permisions_df = util.permisions_df

class DaoNeo4j():
    def make_graph():
        graph = Graph('http://localhost:7474',username='neo4j',password='111111')
        return graph
    
    def make_node(label,name,explanation=None):
        if explanation is None:
            node = Node(label,name=name)
        else:
            node = Node(label,name=name,explanation=explanation)
        return node
    
    def make_relation(node1,relation,node2):
        relation = Relationship(node1,relation,node2)
        return relation

def make_apk_nodes(apk_names):
    apk_nodes = []
    graph = DaoNeo4j.make_graph()
    for name in apk_names:
#         print(name)
        node = DaoNeo4j.make_node(label='APK',name=name)
        graph.create(node)
        apk_nodes.append(node)
    return apk_nodes
        
def make_permision_nodes(permision_names):
    permision_nodes = []
    graph = DaoNeo4j.make_graph()
    for name in permision_names:
        explanation = util.get_permisions_description(name)[name]
        node = DaoNeo4j.make_node(label='PERMISION',name=name,explanation=explanation)
        graph.create(node)
        permision_nodes.append(node)
    return permision_nodes

def store_apk_permisions(apk_nodes,permision_nodes):
    graph = DaoNeo4j.make_graph()
    for apk_node in apk_nodes:
        for permision_node in permision_nodes:
            apk_name = apk_node['name']
            permision_name = permision_node['name']
            if permisions_df[apk_name][permision_name] == 1:
                relation = DaoNeo4j.make_relation(apk_node,'require',permision_node)
                graph.create(relation)
                
def make_user_nodes(user_names):
    user_nodes = []
    graph = DaoNeo4j.make_graph()
    for name in user_names:
        node = DaoNeo4j.make_node(label='USER',name=name)
        graph.create(node)
        user_nodes.append(node)
    return user_nodes

def get_random_name():
    import random
    xing='赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    ming='豫章故郡洪都新府星分翼轸地接衡庐襟三江而带五湖胜光逸飞智初本汝云伟民佳永宁孝然元霸顺'
    X=random.choice(xing)
    M="".join(random.choice(ming) for i in range(2))
    return X+M

def get_fake_user_apk_info(permisions_df):
    user_apk_info = {}
    for i in range(10):
        user_name = get_random_name()
        fake_permision_df = get_fake_apk_info(permisions_df)
        user_apk_info[user_name] = fake_permision_df
    return user_apk_info
        
def get_fake_apk_info(permisions_df):
    apk_cols = np.random.randint(low=0,high=50,size=np.random.randint(5,30),dtype=np.int16)
    fake_permision_df = pd.DataFrame()
    for col in apk_cols:
        apk_name = permisions_df.columns.values[col]
        apk_permision = permisions_df[apk_name].apply(
                    lambda x:1 if x==1 and np.random.randint(0,2)==0 else 0)
        fake_permision_df[apk_name] = apk_permision
    return fake_permision_df

def store_user_apk_permisions(user_nodes,apk_nodes,permision_nodes,user_apk_info):
    graph = DaoNeo4j.make_graph()
    for user_node in user_nodes:
        fake_permision_df = user_apk_info[user_node['name']]
        for apk_node in apk_nodes:
            if apk_node['name'] in fake_permision_df.columns.values:
                use_relation = DaoNeo4j.make_relation(user_node,'use',apk_node)
                graph.create(use_relation)
                for permision_node in permision_nodes:
                    if fake_permision_df[apk_node['name']][permision_node['name']] == 1:
                        allow_relation = DaoNeo4j.make_relation(apk_node,'allow',permision_node)
                        graph.create(allow_relation)
                        
def store_user_friends(user_nodes):
    graph = DaoNeo4j.make_graph()
    for user_node1 in user_nodes:
        for user_node2 in user_nodes:
            if np.random.randint(0,2) == 1 and user_node1['name'] != user_node2['name']:
                friend_relation = DaoNeo4j.make_relation(user_node1,'friend',user_node2)
                graph.create(friend_relation)
                friend_relation = DaoNeo4j.make_relation(user_node2,'friend',user_node1)
                graph.create(friend_relation)
                
apk_names = permisions_df.columns.values
permision_names = permisions_df.index.values
apk_nodes = make_apk_nodes(apk_names)
permision_nodes = make_permision_nodes(permision_names)
user_apk_info = get_fake_user_apk_info(permisions_df)
user_names = user_apk_info.keys()
user_nodes = make_user_nodes(user_names)

store_apk_permisions(apk_nodes,permision_nodes)
store_user_apk_permisions(user_nodes,apk_nodes,permision_nodes,user_apk_info)
store_user_friends(user_nodes)