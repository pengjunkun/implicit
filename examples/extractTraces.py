#%%
base=1430668800


#%%

#1h,3h,8h,1d
needsInHour=[1,3,8,24]
for gap in [base+ 3600*i for i in [1,3,8,24]]:
    print(gap)

#%%

def writeOne(source_csv,path,timestamp):
    with open(path,'w') as file_oneNeed:
        file_oneNeed_dict_writer=csv.DictWriter(file_oneNeed,source_csv.fieldnames)
        file_oneNeed_dict_writer.writeheader()
        oneLine=next(source_csv)
        while True:
            if oneLine["timestamp"]!=timestamp:
                file_oneNeed_dict_writer.writerow(oneLine)
                oneLine=next(source_csv)
            else:
                break

#%%

import csv
import copy
file_url="C:\\Users\\lenovo\\work\\project\\sugarJar\\simu\\data\\"
    # write all the needs one by one(not spend more time to do parallel
for oneNeed in needsInHour:
    with open(file_url+"54.csv") as f:
        timestampNow=str(base+3600*oneNeed)
        path=file_url+str(oneNeed)+"h.csv"
        writeOne(csv.DictReader(f),path,timestampNow)


#%%


