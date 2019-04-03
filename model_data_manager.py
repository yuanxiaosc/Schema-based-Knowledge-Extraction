import os
import json
from bert import tokenization

print("if not have raw data, please dowload data from http://lic2019.ccf.org.cn/kg !")

def unzip_and_move_files():
    "解压原始文件并且放入 raw_data 文件夹下面"
    os.system("unzip dev_data.json.zip")
    os.system("mv dev_data.json ../dev_data.json")
    os.system("unzip train_data.json.zip")
    os.system("mv train_data.json ../train_data.json")

class Model_data_preparation(object):

    def __init__(self, DATA_DIR="raw_data", DATA_OUTPUT_DIR="SKE_2019_tokened_labeling", spo_list_separator='[SPO_SEP]',
                 vocab_file_path="pretrained_model/chinese_L-12_H-768_A-12/vocab.txt", do_lower_case=True, Competition_Mode=False):
        #BERT 自带WordPiece分词工具，对于中文都是分成单字
        self.bert_tokenizer = tokenization.FullTokenizer(vocab_file=vocab_file_path, do_lower_case=do_lower_case)  # 初始化 bert_token 工具
        self.DATA_DIR = DATA_DIR
        self.DATA_OUTPUT_DIR = DATA_OUTPUT_DIR
        self.spo_list_separator = spo_list_separator
        self.Competition_Mode = Competition_Mode

    def generate_SKE_2019_Entity_name_slipe_by_type(self):
        pass

    # 生成训练数据和验证数据中所有实体名称的文件
    def generate_SKE_2019_Entity_name_dict(self):
        entity_name_set = set()
        #检查括号不对称的 spo 三元组
        def _bracket_check(name, spo_slit):
            if ( "（" in name and "）" not in name ) or ( "）" in name and "（" not in name ) \
                    or ( "(" in name and ")" not in name ) or ( ")" in name and "(" not in name):
                print("This spo bracket error!\t", name)

        def _get_entity_name_from_spo_slit(spo_list):
            entity_name_list = []
            for spo in spo_list:
                _bracket_check(spo['object'], spo_list)
                _bracket_check(spo['subject'], spo_list)
                entity_name_list.extend([spo['object'], spo['subject']])
            return entity_name_list

        for file_set_type in ["train", "valid"]:
            if file_set_type == "train":
                path_to_raw_data_file = "train_data.json"
            elif file_set_type == "valid":
                path_to_raw_data_file = "dev_data.json"
            else:
                pass

            with open(os.path.join(self.DATA_DIR, path_to_raw_data_file), 'r', encoding='utf-8') as f:
                while True:
                    line = f.readline()
                    if line:
                        r = json.loads(line)
                        spo_list = r["spo_list"]
                        # text = r["text"]
                        entity_name_list = _get_entity_name_from_spo_slit(spo_list)
                        for name in entity_name_list:
                            entity_name_set.add(name)
                    else:
                        break
        entity_names_list = sorted(list(entity_name_set))
        with open(os.path.join(self.DATA_DIR, "SKE_2019_Entity_name_dict.txt"), "w", encoding='utf-8') as f:
            for name in entity_names_list:
                f.write(name + "\n")
            print("SKE_2019_Entity_name_dict.txt is saved to {}".format(os.path.join(self.DATA_DIR, "SKE_2019_Entity_name_dict.txt")))

    #序列标注对齐：由原始数据文件生成标注好的序列文件
    def subject_object_labeling(self, spo_list, text, bert_tokener_error_log_f):
        # 在列表 k 中确定列表 q 的位置
        def _index_q_list_in_k_list(q_list, k_list):
            """Known q_list in k_list, find index(first time) of q_list in k_list"""
            q_list_length = len(q_list)
            k_list_length = len(k_list)
            for idx in range(k_list_length - q_list_length + 1):
                t = [q == k for q, k in zip(q_list, k_list[idx: idx + q_list_length])]
                # print(idx, t)
                if all(t):
                    # print(idx)
                    idx_start = idx
                    return idx_start

        # 给主体和客体表上BIO分割式类型标签
        def _labeling_type(subject_object, so_type):
            tokener_error_flag = False
            so_tokened = self.bert_tokenizer.tokenize(subject_object)
            so_tokened_length = len(so_tokened)
            idx_start = _index_q_list_in_k_list(q_list=so_tokened, k_list=text_tokened)
            if idx_start is None:
                tokener_error_flag = True
                '''
                实体: "1981年"  原句: "●1981年2月27日，中国人口学会成立"
                so_tokened ['1981', '年']  text_tokened ['●', '##19', '##81', '年', '2', '月', '27', '日', '，', '中', '国', '人', '口', '学', '会', '成', '立']
                so_tokened 无法在 text_tokened 找到！原因是bert_tokenizer.tokenize 分词增添 “##” 所致！
                '''
                bert_tokener_error_log_f.write(subject_object + " @@ " + text + "\n")
                bert_tokener_error_log_f.write(str(so_tokened) + " @@ " + str(text_tokened) + "\n")
            else: #给实体开始处标 B 其它位置标 I
                labeling_list[idx_start] = "B-" + so_type
                if so_tokened_length == 2:
                    labeling_list[idx_start + 1] = "I-" + so_type
                elif so_tokened_length >= 3:
                    labeling_list[idx_start + 1: idx_start + so_tokened_length] = ["I-" + so_type] * (so_tokened_length - 1)
            return tokener_error_flag

        text_tokened = self.bert_tokenizer.tokenize(text)
        text_tokened_not_UNK = self.bert_tokenizer.tokenize_not_UNK(text)
        labeling_list = ["O"] * len(text_tokened)

        tokener_error_flag = False
        for spo_item in spo_list:
            subject = spo_item["subject"]
            subject_type = spo_item["subject_type"]
            object = spo_item["object"]
            object_type = spo_item["object_type"]
            flag_A = _labeling_type(subject, subject_type)
            flag_B = _labeling_type(object, object_type)
            if flag_A or flag_B:
                tokener_error_flag = True
                return text_tokened, text_tokened_not_UNK, labeling_list, tokener_error_flag

        #给被bert_tokenizer.tokenize 拆分的词语打上特殊标签[##WordPiece]
        for idx, token in enumerate(text_tokened):
            """标注被 bert_tokenizer.tokenize 拆分的词语"""
            if token.startswith("##"):
                labeling_list[idx] = "[##WordPiece]"

        return text_tokened, text_tokened_not_UNK, labeling_list, tokener_error_flag

    #处理原始数据
    def separate_raw_data_and_token_labeling(self):
        if not os.path.exists(self.DATA_OUTPUT_DIR):
            os.makedirs(os.path.join(self.DATA_OUTPUT_DIR, "train"))
            os.makedirs(os.path.join(self.DATA_OUTPUT_DIR, "valid"))
            os.makedirs(os.path.join(self.DATA_OUTPUT_DIR, "test"))

        for file_set_type in ["train", "valid", "test"]:
            print(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type)))
            if file_set_type in ["train", "valid"]:
                token_label_out_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "token_label_out.txt"), "w", encoding='utf-8')
                predicate_out_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "predicate_out.txt"), "w", encoding='utf-8')
                spo_out_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "spo_out.txt"), "w", encoding='utf-8')
                bert_tokener_error_log_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "bert_tokener_error_log.txt"), "w", encoding='utf-8')

            text_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "text.txt"), "w", encoding='utf-8')
            token_in_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "token_in.txt"), "w", encoding='utf-8')
            token_in_not_UNK_f = open(os.path.join(os.path.join(self.DATA_OUTPUT_DIR, file_set_type), "token_in_not_UNK.txt"), "w", encoding='utf-8')

            #把原始 spo_list 形式转变成由 spo_list_separator 分隔符分割的一行字符串
            def spo_to_spo_file(spo_list):
                spo_list_new = [" ".join([spo['predicate'], spo['object_type'], spo['subject_type'], spo['object'], spo['subject']])
                            for spo in spo_list]
                predicate_list = [spo['predicate'] for spo in spo_list]
                spo_list_str = self.spo_list_separator.join(spo_list_new)
                predicate_list_str = " ".join(predicate_list)
                spo_out_f.write(spo_list_str + "\n")
                predicate_out_f.write(predicate_list_str + "\n")

            if file_set_type == "train":
                path_to_raw_data_file = "train_data.json"
            elif file_set_type == "valid":
                path_to_raw_data_file = "dev_data.json"
            else:
                if self.Competition_Mode == True:
                    path_to_raw_data_file = "test1_data_postag.json"
                else:
                    path_to_raw_data_file = "dev_data.json"

            with open(os.path.join(self.DATA_DIR, path_to_raw_data_file), 'r', encoding='utf-8') as f:
                count_numbers = 0
                while True:
                    line = f.readline()
                    if line:
                        r = json.loads(line)
                        if file_set_type in ["train", "valid"]:
                            spo_list = r["spo_list"]
                        else:
                            spo_list = []
                        text = r["text"]
                        text_tokened, text_tokened_not_UNK, labeling_list, tokener_error_flag = self.subject_object_labeling(spo_list=spo_list, text=text, bert_tokener_error_log_f=bert_tokener_error_log_f)
                        count_numbers += 1
                        if file_set_type in ["train", "valid"]:
                            token_label_out_f.write(" ".join(labeling_list) + "\n")
                            spo_to_spo_file(spo_list)
                        text_f.write(text + "\n")
                        token_in_f.write(" ".join(text_tokened) + "\n")
                        token_in_not_UNK_f.write(" ".join(text_tokened_not_UNK) + "\n")
                    else:
                        break
            print(file_set_type)
            print("all numbers", count_numbers)
            print("\n")
            text_f.close()
            token_in_f.close()
            token_in_not_UNK_f.close()
            if file_set_type in ["train", "valid"]:
                token_label_out_f.close()
                spo_out_f.close()
                predicate_out_f.close()
                bert_tokener_error_log_f.close()

if __name__=="__main__":
    DATA_DIR = "data/raw_data_corrected"
    DATA_OUTPUT_DIR = "data/SKE_2019_corrected3"
    spo_list_separator = '[SPO_SEP]'
    Competition_Mode = True
    model_data = Model_data_preparation(DATA_DIR=DATA_DIR, DATA_OUTPUT_DIR=DATA_OUTPUT_DIR, spo_list_separator=spo_list_separator, Competition_Mode=Competition_Mode)
    #model_data.generate_SKE_2019_Entity_name_dict()
    model_data.separate_raw_data_and_token_labeling()

