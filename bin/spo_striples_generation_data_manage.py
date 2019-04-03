#coding=gbk
import os

class File_Management(object):
    """读取TXT文件，以列表形式返回文件内容"""
    def __init__(self, TEST_DATA_DIR= None, MODEL_OUTPUT_DIR=None, RAW_DATA_DIR=None, Competition_Mode=False):
        self.TEST_DATA_DIR = TEST_DATA_DIR
        self.MODEL_OUTPUT_DIR = MODEL_OUTPUT_DIR
        self.RAW_DATA_DIR = RAW_DATA_DIR
        self.Competition_Mode = Competition_Mode

    def file_path_and_name(self):
        text_sentence_file_path = os.path.join(self.TEST_DATA_DIR, "text.txt")
        token_in_file_path = os.path.join(self.TEST_DATA_DIR, "token_in_not_UNK.txt")
        # 为了便于区分用 relationship 代替 prediction ，用 predicate 表示模型的输出
        predicate_relationship_file_path = os.path.join(self.MODEL_OUTPUT_DIR, "SPO_predicate_test_results.txt")
        predicate_token_label_file_path = os.path.join(self.MODEL_OUTPUT_DIR, "token_label_prediction_test_results.txt")

        file_path_list = [text_sentence_file_path, token_in_file_path,
                          predicate_relationship_file_path, predicate_token_label_file_path]
        file_name_list = ["text_sentence_list", "token_in_not_NUK_list ",
                          "predicate_relationship_list", "predicate_token_label_list",]
        if not self.Competition_Mode:
            spo_out_file_path = os.path.join(self.TEST_DATA_DIR, "spo_out.txt")
            file_path_list.append(spo_out_file_path)
            file_name_list.append("reference_spo_list")
        return file_path_list, file_name_list

    def read_file_return_content_list(self):
        file_path_list, file_name_list = self.file_path_and_name()
        content_list_summary = []
        for file_path in file_path_list:
            with open(file_path, "r", encoding='utf-8') as f:
                content_list = f.readlines()
                content_list = [content.replace("\n", "") for content in content_list]
                content_list_summary.append(content_list)
        content_list_length_summary = [(file_name, len(content_list)) for content_list, file_name in
                                       zip(content_list_summary, file_name_list)]
        file_line_number = self._check_file_line_numbers(content_list_length_summary)
        return content_list_summary, file_line_number

    def _check_file_line_numbers(self, content_list_length_summary):
        content_list_length_file_one = content_list_length_summary[0][1]
        for file_name, file_line_number in content_list_length_summary:
            assert file_line_number == content_list_length_file_one
        return content_list_length_file_one


class Sorted_relation_and_entity_list_Management(File_Management):
    """
    生成按概率大小排序的可能关系列表和按照原始句子中顺序排序的实体列表
    """
    def __init__(self, TEST_DATA_DIR= None, MODEL_OUTPUT_DIR=None, RAW_DATA_DIR=None, Competition_Mode=False):
        File_Management.__init__(self, TEST_DATA_DIR=TEST_DATA_DIR, MODEL_OUTPUT_DIR=MODEL_OUTPUT_DIR, RAW_DATA_DIR=RAW_DATA_DIR, Competition_Mode=Competition_Mode)
        # 关系列表 把模型输出的实数值对应为标签
        self.relationship_label_list = ['丈夫', '上映时间', '专业代码', '主持人', '主演', '主角', '人口数量', '作曲', '作者', '作词', '修业年限', '出品公司', '出版社', '出生地', '出生日期', '创始人', '制片人', '占地面积', '号', '嘉宾', '国籍', '妻子', '字', '官方语言', '导演', '总部地点', '成立日期', '所在城市', '所属专辑', '改编自', '朝代', '歌手', '母亲', '毕业院校', '民族', '气候', '注册资本', '海拔', '父亲', '目', '祖籍', '简称', '编剧', '董事长', '身高', '连载网站', '邮政编码', '面积', '首都']

    def get_input_list(self,):
        content_list_summary, self.file_line_number = self.read_file_return_content_list()
        if self.Competition_Mode:
            reference_spo_list = [None] * self.file_line_number
            content_list_summary.append(reference_spo_list)

        [text_sentence_list, token_in_list, predicate_relationship_list, predicate_token_label_list,
            reference_spo_list] = content_list_summary
        return text_sentence_list, token_in_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list

    # 把模型输出的关系按照可能性大小排序，然后输出排序后的列表
    def model_predicate_relationship_2_sort_list(self, predicate_relationship_list):
        relationship_dict = dict()
        for relationship_value, relationship_label in zip(predicate_relationship_list, self.relationship_label_list):
            relationship_dict[relationship_label] = float(relationship_value)
        relationship_dict = sorted(relationship_dict.items(), key=lambda x: x[1], reverse=True)
        return relationship_dict

    # 除去模型输出的特殊符号
    def _preprocessing_model_token_lable(self, predicate_token_label_list):

        predicate_token_label_list = predicate_token_label_list[1:-1]  # y_predict.remove('[CLS]') #y_predict.remove('[SEP]')
        #ToDo:检查错误，纠错
        return predicate_token_label_list

    #合并由WordPiece切分的词和单字
    def _merge_WordPiece_and_single_word(self, entity_sort_list):
        # [..['B-音乐专辑', '新', '地', '球', 'ge', '##nes', '##is'] ..]---> [..('音乐专辑', '新地球genesis')..]
        entity_sort_tuple_list = []
        for a_entity_list in entity_sort_list:
            entity_content = ""
            entity_type = None
            for idx, entity_part in enumerate(a_entity_list):
                if idx == 0:
                    entity_type = entity_part
                    if entity_type[:2] not in ["B-", "I-"]:
                        break
                else:
                    if entity_part.startswith("##"):
                        entity_content += entity_part.replace("##", "")
                    else:
                        entity_content += entity_part
            if entity_content != "":
                entity_sort_tuple_list.append((entity_type[2:], entity_content))
        return entity_sort_tuple_list

    # 把spo_out.txt 的[SPO_SEP] 分割形式转换成标准列表字典形式
    # 妻子 人物 人物 杨淑慧 周佛海[SPO_SEP]丈夫 人物 人物 周佛海 杨淑慧 ---> dict
    def _preprocessing_reference_spo_list(self, refer_spo_str):
        refer_spo_list = refer_spo_str.split("[SPO_SEP]")
        refer_spo_list = [spo.split(" ") for spo in refer_spo_list]
        refer_spo_list = [dict([('predicate', spo[0]),
                                ('object_type', spo[2]), ('subject_type', spo[1]),
                                ('object', spo[4]), ('subject', spo[3])]) for spo in refer_spo_list]
        refer_spo_list.sort(key= lambda item:item['predicate'])
        return refer_spo_list

    # 把模型输出实体标签按照原句中相对位置输出
    def model_token_label_2_entity_sort_tuple_list(self, token_in_not_UNK, predicate_token_label):
        """
        :param token_in_not_UNK:  ['紫', '菊', '花', '草', '是', '菊', '目', '，', '菊', '科', '，', '松', '果', '菊', '属', '的', '植', '物']
        :param predicate_token_label: ['B-生物', 'I-生物', 'I-生物', 'I-生物', 'O', 'B-目', 'I-目', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
        :return: [('B-生物', '紫菊花草'), ('B-目', '菊目')]
        """
        token_in_not_UNK_list = token_in_not_UNK.split(" ")
        predicate_token_label_list = predicate_token_label.split(" ")
        predicate_token_label_list = self._preprocessing_model_token_lable(predicate_token_label_list)
        entity_sort_list = []
        entity_part_list = []
        #TODO:需要检查以下的逻辑判断，可能写的不够完备充分
        for idx, token_label in enumerate(predicate_token_label_list):
            # 如果标签为 "O"
            if token_label == "O":
                # entity_part_list 不为空，则直接提交
                if len(entity_part_list) > 0:
                    entity_sort_list.append(entity_part_list)
                    entity_part_list = []
            # 如果标签以字符 "B-" 开始
            if token_label.startswith("B-"):
                # 如果 entity_part_list 不为空，则先提交原来 entity_part_list
                if len(entity_part_list) > 0:
                    entity_sort_list.append(entity_part_list)
                    entity_part_list = []
                entity_part_list.append(token_label)
                entity_part_list.append(token_in_not_UNK_list[idx])
                # 如果到了标签序列最后一个标签处
                if idx == len(predicate_token_label_list) - 1:
                    entity_sort_list.append(entity_part_list)
            # 如果标签以字符 "I-"  开始 或者等于 "[##WordPiece]"
            if token_label.startswith("I-") or token_label == "[##WordPiece]":
                # entity_part_list 不为空，则把该标签对应的内容并入 entity_part_list
                if len(entity_part_list) > 0:
                    entity_part_list.append(token_in_not_UNK_list[idx])
                    # 如果到了标签序列最后一个标签处
                    if idx == len(predicate_token_label_list) - 1:
                        entity_sort_list.append(entity_part_list)
        entity_sort_tuple_list = self._merge_WordPiece_and_single_word(entity_sort_list)
        return entity_sort_tuple_list

    # 检查 标签标注的各种可能情况，比如是否有实体连着标注，中间没有 "O" 相隔
    def check_token_label_out(self):
        text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list = self.get_input_list()

        for [text_sentence, token_in_not_UNK, predicate_relationship, predicate_token_label, refer_spo_str] in\
                zip(text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list):
            predicate_token_label_list = predicate_token_label.split(" ")
            predicate_token_label_list = self._preprocessing_model_token_lable(predicate_token_label_list)
            #print(predicate_token_label_list)
            special_B = 0
            for item in predicate_token_label_list:
                if item == "O":
                    special_B = 0
                if item.startswith("B-"):
                    special_B += 1
                if special_B >= 2:
                    print(text_sentence)
                    print(refer_spo_str)
                    print(predicate_token_label_list)
                    print("\n")
                    break
            if special_B >= 2:
                break

    # 分析 spo_list 在原句中的主客实体位置和数量关系
    def analysis_position_quantity_relations_of_spo_list_in_text_sentence(self):
        def sentence_visualization(text_sentence, spo_list):
            count_so_type = set()
            for spo in spo_list:
                spo_predicate = spo['predicate']
                spo_subject_type = spo['subject_type']
                spo_object_type = spo['object_type']
                spo_subject = spo['subject']
                spo_object = spo['object']
                text_sentence = text_sentence.replace(spo_subject, " [({}){}] ".format(spo_subject_type, spo_subject))
                text_sentence = text_sentence.replace(spo_object, " [({}){}] ".format(spo_object_type, spo_object))
                print("({}, {}):[{}]".format(spo_subject_type, spo_object_type, spo_predicate))
                count_so_type.add(spo_subject_type)
                count_so_type.add(spo_object_type)
            print(text_sentence)

            print("\n")
            return count_so_type

        text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list = self.get_input_list()
        file_line_number = 0
        spo_list_line_two = 0
        so_type_number_dict = dict()
        for [text_sentence, token_in_not_UNK, predicate_relationship, predicate_token_label, refer_spo_str] in\
                zip(text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list):
            refer_spo_list = self._preprocessing_reference_spo_list(refer_spo_str)
            file_line_number += 1
            refer_spo_list_len = len(refer_spo_list)
            if refer_spo_list_len ==5:
                spo_list_line_two += 1
                count_so_type = sentence_visualization(text_sentence, refer_spo_list)
                #print("\n")
                so_type_number_dict[len(count_so_type)] = so_type_number_dict.setdefault(len(count_so_type), 0) + 1
        print(so_type_number_dict)
        print(spo_list_line_two, file_line_number, spo_list_line_two / file_line_number)

    # 生成排好序的关系列表和实体列表
    def produce_relationship_and_entity_sort_list(self):
        text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list = self.get_input_list()

        for [text_sentence, token_in_not_UNK, predicate_relationship, predicate_token_label, refer_spo_str] in\
                zip(text_sentence_list, token_in_not_UNK_list, predicate_relationship_list, predicate_token_label_list, reference_spo_list):

            predicate_relationship_sort_list = self.model_predicate_relationship_2_sort_list(predicate_relationship.split())
            entity_sort_tuple_list = self.model_token_label_2_entity_sort_tuple_list(token_in_not_UNK, predicate_token_label)

            if self.Competition_Mode:
                yield text_sentence, predicate_relationship_sort_list, entity_sort_tuple_list, None
            else:
                refer_spo_list = self._preprocessing_reference_spo_list(refer_spo_str)
                yield text_sentence, predicate_relationship_sort_list, entity_sort_tuple_list, refer_spo_list

    # 打印排好序的关系列表和实体列表
    def show_produce_relationship_and_entity_sort_list(self):
        idx = 0
        for text_sentence, predicate_relationship_sort_list, entity_sort_tuple_list, refer_spo_list in self.produce_relationship_and_entity_sort_list():
            print("序号：           ", idx + 1)
            print("原句：           ", text_sentence)
            print("预测的关系：     ", predicate_relationship_sort_list)
            print("预测的实体：     ", entity_sort_tuple_list)
            print("参考的 spo_slit：", refer_spo_list)
            print("\n")
            idx += 1
            if idx == 10:
                break

if __name__=='__main__':
    sorted_relation_and_entity_list_manager = Sorted_relation_and_entity_list_Management(TEST_DATA_DIR="../data/SKE_2019/valid", MODEL_OUTPUT_DIR="../output/20190326code_test", Competition_Mode=False)
    sorted_relation_and_entity_list_manager.show_produce_relationship_and_entity_sort_list()
    #sorted_relation_and_entity_list_manager.check_token_label_out()
    #sorted_relation_and_entity_list_manager.analysis_position_quantity_relations_of_spo_list_in_text_sentence()
