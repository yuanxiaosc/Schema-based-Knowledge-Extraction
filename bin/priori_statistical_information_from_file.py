import os

def read_special_entity_map_info_from_file(file_name, file_dir="bin/priori_info_storage"):
    with open(os.path.join(file_dir, file_name), "r", encoding="utf-8") as f:
        file_content = f.read()
        return eval(file_content)

class Priori_statistical_information(object):

    def __init__(self):
        # 根据 all_50_schemas 内容由 analysis_schemas.py 生成
        # 1 个 出现在多个三元组中的关系
        self.appears_in_more_than_one_tupules = {"成立日期"}
        # 36 个（主体，客体）-> [关系]                 # 不同关系三元组占比累计率：排行前21种关系累计占比达90.6%，前26占95.2%，前33占98.2%
                                                       # 累计长度率：三元组列表长度不超过3的占 89.1%，不超过4的94.3%，不超过8的99.2%
        self.schemas_dict_subject_object_2_relation = {
                                                        ('地点', '企业'): ['总部地点'],             #27 ('总部地点', 0.007)
                                                        ('目', '生物'): ['目'],                     #14 ('目', 0.03)
                                                        ('Text', '机构'): ['简称'],                 #33 ('简称', 0.003)
                                                        ('Date', '影视作品'): ['上映时间'],         #22 ('上映时间', 0.01)
                                                        ('音乐专辑', '歌曲'): ['所属专辑'],         #13 ('所属专辑', 0.03)
                                                        ('Number', '企业'): ['注册资本'],           #41 ('注册资本', 0.001)
                                                        ('城市', '国家'): ['首都'],                 #42 ('首都', 0.001)
                                                        ('Number', '人物'): ['身高'],               #25 ('身高', 0.008)
                                                        ('企业', '影视作品'): ['出品公司'],         #18 ('出品公司', 0.018)
                                                        ('Number', '学科专业'): ['修业年限'],       #49 ('修业年限', 0.0)
                                                        ('Date', '人物'): ['出生日期'],             #5  ('出生日期', 0.054)
                                                        ('国家', '人物'): ['国籍'],                 #10 ('国籍', 0.035)
                                                        ('Number', '地点'): ['海拔'],               #43 ('海拔', 0.001)
                                                        ('网站', '网络小说'): ['连载网站'],         #9  ('连载网站', 0.037)
                                                        ('Text', '人物'): ['民族'],                 #11 ('民族', 0.033)
                                                        ('出版社', '书籍'): ['出版社'],             #6  ('出版社', 0.051)
                                                        ('Text', '学科专业'): ['专业代码'],         #47 ('专业代码', 0.0)
                                                        ('人物', '网络小说'): ['主角'],             #45 ('主角', 0.001)
                                                        ('Date', '机构'): ['成立日期'],             #8  ('成立日期', 0.037)
                                                        ('学校', '人物'): ['毕业院校'],             #12 ('毕业院校', 0.033)
                                                        ('Number', '机构'): ['占地面积'],           #39 ('占地面积', 0.001)
                                                        ('语言', '国家'): ['官方语言'],             #46 ('官方语言', 0.0)
                                                        ('Text', '行政区'): ['邮政编码'],           #48 ('邮政编码', 0.0)
                                                        ('城市', '景点'): ['所在城市'],             #37 ('所在城市', 0.002)
                                                        ('人物', '图书作品'): ['作者'],             #2  ('作者', 0.097)
                                                        ('Date', '企业'): ['成立日期'],             #8  ('成立日期', 0.037)
                                                        ('气候', '行政区'): ['气候'],               #34 ('气候', 0.003)
                                                        ('作品', '影视作品'): ['改编自'],           #38 ('改编自', 0.002)

                                                       ('地点', '人物'): ['祖籍', '出生地'],        #7  ('出生地', 0.047), 28('祖籍', 0.005)                   0.052
                                                       ('人物', '企业'): ['董事长', '创始人'],      #36 ('创始人', 0.002),44('董事长', 0.001)                  0.003
                                                       ('人物', '电视综艺'): ['主持人', '嘉宾'],    #30 ('主持人', 0.004), 31('嘉宾', 0.004)                   0.008
                                                       ('Number', '行政区'): ['面积', '人口数量'],  #35 ('面积', 0.002), 40('人口数量', 0.001)                 0.003

                                                       ('Text', '历史人物'): ['字', '朝代', '号'],  #24 ('朝代', 0.01)，26('字', 0.008), 29('号', 0.004)       0.022
                                                       ('人物', '歌曲'): ['歌手', '作词', '作曲'],  #3  ('歌手', 0.073)，15('作曲', 0.028), 16('作词', 0.026)  0.127

                                                       ('人物', '人物'): ['父亲', '妻子', '母亲', '丈夫'],        #19 ('父亲', 0.013), 20('妻子', 0.01), 21('丈夫', 0.01)，23('母亲', 0.01)      0.043
                                                       ('人物', '影视作品'): ['导演', '制片人', '编剧', '主演']   #1  ('主演', 0.161), 4('导演', 0.063)，17('编剧', 0.019), 32('制片人', 0.003)  0.246
                                                        }
        # 49 个 关系 -> [（主体，客体）]
        self.schemas_dict_relation_2_subject_object = {
                                            '父亲': [('人物', '人物')],
                                            '妻子': [('人物', '人物')],
                                            '母亲': [('人物', '人物')],
                                            '丈夫': [('人物', '人物')],
                                                  '祖籍': [('地点', '人物')],
                                                  '总部地点': [('地点', '企业')],
                                                  '出生地': [('地点', '人物')],
                                                  '目': [('目', '生物')],
                                                  '面积': [('Number', '行政区')],
                                                  '简称': [('Text', '机构')],
                                                  '上映时间': [('Date', '影视作品')],
                                                  '所属专辑': [('音乐专辑', '歌曲')],
                                                  '注册资本': [('Number', '企业')],
                                                  '首都': [('城市', '国家')],
                                                  '导演': [('人物', '影视作品')],
                                                  '字': [('Text', '历史人物')],
                                                  '身高': [('Number', '人物')],
                                                  '出品公司': [('企业', '影视作品')],
                                                  '修业年限': [('Number', '学科专业')],
                                                  '出生日期': [('Date', '人物')],
                                                  '制片人': [('人物', '影视作品')],
                                                  '编剧': [('人物', '影视作品')],
                                                  '国籍': [('国家', '人物')],
                                                  '海拔': [('Number', '地点')],
                                                  '连载网站': [('网站', '网络小说')],
                                                  '朝代': [('Text', '历史人物')],
                                                  '民族': [('Text', '人物')],
                                                  '号': [('Text', '历史人物')],
                                                  '出版社': [('出版社', '书籍')],
                                                  '主持人': [('人物', '电视综艺')],
                                                  '专业代码': [('Text', '学科专业')],
                                                  '歌手': [('人物', '歌曲')],
                                                  '作词': [('人物', '歌曲')],
                                                  '主角': [('人物', '网络小说')],
                                                  '董事长': [('人物', '企业')],
                                                  '成立日期': [('Date', '机构'), ('Date', '企业')],
                                                  '毕业院校': [('学校', '人物')],
                                                  '占地面积': [('Number', '机构')],
                                                  '官方语言': [('语言', '国家')],
                                                  '邮政编码': [('Text', '行政区')],
                                                  '人口数量': [('Number', '行政区')],
                                                  '所在城市': [('城市', '景点')],
                                                  '作者': [('人物', '图书作品')],
                                                  '作曲': [('人物', '歌曲')],
                                                  '气候': [('气候', '行政区')],
                                                  '嘉宾': [('人物', '电视综艺')],
                                                  '主演': [('人物', '影视作品')],
                                                  '改编自': [('作品', '影视作品')],
                                                  '创始人': [('人物', '企业')]}
        # 16 个 主体集合
        self.subject_type_sort_list = [
                                 'Date', 'Number', 'Text',
                                 '人物', '企业', '作品', '出版社',
                                 '国家', '地点', '城市', '学校',
                                 '气候', '目', '网站', '语言', '音乐专辑']
        # 50 个 所有关系列表
        self.predicate_sort_list = [
                               '丈夫', '上映时间', '专业代码', '主持人', '主演', '主角', '人口数量', '作曲', '作者', '作词', '修业年限', '出品公司', '出版社',
                               '出生地', '出生日期', '创始人', '制片人', '占地面积', '号', '嘉宾', '国籍', '妻子', '字', '官方语言', '导演', '总部地点',
                               '成立日期', '所在城市', '所属专辑', '改编自', '朝代', '歌手', '母亲', '毕业院校', '民族', '气候', '注册资本', '海拔', '父亲',
                               '目', '祖籍', '简称', '编剧', '董事长', '身高', '连载网站', '邮政编码', '面积', '首都']
        # 16 个 客体集合
        self.object_type_sort_list = [
                                  '书籍', '人物', '企业', '历史人物',
                                  '国家', '图书作品', '地点', '学科专业',
                                  '影视作品', '景点', '机构', '歌曲', '生物',
                                  '电视综艺', '网络小说', '行政区']

        # 4 个 既能做主体又能做客体集合
        self.object_type_inter_subject_type_set = {'国家', '企业', '地点', '人物'}

        # 28 种 主体客体的类型
        self.subject_type_and_object_type_sort_list = [
                                                  'Date', 'Number', 'Text', '书籍', '人物', '企业', '作品', '出版社', '历史人物', '国家',
                                                  '图书作品', '地点', '城市', '学校', '学科专业', '影视作品', '景点', '机构', '歌曲', '气候',
                                                  '生物', '电视综艺', '目', '网站', '网络小说', '行政区', '语言', '音乐专辑']

        # special_entity_map
        self.special_entity_map_bian_ju = read_special_entity_map_info_from_file("special_entity_map_bian_ju")
        self.special_entity_map_bian_ju_2_ying_shi_zuo_pin = read_special_entity_map_info_from_file(
            "special_entity_map_bian_ju_2_ying_shi_zuo_pin")
        self.special_entity_map_chao_dai = read_special_entity_map_info_from_file("special_entity_map_chao_dai")
        self.special_entity_map_chao_dai_2_li_shi_ren_wu = read_special_entity_map_info_from_file(
            "special_entity_map_chao_dai_2_li_shi_ren_wu")
        self.special_entity_map_chuang_shi_ren = read_special_entity_map_info_from_file(
            "special_entity_map_chuang_shi_ren")
        self.special_entity_map_chuang_shi_ren_2_qiye = read_special_entity_map_info_from_file(
            "special_entity_map_chuang_shi_ren_2_qiye")
        self.special_entity_map_dao_yan = read_special_entity_map_info_from_file("special_entity_map_dao_yan")
        self.special_entity_map_dao_yan_2_ying_shi_zuo_pin = read_special_entity_map_info_from_file(
            "special_entity_map_dao_yan_2_ying_shi_zuo_pin")
        self.special_entity_map_dian_shi_zong_yi = read_special_entity_map_info_from_file(
            "special_entity_map_dian_shi_zong_yi")
        self.special_entity_map_dian_shi_zong_yi_2_jia_bin = read_special_entity_map_info_from_file(
            "special_entity_map_dian_shi_zong_yi_2_jia_bin")
        self.special_entity_map_dian_shi_zong_yi_2_zhu_chi_ren = read_special_entity_map_info_from_file(
            "special_entity_map_dian_shi_zong_yi_2_zhu_chi_ren")
        self.special_entity_map_dong_shi_zhang = read_special_entity_map_info_from_file(
            "special_entity_map_dong_shi_zhang")
        self.special_entity_map_dong_shi_zhang_2_qiye = read_special_entity_map_info_from_file(
            "special_entity_map_dong_shi_zhang_2_qiye")
        self.special_entity_map_fu_qin = read_special_entity_map_info_from_file("special_entity_map_fu_qin")
        self.special_entity_map_fu_qin_2_zi_nv = read_special_entity_map_info_from_file(
            "special_entity_map_fu_qin_2_zi_nv")
        self.special_entity_map_ge_qu = read_special_entity_map_info_from_file("special_entity_map_ge_qu")
        self.special_entity_map_ge_qu_2_ge_shou = read_special_entity_map_info_from_file(
            "special_entity_map_ge_qu_2_ge_shou")
        self.special_entity_map_ge_qu_2_zuo_ci = read_special_entity_map_info_from_file(
            "special_entity_map_ge_qu_2_zuo_ci")
        self.special_entity_map_ge_qu_2_zuo_qu = read_special_entity_map_info_from_file(
            "special_entity_map_ge_qu_2_zuo_qu")
        self.special_entity_map_ge_shou = read_special_entity_map_info_from_file("special_entity_map_ge_shou")
        self.special_entity_map_ge_shou_2_ge_qu = read_special_entity_map_info_from_file(
            "special_entity_map_ge_shou_2_ge_qu")
        self.special_entity_map_hao = read_special_entity_map_info_from_file("special_entity_map_hao")
        self.special_entity_map_hao_2_li_shi_ren_wu = read_special_entity_map_info_from_file(
            "special_entity_map_hao_2_li_shi_ren_wu")
        self.special_entity_map_jia_bin = read_special_entity_map_info_from_file("special_entity_map_jia_bin")
        self.special_entity_map_jia_bin_2_dian_shi_zong_yi = read_special_entity_map_info_from_file(
            "special_entity_map_jia_bin_2_dian_shi_zong_yi")
        self.special_entity_map_li_shi_ren_wu = read_special_entity_map_info_from_file(
            "special_entity_map_li_shi_ren_wu")
        self.special_entity_map_li_shi_ren_wu_2_chao_dai = read_special_entity_map_info_from_file(
            "special_entity_map_li_shi_ren_wu_2_chao_dai")
        self.special_entity_map_li_shi_ren_wu_2_hao = read_special_entity_map_info_from_file(
            "special_entity_map_li_shi_ren_wu_2_hao")
        self.special_entity_map_li_shi_ren_wu_2_zi = read_special_entity_map_info_from_file(
            "special_entity_map_li_shi_ren_wu_2_zi")
        self.special_entity_map_mian_ji = read_special_entity_map_info_from_file("special_entity_map_mian_ji")
        self.special_entity_map_mian_ji_2_xing_zheng_qu = read_special_entity_map_info_from_file(
            "special_entity_map_mian_ji_2_xing_zheng_qu")
        self.special_entity_map_mu_qin = read_special_entity_map_info_from_file("special_entity_map_mu_qin")
        self.special_entity_map_mu_qin_2_zi_nv = read_special_entity_map_info_from_file(
            "special_entity_map_mu_qin_2_zi_nv")
        self.special_entity_map_pei_ou = read_special_entity_map_info_from_file("special_entity_map_pei_ou")
        self.special_entity_map_pei_ou_2_qi_zi = read_special_entity_map_info_from_file(
            "special_entity_map_pei_ou_2_qi_zi")
        self.special_entity_map_pei_ou_2_zhang_fu = read_special_entity_map_info_from_file(
            "special_entity_map_pei_ou_2_zhang_fu")
        self.special_entity_map_qi_ye = read_special_entity_map_info_from_file("special_entity_map_qi_ye")
        self.special_entity_map_qi_zi = read_special_entity_map_info_from_file("special_entity_map_qi_zi")
        self.special_entity_map_qi_zi_2_pei_ou = read_special_entity_map_info_from_file(
            "special_entity_map_qi_zi_2_pei_ou")
        self.special_entity_map_qiye_2_chuang_shi_ren = read_special_entity_map_info_from_file(
            "special_entity_map_qiye_2_chuang_shi_ren")
        self.special_entity_map_qiye_2_dong_shi_zhang = read_special_entity_map_info_from_file(
            "special_entity_map_qiye_2_dong_shi_zhang")
        self.special_entity_map_ren_kou_shu_liang = read_special_entity_map_info_from_file(
            "special_entity_map_ren_kou_shu_liang")
        self.special_entity_map_ren_kou_shu_liang_2_xing_zheng_qu = read_special_entity_map_info_from_file(
            "special_entity_map_ren_kou_shu_liang_2_xing_zheng_qu")
        self.special_entity_map_xing_zheng_qu = read_special_entity_map_info_from_file(
            "special_entity_map_xing_zheng_qu")
        self.special_entity_map_xing_zheng_qu_2_mian_ji = read_special_entity_map_info_from_file(
            "special_entity_map_xing_zheng_qu_2_mian_ji")
        self.special_entity_map_xing_zheng_qu_2_ren_kou_shu_liang = read_special_entity_map_info_from_file(
            "special_entity_map_xing_zheng_qu_2_ren_kou_shu_liang")
        self.special_entity_map_ying_shi_zuo_pin = read_special_entity_map_info_from_file(
            "special_entity_map_ying_shi_zuo_pin")
        self.special_entity_map_ying_shi_zuo_pin_2_bian_ju = read_special_entity_map_info_from_file(
            "special_entity_map_ying_shi_zuo_pin_2_bian_ju")
        self.special_entity_map_ying_shi_zuo_pin_2_dao_yan = read_special_entity_map_info_from_file(
            "special_entity_map_ying_shi_zuo_pin_2_dao_yan")
        self.special_entity_map_ying_shi_zuo_pin_2_zhi_pian_ren = read_special_entity_map_info_from_file(
            "special_entity_map_ying_shi_zuo_pin_2_zhi_pian_ren")
        self.special_entity_map_ying_shi_zuo_pin_2_zhu_yan = read_special_entity_map_info_from_file(
            "special_entity_map_ying_shi_zuo_pin_2_zhu_yan")
        self.special_entity_map_zhang_fu = read_special_entity_map_info_from_file("special_entity_map_zhang_fu")
        self.special_entity_map_zhang_fu_2_pei_ou = read_special_entity_map_info_from_file(
            "special_entity_map_zhang_fu_2_pei_ou")
        self.special_entity_map_zhi_pian_ren = read_special_entity_map_info_from_file("special_entity_map_zhi_pian_ren")
        self.special_entity_map_zhi_pian_ren_2_ying_shi_zuo_pin = read_special_entity_map_info_from_file(
            "special_entity_map_zhi_pian_ren_2_ying_shi_zuo_pin")
        self.special_entity_map_zhu_chi_ren = read_special_entity_map_info_from_file("special_entity_map_zhu_chi_ren")
        self.special_entity_map_zhu_chi_ren_2_dian_shi_zong_yi = read_special_entity_map_info_from_file(
            "special_entity_map_zhu_chi_ren_2_dian_shi_zong_yi")
        self.special_entity_map_zhu_yan = read_special_entity_map_info_from_file("special_entity_map_zhu_yan")
        self.special_entity_map_zhu_yan_2_ying_shi_zuo_pin = read_special_entity_map_info_from_file(
            "special_entity_map_zhu_yan_2_ying_shi_zuo_pin")
        self.special_entity_map_zi = read_special_entity_map_info_from_file("special_entity_map_zi")
        self.special_entity_map_zi_2_li_shi_ren_wu = read_special_entity_map_info_from_file(
            "special_entity_map_zi_2_li_shi_ren_wu")
        self.special_entity_map_zi_nv = read_special_entity_map_info_from_file("special_entity_map_zi_nv")
        self.special_entity_map_zi_nv_2_fu_qin = read_special_entity_map_info_from_file(
            "special_entity_map_zi_nv_2_fu_qin")
        self.special_entity_map_zi_nv_2_mu_qin = read_special_entity_map_info_from_file(
            "special_entity_map_zi_nv_2_mu_qin")
        self.special_entity_map_zuo_ci = read_special_entity_map_info_from_file("special_entity_map_zuo_ci")
        self.special_entity_map_zuo_ci_2_ge_qu = read_special_entity_map_info_from_file(
            "special_entity_map_zuo_ci_2_ge_qu")
        self.special_entity_map_zuo_qu = read_special_entity_map_info_from_file("special_entity_map_zuo_qu")
        self.special_entity_map_zuo_qu_2_ge_qu = read_special_entity_map_info_from_file(
            "special_entity_map_zuo_qu_2_ge_qu")

if __name__=="__main__":
    priori_info =  Priori_statistical_information()
    for object_info in dir(priori_info):
        print(object_info)