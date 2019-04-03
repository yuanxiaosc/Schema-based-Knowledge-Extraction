from bin.spo_striples_generation_data_manage import Sorted_relation_and_entity_list_Management
from bin.spo_striples_generation_rule import Relationship_Priority_Rule, Sequence_Label_Priority_Combining_Statistical_Law_Rule
from bin.spo_striples_generation_check import SPO_list_check
import json

def produce_competition_result(sorted_relation_and_entity_list_manager, sequence_first_rule, keep_empty_spo_list=False):
    if keep_empty_spo_list:
        out_put_spo_list_file = open("result_not_keep_empty_spo_list.json", "w", encoding='utf-8')
    else:
        out_put_spo_list_file = open("result_keep_empty_spo_list.json", "w", encoding='utf-8')
    for text_sentence, sort_relation_list, sort_entity_list, refer_spo_list in sorted_relation_and_entity_list_manager.produce_relationship_and_entity_sort_list():
        spo_list = sequence_first_rule.rule_generate_spo_list(text_sentence, sort_relation_list, sort_entity_list, refer_spo_list)
        if len(spo_list) > 0 or keep_empty_spo_list:
            line_dict = dict()
            line_dict["text"] = text_sentence
            line_dict["spo_list"] = spo_list
            line_json = json.dumps(line_dict, ensure_ascii=False)
            out_put_spo_list_file.write(line_json + "\n")
    out_put_spo_list_file.close()

def write_competition_spo_list_empty_result(sorted_relation_and_entity_list_manager, sequence_first_rule):
    all_line_num = 0
    spo_list_empty_num = 0
    competition_spo_list_empty_file = open("competition_spo_list_empty.txt", "w", encoding='utf-8')
    for text_sentence, sort_relation_list, sort_entity_list, refer_spo_list in sorted_relation_and_entity_list_manager.produce_relationship_and_entity_sort_list():
        spo_list = sequence_first_rule.rule_generate_spo_list(text_sentence, sort_relation_list, sort_entity_list, refer_spo_list)
        all_line_num += 1
        if len(spo_list) == 0:
            spo_list_empty_num += 1
            #print(spo_list)
            #print(text_sentence)
            #print(sort_relation_list)
            #print(sort_entity_list)
            #print("\n")
            competition_spo_list_empty_file.write(str(spo_list) + "\n")
            competition_spo_list_empty_file.write(text_sentence + "\n")
            competition_spo_list_empty_file.write(str(sort_entity_list) + "\n")
            competition_spo_list_empty_file.write(str(sort_relation_list) + "\n")
            competition_spo_list_empty_file.write("\n")
    print(spo_list_empty_num, all_line_num, spo_list_empty_num / all_line_num)
    competition_spo_list_empty_file.close()

#708 9949 0.07116293094783395

if __name__ == "__main__":
    Competition_Mode = True
    sorted_relation_and_entity_list_manager = Sorted_relation_and_entity_list_Management(
        TEST_DATA_DIR="data/SKE_2019_corrected3/test", MODEL_OUTPUT_DIR="output/competition", Competition_Mode=Competition_Mode)
    sequence_first_rule = Sequence_Label_Priority_Combining_Statistical_Law_Rule()
    if not Competition_Mode:
        spo_list_check = SPO_list_check(sorted_relation_and_entity_list_manager, sequence_first_rule, show_detail=False)
        spo_list_check.spo_list_length_check()
    else:
        produce_competition_result(sorted_relation_and_entity_list_manager, sequence_first_rule, keep_empty_spo_list=True)







