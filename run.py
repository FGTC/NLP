# -*- coding: utf-8 -*-

from model import model
from dataset import ori_to_res


def viterbi(line, input_data):
    pi, a, b, word_set, tag_set = model(input_data)
    # 去掉不标注的词
    line = line.replace("<sub>", "").replace("</sub>", "").replace("<sup>", "").replace("</sup>", "").replace("$$_ ", "")
    sentence = line.split()
    # 每次都找出以tag为最终状态，长度为i的tag链
    viterbi = []
    # 把所有tag前一个tag记下来
    back = []
    # 初始化
    first_viterbi = {}
    first_back = {}
    for tag in tag_set:
        if sentence[0] not in word_set:
            # 此处处理未标注集中未在训练集中出现的单词
            first_viterbi[tag] = pi[tag] * (1 / len(word_set))
        else:
            first_viterbi[tag] = pi[tag] * b[tag][sentence[0]]
        first_back[tag] = "START"
    # 将所有的viterbi和back都记录下来
    viterbi.append(first_viterbi)
    back.append(first_back)
    for i in range(1, len(sentence)):
        # 对于未在词集合中出现的词，跳过本次处理
        if sentence[i] not in word_set:
            continue
        this_viterbi = {}
        this_back = {}
        # 前一个viterbi
        prev_viterbi = viterbi[-1]
        for tag in tag_set:
            # 得到前一个最好的tag，并且记录下来
            best_previous = max(prev_viterbi.keys(), key=lambda prevtag: prev_viterbi[prevtag] * a[prevtag][tag] * b[tag][sentence[i]])
            this_viterbi[tag] = prev_viterbi[best_previous] * a[best_previous][tag] * b[tag][sentence[i]]
            this_back[tag] = best_previous
        viterbi.append(this_viterbi)
        back.append(this_back)
    prev_viterbi = viterbi[-1]
    best_previous = max(prev_viterbi.keys(), key=lambda prevtag: prev_viterbi[prevtag] * a[prevtag]["END"])
    # 首先倒着存
    best_tag_sequence = [best_previous]
    # 这里也倒存
    back.reverse()
    current_best_tag = best_previous
    # 回溯tag
    for bp in back:
        best_tag_sequence.append(bp[current_best_tag])
        current_best_tag = bp[current_best_tag]
    best_tag_sequence.reverse()
    # 删除"START"
    del best_tag_sequence[0]
    # 返回标注词性列表及单词集合
    return best_tag_sequence, word_set


def main(input_data, ori_data, res_data):
    # op = open("ori_pos.txt", "r", encoding="utf-8")
    # 未标注集
    od = open(ori_data, "r", encoding="utf-8")
    # 标注结果集
    rd = open(res_data, "a", encoding="utf-8")
    # pt = open("pos_res.txt", "a", encoding="utf-8")
    while True:
        line = od.readline()
        # 退出循环条件
        if not line:
            break
        line = line.strip()
        tag_list, word_set = viterbi(line, input_data)
        token_list = line.split()
        newline = ""
        newtoken_list = []
        # 去掉"$$_"
        for token in token_list:
            if "$$_" in token:
                continue
            else:
                newtoken_list.append(token)
        m = 0
        # 标注
        for i in range(len(tag_list)):
            line_list = []
            if newtoken_list[m] not in word_set:
                line_list.append(newtoken_list[m])
                line_list.append("/n")
                m += 1
            else:
                line_list.append(newtoken_list[m])
                line_list.append("/")
                line_list.append(tag_list[i])
                m += 1
            newline = newline + "".join(line_list) + " "
        newline.strip()
        rd.write(newline + "\n")
    od.close()
    rd.close()


# 合并两个文件为一个
def merge(data_1, data_2):
    f2 = open(data_2, "a", encoding="utf-8")
    with open(data_1, "r", encoding="utf-8") as f1:
        while True:
            line = f1.readline()
            if not line:
                break
            # 将f1写到f2中去，最终的新文件名是f2打开的文件名
            f2.write(line)
    f2.close()


if __name__ == "__main__":
    # merge("test_pos1.txt", "train_pos.txt")
    # 第一个参数是验证集数据，第二个参数是预处理后得到的供模型使用的数据
    # 数据预处理
    ori_to_res("test_pos1.txt", "ori_pos.txt")
    # 第一个参数是训练集数据，第二个参数是预处理后得到的供模型使用的数据，第三个参数是最终标注结果
    main("train_pos.txt", "ori_pos.txt", "pos_res.txt")
