import os


class SPO_out_file_manager(object):
    def __init__(self, file_path_list, file_name_list):
        self.file_path_list = file_path_list
        self.file_name_list = file_name_list

    #读取 spo_out.txt 文件
    def read_file_return_content_list(self):
        content_list_summary = []
        for file_path in self.file_path_list:
            with open(file_path, "r", encoding='utf-8') as f:
                content_list = f.readlines()
                content_list = [content.replace("\n", "") for content in content_list]
                content_list_summary.append(content_list)
        content_list_length_summary = [(file_name, len(content_list)) for content_list, file_name in zip(content_list_summary, self.file_name_list)]
        return content_list_summary, content_list_length_summary

    #获取 spo_out.txt 文件长度和文件内容列表
    def show_reference_spo_list(self, refer_spo_str):
        refer_spo_list = refer_spo_str.split("[SPO_SEP]")
        refer_spo_list = [spo.split(" ") for spo in refer_spo_list]
        refer_spo_list = [dict([('predicate', spo[0]),
                                ('object_type', spo[2]), ('subject_type', spo[1]),
                                ('object', spo[4]), ('subject', spo[3])]) for spo in refer_spo_list]
        return len(refer_spo_list), refer_spo_list

    #获取比较固定的常识信息，比如企业的创始人，行政区的面积
    def get_predicate_common_sense_priori_info(self, predicate_name):
        subject_2_object_set_dict = dict()
        object_2_subject_set_dict = dict()
        content_list_summary, content_list_length_summary = self.read_file_return_content_list()
        for reference_spo_list in content_list_summary:
            for spo_str in reference_spo_list:
                spo_list_length, spo_list = self.show_reference_spo_list(spo_str)
                for spo_item in spo_list:
                    if spo_item["predicate"] == predicate_name:
                        subject_2_object_set_dict.setdefault(spo_item["subject"], set()).add(spo_item["object"])
                        object_2_subject_set_dict.setdefault(spo_item["object"], set()).add(spo_item["subject"])
        print(len(subject_2_object_set_dict))
        print(subject_2_object_set_dict)
        print(len(object_2_subject_set_dict))
        print(object_2_subject_set_dict)
        return subject_2_object_set_dict, object_2_subject_set_dict


    #统计各个 spo 长度的数量和占比
    def count_spo_length(self, reference_spo_list):
        file_line_number = len(reference_spo_list)
        spo_list_predicate_count_dict = dict()
        for spo_str in reference_spo_list:
            spo_list_length, spo_list = self.show_reference_spo_list(spo_str)
            spo_list_predicate_count_dict.setdefault(spo_list_length, 0)
            spo_list_predicate_count_dict[spo_list_length] += 1
        spo_list_predicate_count_list = []
        for k, v in spo_list_predicate_count_dict.items():
            spo_list_predicate_count_list.append((k, round(v/file_line_number, 3)))
        spo_list_predicate_count_list.sort()

        return spo_list_predicate_count_dict, spo_list_predicate_count_list


    #按照 关系划分，并且统计各个 spo 长度的数量和占比
    def count_spo_list_length_according_predicate(self, reference_spo_list):
        predicate_name_list = {'所属专辑', '朝代', '连载网站', '丈夫', '创始人', '所在城市', '简称', '主演', '专业代码', '总部地点', '毕业院校', '字', '号', '占地面积', '国籍', '出生地', '父亲', '祖籍', '出品公司', '上映时间', '编剧', '妻子', '出版社', '官方语言', '目', '制片人', '成立日期', '歌手', '出生日期', '海拔', '人口数量', '身高', '作词', '主角', '嘉宾', '作者', '修业年限', '母亲', '邮政编码', '注册资本', '民族', '主持人', '董事长', '气候', '改编自', '作曲', '面积', '首都', '导演'}

        spo_list_length_according_predicate = dict()
        for name in predicate_name_list:
            spo_list_length_according_predicate[name] = 0

        for spo_str in reference_spo_list:
            spo_list_length, spo_list = self.show_reference_spo_list(spo_str)
            #print(spo_list_length, spo_list )
            for spo in spo_list:
                spo_list_length_according_predicate[spo["predicate"]] += 1

        spo_list_length_according_predicate_list = sorted(
            spo_list_length_according_predicate.items(), key=lambda x:x[1], reverse=True)

        predicate_count = 0
        for predicate, value in spo_list_length_according_predicate_list:
            predicate_count += value
        spo_list_length_according_predicate_list = [(predicate, round(value/ predicate_count, 3)) for predicate, value in spo_list_length_according_predicate_list]
        return spo_list_length_according_predicate, spo_list_length_according_predicate_list


    def write_info_to_file(self):
        Big_reference_spo_list, content_list_length_summary = self.read_file_return_content_list()
        for idx, reference_spo_list in enumerate(Big_reference_spo_list):
            file_line_number = len(reference_spo_list)
            spo_list_predicate_count_dict, spo_list_predicate_count_list = self.count_spo_length(reference_spo_list)
            spo_list_length_according_predicate, spo_list_length_according_predicate_list = self.count_spo_list_length_according_predicate(reference_spo_list)

            with open("spo_out_info_{}.txt".format(idx), 'w', encoding='utf-8') as f:
                f.write("file_line_number:\t" + str(file_line_number) + '\n')
                f.write("spo_list_predicate_count_dict:\t" + str(spo_list_predicate_count_dict) + '\n')
                f.write("spo_list_predicate_count_list:\t" + str(spo_list_predicate_count_list) + '\n')
                f.write("spo_list_length_according_predicate:\t" + str(spo_list_length_according_predicate) + '\n')
                f.write("spo_list_length_according_predicate_list:\t" + str(spo_list_length_according_predicate_list) + '\n')

                print("file_line_number:\t" + str(file_line_number) + '\n')
                print("spo_list_predicate_count_dict:\t" + str(spo_list_predicate_count_dict) + '\n')
                print("spo_list_predicate_count_list:\t" + str(spo_list_predicate_count_list) + '\n')
                print("spo_list_length_according_predicate:\t" + str(spo_list_length_according_predicate) + '\n')
                print("spo_list_length_according_predicate_list:\t" + str(spo_list_length_according_predicate_list) + '\n')


if __name__=='__main__':
    DATA_DIR = "SKE_2019/train"
    DATA_DIR_2 = "SKE_2019/valid"
    spo_out_file_path = os.path.join(DATA_DIR, "spo_out.txt")
    spo_out_file_path_2 = os.path.join(DATA_DIR_2, "spo_out.txt")
    file_path_list = [spo_out_file_path, spo_out_file_path_2]
    file_name_list = ["reference_spo_list_train", "reference_spo_list_test"]
    spo_out_manager = SPO_out_file_manager(file_path_list, file_name_list)
    subject_2_object_set_dict, object_2_subject_set_dict = spo_out_manager.get_predicate_common_sense_priori_info("成立日期")


