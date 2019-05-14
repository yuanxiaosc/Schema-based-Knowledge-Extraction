# Schema-based-Knowledge-Extraction
Code for http://lic2019.ccf.org.cn/kg 信息抽取。使用基于 BERT 的实体抽取和关系抽取的联合端到端模型。

More efficient task solutions：https://github.com/yuanxiaosc/Multiple-Relations-Extraction-Only-Look-Once

## 竞赛简介
信息抽取(Information Extraction, IE)是从自然语言文本中抽取实体、属性、关系及事件等事实类信息的文本处理技术，是信息检索、智能问答、智能对话等人工智能应用的重要基础，一直受到业界的广泛关注。信息抽取任务涉及命名实体识别、指代消解、关系分类等复杂技术，极具挑战性。本次竞赛发布基于schema约束的SPO信息抽取任务，即在给定schema集合下，从自然语言文本中抽取出符合schema要求的SPO三元组知识。本次竞赛将提供业界规模最大的基于schema的中文信息抽取数据集(Schema based Knowledge Extraction, SKE)，旨在为研究者提供学术交流平台，进一步提升中文信息抽取技术的研究水平，推动相关人工智能应用的发展。

## 竞赛详情
###1. 竞赛任务
给定schema约束集合及句子sent，其中schema定义了关系P以及其对应的主体S和客体O的类别，例如（S_TYPE:人物，P:妻子，O_TYPE:人物）、（S_TYPE:公司，P:创始人，O_TYPE:人物）等。 任务要求参评系统自动地对句子进行分析，输出句子中所有满足schema约束的SPO三元组知识Triples=[(S1, P1, O1), (S2, P2, O2)…]。
输入/输出:
(1) 输入:schema约束集合及句子sent
(2) 输出:句子sent中包含的符合给定schema约束的三元组知识Triples
### 2. 数据简介
本次竞赛使用的SKE数据集是业界规模最大的基于schema的中文信息抽取数据集，其包含超过43万三元组数据、21万中文句子及50个已定义好的schema，表1中展示了SKE数据集中包含的50个schema及对应的例子。数据集中的句子来自百度百科和百度信息流文本。数据集划分为17万训练集，2万验证集和2万测试集。其中训练集和验证集用于训练，可供自由下载，测试集分为两个，测试集1供参赛者在平台上自主验证，测试集2在比赛结束前一周发布，不能在平台上自主验证，并将作为最终的评测排名。
