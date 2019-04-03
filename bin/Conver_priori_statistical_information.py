from priori_statistical_information import Priori_statistical_information
import os


# 把 priori_statistical_information.py 转换成 priori_statistical_information_from_file.py 文件
class Conver_priori_statistical_information_2_file():
    def __init__(self):
        self.file_name = "priori_info_storage"

    #显示 priori_statistical_information.py 文件中类 Priori_statistical_information 中需要存储的信息
    #把该信息复制粘贴到 priori_statistical_information_from_file.py 文件中
    def show_special_entity_map_info(self, a_object):
        need_file_name_list = []
        a_object_dir = dir(a_object)
        for dir_name in a_object_dir:
            if "special_entity_map" in dir_name:
                print('self.{} = read_special_entity_map_info_from_file("{}")'.format(dir_name, dir_name))
                need_file_name_list.append(dir_name)
        return need_file_name_list

    #把priori_statistical_information.py 文件中类 Priori_statistical_information 中需要存储的信息写入文件
    def write_special_entity_map_info(self, a_object):
        if not os.path.exists(self.file_name):
            os.makedirs(self.file_name)
        a_object_dir = dir(a_object)
        for dir_name in a_object_dir:
            if "special_entity_map" in dir_name:
                a_object_element = getattr(a_object, dir_name)
                print(dir_name)
                print(a_object_element)
                with open(os.path.join(self.file_name, dir_name), "w", encoding="utf-8") as f:
                    f.write(str(a_object_element))

    #在priori_statistical_information_from_file.py 文件中读取存储的信息
    def read_special_entity_map_info_from_file(self, file_name, file_dir = "priori_info_storage"):
            with open(os.path.join(file_dir, file_name), "r", encoding="utf-8") as f:
                file_content = f.read()
                return eval(file_content)

if __name__=="__main__":
    priori_info =  Priori_statistical_information()
    conver = Conver_priori_statistical_information_2_file()
    conver.show_special_entity_map_info(priori_info)
    conver.write_special_entity_map_info(priori_info)
