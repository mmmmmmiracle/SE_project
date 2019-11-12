import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import json

class Permision(object):
    def __init__(self):
        f =  open('android_all_permisions.json', 'r')
        self.all_permisions_dict = json.load(f)
        self.all_permisions = set(self.all_permisions_dict.keys())
        self.key2index()
        self.index2key()
    
    def key2index(self):
        index = 0
        self.key2index_dict = {}
        for key in self.all_permisions_dict.keys():
            self.key2index_dict[key] = index
            index += 1
    
    def index2key(self):
        index = 0
        self.index2key_dict = {}
        for key in self.all_permisions_dict.keys():
            self.index2key_dict[index] = key
            index += 1

class ApkPermision(Permision):
    def __init__(self,permision_file):
        super(ApkPermision,self).__init__()
        self.name = permision_file.split('\\')[-1].split('.')[0][:-3]
        self.permisions = pd.read_csv(permision_file,header=None,index_col=None)[0].values[:-1]
        
    def permision2array(self):
        res = np.zeros(len(self.all_permisions))
        for permision in self.permisions:
            if permision in self.all_permisions:
#                 print(self.key2index_dict[permision])
                res[self.key2index_dict[permision]] = 1
        return res

class PermisionAnalysisUtil(object):
    '''权限分析工具类'''
    
    def __init__(self,path):
        self.permision = Permision()
        self.permisions_df = self.get_apks_permisions(path)
    
    def get_apks_permisions(self,path):
        '''得到所有APK的所有权限'''
        import glob
        apks = glob.glob(f'{path}/*.txt')
        permision = self.permision.all_permisions
        permisions_df = pd.DataFrame(index=permision)
        for apk in apks:
            apk = ApkPermision(apk)
            permisions_df[apk.name] = apk.permision2array()
        permisions_df = permisions_df.astype(np.int16)
        return permisions_df
    
    def get_permision_num(self):
        '''得到每一个APK的权限数量'''
        return self.permisions_df.sum()
    
    def get_permision_list(self,apk_names=None):
        '''得到APK的权限列表'''
        from collections import Iterable
        res = {}
        if apk_names is None:
            for apk_name in self.permisions_df.columns.values:
                res[apk_name] = set(self.permisions_df[self.permisions_df[apk_name] == 1.0].index.values)
        else:
            if isinstance(apk_names,tuple) or isinstance(apk_names,list):
                for apk_name in apk_names:
                    res[apk_name] = set(self.permisions_df[self.permisions_df[apk_name] == 1.0].index.values)
            else:
                print('apk_names should be a list or a tuple of apk names')
        return res
    
    def get_top_permision(self,top=10):
        '''得到需求最多的权限'''
        if top < 1 or top > len(self.permisions_df):
            print(f'please type in a num in [1,{len(self.permisions_df)}]')
            return None
        else:
            return self.permisions_df.sum(axis=1).sort_values(ascending=False)[:top]
    
    def get_permisions_all_have(self):
        '''得到所有apk共有的权限'''
        top100_permision_df = self.get_top_permision(100)
        return top100_permision_df[top100_permision_df[top100_permision_df.index]==len(self.permisions_df.columns)]
    
    def get_permisions_description(self,permisions=None,is_index=False):
        '''
            功能：得到权限的说明
            参数：
                permisions 权限名称或者列表
                is_index   是通过下标还是名称访问，每个权限有一个唯一标识[0-134](共有135个权限)  
        ''' 
        res = {}
        indexes = permisions
        permisions = []
        if is_index:
            if isinstance(indexes,int):
                permisions.append(self.permision.index2key_dict[indexes])
            elif isinstance(indexes,tuple) or isinstance(indexes,list):
                for index in indexes:
                    permisions.append(self.permision.index2key_dict[index])
            else:
                pass
        
        if isinstance(permisions,str):
            res = {permisions:self.permision.all_permisions_dict[permisions] }
        elif isinstance(permisions,tuple) or isinstance(permisions,list):
            for permision in permisions:
                res[permision] = self.permision.all_permisions_dict[permision]
        elif permisions is None:
            res = self.permision.all_permisions_dict
        return res
    
    
    def get_cosine_similarity(self,vectors):
        '''计算余弦相似度'''
        from sklearn.metrics.pairwise import cosine_similarity,pairwise_distances
        cos_sim = cosine_similarity(vectors)
        pair_dis = pairwise_distances(vectors,metric="cosine")
        return {'cos_sim':cos_sim,'pair_dis':pair_dis}

def main():
    util = PermisionAnalysisUtil('apk_permisions')
    print('所有APK的所有权限*******************\n',util.permisions_df)
    print('\n权限列表*******************\n',util.get_permision_list(['ruanruan']))
    print('\n每一个APK的权限数量*******************\n',util.get_permision_num())
    print('\n需求最多的权限*******************\n',util.get_top_permision(15))
    print('\n每个APK都需要的权限*******************\n',util.get_permisions_all_have())
    print('\n权限的解释说明*******************\n',util.get_permisions_description([i for i in range(10)],is_index=True))
    print('\n权限的余弦相似度*******************\n',util.get_cosine_similarity(np.array(util.permisions_df).transpose()))
    
if __name__ == '__main__':
    main()