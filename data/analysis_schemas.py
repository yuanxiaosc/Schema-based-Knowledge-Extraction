import json
import os



def show_schemas_info(path_to_schemas):
    schemas_dict = dict()
    object_type_set = set()
    predicate_set = set()
    subject_type_set = set()
    with open(path_to_schemas, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if line:
                r = json.loads(line)
                object_type = r["object_type"]
                predicate = r["predicate"]
                subject_type = r["subject_type"]
                object_type_set.add(object_type)
                schemas_dict.setdefault(tuple((object_type, subject_type)), []).append(predicate)
                if predicate in predicate_set:
                    print(predicate)
                predicate_set.add(predicate)
                subject_type_set.add(subject_type)
            else:
                break
    object_type_and_subject_type_set = object_type_set | subject_type_set
    object_type_inter_subject_type_set = object_type_set & subject_type_set
    print("schemas_dict:\t", len(schemas_dict), schemas_dict)
    print("object_type_set:\t", len(object_type_set), object_type_set)
    print("predicate_set:\t", len(predicate_set), predicate_set)
    print("subject_type_se:\t", len(subject_type_set), subject_type_set)
    print("object_type_and_subject_type_set:\t", len(object_type_and_subject_type_set), object_type_and_subject_type_set)
    print("object_type_inter_subject_type_set:\t", len(object_type_inter_subject_type_set), object_type_inter_subject_type_set)

    object_type_sort_list = list(object_type_set)
    object_type_sort_list.sort()
    predicate_sort_list = list(predicate_set)
    predicate_sort_list.sort()
    subject_type_sort_list = list(subject_type_set)
    subject_type_sort_list.sort()
    subject_type_and_object_type_sort_list = list(object_type_and_subject_type_set)
    subject_type_and_object_type_sort_list.sort()
    with open("schemas_info.txt", 'w', encoding='utf-8') as f:
        f.write("schemas_dict:\t" + str(schemas_dict) + "\n")
        f.write("object_type_sort_list:\t" + str(object_type_sort_list) + "\n")
        f.write("predicate_sort_list:\t" + str(predicate_sort_list) + "\n")
        f.write("subject_type_sort_list:\t" + str(subject_type_sort_list) + "\n")
        f.write("subject_type_and_object_type_sort_list:\t" + str(subject_type_and_object_type_sort_list) + "\n")



path_to_schemas = '../data/raw_data/all_50_schemas'

show_schemas_info(path_to_schemas)



data_dir = "../data/SKE_2019/train"

def show_repetitive_relationship(data_dir):
    with open(os.path.join(data_dir, "predicate_out.txt"), encoding='utf-8') as label_f:
        predicate_label_list = [seq.replace("\n", '') for seq in label_f.readlines()]

        print(len(predicate_label_list))

        num = 0
        for raw in predicate_label_list:
            raw_list = raw.split(" ")
            if len(set(raw_list)) < len(raw_list):
                num += 1
        print(num)
        print(num / len(predicate_label_list))

#show_repetitive_relationship(data_dir)


def schemas_info_to_dict(path_to_schemas):
    schemas_dict = dict()
    with open(path_to_schemas, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if line:
                r = json.loads(line)
                object_type = r["object_type"]
                predicate = r["predicate"]
                subject_type = r["subject_type"]
                schemas_dict.setdefault(tuple((object_type, subject_type)), []).append(predicate)
            else:
                break
    return schemas_dict

schemas_dict = schemas_info_to_dict(path_to_schemas)
print(schemas_dict)
print(len(schemas_dict))
