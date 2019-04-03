

class SPO_list_check(object):

    def __init__(self, sorted_relation_and_entity_list_manager=None, generation_rule=None, show_detail=False):
        self.sorted_relation_and_entity_list_manager = sorted_relation_and_entity_list_manager
        self.generation_rule = generation_rule
        self.show_detail = show_detail

    # 对比按照规则生成 spo_list 长度与参照的长度
    def spo_list_length_check(self,):
        read_line_number = 0
        length_Longer, length_Shorter, length_Equal = 0, 0, 0
        for text_sentence, sort_relation_list, sort_entity_list, refer_spo_list in self.sorted_relation_and_entity_list_manager.produce_relationship_and_entity_sort_list():
            read_line_number += 1
            spo_list = self.generation_rule.rule_generate_spo_list(text_sentence, sort_relation_list, sort_entity_list, refer_spo_list)
            refer_spo_list_len = len(refer_spo_list)
            spo_list_len = len(spo_list)
            if self.show_detail:
                print("输入的原句：", text_sentence)
                print("输入的关系：", sort_relation_list)
                print("输入的实体：", sort_entity_list)
                print("参照的SPO列表：", refer_spo_list_len, refer_spo_list)
                print("预测的SPO列表：", spo_list_len, spo_list)
                print("\n")
            if spo_list_len == refer_spo_list_len:
                length_Equal += 1
            elif spo_list_len < refer_spo_list_len:
                length_Shorter += 1
            else:
                length_Longer += 1
        print("length_equal:\t", round(length_Equal / read_line_number, 3))
        print("length_shorter:\t", round(length_Shorter / read_line_number, 3))
        print("length_longer:\t", round(length_Longer / read_line_number, 3))