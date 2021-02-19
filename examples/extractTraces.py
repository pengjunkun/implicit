# this file used to extract all the trace subset from a big one
# this will generate both traces and its video frequency
from collections import Counter
import csv

base = 1430668800

# 1h,3h,8h,1d
needsInHour = [1, 3, 8, 24]
for gap in [base + 3600 * i for i in [1, 3, 8, 24]]:
    print(gap)


def writeOne(source_csv, path, timestamp):
    records = []
    with open(path + "h.csv", 'w') as file_oneNeed:
        file_oneNeed_dict_writer = csv.DictWriter(file_oneNeed, source_csv.fieldnames)
        file_oneNeed_dict_writer.writeheader()
        oneLine = next(source_csv)
        while True:
            if oneLine["timestamp"] != timestamp:
                file_oneNeed_dict_writer.writerow(oneLine)
                records.append(oneLine['video_id'])
                oneLine = next(source_csv)
            else:
                break

    # to generate frequency, the miss video_id is the one whose frequency is 1
    with open(path + "h_frequency.csv", 'w') as file_freq:

        freq_writer = csv.writer(file_freq)
        freq_writer.writerow(['video_id','frequency'])

        # sort first
        freq = Counter(records)
        res = freq.most_common(len(freq))
        for row in res:
            if row[1] == 1:
                break
            if len(row)==0:
                continue
            freq_writer.writerow(row)


# file_url="C:\\Users\\lenovo\\work\\project\\sugarJar\\simu\\data\\"
file_url = "C:\\Users\\HP\\work\\project\\SugarJar\\simu\\data\\"


def generate():
    # write all the needs one by one(not spend more time to do parallel
    for oneNeed in needsInHour:
        with open(file_url + "54.csv") as f:
            timestampNow = str(base + 3600 * oneNeed)
            path = file_url + str(oneNeed)
            writeOne(csv.DictReader(f), path, timestampNow)


generate()
