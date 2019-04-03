from sklearn import metrics
import os
import sys
import time
import numpy as np
import tensorflow as tf
from tensorflow.python.ops.metrics_impl import _streaming_confusion_matrix

"""
Multiclass tf_metrics
from: 
https://github.com/guillaumegenthial/tf_metrics/blob/master/tf_metrics/__init__.py
__author__ = "Guillaume Genthial"
"""


def precision(labels, predictions, num_classes, pos_indices=None,
              weights=None, average='micro'):
    """Multi-class precision metric for Tensorflow
    Parameters
    ----------
    labels : Tensor of tf.int32 or tf.int64
        The true labels
    predictions : Tensor of tf.int32 or tf.int64
        The predictions, same shape as labels
    num_classes : int
        The number of classes
    pos_indices : list of int, optional
        The indices of the positive classes, default is all
    weights : Tensor of tf.int32, optional
        Mask, must be of compatible shape with labels
    average : str, optional
        'micro': counts the total number of true positives, false
            positives, and false negatives for the classes in
            `pos_indices` and infer the metric from it.
        'macro': will compute the metric separately for each class in
            `pos_indices` and average. Will not account for class
            imbalance.
        'weighted': will compute the metric separately for each class in
            `pos_indices` and perform a weighted average by the total
            number of true labels for each class.
    Returns
    -------
    tuple of (scalar float Tensor, update_op)
    """
    cm, op = _streaming_confusion_matrix(
        labels, predictions, num_classes, weights)
    pr, _, _ = metrics_from_confusion_matrix(
        cm, pos_indices, average=average)
    op, _, _ = metrics_from_confusion_matrix(
        op, pos_indices, average=average)
    return (pr, op)


def recall(labels, predictions, num_classes, pos_indices=None, weights=None,
           average='micro'):
    """Multi-class recall metric for Tensorflow
    Parameters
    ----------
    labels : Tensor of tf.int32 or tf.int64
        The true labels
    predictions : Tensor of tf.int32 or tf.int64
        The predictions, same shape as labels
    num_classes : int
        The number of classes
    pos_indices : list of int, optional
        The indices of the positive classes, default is all
    weights : Tensor of tf.int32, optional
        Mask, must be of compatible shape with labels
    average : str, optional
        'micro': counts the total number of true positives, false
            positives, and false negatives for the classes in
            `pos_indices` and infer the metric from it.
        'macro': will compute the metric separately for each class in
            `pos_indices` and average. Will not account for class
            imbalance.
        'weighted': will compute the metric separately for each class in
            `pos_indices` and perform a weighted average by the total
            number of true labels for each class.
    Returns
    -------
    tuple of (scalar float Tensor, update_op)
    """
    cm, op = _streaming_confusion_matrix(
        labels, predictions, num_classes, weights)
    _, re, _ = metrics_from_confusion_matrix(
        cm, pos_indices, average=average)
    _, op, _ = metrics_from_confusion_matrix(
        op, pos_indices, average=average)
    return (re, op)


def f1(labels, predictions, num_classes, pos_indices=None, weights=None,
       average='micro'):
    return fbeta(labels, predictions, num_classes, pos_indices, weights,
                 average)


def fbeta(labels, predictions, num_classes, pos_indices=None, weights=None,
          average='micro', beta=1):
    """Multi-class fbeta metric for Tensorflow
    Parameters
    ----------
    labels : Tensor of tf.int32 or tf.int64
        The true labels
    predictions : Tensor of tf.int32 or tf.int64
        The predictions, same shape as labels
    num_classes : int
        The number of classes
    pos_indices : list of int, optional
        The indices of the positive classes, default is all
    weights : Tensor of tf.int32, optional
        Mask, must be of compatible shape with labels
    average : str, optional
        'micro': counts the total number of true positives, false
            positives, and false negatives for the classes in
            `pos_indices` and infer the metric from it.
        'macro': will compute the metric separately for each class in
            `pos_indices` and average. Will not account for class
            imbalance.
        'weighted': will compute the metric separately for each class in
            `pos_indices` and perform a weighted average by the total
            number of true labels for each class.
    beta : int, optional
        Weight of precision in harmonic mean
    Returns
    -------
    tuple of (scalar float Tensor, update_op)
    """
    cm, op = _streaming_confusion_matrix(
        labels, predictions, num_classes, weights)
    _, _, fbeta = metrics_from_confusion_matrix(
        cm, pos_indices, average=average, beta=beta)
    _, _, op = metrics_from_confusion_matrix(
        op, pos_indices, average=average, beta=beta)
    return (fbeta, op)


def safe_div(numerator, denominator):
    """Safe division, return 0 if denominator is 0"""
    numerator, denominator = tf.to_float(numerator), tf.to_float(denominator)
    zeros = tf.zeros_like(numerator, dtype=numerator.dtype)
    denominator_is_zero = tf.equal(denominator, zeros)
    return tf.where(denominator_is_zero, zeros, numerator / denominator)


def pr_re_fbeta(cm, pos_indices, beta=1):
    """Uses a confusion matrix to compute precision, recall and fbeta"""
    num_classes = cm.shape[0]
    neg_indices = [i for i in range(num_classes) if i not in pos_indices]
    cm_mask = np.ones([num_classes, num_classes])
    cm_mask[neg_indices, neg_indices] = 0
    diag_sum = tf.reduce_sum(tf.diag_part(cm * cm_mask))

    cm_mask = np.ones([num_classes, num_classes])
    cm_mask[:, neg_indices] = 0
    tot_pred = tf.reduce_sum(cm * cm_mask)

    cm_mask = np.ones([num_classes, num_classes])
    cm_mask[neg_indices, :] = 0
    tot_gold = tf.reduce_sum(cm * cm_mask)

    pr = safe_div(diag_sum, tot_pred)
    re = safe_div(diag_sum, tot_gold)
    fbeta = safe_div((1. + beta ** 2) * pr * re, beta ** 2 * pr + re)

    return pr, re, fbeta


def metrics_from_confusion_matrix(cm, pos_indices=None, average='micro',
                                  beta=1):
    """Precision, Recall and F1 from the confusion matrix
    Parameters
    ----------
    cm : tf.Tensor of type tf.int32, of shape (num_classes, num_classes)
        The streaming confusion matrix.
    pos_indices : list of int, optional
        The indices of the positive classes
    beta : int, optional
        Weight of precision in harmonic mean
    average : str, optional
        'micro', 'macro' or 'weighted'
    """
    num_classes = cm.shape[0]
    if pos_indices is None:
        pos_indices = [i for i in range(num_classes)]

    if average == 'micro':
        return pr_re_fbeta(cm, pos_indices, beta)
    elif average in {'macro', 'weighted'}:
        precisions, recalls, fbetas, n_golds = [], [], [], []
        for idx in pos_indices:
            pr, re, fbeta = pr_re_fbeta(cm, [idx], beta)
            precisions.append(pr)
            recalls.append(re)
            fbetas.append(fbeta)
            cm_mask = np.zeros([num_classes, num_classes])
            cm_mask[idx, :] = 1
            n_golds.append(tf.to_float(tf.reduce_sum(cm * cm_mask)))

        if average == 'macro':
            pr = tf.reduce_mean(precisions)
            re = tf.reduce_mean(recalls)
            fbeta = tf.reduce_mean(fbetas)
            return pr, re, fbeta
        if average == 'weighted':
            n_gold = tf.reduce_sum(n_golds)
            pr_sum = sum(p * n for p, n in zip(precisions, n_golds))
            pr = safe_div(pr_sum, n_gold)
            re_sum = sum(r * n for r, n in zip(recalls, n_golds))
            re = safe_div(re_sum, n_gold)
            fbeta_sum = sum(f * n for f, n in zip(fbetas, n_golds))
            fbeta = safe_div(fbeta_sum, n_gold)
            return pr, re, fbeta

    else:
        raise NotImplementedError()


class Sequence_Labeling_and_Text_Classification_Calculate(object):

    def get_token_labeling_labels(self):
        """for Sequence_Labeling labels"""
        raise NotImplementedError()

    def get_intent_labels(self):
        """for Text_Classification labels"""
        raise NotImplementedError()

    def show_intent_prediction_report(self, store_report=True):
        raise NotImplementedError()

    def show_token_labeling_filling_report(self, store_report=True):
        raise NotImplementedError()

    @classmethod
    def show_metrics(cls, y_test_list, y_predict_list, label_list):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('准确率:', metrics.accuracy_score(y_test_list, y_predict_list))  # 预测准确率输出

        print('宏平均精确率:', metrics.precision_score(y_test_list, y_predict_list, average='macro'))  # 预测宏平均精确率输出
        print('微平均精确率:', metrics.precision_score(y_test_list, y_predict_list, average='micro'))  # 预测微平均精确率输出
        print('加权平均精确率:', metrics.precision_score(y_test_list, y_predict_list, average='weighted'))  # 预测加权平均精确率输出

        print('宏平均召回率:', metrics.recall_score(y_test_list, y_predict_list, average='macro'))  # 预测宏平均召回率输出
        print('微平均召回率:', metrics.recall_score(y_test_list, y_predict_list, average='micro'))  # 预测微平均召回率输出
        print('加权平均召回率:', metrics.recall_score(y_test_list, y_predict_list, average='micro'))  # 预测加权平均召回率输出

        print('宏平均F1-score:',
              metrics.f1_score(y_test_list, y_predict_list, labels=label_list, average='macro'))  # 预测宏平均f1-score输出
        print('微平均F1-score:',
              metrics.f1_score(y_test_list, y_predict_list, labels=label_list, average='micro'))  # 预测微平均f1-score输出
        print('加权平均F1-score:',
              metrics.f1_score(y_test_list, y_predict_list, labels=label_list, average='weighted'))  # 预测加权平均f1-score输出

        print('混淆矩阵输出:\n', metrics.confusion_matrix(y_test_list, y_predict_list))  # 混淆矩阵输出
        print('分类报告:\n', metrics.classification_report(y_test_list, y_predict_list))  # 分类报告输出
        print("\n")

    @classmethod
    def store_model_score(cls, y_test_list=None, y_predict_list=None, label_list=None,
                          log_out_file=None, is_show_numpy_big_array=False):
        log_out_file_path = os.path.join(log_out_file, "model_score_log.txt")
        with open(log_out_file_path, "a") as log_f:
            log_f.write("时间:\t" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "\n")
            log_f.write('准确率:\t' + str(metrics.accuracy_score(y_test_list, y_predict_list)) + "\n")  # 预测准确率输出

            log_f.write('宏平均精确率:\t' + str(
                metrics.precision_score(y_test_list, y_predict_list, average='macro')) + "\n")  # 预测宏平均精确率输出
            log_f.write('微平均精确率:\t' + str(
                metrics.precision_score(y_test_list, y_predict_list, average='micro')) + "\n")  # 预测微平均精确率输出
            log_f.write('加权平均精确率:\t' + str(
                metrics.precision_score(y_test_list, y_predict_list, average='weighted')) + "\n")  # 预测加权平均精确率输出

            log_f.write('宏平均召回率:\t' + str(
                metrics.recall_score(y_test_list, y_predict_list, average='macro')) + "\n")  # 预测宏平均召回率输出
            log_f.write('微平均召回率:\t' + str(
                metrics.recall_score(y_test_list, y_predict_list, average='micro')) + "\n")  # 预测微平均召回率输出
            log_f.write('加权平均召回率:\t' + str(
                metrics.recall_score(y_test_list, y_predict_list, average='micro')) + "\n")  # 预测加权平均召回率输出

            log_f.write('宏平均F1-score:\t' + str(metrics.f1_score(y_test_list, y_predict_list, labels=label_list,
                                                                average='macro')) + "\n")  # 预测宏平均f1-score输出
            log_f.write('微平均F1-score:\t' + str(metrics.f1_score(y_test_list, y_predict_list, labels=label_list,
                                                                average='micro')) + "\n")  # 预测微平均f1-score输出
            log_f.write('加权平均F1-score:\t' + str(metrics.f1_score(y_test_list, y_predict_list, labels=label_list,
                                                                 average='weighted')) + "\n")  # 预测加权平均f1-score输出
            log_f.write("\n")
            log_f.write('混淆矩阵输出:\n')

            def show_numpy_big_array(a_array):
                for a_row in a_array:
                    a_row_str = [str(a_data) for a_data in a_row]
                    a_line = " ".join(a_row_str)
                    log_f.write(str(a_line) + "\n")
                log_f.write("\n")

            if is_show_numpy_big_array:
                np.set_printoptions(threshold=np.nan)
                show_numpy_big_array(metrics.confusion_matrix(y_test_list, y_predict_list))
            else:
                log_f.writelines(str(metrics.confusion_matrix(y_test_list, y_predict_list)))
            log_f.write("\n")
            log_f.write('分类报告:\n')
            classification_report = metrics.classification_report(y_test_list, y_predict_list)
            log_f.writelines(classification_report)
            log_f.write("\n\n\n")

    @classmethod
    def delete_both_sides_is_O_word(cls, y_test_list, clean_y_predict_list):
        new_y_test_list, new_clean_y_predict_list = [], []
        for test, pred in zip(y_test_list, clean_y_predict_list):
            if test == "O" and pred == "O":
                continue
            new_y_test_list.append(test)
            new_clean_y_predict_list.append(pred)
        assert len(new_y_test_list) == len(new_clean_y_predict_list)
        return new_y_test_list, new_clean_y_predict_list


class SKE_2019_Sequnce_labeling_Caculate(Sequence_Labeling_and_Text_Classification_Calculate):

    def __init__(self, path_to_label_file=None, path_to_predict_label_file=None, log_out_file=None):
        if path_to_label_file is None and path_to_predict_label_file is None:
            raise Exception("At least have `path_to_label_file")
        self.path_to_label_file = path_to_label_file
        if path_to_predict_label_file is not None:
            self.path_to_predict_label_file = path_to_predict_label_file
        else:
            self.path_to_predict_label_file = path_to_label_file
        if log_out_file is None:
            self.log_out_file = os.getcwd()
        else:
            if not os.path.exists(log_out_file):
                os.makedirs(log_out_file)
            self.log_out_file = log_out_file

    def _get_token_labeling_list(self, path_to_token_labeling_file):
        with open(path_to_token_labeling_file, "r", encoding='utf-8') as token_labeling_f:
            token_labeling_list = [sententce.split() for sententce in token_labeling_f.readlines()]
        return token_labeling_list

    def _get_predict_token_labeling_list(self, path_to_token_labeling_test_results_file):
        with open(path_to_token_labeling_test_results_file, "r", encoding='utf-8') as token_labeling_predict_f:
            predict_token_labeling_list = [predict_label.split() for predict_label in token_labeling_predict_f.readlines()]
        return predict_token_labeling_list

    def get_token_labeling_labels(self):
        """only contain Task labels"""
        return ['Date', 'Number', 'Text', '书籍', '人物', '企业', '作品', '出版社', '历史人物', '国家', '图书作品', '地点', '城市', '学校', '学科专业',
                '影视作品', '景点', '机构', '歌曲', '气候', '生物', '电视综艺', '目', '网站', '网络小说', '行政区', '语言', '音乐专辑', 'O']

    def producte_token_labeling_list(self):
        """input seq.out and token_labeling_test_results.txt file
           output token_labeling_test_list, clean_predict_token_labeling_list
        """
        path_to_token_labeling_file = os.path.join(self.path_to_label_file, "token_label_out.txt")
        token_labeling_list = self._get_token_labeling_list(path_to_token_labeling_file)
        path_to_token_labeling_test_results_file = os.path.join(self.path_to_predict_label_file,
                                                              "token_label_prediction_test_results.txt")
        predict_token_labeling_list = self._get_predict_token_labeling_list(path_to_token_labeling_test_results_file)
        token_labeling_test_list = []
        clean_predict_token_labeling_list = []
        seqence_length_dont_match_index = 0
        for y_test, y_predict in zip(token_labeling_list, predict_token_labeling_list):
            y_predict = y_predict[1:-1]  # y_predict.remove('[CLS]') #y_predict.remove('[SEP]')
            while '[Padding]' in y_predict:
                print("X" * 100)
                y_predict.remove('[Padding]')
            while '[##WordPiece]' in y_predict:
                y_predict.remove('[##WordPiece]')
            while '[##WordPiece]' in y_test:
                y_test.remove('[##WordPiece]')
            if len(y_predict) > len(y_test):
                print(y_predict)
                print(y_test)
                print("~*" * 100)
                seqence_length_dont_match_index += 1
                y_predict = y_predict[0:len(y_test)]
            elif len(y_predict) < len(y_test):
                print(y_predict)
                print(y_test)
                print("~" * 100)
                y_predict = y_predict + ["O"] * (len(y_test) - len(y_predict))
                seqence_length_dont_match_index += 1
            assert len(y_predict) == len(y_test)
            # 如果有较多的预测句子与正确句子长度不匹配（> 句子总数的1%），说明不能用上述简单方法处理预测出来的句子
            #assert seqence_length_dont_match_index < int(len(token_labeling_list) * 0.01)
            token_labeling_test_list.extend(y_test)
            clean_predict_token_labeling_list.extend(y_predict)
        if "[CLS]" in clean_predict_token_labeling_list:
            print("[CLS] doesn't just appear at the beginning of a sentence.")
            clean_predict_token_labeling_list = [y_p.replace("[CLS]", "O") for y_p in clean_predict_token_labeling_list]
            print("[CLS]" * 10 + "\n")
        if "[SEP]" in clean_predict_token_labeling_list:
            print("[SEP] doesn't just appear at the end of a sentence.")
            clean_predict_token_labeling_list = [y_p.replace("[SEP]", "O") for y_p in clean_predict_token_labeling_list]
            print("[SEP]" * 10 + "\n")
        print("seqence_length_dont_match numbers", seqence_length_dont_match_index)
        return token_labeling_test_list, clean_predict_token_labeling_list


    def show_token_labeling_report(self, store_report=True, label_choose=None):
        token_labeling_test_list, clean_predict_token_labeling_list = self.producte_token_labeling_list()
        token_labeling_test_list, clean_predict_token_labeling_list = self.delete_both_sides_is_O_word(token_labeling_test_list,
                                                                                   clean_predict_token_labeling_list)
    
        labels = self.get_token_labeling_labels()


        if len(labels) > len(set(token_labeling_test_list)):
            print("token_labeling Task Labels number:\t", len(labels))
            print("token_labeling token_labeling_test_list Labels number:\t", len(set(token_labeling_test_list)))
            print("token_labeling predict_token_labeling_list Labels number:\t", len(set(clean_predict_token_labeling_list)))
        # 以下方法保证预测标签和真实标签个数一样，且不会增加计算分数，因为让
        #  token_labeling_test_list[idx] = "O"  clean_predict_token_labeling_list[idx]="other"
        # The following method ensures that the number of predicted tags is the same as that of real tags,
        # and does not increase the calculation score because the number of predicted tags is the same as that of real tags.
        for idx, test_label in enumerate(token_labeling_test_list):
            if test_label not in clean_predict_token_labeling_list:
                token_labeling_test_list[idx] = "O"
                clean_predict_token_labeling_list[idx] = self.get_token_labeling_labels()[0]  # self.get_token_labeling_labels()[0] is not "O"

        labels = list(set(token_labeling_test_list))
        print("---show_token_labeling_report---")
        self.show_metrics(token_labeling_test_list, clean_predict_token_labeling_list, labels)
        print("--" * 30)

            
            
            

if __name__ == '__main__':
    path_to_label_file = "data/SKE_2019/test/"

    path_to_predict_label_file = "output/SKE_2019_epochs3_ckpt9000"
    log_out_file = path_to_predict_label_file
    intent_token_labeling_reports = SKE_2019_Sequnce_labeling_Caculate(
        path_to_label_file, path_to_predict_label_file, log_out_file)
    intent_token_labeling_reports.show_token_labeling_report(store_report=True)
