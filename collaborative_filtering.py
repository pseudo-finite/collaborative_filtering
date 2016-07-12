# -*- coding:utf-8 -*-

import sys
import math
import dataset


class cf:
    def __init__(self, Us, Is, U2I2Rating, sim_func_name):
        self.Us = []         # user list
        self.Is = []         # item list
        self.U2I2Rating = {} # user の item に対する rating
        self.I2Us = {}       # item を評価した user list
        self.U2Is = {}       # user が評価した item set
        self.U2U2Sim = {}    # user と user の similarity 

        # データのセット
        self.Us = Us
        self.Is = Is
        self.U2I2Rating = U2I2Rating

        # 類似度関数のセット
        if sim_func_name == "peason":
            self.calc_sim = self.pearson_correlation
        elif sim_func_name == "cosine":
            self.calc_sim = self.cosine_similarity
        else:
            assert False

        # データの前処理・計算
        self.setI2Us()
        self.setU2Is() 
        self.setU2U2Sim(sim_func_name)
        return

    def setU2Is(self):
        for user in self.Us:
            self.U2Is[user] = set(self.U2I2Rating[user].keys())
        return 

    def setI2Us(self):
        for item in self.Is:
            self.I2Us[item] = set()
        for user in self.Us:
            Is = self.U2I2Rating[user].keys()
            for item in Is:
                self.I2Us[item].add(user)
        return 


    def setU2U2Sim(self, sim_func_name):
        for user1 in self.Us:
            for user2 in self.Us:
                self.U2U2Sim.setdefault(user1, {})
                self.U2U2Sim.setdefault(user2, {})
                if user1 >= user2:continue
                sim = self.calc_sim(user1, user2)
                if sim != 0:
                    self.U2U2Sim[user1][user2] = sim
                    self.U2U2Sim[user2][user1] = sim
        return

    def pearson_correlation(self, user1, user2):
        Is1 = self.U2Is[user1]
        Is2 = self.U2Is[user2]
        if len(Is1)<=1 or len(Is2)<=1:
            sim = 0
        else:
            Is12 = Is1 & Is2
            if len(Is12) <= 1:
                sim = 0
            else:
                Ratings1 = [self.U2I2Rating[user1][item] for item in Is12]
                Ratings2 = [self.U2I2Rating[user2][item] for item in Is12]
                avg1 = 1.0 * sum(Ratings1) / len(Ratings1)
                avg2 = 1.0 * sum(Ratings2) / len(Ratings2)
                X = sum([(rating-avg1)*(rating-avg1) for rating in Ratings1])
                Y = sum([(rating-avg2)*(rating-avg2) for rating in Ratings2])
                if X==0 or Y==0:
                    sim = 0
                else:
                    XY = sum([(Ratings1[i]-avg1)*(Ratings2[i]-avg2) for i in range(len(Ratings1))])
                    sim = XY / math.sqrt(X*Y)
        return sim


    def cosine_similarity(self, user1, user2):
        I2Rating1 = self.U2I2Rating[user1]
        I2Rating2 = self.U2I2Rating[user2]
        XY = sum([rating1*I2Rating2[item] for item,rating1 in I2Rating1.items() if item in I2Rating2])
        if XY == 0:
            sim = 0
        else:
            X = sum([rating*rating for rating in I2Rating1.values()])
            Y = sum([rating*rating for rating in I2Rating2.values()])
            sim = XY / math.sqrt(X*Y)
        return sim

    def calc_score(self, user1, item):
        U2Sim = self.U2U2Sim[user1]
        x = 0.0
        y = 0.0
        for user2 in self.I2Us[item]:
            sim = U2Sim[user2] if user2 in U2Sim else 0
            if sim==0:continue
            Is12 = self.U2Is[user1] & self.U2Is[user2]
            Ratings2 = [self.U2I2Rating[user2][item] for item in Is12]
            avg2 = 1.0 * sum(Ratings2) / len(Ratings2)
            x += sim * (self.U2I2Rating[user2][item] - avg2)
            y += abs(sim)

        I2Rating = self.U2I2Rating[user1]
        avg = 1.0*sum(I2Rating.values()) / len(I2Rating)
        if y !=0:
            score = avg + x/y
        else:
            score = avg
        return score

        
if __name__ == "__main__":
    print('=== set sim_func ===')
    sim_func_name = "peason"
    # sim_func_name = "cosine"
    print(sim_func_name)

    print('=== get dataset ===')
    no = 3
    data = dataset.dataset(no)
    # print(data)
    sys.stdout.flush()

    
    print('=== create CF model ===')
    cf_model = cf(data.Us, data.Is, data.U2I2Rating, sim_func_name)
    # print("U2Is :", cf_model.U2Is)
    # print("I2Us :", cf_model.I2Us)
    # print("U2Avg:", cf_model.U2Avg)
    # print(cf_model.U2U2Sim)
    sys.stdout.flush()

    print('=== calc score ===')
    for user in cf_model.Us:
        # print(user, "-"*50)
        for item in cf_model.Is:
            score = cf_model.calc_score(user, item)
            # print("  ", item, score)

