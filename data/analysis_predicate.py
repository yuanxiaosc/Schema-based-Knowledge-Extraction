
f_name = "train"

if True:
    f_name = "train"
else:
    f_name = "test"

predicate_file = open("SKE_2019/{}/predicate_out.txt".format(f_name), "r", encoding='utf-8')
predicate_list = [line.replace("\n", "") for line in predicate_file.readlines()]
predicate_file_number = len(predicate_list)

text_file = open("SKE_2019/{}/text.txt".format(f_name), "r", encoding='utf-8')
text_list = [line.replace("\n", "") for line in text_file.readlines()]

class SPO_feature_word_co_occurence(object):

    def __init__(self, relation_A, relation_B, word_A, word_B):
        self.relation_A = relation_A
        self.relation_B = relation_B
        self.word_A = word_A
        self.word_B = word_B
        pass

    def feature_word_count(self, word_A, word_B, text):
        if word_A in text and word_B not in text:
            return 1, 0
        elif word_A not in text and word_B in text:
            return 0, 1
        elif word_A in text and word_B in text:
            return 1, 1
        else:
            return 0, 0

    def feature_tuple_count(self, feature_list):
        A, B, C, D = 0, 0, 0, 0
        for a_tuple in feature_list:
            if a_tuple == (1, 0):
                A += 1
            elif a_tuple == (0, 1):
                B += 1
            elif a_tuple == (1, 1):
                C += 1
            elif a_tuple == (0, 0):
                D += 1
        K = [A, B, C, D]
        return K

    def statistical_relation_co_occurrence_frequency(self):
        feature_list_1_0 = []
        feature_list_0_1 = []
        feature_list_1_1 = []
        feature_list_0_0 = []
        relation_A_number, relation_B_number, relation_A_B_number, relation_no_A_no_B_number = 0, 0, 0, 0
        predicate_list_num = len(predicate_list)
        for idx, line in enumerate(predicate_list):
            text = text_list[idx]
            feature_tuple = self.feature_word_count(self.word_A, self.word_B, text)
            # print(str(feature_tuple) + '\t' + text)
            if self.relation_A in line and self.relation_B not in line:
                relation_A_number += 1
                feature_list_1_0.append(feature_tuple)
                print(text)
            elif self.relation_A not in line and  self.relation_B in line:
                relation_B_number += 1
                feature_list_0_1.append(feature_tuple)
            elif self.relation_A in line and self.relation_B in line:
                relation_A_B_number += 1
                feature_list_1_1.append(feature_tuple)
            else:
                relation_no_A_no_B_number += 1
                feature_list_0_0.append(feature_tuple)
        L_num = [relation_A_number, relation_B_number, relation_A_B_number, relation_no_A_no_B_number]
        L_rate = [round(rate/predicate_list_num, 5) for rate in L_num]
        K_list = [self.feature_tuple_count(feature_list) for feature_list in [feature_list_1_0, feature_list_0_1, feature_list_1_1, feature_list_0_0]]
        feature_word_column_list = []
        for i in range(4):
            feature_word_column_list.append(sum([K_list[0][i], K_list[1][i], K_list[2][i], K_list[3][i]]))
        return L_num, L_rate, K_list, feature_word_column_list

    def show_statistical_info(self):
        L_num, L_rate, K_list, feature_word_column_list = self.statistical_relation_co_occurrence_frequency()
        print("{}、{} predicate 共现信息：10 01 11 00".format(self.relation_A, self.relation_B))
        print("数量：", L_num)
        print("比例：", L_rate)
        print("{}、{} 关键词 在 predicate 不同共现情况下的共现信息：10 01 11 00".format(self.word_A, self.word_B))
        for idx, K in enumerate(K_list):
            # print("%-9s" % str(L_num[idx]), K)
            print("{:15s}{}".format(str(L_num[idx]), K))
        print("-"*40)
        print("{:15s}{}".format("column_sum", feature_word_column_list))

if __name__=="__main__":
    feature_co_occurence = SPO_feature_word_co_occurence('祖籍', '出生地', '祖籍', '出生地')
    feature_co_occurence.show_statistical_info()