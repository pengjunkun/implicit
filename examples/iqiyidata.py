#%%
import csv
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd

#%%
def getData(variant):
    # file_url="C:\\Users\\lenovo\\work\\project\\sugarJar\\simu\\data\\"
    file_url="C:\\Users\\HP\\work\\project\\SugarJar\\simu\\data\\"
    file_url=file_url+variant+".csv"
    #user_id,timestamp,longitude,latitude,video_id
    file=pd.read_csv(file_url,usecols=['video_id','user_id'])[['video_id','user_id']]
    # u14=[]
    # u5459=[]
    # u5404=[]
    # for l in file.values:
    #     if l[0]==14:
    #         u14.append(l[1])
    #     elif l[0]==5459:
    #         u5459.append(l[1])
    #     elif l[0]==5404:
    #         u5404.append(l[1])
    #
    # u14.sort()
    # u5404.sort()
    # u5459.sort()
    # for i in u5404:
    #     print(i in u14)
    # for i in u5459:
    #     print(i in u14)
    # print(u14)
    # print(u5404)
    # print(u5459)
    #%%
    #.sort_values(['video_id','user_id'])
    file
    row=file["video_id"].to_numpy()
    coloumn=file["user_id"].to_numpy()

    #%%
    a=csr_matrix((np.ones(len(row)),(row,coloumn)))
    return a
