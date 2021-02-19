import heapq
import sys
import csv

file_base_url = "C:\\Users\\HP\\work\\project\\SugarJar\\cf\\implicit\\data\\"


class ClusterFounder:

    def __init__(self, path):
        self.posTable = dict()
        self.__readyKey = set()
        self.__freq_dict = dict()
        with open(path, 'r') as f:
            csvReader = csv.DictReader(f)
            for row in csvReader:
                self.__freq_dict.update({row['video_id']: int(row['frequency'])})

    def getFreq(self, key):
        if key in self.__freq_dict:
            return self.__freq_dict[key]
        else:
            return 1

    def getPositionTestValue(self, top10, x):
        """
        this func is used to calculate once test result of x
        Args:
            top10 (list(freq, vid, diff)):
            x (int):

        Returns:
            result (float)

        """
        result = 0
        for nei in top10:
            freq, vid, diff = nei
            result += freq * (abs(abs(x - self.posTable[vid]) - diff))
        return result

    def getTop10(self, neighbors):
        # 1
        # heap[0] is the smallest item
        top10 = []
        for nei in neighbors:
            vid, diff = nei
            if vid in self.__readyKey:
                # put it in
                if len(top10) > 10000:
                    heapq.heappushpop(top10, (self.getFreq(vid), vid, diff))
                else:
                    heapq.heappush(top10, (self.getFreq(vid), vid, diff))
        return top10

    def cluster(self, fileName):
        with open(file_base_url + fileName) as f:
            reader = csv.reader(f)
            key = None
            neighbors = []
            for row in reader:
                if len(row)==0:
                    continue
                if row[0] != key:
                    # assign one key
                    if key != None:
                        print("try to get position for: "+key)
                        self.posTable.update({key: self.getPosition(key, neighbors)})
                        self.__readyKey.add(key)
                    key = row[0]
                    neighbors.clear()
                    neighbors.append((row[1], 100 * (1 - float(row[2]))))
                else:
                    # neighbors (list[tuple(vid (str),diff (float))]):
                    neighbors.append((row[1], 100 * (1 - float(row[2]))))
            # the last key
            self.posTable.update({key: self.getPosition(key, neighbors)})

    # from the most frequency to least
    def getPosition(self, key, neighbors):
        """

        Args:
            key (str):
            neighbors (list[tuple(vid (str),diff (float))]):

        Returns:
            x (integer)

        """

        if key in self.__readyKey:
            return


        # for the 1st key, assign it as 100
        if len(self.posTable) == 0:
            return 100

        # 1.for all neighbor whose position has been determined
        # 2.choose the top frequency 10 for computation
        # 3.test method for finding the proper position value
        top10 = self.getTop10(neighbors)

        # 3 try
        pos = -1
        smallest = sys.maxsize
        for i in range(201):
            # print("test: "+str(i))
            tmp = self.getPositionTestValue(top10, i)
            if tmp < smallest:
                pos = i
                smallest = tmp

        return pos


clusterFounder = ClusterFounder(file_base_url + "24h_frequency.csv")
clusterFounder.cluster("24h_similarity.csv")
with open(file_base_url + "out_24h.csv", 'w') as f:
    writer=csv.writer(f)
    writer.writerows(clusterFounder.posTable.items())
