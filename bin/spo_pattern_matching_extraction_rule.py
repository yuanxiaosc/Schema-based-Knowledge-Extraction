from .priori_statistical_information import Priori_statistical_information
#from .priori_statistical_information_from_file import Priori_statistical_information

class SPO_pattern_matching(Priori_statistical_information):

    def __init__(self):
        Priori_statistical_information.__init__(self)

    def spo_pattern_matching_extraction_rule_by_relation(self, relation_name, sentence_text):
        if relation_name == "祖籍":
            return self.zu_ji_relation_extract_raw_text(sentence_text)
        elif relation_name == "出生地":
            return self.chu_sheng_di_extract_raw_text(sentence_text)
        elif relation_name == "董事长":
            return self.dong_shi_zhang_extract_raw_text(sentence_text)
        elif relation_name == "创始人":
            return self.chu_sheng_di_extract_raw_text(sentence_text)
        elif relation_name == "主持人":
            return self.zhu_chi_ren_extract_raw_text(sentence_text)
        elif relation_name == "嘉宾":
            return self.jia_bin_extract_raw_text(sentence_text)
        elif relation_name == "面积":
            return self.mian_ji_extract_raw_text(sentence_text)
        elif relation_name == "人口数量":
            return self.ren_kou_shu_liang_extract_raw_text(sentence_text)
        elif relation_name == "字":
            return self.zi_extract_raw_text(sentence_text)
        elif relation_name == "朝代":
            return self.chao_dai_extract_raw_text(sentence_text)
        elif relation_name == "号":
            return self.hao_extract_raw_text(sentence_text)
        elif relation_name == "歌手":
            return self.ge_shou_extract_raw_text(sentence_text)
        elif relation_name == "作词":
            return self.zuo_ci_extract_raw_text(sentence_text)
        elif relation_name == "作曲":
            return self.zuo_qu_extract_raw_text(sentence_text)
        elif relation_name == "父亲":
            return self.fu_qin_extract_raw_text(sentence_text)
        elif relation_name == "母亲":
            return self.mu_qin_extract_raw_text(sentence_text)
        elif relation_name == "丈夫":
            return self.zhang_fu_extract_raw_text(sentence_text)
        elif relation_name == "妻子":
            return self.qi_zi_extract_raw_text(sentence_text)
        elif relation_name == "导演":
            return self.dao_yan_extract_raw_text(sentence_text)
        elif relation_name == "制片人":
            return self.zhi_pian_ren_extract_raw_text(sentence_text)
        elif relation_name == "编剧":
            return self.bian_ju_extract_raw_text(sentence_text)
        elif relation_name == "主演":
            return self.zhu_yan_extract_raw_text(sentence_text)
        else:
            raise ValueError()

    def dao_yan_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_dao_yan
        feature_word_set.add("导演")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def zhi_pian_ren_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_zhi_pian_ren
        feature_word_set.add("制片人")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def bian_ju_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_bian_ju
        feature_word_set.add("编剧")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def zhu_yan_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_zhu_yan
        feature_word_set.add("主演")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def zhang_fu_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_zhang_fu
        feature_word_set.add("丈夫")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def qi_zi_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_qi_zi
        feature_word_set.add("妻子")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def mu_qin_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_mu_qin
        feature_word_set.add("母亲")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def fu_qin_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_fu_qin
        feature_word_set.add("父亲")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def zuo_qu_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_zuo_qu
        feature_word_set.add("作曲")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def zuo_ci_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_zuo_ci
        feature_word_set.add("作词")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def ge_shou_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_ge_shou
        feature_word_set.add("歌手")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def hao_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_hao
        feature_word_set.add("号")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def chao_dai_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_chao_dai
        feature_word_set.add("朝代")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def zi_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_zi
        feature_word_set.add("字")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def mian_ji_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_mian_ji
        for word in ["面积", "公顷", "平方千米", "平方公里", "亩"]:
            feature_word_set.add(word)
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def ren_kou_shu_liang_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_ren_kou_shu_liang
        for word in ["人口数量", "人口", "口人", "万人"]:
            feature_word_set.add(word)
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def jia_bin_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_jia_bin
        feature_word_set.add("嘉宾")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def zhu_chi_ren_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_zhu_chi_ren
        feature_word_set.add("主持人")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, value

    def dong_shi_zhang_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_dong_shi_zhang
        feature_word_set.add("董事长")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, None

    def chuang_shi_ren_extract_raw_text(self, text):
        relation_existence_flag, value = False, None
        feature_word_set = self.special_entity_map_chuang_shi_ren
        feature_word_set.add("创始人")
        for feature_word in feature_word_set:
            if feature_word in text:
                relation_existence_flag = True
                break
        return relation_existence_flag, None

    def chu_sheng_di_extract_raw_text(self, text):
        feature_word_list = ["出生地", "出生于"]
        relation_existence_flag = any([True for feature_word in feature_word_list if feature_word in text])
        return relation_existence_flag, None

    def zu_ji_relation_extract_raw_text(self, text):
        feature_word_list = ["祖籍", "籍贯"]
        relation_existence_flag = any([True for feature_word in feature_word_list if feature_word in text])
        if "祖籍" in text or "籍贯" in text:
            zu_ji_contain_str = ""
            if "祖籍" in text:
                zu_ji_index = text.index("祖籍")
                zu_ji_contain_str = text[zu_ji_index:]
            elif "籍贯" in text:
                zu_ji_index = text.index("籍贯")
                zu_ji_contain_str = text[zu_ji_index:]
            if "，" in zu_ji_contain_str:
                the_nearest_comma_index = zu_ji_contain_str.index("，")
                zu_ji_contain_str = zu_ji_contain_str[:the_nearest_comma_index]
            elif "、" in zu_ji_contain_str:
                the_nearest_dun_index = zu_ji_contain_str.index("、")
                zu_ji_contain_str = zu_ji_contain_str[:the_nearest_dun_index]
            if " " in zu_ji_contain_str:
                k_index = zu_ji_contain_str.index(" ")
                zu_ji_contain_str = zu_ji_contain_str[:k_index]
            for redundancy_word in ["祖籍是", "祖籍在", "祖籍", "籍贯是", "籍贯"]:
                zu_ji_contain_str = zu_ji_contain_str.replace(redundancy_word, "")
            return relation_existence_flag, zu_ji_contain_str
        return relation_existence_flag, None

