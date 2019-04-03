import json

keep_empty_spo_list=True

def convert_subject_object_2_object_subject(file_name="result.json", keep_empty_spo_list=True):
    with open(file_name, 'r', encoding='utf-8') as result_json_read_f:
        with open(file_name.replace(".json", "_convert") + ".json", 'w', encoding='utf-8') as result_json_write_f:
            count_numbers = 0
            while True:
                line = result_json_read_f.readline()
                if line:
                    count_numbers += 1
                    spo_list_convert = list()
                    r = json.loads(line)
                    text = r["text"]
                    spo_list = r["spo_list"]
                    for spo in spo_list:
                        spo_object_type = spo["object_type"]
                        spo_predicate = spo["predicate"]
                        spo_object = spo["object"]
                        spo_subject_type = spo["subject_type"]
                        spo_subject = spo["subject"]
                        spo_list_convert.append({"object_type": spo_subject_type, "predicate": spo_predicate,
                                                 "object": spo_subject, "subject_type": spo_object_type,
                                                 "subject": spo_object})

                    if len(spo_list_convert) > 0 or keep_empty_spo_list:
                        line_dict = dict()
                        line_dict["text"] = text
                        line_dict["spo_list"] = spo_list_convert
                        line_json = json.dumps(line_dict, ensure_ascii=False)
                        result_json_write_f.write(line_json + "\n")
                else:
                    break
        print("all numbers", count_numbers)
        print("\n")

if __name__=="__main__":
    keep_empty_spo_list = False
    convert_subject_object_2_object_subject(file_name="result_not_keep_empty_spo_list.json", keep_empty_spo_list=keep_empty_spo_list)