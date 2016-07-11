# -*- coding:utf-8 -*-

'''
次の rating matrix と同等のデータを作成
[[5,3,0,0]
,[4,0,4,1]
,[1,1,0,5]
,[0,0,4,4]
,[0,1,5,4]]
'''

class dataset:
    def __init__(self):
        
        self.Us = []         # user list
        self.Is = []         # item list
        self.U2I2Rating = {} # user's rating for an item(sparse)
        self.IRss = []       # user's item rating list(dense)

        # (user,item)=5*4 の rating dictionary を作成
        self.Us = ["u"+str(i) for i in range(1,6)]
        self.Is = ["i"+str(i) for i in range(1,5)]
        for user in self.Us:self.U2I2Rating[user]  = {}
        self.U2I2Rating["u1"]["i1"] = 5;    self.U2I2Rating["u1"]["i2"] = 3
        self.U2I2Rating["u2"]["i1"] = 4;    self.U2I2Rating["u2"]["i3"] = 4;    self.U2I2Rating["u2"]["i4"] = 1;
        self.U2I2Rating["u3"]["i1"] = 1;    self.U2I2Rating["u3"]["i2"] = 1;    self.U2I2Rating["u3"]["i4"] = 5
        self.U2I2Rating["u4"]["i3"] = 4;    self.U2I2Rating["u4"]["i4"] = 4
        self.U2I2Rating["u5"]["i2"] = 1;    self.U2I2Rating["u5"]["i3"] = 5;    self.U2I2Rating["u5"]["i4"] = 4

        # rating list を作成
        for user in self.Us:
            IRs = []
            for item in self.Is:
                rating = self.U2I2Rating[user][item] if item in self.U2I2Rating[user] else 0
                IRs.append(rating)
            self.IRss.append(IRs)

        return

    def __str__(self):
        Us_s = "user:" + " ".join(self.Us) + "\n"
        Is_s = "item:" + " ".join(self.Is) + "\n"

        U2I2R_s = ""
        for user in self.Us:
            IRs = [(item, str(self.U2I2Rating[user][item])) for item in self.U2I2Rating[user]]
            U2I2R_s += user + ": " + "".join(["({},{}) ".format(i,r) for i,r in IRs]) + "\n"

        IRss_s = ""
        for IRs in self.IRss:
            IRss_s += " ".join(map(str, IRs)) + "\n"

        return "".join([Us_s, Is_s, U2I2R_s, IRss_s])



if __name__ == "__main__":
    data = dataset()
    print(data)
    
