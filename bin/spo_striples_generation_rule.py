#coding=gbk
from itertools import permutations
import operator
import random
from .spo_striples_generation_data_manage import Sorted_relation_and_entity_list_Management
from .priori_statistical_information import Priori_statistical_information
#from .priori_statistical_information_from_file import Priori_statistical_information
from .spo_pattern_matching_extraction_rule import SPO_pattern_matching

# 通过模型结果启发式生成 spo_list
class SPO_List_Heuristic_Generation(Priori_statistical_information):

    def __init__(self):
        Priori_statistical_information.__init__(self)
        self.spo_predicate_temple = SPO_Predicate_Temple()
        self.relational_location_word = {
            '祖籍': ["祖籍"], '出生地': ["出生", "出生于", "人"],
            '歌手': ['歌手', "演唱", "单曲"], '作词': ['作词',"填词"], '作曲': ['作曲'],
            "导演": ["导演", "执导"], '制片人': ["制片"], '编剧': ['编剧'], '主演': ['主演', "饰演"],
            '父亲': ['父亲'], '母亲': ['母亲'], '妻子': ['妻子', "妻", "女友"], '丈夫': ['丈夫', "夫"],
            '董事长': ['董事长', '董事'], '创始人': ["创始人", "创始", "创办", "创立"],
            '主持人': ['主持人', '主持', "主播"], '嘉宾': ['嘉宾',"评委"],
        }

    def create_new_spo_item(self, a_relationship=None, subject_type=None, object_type=None, subject_value=None,
                            object_value=None):
        spo_item = dict()
        spo_item["predicate"] = a_relationship
        spo_item["object_type"] = object_type
        spo_item["subject_type"] = subject_type
        spo_item["object"] = object_value
        spo_item["subject"] = subject_value
        return spo_item

    def get_entity_value_list_by_name(self, entity_name, sort_entity_list):
        return [entity_value for entity_type, entity_value in sort_entity_list if entity_type == entity_name]

    def heuristic_generate_zuji_chushengdi(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        didian_list = self.get_entity_value_list_by_name("地点", sort_entity_list)
        renwu_list = self.get_entity_value_list_by_name("人物", sort_entity_list)
        didian_list_len = len(didian_list)
        for renwu in renwu_list:
            if didian_list_len == 1:
                if need_analysis_relation_flag_dict["祖籍"] == 1:
                    spo_item = self.create_new_spo_item("祖籍", '地点', '人物', didian_list[0], renwu)
                    spo_list.append(spo_item)
            if didian_list_len >= 2:
                relational_location_word_list = self.relational_location_word["祖籍"]
                for relational_location_word in relational_location_word_list:
                    if relational_location_word in text_sentence:
                        nearest_didian_word = self.find_word_B_nearest_to_word_A_for_single_relation(
                            text_sentence, relational_location_word, didian_list)
                        if nearest_didian_word is not None and nearest_didian_word in didian_list:
                            spo_item = self.create_new_spo_item("祖籍", "地点", "人物", nearest_didian_word, renwu)
                            spo_list.append(spo_item)
                            didian_list.remove(nearest_didian_word)
                        break
                for didian in didian_list:
                    spo_item = self.create_new_spo_item("出生地", "地点", "人物", didian, renwu)
                    spo_list.append(spo_item)
        if len(spo_list) == 0:
            for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                if relation_flag == 1:
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        return spo_list

    # 处理['歌手', '作词', '作曲']关系通过词的距离关系
    def handle_geshou_zuoci_zuoqu_by_word_distence(self, text_sentence, need_analysis_relation_flag_dict, renwu_list, gequ_list):
        spo_list = []
        for gequ in gequ_list:
            nearest_renwu_word_list = [None, None, None]
            for idx, relation_name in enumerate(['歌手', '作词', '作曲']):
                if need_analysis_relation_flag_dict[relation_name] == 1:
                    relational_location_word_list = self.relational_location_word[relation_name]
                    for relational_location_word in relational_location_word_list:
                        if relational_location_word in text_sentence:
                            nearest_renwu_word = self.find_word_B_nearest_to_word_A_for_single_relation(
                                text_sentence, relational_location_word, renwu_list)
                            nearest_renwu_word_list[idx] = nearest_renwu_word
                            break
            for relation_name, nearest_renwu_word in zip(['歌手', '作词', '作曲'], nearest_renwu_word_list):
                if nearest_renwu_word is not None and nearest_renwu_word in renwu_list:
                    spo_item = self.create_new_spo_item(relation_name, "人物", "歌曲", nearest_renwu_word, gequ)
                    spo_list.append(spo_item)
                    renwu_list.remove(nearest_renwu_word)
            if len(renwu_list) > 0:
                for renwu in renwu_list:
                    spo_item = self.create_new_spo_item('歌手', "人物", "歌曲", renwu, gequ)
                    spo_list.append(spo_item)
        return spo_list

    #处理导演制片人编剧演员关系通过词的距离关系
    def handle_daoyan_zhipianren_bianju_zhuyan_by_word_distence(self, text_sentence, need_analysis_relation_flag_dict, renwu_list, yingshizuopin):
        spo_list = []
        nearest_renwu_word_list = [None, None, None]
        for idx, relation_name in enumerate(["导演","制片人","编剧"]):
            if need_analysis_relation_flag_dict[relation_name] == 1:
                relational_location_word_list = self.relational_location_word[relation_name]
                for relational_location_word in relational_location_word_list:
                    if relational_location_word in text_sentence:
                        nearest_renwu_word = self.find_word_B_nearest_to_word_A_for_single_relation(
                            text_sentence, relational_location_word, renwu_list)
                        nearest_renwu_word_list[idx] = nearest_renwu_word
                        break
        for relation_name, nearest_renwu_word in  zip(["导演","制片人","编剧"], nearest_renwu_word_list):
            if nearest_renwu_word is not None and nearest_renwu_word in renwu_list:
                spo_item = self.create_new_spo_item(relation_name, "人物", "影视作品", nearest_renwu_word, yingshizuopin)
                spo_list.append(spo_item)
                renwu_list.remove(nearest_renwu_word)
        if len(renwu_list) > 0:
            for renwu in renwu_list:
                spo_item = self.create_new_spo_item("主演", "人物", "影视作品", renwu, yingshizuopin)
                spo_list.append(spo_item)
        return spo_list

    # 在候选词列表 candidate_word_list 中找出距离中心词 center_word 最近的词语
    def find_word_B_nearest_to_word_A_for_single_relation(self, text_sentence, center_word, candidate_word_list):
        candidate_word_list_distance = []
        if center_word in text_sentence:
            word_A_index = text_sentence.index(center_word) + len(center_word) / 2
            candidate_word_list.reverse()  # 列表反顺序，是为了当有两个单词距离中心词相同距离时，优先返回右边的单词
        else:
            word_A_index = 0
        for candidate_word in candidate_word_list:
            if candidate_word in text_sentence:
                candidate_word_index = text_sentence.index(candidate_word) + len(candidate_word) / 2
            else:
                candidate_word_index = 1000
            candidate_word_list_distance.append(abs(candidate_word_index - word_A_index))
        if len(candidate_word_list_distance) > 0:
            nearest_word = candidate_word_list[candidate_word_list_distance.index(min(candidate_word_list_distance))]
            return nearest_word
        else:
            return ""

    def heuristic_handle_multiple_relations(self, text_sentence, need_analysis_relation_flag_dict, sort_entity_list):
        spo_list = []
        if "父亲" in need_analysis_relation_flag_dict: # 处理('人物', '人物'): ['父亲', '妻子', '母亲', '丈夫'],
            spo_list.extend(self.heuristic_generate_fuqin_muqin_zhangfu_qizi(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "导演" in need_analysis_relation_flag_dict:#处理 ('人物', '影视作品'): ['导演', '制片人', '编剧', '主演']
            spo_list.extend(self.heuristic_generate_daoyan_zhipian_bianju_zhuyan(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "字" in need_analysis_relation_flag_dict:#处理 ('Text', '历史人物'): ['字', '朝代', '号'],
            spo_list.extend(self.heuristic_generate_zi_chaodai_hao(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "歌手" in need_analysis_relation_flag_dict:#处理 ('人物', '歌曲'): ['歌手', '作词', '作曲'],
            spo_list.extend(self.heuristic_generate_geshou_zuoci_zuoqu(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "祖籍" in need_analysis_relation_flag_dict:
            spo_list.extend(self.heuristic_generate_zuji_chushengdi(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "董事长" in need_analysis_relation_flag_dict:
            spo_list.extend(self.heuristic_generate_dongshizhang_chuangshiren(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        elif "主持人" in need_analysis_relation_flag_dict:
            spo_list.extend(self.heuristic_generate_zhuchiren_jiabin(
                text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        else:
            pass
        return spo_list

    # ('人物', '电视综艺'): ['主持人', '嘉宾']
    def heuristic_generate_zhuchiren_jiabin(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        renwu_list = self.get_entity_value_list_by_name("人物", sort_entity_list)
        dianshizongyi_list = self.get_entity_value_list_by_name("电视综艺", sort_entity_list)
        renwu_list_len = len(renwu_list)
        dianshizongyi_list_len = len(dianshizongyi_list)
        if dianshizongyi_list_len > 0:
            for dianshizongyi in dianshizongyi_list:
                if renwu_list_len == 1:
                    for zhuchi_feature_word in ['主持人', '主持', "主播"]:
                        if zhuchi_feature_word in text_sentence:
                            spo_item = self.create_new_spo_item("主持人", "人物", "电视综艺", renwu_list[0], dianshizongyi)
                            spo_list.append(spo_item)
                            break
                    if "嘉宾" in text_sentence:
                        spo_item = self.create_new_spo_item("嘉宾", "人物", "电视综艺", renwu_list[0], dianshizongyi)
                        spo_list.append(spo_item)
                elif renwu_list_len >= 2:
                    if "主持人" in text_sentence and "嘉宾" in text_sentence:
                        for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                            spo_list.extend(
                                self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
                    else:
                        for zhuchi_feature_word in ['主持人', '主持', "主播"]:
                            if zhuchi_feature_word in text_sentence:
                                for renwu in renwu_list:
                                    spo_item = self.create_new_spo_item("主持人", "人物", "电视综艺", renwu, dianshizongyi)
                                    spo_list.append(spo_item)
                                break
                            else:
                                for renwu in renwu_list:
                                    spo_item = self.create_new_spo_item("嘉宾", "人物", "电视综艺", renwu, dianshizongyi)
                                    spo_list.append(spo_item)
                                break
        #使用先验知识捕捉
        if len(spo_list) == 0:
            for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        return spo_list

    def heuristic_generate_geshou_zuoci_zuoqu(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        #使用先验知识捕捉
        for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
            if relation_flag == 1:
                spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        if len(spo_list) == 0:
            gequ_list = self.get_entity_value_list_by_name("歌曲", sort_entity_list)
            renwu_list = self.get_entity_value_list_by_name("人物", sort_entity_list)
            renwu_list_len = len(renwu_list)
            for gequ in gequ_list:
                if renwu_list_len == 1:
                    for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                        if relation_flag == 1:
                            spo_item = self.create_new_spo_item(relation_name, "人物", "歌曲", renwu_list[0], gequ)
                            spo_list.append(spo_item)
                elif renwu_list_len == 2:
                      renwu_2_index = 0
                      for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                          if relation_flag == 1 and renwu_2_index == 0:
                              renwu_2_index += 1
                              spo_item = self.create_new_spo_item(relation_name, "人物", "歌曲", renwu_list[0], gequ)
                          else:
                              spo_item = self.create_new_spo_item(relation_name, "人物", "歌曲", renwu_list[1], gequ)
                          spo_list.append(spo_item)
                elif renwu_list_len >= 3:
                    spo_list.extend(self.handle_geshou_zuoci_zuoqu_by_word_distence(
                        text_sentence, need_analysis_relation_flag_dict, renwu_list, gequ_list))

        return spo_list

    def heuristic_generate_dongshizhang_chuangshiren(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        for relation_name in ['董事长', '创始人']:
            spo_list.extend(self.spo_predicate_temple.temple_priori_information(
                relation_name=relation_name, text_sentence=text_sentence))
        return spo_list

    def heuristic_generate_zi_chaodai_hao(self, text_sentence, need_analysis_relation_flag_dict,
                                                        sort_entity_list):
        spo_list = []
        for relation_name in ['字', '朝代', '号']:
            spo_list.extend(self.spo_predicate_temple.temple_priori_information(
                relation_name=relation_name, text_sentence=text_sentence))
        return spo_list

    # ('人物', '影视作品'): ['导演', '制片人', '编剧', '主演']
    def heuristic_generate_daoyan_zhipian_bianju_zhuyan(self,text_sentence, need_analysis_relation_flag_dict, sort_entity_list):
        def yingshizuopin_two_ren_distence():
            pass
        spo_list = []
        #print("heuristic_generate_daoyan_zhipian_bianju_zhuyan:\t",need_analysis_relation_flag_dict)
        yingshizuopin_list = self.get_entity_value_list_by_name("影视作品", sort_entity_list)
        renwu_list = self.get_entity_value_list_by_name("人物", sort_entity_list)
        yingshizuopin_list_len = len(yingshizuopin_list)
        renwu_list_len = len(renwu_list)
        #在只有一个影视作品的前提下进行启发式推导，否则直接使用先验知识
        if yingshizuopin_list_len == 1:
            if renwu_list_len == 1:
                for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                    if relation_flag == 1:
                        spo_item = self.create_new_spo_item(relation_name, "人物", "影视作品", renwu_list[0],
                                                            yingshizuopin_list[0])
                        spo_list.append(spo_item)
            elif renwu_list_len == 2:
                  renwu_2_index = 0
                  for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                      if relation_flag == 1 and renwu_2_index == 0:
                          renwu_2_index += 1
                          spo_item = self.create_new_spo_item(relation_name, "人物", "影视作品", renwu_list[0],
                                                              yingshizuopin_list[0])
                      else:
                          spo_item = self.create_new_spo_item(relation_name, "人物", "影视作品", renwu_list[1],
                                                              yingshizuopin_list[0])
                      spo_list.append(spo_item)
            elif renwu_list_len >= 3:
                spo_list.extend(self.handle_daoyan_zhipianren_bianju_zhuyan_by_word_distence(
                    text_sentence, need_analysis_relation_flag_dict, renwu_list, yingshizuopin_list[0]))
        else:
            for relation_name, relation_flag in need_analysis_relation_flag_dict.items():
                if relation_flag == 1:
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        return spo_list


class SPO_Predicate_Temple(SPO_pattern_matching, Priori_statistical_information):

    def __init__(self):
        SPO_pattern_matching.__init__(self)
        Priori_statistical_information.__init__(self)

    def create_new_spo_item(self, a_relationship=None, subject_type=None, object_type=None, subject_value=None,
                            object_value=None):
        spo_item = dict()
        spo_item["predicate"] = a_relationship
        spo_item["object_type"] = object_type
        spo_item["subject_type"] = subject_type
        spo_item["object"] = object_value
        spo_item["subject"] = subject_value
        return spo_item

    def get_entity_value_list_by_name(self, entity_name, sort_entity_list):
        return [entity_value for entity_type, entity_value in sort_entity_list if entity_type == entity_name]

    # 通用模板，穷举所有可能的spo匹配关系生成 spo_list
    def temple_one(self, relation_name, sort_entity_list):  #
        spo_list = list()
        subject_type = self.schemas_dict_relation_2_subject_object[relation_name][0][0]
        object_type = self.schemas_dict_relation_2_subject_object[relation_name][0][1]
        subject_value_list = self.get_entity_value_list_by_name(subject_type, sort_entity_list)
        object_value_list = self.get_entity_value_list_by_name(object_type, sort_entity_list)
        for subject_value in subject_value_list:
            for object_value in object_value_list:
                spo_item = self.create_new_spo_item(relation_name, subject_type, object_type, subject_value, object_value)
                spo_list.append(spo_item)
        return spo_list

    def temple_priori_information(self, relation_name, text_sentence):
        spo_list = list()
        candidate_combination_set = set()
        entityA_2_entityB_set_dict = dict()
        subject_type = self.schemas_dict_relation_2_subject_object[relation_name][0][0]
        object_type = self.schemas_dict_relation_2_subject_object[relation_name][0][1]

        # ('地点', '人物'): ['祖籍', '出生地'],
        if relation_name == "祖籍":
            entityA_2_entityB_set_dict = self.special_entity_map_zu_ji_2_ren_wu
        elif relation_name == "出生地":
            entityA_2_entityB_set_dict = self.special_entity_map_chu_sheng_di_2_ren_wu
        # ('人物', '企业'): ['董事长', '创始人']
        elif relation_name == "董事长":
            entityA_2_entityB_set_dict = self.special_entity_map_dong_shi_zhang_2_qiye
        elif relation_name == "创始人":
            entityA_2_entityB_set_dict = self.special_entity_map_chuang_shi_ren_2_qiye
        # ('人物', '电视综艺'): ['主持人', '嘉宾']
        elif relation_name == "主持人":
            entityA_2_entityB_set_dict = self.special_entity_map_zhu_chi_ren_2_dian_shi_zong_yi
        elif relation_name == "嘉宾":
            entityA_2_entityB_set_dict = self.special_entity_map_jia_bin_2_dian_shi_zong_yi
        # ('Number', '行政区'): ['面积', '人口数量']
        elif relation_name == "面积" :
            entityA_2_entityB_set_dict = self.special_entity_map_mian_ji_2_xing_zheng_qu
        elif relation_name == "人口数量" :
            entityA_2_entityB_set_dict = self.special_entity_map_ren_kou_shu_liang_2_xing_zheng_qu
        # ('Text', '历史人物'): ['字', '朝代', '号']
        elif relation_name == "字":
            entityA_2_entityB_set_dict = self.special_entity_map_zi_2_li_shi_ren_wu
        elif relation_name == "朝代":
            entityA_2_entityB_set_dict = self.special_entity_map_chao_dai_2_li_shi_ren_wu
        elif relation_name == "号":
            entityA_2_entityB_set_dict = self.special_entity_map_hao_2_li_shi_ren_wu
        # ('人物', '歌曲'): ['歌手', '作词', '作曲']
        elif relation_name == "歌手":
            entityA_2_entityB_set_dict = self.special_entity_map_ge_shou_2_ge_qu
        elif relation_name == "作词":
            entityA_2_entityB_set_dict = self.special_entity_map_zuo_ci_2_ge_qu
        elif relation_name == "作曲":
            entityA_2_entityB_set_dict = self.special_entity_map_zuo_qu_2_ge_qu
        # ('人物', '人物'): ['父亲', '妻子', '母亲', '丈夫']
        elif relation_name == "父亲":
            entityA_2_entityB_set_dict = self.special_entity_map_fu_qin_2_zi_nv
        elif relation_name == "母亲":
            entityA_2_entityB_set_dict = self.special_entity_map_mu_qin_2_zi_nv
        elif relation_name == "丈夫":
            entityA_2_entityB_set_dict = self.special_entity_map_zhang_fu_2_pei_ou
        elif relation_name == "妻子":
            entityA_2_entityB_set_dict = self.special_entity_map_qi_zi_2_pei_ou
        # ('人物', '影视作品'): ['导演', '制片人', '编剧', '主演']
        elif relation_name == "导演":
            entityA_2_entityB_set_dict = self.special_entity_map_dao_yan_2_ying_shi_zuo_pin
        elif relation_name == "制片人":
            entityA_2_entityB_set_dict = self.special_entity_map_zhi_pian_ren_2_ying_shi_zuo_pin
        elif relation_name == "编剧":
            entityA_2_entityB_set_dict = self.special_entity_map_bian_ju_2_ying_shi_zuo_pin
        elif relation_name == "主演":
            entityA_2_entityB_set_dict = self.special_entity_map_zhu_yan_2_ying_shi_zuo_pin
        elif relation_name == "成立日期":
            entityA_2_entityB_set_dict = self.special_entity_map_special_entity_shi_jien_2_qi_ye


        if relation_name in ["祖籍", "出生地", "董事长", "创始人", "主持人", "嘉宾", '面积', '人口数量',
                            '字', '朝代', '号', '父亲', '妻子', '母亲', '丈夫', '导演', '制片人', '编剧', '主演',
                             "成立日期" ]:
            for spo_subject, spo_object_set in entityA_2_entityB_set_dict.items():
                for spo_object in spo_object_set:
                    if spo_subject in text_sentence and spo_object in text_sentence:
                        candidate_combination_set.add((spo_subject, spo_object))

        if relation_name in ['歌手', '作词', '作曲']: # ('人物', '歌曲'): ['歌手', '作词', '作曲']
            for spo_subject, spo_object_set in entityA_2_entityB_set_dict.items():
                for spo_object in spo_object_set:
                    if spo_subject in text_sentence and "《{}》".format(spo_object) in text_sentence:
                        candidate_combination_set.add((spo_subject, spo_object))

        for spo_subject, spo_object in candidate_combination_set:
            spo_item = self.create_new_spo_item(relation_name, subject_type, object_type, spo_subject, spo_object)
            spo_list.append(spo_item)
        return spo_list

class SPO_Generation_Rule_Base(SPO_pattern_matching, Priori_statistical_information):

    def __init__(self):
        SPO_pattern_matching.__init__(self)
        Priori_statistical_information.__init__(self)

    # 以 0.5 为标准划分预测的可能的关系
    def _split_relationship_by_score(self, sort_list):
        sort_list_positive = []
        sort_list_negative = []
        for relationship, value in sort_list:
            if value > 0.5:
                sort_list_positive.append(relationship)
            else:
                sort_list_negative.append(relationship)
        return sort_list_positive, sort_list_negative

    # 以关系对应数量划分关系
    def _split_relationship_by_single_or_multiple(self, relation_list):
        #single: ('企业', '影视作品')->['出品公司'], multiple: ('人物', '歌曲')->['歌手', '作词', '作曲']
        single_list, multiple_list = [], []
        single_relation_list = ["总部地点", "目", "简称", "上映时间", "所属专辑", "注册资本", "首都", "身高",
                                "出品公司", "修业年限", "出生日期", "国籍", "海拔", "连载网站", "民族", "出版社",
                                "专业代码", "主角", "毕业院校", "占地面积", "官方语言", "邮政编码",
                                "所在城市", "作者", "气候", "改编自", '成立日期']
        multiple_relation_list = ["祖籍", "出生地", "董事长", "创始人", "主持人", "嘉宾", '面积', '人口数量',
                                  '字', '朝代', '号', '歌手', '作词', '作曲', '父亲', '妻子', '母亲', '丈夫',
                                 '导演', '制片人', '编剧', '主演']
        for relation in relation_list:
            if relation in single_relation_list:
                single_list.append(relation)
            if relation in multiple_relation_list:
                multiple_list.append(relation)
        return single_list, multiple_list


    def rule_generate_spo_list(self, text_sentence, sort_relation_list, sort_entity_list, refer_spo_list):
        raise NotImplemented("need a function that return spo_list")

    # 通过特征词，取舍“祖籍”“出生地”关系
    def distinguishing_zu_ji_and_chu_sheng_di_relation(self, combine_relation_list, text_sentence):
        zu_ji_flag, zuji_value = self.spo_pattern_matching_extraction_rule_by_relation("祖籍", text_sentence)
        if "祖籍" in combine_relation_list and "出生地" in combine_relation_list:
            if zu_ji_flag == False or zuji_value is None:
                combine_relation_list.remove("祖籍")
        return combine_relation_list

    # 通过特征词，取舍“董事长”“创始人”关系
    def distinguishing_chuang_shi_ren_and_dong_shi_zhang(self, combine_relation_list, text_sentence):
        dong_shi_zhang_flag, dong_shi_zhang_value = self.spo_pattern_matching_extraction_rule_by_relation("董事长", text_sentence)
        chuang_shi_ren_flag, chuang_shi_ren_value = self.spo_pattern_matching_extraction_rule_by_relation("创始人", text_sentence)
        if "董事长" not in combine_relation_list and dong_shi_zhang_flag == True:
            combine_relation_list.append("董事长")
        if "创始人" not in combine_relation_list and chuang_shi_ren_flag == True:
            combine_relation_list.append("创始人")
        return combine_relation_list

    # 通过特征词，取舍“嘉宾”“主持人”关系
    def distinguishing_zhu_chi_ren_and_jia_bin(self, combine_relation_list, text_sentence):

        zhu_chi_ren_flag, zhu_chi_ren_value = self.spo_pattern_matching_extraction_rule_by_relation("主持人", text_sentence)
        jia_bin_flag, jia_bin_value = self.spo_pattern_matching_extraction_rule_by_relation("嘉宾", text_sentence)
        if "主持人" not in combine_relation_list and zhu_chi_ren_flag == True:
            combine_relation_list.append("主持人")
        if "嘉宾" not in combine_relation_list and jia_bin_flag == True:
            combine_relation_list.append("嘉宾")
        return combine_relation_list

    # 通过特征词，取舍“面积”“人口数量”关系
    def distinguishing_mian_ji_and_ren_kou_shu_liang(self, combine_relation_list, text_sentence):
        mian_ji_flag, mian_ji_value = self.spo_pattern_matching_extraction_rule_by_relation("面积", text_sentence)
        ren_kou_shu_liang_flag, ren_kou_value = self.spo_pattern_matching_extraction_rule_by_relation("人口数量", text_sentence)
        if "面积" not in combine_relation_list and mian_ji_flag == True:
            combine_relation_list.append("面积")
        if "人口" not in combine_relation_list and ren_kou_shu_liang_flag == True:
            combine_relation_list.append("人口数量")
        return combine_relation_list

    # 通过特征词，取舍“字”“朝代”“号”关系
    def distinguishing_zi_chao_dai_and_hao(self, combine_relation_list, text_sentence):
        zi_flag, zi_value = self.spo_pattern_matching_extraction_rule_by_relation("字", text_sentence)
        chao_dai_flag, chao_dai_value = self.spo_pattern_matching_extraction_rule_by_relation("朝代", text_sentence)
        hao_flag, hao_value = self.spo_pattern_matching_extraction_rule_by_relation("号", text_sentence)
        if "字" not in combine_relation_list and zi_flag == True:
            combine_relation_list.append("字")
        if "朝代" not in combine_relation_list and chao_dai_flag == True:
            combine_relation_list.append("朝代")
        if "号" not in combine_relation_list and hao_flag == True:
            combine_relation_list.append("号")
        return combine_relation_list

    # 通过特征词，取舍“歌手”“作词”“作曲”关系
    def distinguishing_ge_shou_zuo_ci_and_zuo_qu(self, combine_relation_list, text_sentence):
        ge_shou_flag, ge_shou_value = self.spo_pattern_matching_extraction_rule_by_relation("歌手", text_sentence)
        zuo_ci_flag, zuo_ci_value = self.spo_pattern_matching_extraction_rule_by_relation("作词", text_sentence)
        zuo_qu_flag, zuo_qu_value = self.spo_pattern_matching_extraction_rule_by_relation("作曲", text_sentence)
        if "歌手" not in combine_relation_list and ge_shou_flag == True:
            combine_relation_list.append("歌手")
        if "作词" not in combine_relation_list and zuo_ci_flag == True:
            combine_relation_list.append("作词")
        if "作曲" not in combine_relation_list and zuo_qu_flag == True:
            combine_relation_list.append("作曲")
        return combine_relation_list

    # 通过特征词，取舍“父亲”“母亲”“丈夫”“妻子”关系
    def distinguishing_fu_qin_mu_qin_zhang_fu_and_qi_zi(self, combine_relation_list, text_sentence):
        fu_qin_flag, fu_qin_value = self.spo_pattern_matching_extraction_rule_by_relation("父亲", text_sentence)
        mu_qin_flag, mu_qin_value = self.spo_pattern_matching_extraction_rule_by_relation("母亲", text_sentence)
        zhang_fu_flag, zhang_fu_value = self.spo_pattern_matching_extraction_rule_by_relation("丈夫", text_sentence)
        qi_zi_flag, qi_zi_value = self.spo_pattern_matching_extraction_rule_by_relation("妻子", text_sentence)
        if "父亲" not in combine_relation_list and fu_qin_flag == True:
            combine_relation_list.append("父亲")
        if "母亲" not in combine_relation_list and mu_qin_flag == True:
            combine_relation_list.append("母亲")
        if "丈夫" not in combine_relation_list and zhang_fu_flag == True:
            combine_relation_list.append("丈夫")
        if "妻子" not in combine_relation_list and qi_zi_flag == True:
            combine_relation_list.append("妻子")
        return combine_relation_list

    # 通过特征词，取舍“导演”“制片人”“编剧”“主演”关系
    def distinguishing_dao_yan_zhi_pian_ren_bian_ju_and_zhu_yan(self, combine_relation_list, text_sentence):
        dao_yan_flag, dao_yan_value = self.spo_pattern_matching_extraction_rule_by_relation("导演", text_sentence)
        zhi_pian_ren_flag, zhi_pian_ren_value = self.spo_pattern_matching_extraction_rule_by_relation("制片人", text_sentence)
        bian_ju_flag, bian_ju_value = self.spo_pattern_matching_extraction_rule_by_relation("编剧", text_sentence)
        zhu_yan_flag, zhu_yan_value = self.spo_pattern_matching_extraction_rule_by_relation("主演", text_sentence)
        if "导演" not in combine_relation_list and dao_yan_flag == True:
            combine_relation_list.append("导演")
        if "制片人" not in combine_relation_list and zhi_pian_ren_flag == True:
            combine_relation_list.append("制片人")
        if "编剧" not in combine_relation_list and bian_ju_flag == True:
            combine_relation_list.append("编剧")
        if "主演" not in combine_relation_list and zhu_yan_flag == True:
            combine_relation_list.append("主演")
        return combine_relation_list


# 直接由模型推测的关系来找对应需要的实体，最后给出所有关系的所有可能实体，最终输出 spo_list。速度快，但是准确率低！
class Relationship_Priority_Rule(SPO_Generation_Rule_Base):
    """
    length_equal:	 0.523
    length_shorter:	 0.312
    length_longer:	 0.166
    """
    def __init__(self):
        SPO_Generation_Rule_Base.__init__(self,)

    def rule_generate_spo_list(self, text_sentence, sort_relation_list, sort_entity_list, refer_spo_list):
        """
        规则1：关系 -> (主体，客体)
            特殊情况：“Data-成立日期-企业” “Data-成立日期-机构”
            处理办法：1. 日期为主体

        规则2：关系概率大于 0.5 的存放在 sort_list_positive，否则存 sort_list_negative
            默认只对 sort_list_positive 中关系进行处理
            特殊情况：sort_list_positive 为空，则将“一个”相对概率最大的放入该列表

        规则3：至少在实体列表中发现主体或者客体之一，才放入候选三元组列表spo_list中
            处理办法：对于缺少主体或者客体之一的三元组, 则用其中之一代替另一个，目前用 None 表示

        规则4：如果同一种类型的实体有多个，尽量输出每一个实体，而且以第一个实体为主体，其余实体为客体
        规则5：如果发现关系是妻子或者丈夫，可由其中一个推知另一个
        """
        sort_list_positive, sort_list_negative = self._split_relationship_by_score(sort_relation_list)

        # 规则2
        if len(sort_list_positive) == 0:
            sort_list_positive.append(sort_list_negative[0])
        sort_entity_list = [[name, value, 0] for name, value in sort_entity_list]
        spo_list = []

        for a_relationship in sort_list_positive:
            # 规则1
            subject_object_type = self.schemas_dict_relation_2_subject_object[a_relationship]
            subject_type = subject_object_type[0][0]
            object_type = subject_object_type[0][1]
            #print("{} ---> ({}, {})".format(a_relationship, subject_type, object_type))
            spo_item = dict()
            spo_item["predicate"] = a_relationship
            spo_item["object_type"] = object_type
            spo_item["subject_type"] = subject_type
            spo_item["object"] = None
            spo_item["subject"] = None

            if object_type != subject_type:
                for idx, entity_tuple in enumerate(sort_entity_list):
                    if entity_tuple[0] == subject_type:
                        spo_item["subject"] = entity_tuple[1]
                        sort_entity_list[idx][2] += 1
                    if entity_tuple[0] == object_type:
                        spo_item["object"] = entity_tuple[1]
                        sort_entity_list[idx][2] += 1
            else:
                same_type_entity_list = [entity for entity_type, entity, loc in sort_entity_list if entity_type == object_type]
                for idx, entity in enumerate(same_type_entity_list):
                    if idx == 0:
                        spo_item["subject"] = entity
                    else:
                        spo_item["object"] = entity

                    if spo_item["subject"] is not None or spo_item["object"] is not None:
                        spo_list.append(spo_item)

            # 规则3
            if spo_item["subject"] is not None or spo_item["object"] is not None:
                spo_list.append(spo_item)

        spo_list.sort(key= lambda item:item['predicate'])
        # print(len(spo_list), spo_list)

        spo_list_len = len(spo_list)
        refer_spo_list_len = len(refer_spo_list)

        # if refer_spo_list_len==spo_list_len:
        def check_SPO_list():
            print("输入信息:")
            print(sort_relation_list)
            print(sort_entity_list)
            print(refer_spo_list)
            print("解析信息:")
            print("预测的关系：", len(sort_list_positive), sort_list_positive)
            print("预测的顺序实体：", len(sort_entity_list), sort_entity_list)
            print("参照的SPO列表：", refer_spo_list_len, refer_spo_list)
            print("预测的SPO列表：", spo_list_len, spo_list)
            print("\n")

        return spo_list


# 结合模型输出与先验知识（训练数据中抽取，没有利用外部资源）生成 spo_list。通过参数控制，可以在模型效果和速度上取舍！
class Sequence_Label_Priority_Combining_Statistical_Law_Rule(SPO_Generation_Rule_Base):

    def __init__(self, ):
        SPO_Generation_Rule_Base.__init__(self)
        self.spo_list_heuristic_generation = SPO_List_Heuristic_Generation()
        self.spo_predicate_temple = SPO_Predicate_Temple()

    # 程序调试时使用，显示指定关系输出
    def check_refer_spo_list_predicate(self, refer_spo_list, check_predicate_list):
        refer_predicate_list = [spo["predicate"] for spo in refer_spo_list]
        for predicate in check_predicate_list:
            if predicate in refer_predicate_list:
                return True
        return False

    # 生成 spo_list 返回  **对外接口函数**
    def rule_generate_spo_list(self, text_sentence, sort_relation_list, sort_entity_list, refer_spo_list, show_detail=False):
        def _combine_a_b_spo_list(spo_list_superset_A, spo_list_superset_B):
            spo_list_superset = []  # TODO:编写函数逻辑处理而不是直接合并
            for a in spo_list_superset_A:
                spo_list_superset.append(a)
            for b in spo_list_superset_B:
                spo_list_superset.append(b)
            return spo_list_superset

        # 利用模型输出生成 spo_list
        spo_list_superset_by_model_output = self.generate_spo_list_by_model_output(text_sentence, sort_relation_list, sort_entity_list)
        # 利用先验知识生成 spo_list
        if len(spo_list_superset_by_model_output) == 0:
            spo_list_superset_by_key_word = self.generate_spo_list_only_by_priori_information(text_sentence)
            # 合并不同方法生成的 spo_list
            spo_list_superset = _combine_a_b_spo_list(spo_list_superset_by_model_output, spo_list_superset_by_key_word)
        else:
            spo_list_superset = spo_list_superset_by_model_output
        # 对 spo_list 超集进行剪枝
        spo_list = self.prune_spo_list_superset_and_change_order(spo_list_superset)
        #show_predicate_flag = self.check_refer_spo_list_predicate(refer_spo_list, ['面积', '人口数量'] )
        show_predicate_flag = False
        if show_predicate_flag and random.random()> 0.7 :
            print("text_sentence:        ", text_sentence)
            print("sort_relation_list:   ", sort_relation_list)
            print("sort_entity_list:     ", sort_entity_list)
            print("-"*100)
            print("refer_spo_list:       ", refer_spo_list)
            #print("spo_list_superset_A:   ", spo_list_superset_by_model_output)
            #print("spo_list_superset_B:   ", spo_list_superset_by_key_word)
            print("spo_list:             ", spo_list)
            print("\n")

        return spo_list

    # 利用先验知识生成候选 spo_list
    def generate_spo_list_only_by_priori_information(self, text_sentence):
        # TODO：Wait coding 等待编写代码通过先验信息处理的关系
        wait_relation_list = ["总部地点", "目", "简称", "上映时间", "所属专辑", "注册资本", "首都", "身高",
                            "出品公司", "修业年限", "出生日期", "国籍", "海拔", "连载网站", "民族", "出版社",
                            "专业代码", "主角", "毕业院校", "占地面积", "官方语言", "邮政编码",
                            "所在城市", "作者", "气候", "改编自"]
        # 已经可以通过先验信息处理的关系
        relation_list = ["祖籍", "出生地", "董事长", "创始人", "主持人", "嘉宾", '面积', '人口数量',
                        '字', '朝代', '号', '歌手', '作词', '作曲', '父亲', '妻子', '母亲', '丈夫',
                         '导演', '制片人', '编剧', '主演', "成立日期"]
        spo_list_by_priori_info = []
        for relation_name in relation_list:
                spo_list_by_temple = self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence)
                spo_list_by_priori_info.extend(spo_list_by_temple)
        return spo_list_by_priori_info

    #利用模型输出生成候选 spo_list
    def generate_spo_list_by_model_output(self, text_sentence, sort_relation_list, sort_entity_list):
        spo_list = []
        # 单独处理 ('Number', '行政区'): ['面积', '人口数量'], 问题
        mianji_spo_list, sort_relation_list = self.handle_mianji_renkoushuliang_problem(text_sentence, sort_relation_list, sort_entity_list)
        spo_list.extend(mianji_spo_list)
        #spo_list.extend(mianji_spo_list)
        # 单独处理 ('人物', '电视综艺'): ['主持人', '嘉宾'], 问题
        sort_relation_list = self.handle_zhuchiren_jiabin_problem(text_sentence, sort_relation_list, sort_entity_list)
        # 单独处理 ('人物', '企业'): ['董事长', '创始人'], 问题
        sort_relation_list = self.handle_dongshizhang_chuangshiren_problem(text_sentence, sort_relation_list, sort_entity_list)
        # 单独处理 ('地点', '人物'): ['祖籍', '出生地'],问题
        sort_relation_list = self.handle_zuji_chushengdi_problem(text_sentence, sort_relation_list, sort_entity_list)
        # 单独处理 ('人物', '人物'): ['父亲', '妻子', '母亲', '丈夫'] 问题
        renwu_renwu_problem_spo_list, sort_relation_list = self.handle_renwu_renwu_problem(text_sentence, sort_relation_list, sort_entity_list)
        spo_list.extend(renwu_renwu_problem_spo_list)
        # 使用先验知识调整关系列表
        sort_relation_list = self.use_prior_knowledg_adjustment_relationships(sort_relation_list, text_sentence)
        # 划分模型输出的关系为正负列表
        relation_positive_list, relation_negative_list = self._split_relationship_by_score(sort_relation_list)
        # 划分正关系为 单\多重 关系
        relation_positive_single_list, relation_positive_multiple_list = \
            self._split_relationship_by_single_or_multiple(relation_positive_list)
        # 处理单关系
        spo_list_by_single = self.handle_single_relation(text_sentence, relation_positive_single_list, sort_entity_list)
        spo_list.extend(spo_list_by_single)
        # 处理多重关系
        spo_list_by_grouping_form = self.handle_multiple_relations_in_grouping_form(
            text_sentence, relation_positive_multiple_list, sort_entity_list)
        spo_list.extend(spo_list_by_grouping_form)
        return spo_list

    def handle_mianji_renkoushuliang_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        #在候选词列表 candidate_word_list 中找出距离中心词 center_word 最近的词语
        def find_word_B_nearest_to_word_A_for_single_relation(text_sentence, center_word, candidate_word_list):
            candidate_word_list_distance = []
            if center_word in text_sentence:
                word_A_index = text_sentence.index(center_word) + len(center_word) / 2
                candidate_word_list.reverse()  # 列表反顺序，是为了当有两个单词距离中心词相同距离时，优先返回右边的单词
            else:
                word_A_index = 0
            for candidate_word in candidate_word_list:
                if candidate_word in text_sentence:
                    candidate_word_index = text_sentence.index(candidate_word) + len(candidate_word) / 2
                else:
                    candidate_word_index = 1000
                candidate_word_list_distance.append(abs(candidate_word_index - word_A_index))
            if len(candidate_word_list_distance) > 0 :
                nearest_word = candidate_word_list[candidate_word_list_distance.index(min(candidate_word_list_distance))]
                return nearest_word
            else:
                return ""
        spo_list = []
        relation_list_new = []
        is_mianji_ren_kou_problem = False
        is_mianji_problem = False
        is_renkou_problem = False
        for relation_name, relation_value in sort_relation_list:
            if relation_name == "面积" or relation_name == "人口数量":
                relation_list_new.append((relation_name, 0.0))
            relation_list_new.append((relation_name, relation_value))
        for relation_name, relation_value in sort_relation_list:
            if relation_name in ["面积", "人口数量"] and relation_value > 0.5:
                is_mianji_ren_kou_problem = True
        for mianji_feature_word in ["面积", "公顷", "平方千米", "平方公里", "亩"]:
            if mianji_feature_word in text_sentence:
                is_mianji_problem = True
                break
        for renkou_feature_word in ["人口数量", "人口", "口人", "万人"]:
            if renkou_feature_word in text_sentence:
                is_renkou_problem = True
                break
        if is_mianji_ren_kou_problem or is_mianji_problem or is_renkou_problem:
            xingzhengqu_list = self.spo_predicate_temple.get_entity_value_list_by_name("行政区", sort_entity_list)
            Number_list = self.spo_predicate_temple.get_entity_value_list_by_name("Number", sort_entity_list)
            if len(xingzhengqu_list) == 1:
                xingzhengqu = xingzhengqu_list[0]
                for Number in Number_list[:]:
                    if "人" in Number:
                        spo_item = self.spo_predicate_temple.create_new_spo_item("人口数量", 'Number', '行政区', Number, xingzhengqu)
                        spo_list.append(spo_item)
                        Number_list.remove(Number)
                    else:
                        for mianji_feature_word in ["公顷", "平方", "亩"]:
                            if mianji_feature_word in Number:
                                spo_item = self.spo_predicate_temple.create_new_spo_item("面积", 'Number', '行政区', Number, xingzhengqu)
                                spo_list.append(spo_item)
                                Number_list.remove(Number)
                                break
                if len(Number_list) > 0:
                    for Number in Number_list:
                        flag = find_word_B_nearest_to_word_A_for_single_relation(text_sentence, Number, ["人", "面积"])
                        if flag == "人" and "平方" not in Number:
                            spo_item = self.spo_predicate_temple.create_new_spo_item("人口数量", 'Number', '行政区', Number, xingzhengqu)
                            spo_list.append(spo_item)
                        else:
                            if "人" not in Number:
                                spo_item = self.spo_predicate_temple.create_new_spo_item("面积", 'Number', '行政区', Number, xingzhengqu)
                                spo_list.append(spo_item)
        if len(spo_list) == 0:
            for relation_name in ["人口数量", "面积"]:
                spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation_name, text_sentence))
        return spo_list, relation_list_new

    def handle_zhuchiren_jiabin_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        change_flag = False
        relation_list_new = []
        for (relation_name, relation_value) in sort_relation_list[:]:
            if relation_name in ["主持人", "嘉宾"] and relation_value < 0.5:
                location_relation_word = self.spo_list_heuristic_generation.relational_location_word[relation_name]
                for location_word in location_relation_word:
                    if location_word in text_sentence:
                        relation_list_new.append((relation_name, 0.9))
                        change_flag = True
                        break
            else:
                relation_list_new.append((relation_name, relation_value))
        if change_flag:
            relation_list_new = sorted(relation_list_new, key=lambda x: x[1], reverse=True)
            return relation_list_new
        else:
            return sort_relation_list

    def handle_dongshizhang_chuangshiren_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        change_flag = False
        relation_list_new = []
        for relation_name, relation_value in sort_relation_list:
            if relation_name in ["董事长", "创始人"] and relation_value < 0.5:
                location_relation_word = self.spo_list_heuristic_generation.relational_location_word[relation_name]
                for location_word in location_relation_word:
                    if location_word in text_sentence:
                        relation_list_new.append((relation_name, 0.9))
                        change_flag = True
                        break
            else:
                relation_list_new.append((relation_name, relation_value))
        if change_flag:
            relation_list_new = sorted(relation_list_new, key=lambda x: x[1], reverse=True)
            return relation_list_new
        else:
            return sort_relation_list

    #处理( '地点', '人物'): ['祖籍', '出生地'], 问题
    def handle_zuji_chushengdi_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        change_flag = False
        relation_list_new = []
        for relation_name, relation_value in sort_relation_list:
            if relation_name == "祖籍" and "祖籍" in text_sentence and relation_value < 0.5:
                relation_list_new.append((relation_name, 0.9))
                change_flag = True
            else:
                relation_list_new.append((relation_name, relation_value))

        if change_flag:
            relation_list_new = sorted(relation_list_new, key=lambda x: x[1], reverse=True)
            return relation_list_new
        else:
            return sort_relation_list

    # 处理 ('人物', '人物'): ['父亲', '妻子', '母亲', '丈夫'] 问题
    def handle_renwu_renwu_problem(self, text_sentence, sort_relation_list, sort_entity_list):
        spo_list = []
        is_renwu_renwu_problem = False
        renwu_entity_number = 0
        ren_ren_problem_possibility_dict = dict()
        # 获取['父亲', '妻子', '母亲', '丈夫']可能性大小
        for relation, value in sort_relation_list:
            if relation in ['父亲', '妻子', '母亲', '丈夫']:
                ren_ren_problem_possibility_dict[relation] = value

        for entity_name, entity_value in sort_entity_list:
            if entity_name == "人物":
                renwu_entity_number += 1

        if renwu_entity_number >= 2:
            for item in sort_relation_list[0:4]: #只查看排序关系列表的前四位确定是否为 renwu_renwu_problem
                relation, value = item
                if relation in ['父亲', '妻子', '母亲', '丈夫']:
                    sort_relation_list.remove(item)
                    is_renwu_renwu_problem = True

        # ('人物', '人物'): ['父亲', '妻子', '母亲', '丈夫'],
        def heuristic_generate_fuqin_muqin_zhangfu_qizi(text_sentence, ren_ren_problem_possibility_dict, sort_entity_list):
            spo_list = []
            greater_flag = False
            for relation, value in ren_ren_problem_possibility_dict.items():
                if value > 0.5:
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation, text_sentence))
                    # print("@@heuristic_generate_fuqin_muqin_zhangfu_qizi由先验知识获取",
                    #       self.spo_predicate_temple.temple_priori_information(relation, text_sentence))
                    greater_flag = True
            if greater_flag == False:
                for relation, value in ren_ren_problem_possibility_dict.items():
                    spo_list.extend(self.spo_predicate_temple.temple_priori_information(relation, text_sentence))
            return spo_list
        if is_renwu_renwu_problem:
            spo_list = heuristic_generate_fuqin_muqin_zhangfu_qizi(text_sentence, ren_ren_problem_possibility_dict, sort_entity_list)
        return spo_list, sort_relation_list

    # 处理单关系
    def handle_single_relation(self, text_sentence, relation_positive_single_list, sort_entity_list):
        #在候选词列表 candidate_word_list 中找出距离中心词 center_word 最近的词语
        def find_word_B_nearest_to_word_A_for_single_relation(text_sentence, center_word, candidate_word_list):
            candidate_word_list_distance = []
            if center_word in text_sentence:
                word_A_index = text_sentence.index(center_word) + len(center_word) / 2
                candidate_word_list.reverse()  # 列表反顺序，是为了当有两个单词距离中心词相同距离时，优先返回右边的单词
            else:
                word_A_index = 0
            for candidate_word in candidate_word_list:
                if candidate_word in text_sentence:
                    candidate_word_index = text_sentence.index(candidate_word) + len(candidate_word) / 2
                else:
                    candidate_word_index = 1000
                candidate_word_list_distance.append(abs(candidate_word_index - word_A_index))
            if len(candidate_word_list_distance) > 0 :
                nearest_word = candidate_word_list[candidate_word_list_distance.index(min(candidate_word_list_distance))]
                return nearest_word
            else:
                return ""

        spo_list = []
        if len(sort_entity_list) <= 1:
            return []
        if len(sort_entity_list) == 2:
            for relation_name in relation_positive_single_list:
                spo_list_by_temple_one = self.spo_predicate_temple.temple_one(relation_name, sort_entity_list)
                spo_list.extend(spo_list_by_temple_one)
        else:
            for relation_name in relation_positive_single_list:
                subject_type = self.schemas_dict_relation_2_subject_object[relation_name][0][0]
                object_type = self.schemas_dict_relation_2_subject_object[relation_name][0][1]
                subject_value_list = self.spo_predicate_temple.get_entity_value_list_by_name(subject_type, sort_entity_list)
                object_value_list = self.spo_predicate_temple.get_entity_value_list_by_name(object_type, sort_entity_list)
                subject_value_list_len = len(subject_value_list)
                object_value_list_len = len(object_value_list)
                if relation_name in ['主持人', '嘉宾']: #('人物', '电视综艺'): ['主持人', '嘉宾'],
                    for subject_value in subject_value_list:
                        object_value = find_word_B_nearest_to_word_A_for_single_relation(text_sentence, subject_value,
                                                                                         object_value_list)
                        spo_item = self.spo_predicate_temple.create_new_spo_item(relation_name, subject_type,
                                                                                 object_type, subject_value,
                                                                                 object_value)
                        spo_list.append(spo_item)
                else:
                    if object_value_list_len <= subject_value_list_len:
                        for object_value in object_value_list:
                            subject_value = find_word_B_nearest_to_word_A_for_single_relation(text_sentence, object_value, subject_value_list)
                            spo_item = self.spo_predicate_temple.create_new_spo_item(relation_name, subject_type, object_type, subject_value,
                                                                object_value)
                            spo_list.append(spo_item)
                    else:
                        for subject_value in subject_value_list:
                            object_value = find_word_B_nearest_to_word_A_for_single_relation(text_sentence, subject_value, object_value_list)
                            spo_item = self.spo_predicate_temple.create_new_spo_item(relation_name, subject_type, object_type, subject_value,
                                                                object_value)
                            spo_list.append(spo_item)
        return spo_list

    # 用分组的办法处理多重关系
    def handle_multiple_relations_in_grouping_form(self, text_sentence, relation_positive_multiple_list, sort_entity_list):
        def split_form_relation_by_one_zero_flag(need_analysis_relation_flag_dict):
            need_analysis_relation_list = [relation for relation, flag in need_analysis_relation_flag_dict.items() if flag == 1]
            return need_analysis_relation_list

        spo_list = []
        if len(sort_entity_list) <= 1:
            return []
        # 多关系分组
        form_zuji_chushengdi = ["祖籍", "出生地"]
        form_dongshizhang_chuangshiren = ["董事长", "创始人"]
        form_zhuchiren_jiabin = ["主持人", "嘉宾"]
        form_mianji_renkoushuliang = ['面积', '人口数量']
        form_zi_chaodai_hao = ['字', '朝代', '号']
        form_geshou_zuoci_zuoqu = ['歌手', '作词', '作曲']
        form_daoyan_zhipianren_bianju_zhuyan = ['导演', '制片人', '编剧', '主演']
        multiple_relations_in_group_list = [form_zuji_chushengdi, form_dongshizhang_chuangshiren, form_zhuchiren_jiabin,
                                            form_mianji_renkoushuliang, form_zi_chaodai_hao, form_geshou_zuoci_zuoqu,
                                            form_geshou_zuoci_zuoqu, form_daoyan_zhipianren_bianju_zhuyan]
        # 以组的形式遍历多重关系列表
        for multiple_relations_form in multiple_relations_in_group_list:
            need_analysis_relation_flag_dict = dict()
            for relation in multiple_relations_form:
                if relation in relation_positive_multiple_list:
                    need_analysis_relation_flag_dict[relation] = 1
                else:
                    need_analysis_relation_flag_dict[relation] = 0
            need_analysis_relation_list = split_form_relation_by_one_zero_flag(need_analysis_relation_flag_dict)
            # 如果只有一个关系，仍然用单关系处理办法 TODO:针对['导演', '制片人', '编剧', '主演']，即使是单关系也应该使用不同的处理方法，后面改进
            if len(need_analysis_relation_list) == 1:
                spo_list.extend(self.handle_single_relation(text_sentence, need_analysis_relation_list, sort_entity_list))
            # 如果是有多个关系，则用启发式处理办法
            elif len(need_analysis_relation_list) > 1:
                spo_list.extend(self.spo_list_heuristic_generation.heuristic_handle_multiple_relations(
                    text_sentence, need_analysis_relation_flag_dict, sort_entity_list))
        # 多关系分组标志
        form_zuji_chushengdi_flag = False
        form_dongshizhang_chuangshiren_flag = False
        form_zhuchiren_jiabin_flag = False
        form_mianji_renkoushuliang_flag = False
        form_zi_chaodai_hao_flag = False
        form_geshou_zuoci_zuoqu_flag = False
        form_fuqin_muqin_zhangfu_qizi_flag = False
        form_daoyan_zhipianren_bianju_zhuyan_flag = False

        for relation in relation_positive_multiple_list:
            if relation in form_zuji_chushengdi:
                form_zuji_chushengdi_flag = True
            if relation in form_dongshizhang_chuangshiren:
                form_dongshizhang_chuangshiren_flag = True
            if relation in form_zhuchiren_jiabin:
                form_zhuchiren_jiabin_flag = True
            if relation in form_mianji_renkoushuliang:
                form_mianji_renkoushuliang_flag = True
            if relation in form_zi_chaodai_hao:
                form_zi_chaodai_hao_flag = True
            if relation in form_geshou_zuoci_zuoqu:
                form_geshou_zuoci_zuoqu_flag = True
            if relation in form_daoyan_zhipianren_bianju_zhuyan:
                form_daoyan_zhipianren_bianju_zhuyan_flag = True

        return spo_list

    # 对生成的列表进行剪枝
    def prune_spo_list_superset_and_change_order(self, spo_list_superset, show_details=False):
        spo_list = []
        spo_list_superset_tuple = set()
        for spo in spo_list_superset:
            spo_list_superset_tuple.add(tuple((k, v) for k, v in spo.items()))
        for spo in spo_list_superset_tuple:
            spo_list.append(dict(spo))
        spo_list_ordered = []
        for spo in spo_list:
            spo_object_type = spo["object_type"]
            spo_predicate = spo["predicate"]
            spo_object = spo["object"]
            spo_subject_type = spo["subject_type"]
            spo_subject = spo["subject"]
            if len(spo_subject) > 0 and len(spo_object) > 0:
                spo_list_ordered.append({"predicate":spo_predicate,
                                         "object_type":spo_object_type, "subject_type":spo_subject_type,
                                         "object":spo_object, "subject":spo_subject, })
            else:
                #print("$$剪枝prune_spo_list_superset_and_change_order", spo)
                pass

        if show_details and (len(spo_list) < len(spo_list_superset)):
            print("prune_spo_list_superset...")
            print(len(spo_list), len(spo_list_superset))
            print(spo_list)
            print(spo_list_superset)
            print("\n")
        return spo_list_ordered

    # 使用先验知识调整关系列表
    def use_prior_knowledg_adjustment_relationships(self, sort_relation_list, text_sentence):
        # combine_relation_list = self.distinguishing_zu_ji_and_chu_sheng_di_relation(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_chuang_shi_ren_and_dong_shi_zhang(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_zhu_chi_ren_and_jia_bin(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_mian_ji_and_ren_kou_shu_liang(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_zi_chao_dai_and_hao(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_ge_shou_zuo_ci_and_zuo_qu(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_fu_qin_mu_qin_zhang_fu_and_qi_zi(combine_relation_list, text_sentence)
        # combine_relation_list = self.distinguishing_dao_yan_zhi_pian_ren_bian_ju_and_zhu_yan(combine_relation_list, text_sentence)
        relation_list_new = []
        for (relation_name, relation_value) in sort_relation_list:
            if relation_name in ['导演', '制片人', '编剧', '主演']:
                change_Flag = False
                feature_word_list = self.spo_list_heuristic_generation.relational_location_word[relation_name]
                for feature_word in feature_word_list:
                    if feature_word in text_sentence and relation_value < 0.5:
                        change_Flag = True
                        break
                if change_Flag:
                    relation_list_new.append((relation_name, 0.7))
                else:
                    relation_list_new.append((relation_name, relation_value))
            else:
                relation_list_new.append((relation_name, relation_value))

        sort_relation_list_new = sorted(relation_list_new, key=lambda x: x[1], reverse=True)

        # if relation_list_new != sort_relation_list_new:
        #     print("@@先验use_prior_knowledg_adjustment_relationships - sort_relation_list_new", sort_relation_list_new)
        #     print("@@先验use_prior_knowledg_adjustment_relationships - sort_relation_list_old", sort_relation_list)
        return sort_relation_list_new

    # 结合模型和先验知识预测关系
    def combine_model_output_and_priori_knowledge_prediction_relation(self, text_sentence, sort_relation_list, sort_entity_list):
        # 由模型直接输出的关系
        relation_positive_list, relation_negative_list = self._split_relationship_by_score(sort_relation_list)
        # 序列实体名字列表
        subject_object_type_list = [name for name, value in sort_entity_list]
        # 由实体类型推测关系
        relation_infer_from_labeling_positive_list, relation_infer_from_labeling_supplement_list = self.subject_object_type_2_relation_list(subject_object_type_list)
        # 由句子中特征词推测关系
        relation_feature_by_feature_word_list = []
        # 使用先验知识调整关系列表
        combine_relation_list = self.use_prior_knowledg_adjustment_relationships(relation_positive_list, text_sentence)
        # 合并模型直接输出的关系、由实体类型推测的关系和特征词关系列表
        combine_relation_list = self._merge_possible_relation_list(relation_positive_list, relation_negative_list,
                                                                   relation_infer_from_labeling_positive_list,
                                                                   relation_infer_from_labeling_supplement_list,
                                                                   relation_feature_by_feature_word_list)
        # 去重
        combine_relation_list = list(set(combine_relation_list))
        return combine_relation_list

    # 合并由不同途径产生的被选关系
    def _merge_possible_relation_list(self, relation_positive_list, relation_negative_list,
                                     relation_infer_from_labeling_positive_list, relation_infer_from_labeling_supplement_list,
                                      relation_feature_by_feature_word_list, guaranteed_not_empty_relation_list=False):
        # 合并模型直接输出的正关系、由实体类型推测出的正关系
        combine_relation_list = list(set(relation_positive_list) | set(relation_infer_from_labeling_positive_list))
        # 合并特征词关系列表
        combine_relation_list = list(set(combine_relation_list) | set(relation_feature_by_feature_word_list))
        # 如果并集仍然为空，且 guaranteed_not_empty_relation_list = True，则添加使用模型直接输出相对概率最大的关系（概率<0.5）
        if guaranteed_not_empty_relation_list and len(combine_relation_list) == 0:
            combine_relation_list.append(relation_negative_list[0])
        return combine_relation_list

    # 由实体类型推测可能关系
    def subject_object_type_2_relation_list(self, subject_object_type_list):
        #由实体推出的单关系，例如('地点', '企业')--> ['总部地点'],  正关系列表
        relation_infer_from_labeling_positive_list = []
        #由实体推出的多关系，例如('人物', '歌曲')-->['歌手', '作词', '作曲']，由于这样会导致多出冗余关系，难以区分，所以仅仅做补充参考
        relation_infer_from_labeling_supplement_list = []
        # 根据多个实体类型的各种组合找最可能的关系：
        if len(subject_object_type_list) >= 2:
            subject_object_type_permutations = permutations(subject_object_type_list, 2)
            lawful_subject_object_type_tuple_list = [
                subject_object for subject_object in subject_object_type_permutations
                if subject_object in self.schemas_dict_subject_object_2_relation]
            relation_infer_from_labeling_positive_list = list()
            for subject_object in lawful_subject_object_type_tuple_list:
                if subject_object not in [('地点', '人物'), ('人物', '企业'), ('人物', '电视综艺'),
                                          ('Number', '行政区'), ('Text', '历史人物'), ('人物', '歌曲'),
                                          ('人物', '人物'), ('人物', '影视作品')]:
                    relation_infer_from_labeling_positive_list.extend(self.schemas_dict_subject_object_2_relation[subject_object])
                else:
                    relation_infer_from_labeling_supplement_list.extend(self.schemas_dict_subject_object_2_relation[subject_object])
        return relation_infer_from_labeling_positive_list, relation_infer_from_labeling_supplement_list

if __name__=='__main__':
    sorted_relation_and_entity_list = Sorted_relation_and_entity_list_Management(TEST_DATA_DIR="../data/SKE_2019/test", MODEL_OUTPUT_DIR="../output/20190319code_test", Competition_Mode=False)
    relation_first_rule = Relationship_Priority_Rule()





