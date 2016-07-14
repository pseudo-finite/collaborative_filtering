# -*- coding:utf-8 -*-

import math

def pearson_correlation(I2Rating1, I2Rating2):
    Is1 = set(I2Rating1)
    Is2 = set(I2Rating2)
    if len(Is1)<=1 or len(Is2)<=1:
        sim = 0
    else:
        Is12 = Is1 & Is2
        if len(Is12) <= 1:
            sim = 0
        else:
            Ratings1 = [I2Rating1[item] for item in Is12]
            Ratings2 = [I2Rating2[item] for item in Is12]
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

def cosine_similarity(I2Rating1, I2Rating2):
    XY = sum([rating1*I2Rating2[item] for item,rating1 in I2Rating1.items() if item in I2Rating2])
    if XY == 0:
        sim = 0
    else:
        X = sum([rating*rating for rating in I2Rating1.values()])
        Y = sum([rating*rating for rating in I2Rating2.values()])
        sim = XY / math.sqrt(X*Y)
    return sim


class cf:
    def __init__(self, Us, Is, U2I2Rating, sim_func_name):
        self.Us = []         # user list
        self.Is = []         # item list
        self.U2I2Rating = {} # user の item に対する rating
        self.I2Us = {}       # item を評価した user list
        self.sim_func_name = ""
        self.U2Is = {}
        self.UU2Sim = {}

        # データのセット
        self.Us = Us
        self.Is = Is
        self.U2I2Rating = U2I2Rating
        self.sim_func_name = sim_func_name

        # データの前処理・計算
        self.setI2Us()
        return

    def setI2Us(self):
        for item in self.Is:
            self.I2Us[item] = set()
        for user in self.Us:
            Is = self.U2I2Rating[user].keys()
            for item in Is:
                self.I2Us[item].add(user)
        return 

    def get_sim(self, user1, user2):
        if (user1, user2) in self.UU2Sim:
            sim = self.UU2Sim[user1,user2]
        elif (user2, user1) in self.UU2Sim:
            sim = self.UU2Sim[user2,user1]
        else:
            if self.sim_func_name == "pearson":
                sim = pearson_correlation(self.U2I2Rating[user1], self.U2I2Rating[user2])
            elif self.sim_func_name == "cosine":
                sim = cosine_similarity(self.U2I2Rating[user1], self.U2I2Rating[user2])
            else:
                assert False
            self.UU2Sim[user1,user2] = sim
        return sim


    def calc_other_rating_avg(self, user1, user2):
        if user1 in self.U2Is:
            Is1 = self.U2Is[user1]
        else:
            Is1 = set(self.U2I2Rating[user1])
        if user2 in self.U2Is:
            Is2 = self.U2Is[user2]
        else:
            Is2 = set(self.U2I2Rating[user2])

        Is12 = Is1 & Is2
        Ratings2 = [self.U2I2Rating[user2][item] for item in Is12]
        avg2 = 1.0 * sum(Ratings2) / len(Ratings2)
        return avg2

    def calc_target_rating_avg(self, user1):
        I2Rating = self.U2I2Rating[user1]
        avg1 = 1.0*sum(I2Rating.values()) / len(I2Rating)
        return avg1

    def calc_score(self, user1, item):
        x = 0.0
        y = 0.0
        for user2 in self.I2Us[item]:
            if user1 == user2:continue
            
            # user1 と user2 の similarity の取得
            sim = self.get_sim(user1, user2)
            if sim==0:continue
            # user1 user2 が共通に評価した item 集合から user2 の rating average を計算
            avg2 = self.calc_other_rating_avg(user1, user2)

            x += sim * (self.U2I2Rating[user2][item] - avg2)
            y += abs(sim)

        # 対象 user の rating average を計算
        avg1 = self.calc_target_rating_avg(user1)

        # score の計算
        score = avg1 + x/y if y != 0 else avg1
        return score

    def recommend_item(self, user, N):
        I2Score = []
        for item in self.Is:
            if item in set(self.U2I2Rating[user]):continue
            score = self.calc_score(user, item)
            I2Score.append((item, score))

        I2Score.sort(key=lambda x:x[1], reverse=True)
        RecIs = [item for item,score in I2Score[:N]]
        return RecIs

        
if __name__ == "__main__":
    import sys
    import dataset

    print('*** begin ***');sys.stdout.flush()

    print('=== get dataset ===');sys.stdout.flush()
    # no = 0
    # data = dataset(no, N=2000, M=400, K=20, R=5, seed=1)
    no = 3
    data = dataset.dataset(no)
    # print(data)
    
    print('=== create CF model ===');sys.stdout.flush()
    sim_func_name = "pearson"
    # sim_func_name = "cosine"
    cf_model = cf(data.Us, data.Is, data.U2I2Rating, sim_func_name)
    print(sim_func_name)
    # print("I2Us :", cf_model.I2Us)

    print('=== calc score ===');sys.stdout.flush()
    for user in cf_model.Us:
        print("user:", user);sys.stdout.flush()
        for item in cf_model.Is:
            score = cf_model.calc_score(user, item)
            print("     ", item, score)

    print('=== recommend item ===');sys.stdout.flush()
    N = 10
    for user in cf_model.Us:
        RecIs =cf_model.recommend_item(user, N)
        print("user:", user);sys.stdout.flush()
        print("     ", "|".join(RecIs));sys.stdout.flush()

    print('***  end  ***');sys.stdout.flush()

    # dataset:no=3
    # pearson
    # u1 - i6:score = 4.56?(=4.555555555555555)  

    # dataset:no=2
    # pearson
    # u2 - i1:score = 2.75?
