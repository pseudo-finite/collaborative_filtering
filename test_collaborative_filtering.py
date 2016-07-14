# -*- coding:utf-8 -*-

import unittest
from collaborative_filtering import *

class TestCollaborativeFiltering(unittest.TestCase):
    def setUp(self):
        pass

    def rearDown(self):
        pass

    ### pearson correlation test
    def test_pearson_correlation1(self):
        I2Rating1 = {"i1":1}
        I2Rating2 = {"i1":1, "i2":2}
        self.assertEqual(pearson_correlation(I2Rating1, I2Rating2), 0.0)
        return

    def test_pearson_correlation2(self):
        I2Rating1 = {"i1":1, "i2":2}
        I2Rating2 = {"i1":1}
        self.assertEqual(pearson_correlation(I2Rating1, I2Rating2), 0.0)
        return

    def test_pearson_correlation3(self):
        I2Rating1 = {"i1":1, "i2":2}
        I2Rating2 = {        "i2":2, "i3":3}
        self.assertEqual(pearson_correlation(I2Rating1, I2Rating2), 0.0)
        return

    def test_pearson_correlation4(self):
        I2Rating1 = {"i1":1, "i2":2, "i3":3}
        I2Rating2 = {        "i2":2, "i3":3, "i4":4}
        self.assertEqual(pearson_correlation(I2Rating1, I2Rating2), 1.0)
        return

    def test_pearson_correlation5(self):
        I2Rating1 = {"i1":1, "i2":2, "i3":3}
        I2Rating2 = {        "i2":3, "i3":2, "i4":4}
        self.assertEqual(pearson_correlation(I2Rating1, I2Rating2), -1.0)
        return

    def test_pearson_correlation6(self):
        I2Rating1 = {"i1":4, "i2":3, "i3":2, "i4":6, "i5":5}
        I2Rating2 = {"i1":6, "i2":8, "i3":12,"i4":10,"i5":4}
        self.assertEqual(pearson_correlation(I2Rating1, I2Rating2), -0.4)
        return

    def test_pearson_correlation7(self):
        I2Rating1 = {"i0":1, "i1":4, "i2":3, "i3":2, "i4":6, "i5":5}
        I2Rating2 = {        "i1":6, "i2":8, "i3":12,"i4":10,"i5":4, "i6":1}
        self.assertEqual(pearson_correlation(I2Rating1, I2Rating2), -0.4)
        return


    ### cosine similarity test
    def test_cosine_similarity1(self):
        I2Rating1 = {"i1":1}
        I2Rating2 = {"i1":1}
        self.assertEqual(cosine_similarity(I2Rating1, I2Rating2), 1.0)
        return

    def test_cosine_similarity2(self):
        I2Rating1 = {"i1":1, "i2":1}
        I2Rating2 = {"i1":1, "i2":1}
        self.assertEqual(cosine_similarity(I2Rating1, I2Rating2), 1.0)
        return

    def test_cosine_similarity3(self):
        I2Rating1 = {"i1":1}
        I2Rating2 = {        "i2":1}
        self.assertEqual(cosine_similarity(I2Rating1, I2Rating2), 0.0)
        return

    def test_cosine_similarity4(self):
        I2Rating1 = {"i1":1, "i2":1}
        I2Rating2 = {                "i3":1, "i4":1}
        self.assertEqual(cosine_similarity(I2Rating1, I2Rating2), 0.0)
        return

    def test_cosine_similarity5(self):
        import math
        I2Rating1 = {"i1":1, "i2":1}
        I2Rating2 = {"i1":1}
        self.assertEqual(cosine_similarity(I2Rating1, I2Rating2), 1.0/math.sqrt(2))
        return

    def test_cosine_similarity5(self):
        import math
        I2Rating1 = {"i1":1, "i2":7}
        I2Rating2 = {"i1":5, "i2":-3}
        self.assertEqual(cosine_similarity(I2Rating1, I2Rating2), -16.0 / (math.sqrt(50)*math.sqrt(34)))
        return

    def test_cosine_similarity6(self):
        import math
        I2Rating1 = {"i1":3, "i2":-5,"i3":6}
        I2Rating2 = {"i1":2, "i2":4, "i3":-1}
        self.assertEqual(cosine_similarity(I2Rating1, I2Rating2), -20.0 / (math.sqrt(70)*math.sqrt(21)))
        return

    ### recommendation test
    def test_pearson_recommendation1(self):
        # データセットの指定
        import dataset
        no = 2
        data = dataset.dataset(no)
        
        # テストパラメータの設定
        sim_func_name = "pearson"
        cf_model = cf(data.Us, data.Is, data.U2I2Rating, sim_func_name)

        # 類似度テスト
        user1 = "u1"
        user2 = "u2" # target
        user3 = "u3"
        user4 = "u4"
        self.assertEqual(cf_model.get_sim(user2, user1),  0.0)
        self.assertEqual(cf_model.get_sim(user2, user3),  1.0)
        self.assertEqual(cf_model.get_sim(user2, user4), -1.0)
    
        # スコアテスト
        user = "u2"
        item = "i1"
        score = cf_model.calc_score(user, item)
        self.assertEqual(score, 2.75)
        return

    def test_pearson_recommendation2(self):
        # データセットの指定
        import dataset
        no = 3
        data = dataset.dataset(no)

        # テストパラメータの設定
        sim_func_name = "pearson"
        cf_model = cf(data.Us, data.Is, data.U2I2Rating, sim_func_name)

        # 類似度テスト
        user1 = "u1" # target
        user2 = "u2"
        user3 = "u3"
        user4 = "u4"
        self.assertEqual(cf_model.get_sim(user1, user2), -0.8)
        self.assertEqual(cf_model.get_sim(user1, user3),  1.0)
        self.assertEqual(cf_model.get_sim(user1, user4),  0.0)
    
        # スコアテスト
        user = "u1"
        item = "i6"
        score = cf_model.calc_score(user, item)
        self.assertEqual(score, 3.0 + (2-(-0.8)) / (abs(1) + abs(-0.8)) ) # 4.555...
        return


if __name__ == "__main__":
    unittest.main()
