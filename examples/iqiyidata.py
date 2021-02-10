#%%
import csv
from scipy.sparse import csr_matrix
import numpy as np
import pandas as pd

#%%
def getData():
    file_url="C:\\Users\\lenovo\\work\\project\\sugarJar\\simu\\data\\test.csv"
    file=pd.read_csv(file_url,usecols=['video_id','user_id'])[['video_id','user_id']]
    #%%
    #.sort_values(['video_id','user_id'])
    file
    row=file["video_id"].to_numpy()
    coloumn=file["user_id"].to_numpy()

    #%%
    a=csr_matrix((np.ones(len(row)),(row,coloumn)))
    return a
