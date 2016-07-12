# -*- coding:utf-8 -*-

'''
no=1
[[5,3,0,0]
,[4,0,4,1]
,[1,1,0,5]
,[0,0,4,4]
,[0,1,5,4]]
'''

'''
no=2
[[1,3,0,3]
,[0,1,3,0]
,[2,1,3,1]
,[1,3,2,0]
'''

'''
no=3
中規模データの作成
'''

def createDummyData(N=2000, M=400, K=20, R=5, seed=1):
    import random
    random.seed(seed)
    
    # user, item 生成
    N_len = len(str(N))
    M_len = len(str(M))
    Us = [("u%0"+ str(N_len) +"d") % i for i in range(1,N+1)]
    Is = [("i%0"+ str(M_len) +"d") % i for i in range(1,M+1)]

    # user * item -> rating 生成
    U2I2Value = {}
    for u in Us:
        U2I2Value[u]  = {}
        m = random.randint(1,K)
        tmpIs = random.sample(Is, m)
        for i in tmpIs:
            U2I2Value[u][i] = random.randint(1, R)
    return Us, Is, U2I2Value


class dataset:
    def __init__(self, no):
        
        self.Us = []         # user list
        self.Is = []         # item list
        self.U2I2Rating = {} # [sparse] user の item に対する rating
        self.Rss = []       # [dense]  rating list の list

        if no==1:
            # (user,item)=5*4 の rating dictionary を作成
            self.Us = ["u"+str(i) for i in range(1,6)]
            self.Is = ["i"+str(i) for i in range(1,5)]
            for user in self.Us:self.U2I2Rating[user]  = {}
            self.U2I2Rating["u1"]["i1"] = 5;    self.U2I2Rating["u1"]["i2"] = 3
            self.U2I2Rating["u2"]["i1"] = 4;    self.U2I2Rating["u2"]["i3"] = 4;    self.U2I2Rating["u2"]["i4"] = 1;
            self.U2I2Rating["u3"]["i1"] = 1;    self.U2I2Rating["u3"]["i2"] = 1;    self.U2I2Rating["u3"]["i4"] = 5
            self.U2I2Rating["u4"]["i3"] = 4;    self.U2I2Rating["u4"]["i4"] = 4
            self.U2I2Rating["u5"]["i2"] = 1;    self.U2I2Rating["u5"]["i3"] = 5;    self.U2I2Rating["u5"]["i4"] = 4
        elif no==2:
            # (user,item)=4*4 の rating dictionary を作成
            self.Us = ["u"+str(i) for i in range(1,5)]
            self.Is = ["i"+str(i) for i in range(1,5)]
            for user in self.Us:self.U2I2Rating[user]  = {}
            self.U2I2Rating["u1"]["i1"] = 1;  self.U2I2Rating["u1"]["i2"] = 3;  self.U2I2Rating["u1"]["i4"] = 3
            self.U2I2Rating["u2"]["i2"] = 1;  self.U2I2Rating["u2"]["i3"] = 3;
            self.U2I2Rating["u3"]["i1"] = 2;  self.U2I2Rating["u3"]["i2"] = 1;  self.U2I2Rating["u3"]["i3"] = 3;  self.U2I2Rating["u3"]["i4"] = 1
            self.U2I2Rating["u4"]["i1"] = 1;  self.U2I2Rating["u4"]["i2"] = 3;  self.U2I2Rating["u4"]["i3"] = 2;  
        elif no==3:
            self.Us, self.Is, self.U2I2Rating = createDummyData()
        else:
            assert False
            
        # rating list の list を作成
        for user in self.Us:
            IRs = []
            for item in self.Is:
                rating = self.U2I2Rating[user][item] if item in self.U2I2Rating[user] else 0
                IRs.append(rating)
            self.Rss.append(IRs)
        return


    def __str__(self):
        Us_s = "user:" + " ".join(self.Us) + "\n"
        Is_s = "item:" + " ".join(self.Is) + "\n"

        U2I2R_s = ""
        for user in self.Us:
            IRs = [(item, str(self.U2I2Rating[user][item])) for item in self.U2I2Rating[user]]
            U2I2R_s += user + ": " + "".join(["({},{}) ".format(i,r) for i,r in IRs]) + "\n"

        Rss_s = ""
        for IRs in self.Rss:
            Rss_s += " ".join(map(str, IRs)) + "\n"

        return "".join([Us_s, Is_s, U2I2R_s, Rss_s])



if __name__ == "__main__":
    no = 1
    data = dataset(no)
    print(data)

    no = 2
    data = dataset(no)
    print(data)

    no = 3
    data = dataset(no)
    # print(data)
    
