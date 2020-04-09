# -*- coding: utf-8 -*-

# 二元隐马尔科夫模型（Bigram HMMs）

# 初始状态概率字典
Pi = {}
# 状态转移概率字典，key也是一个字典
A = {}
# 发射概率字典，key也是一个字典
B = {}
# 统计词性计数字典，key为词性，value为总计数
Count = {}
# 词性列表，里面是所有词性的集合
tag_set = []
# 单词列表，里面是数据集中出现的所有单词
word_set = []
# 数据集总行数
line_num = -1


# 初始化A、B、Pi
def init(input_data):
    get_tag_word_list(input_data)
    # 初始化A
    for tag in tag_set:
        A[tag] = {}
        for tag1 in tag_set:
            A[tag][tag1] = 0.0
    # 初始化B
    for tag in tag_set:
        B[tag] = {}
        for word in word_set:
            B[tag][word] = 0.0
    # 初始化Pi
    for tag in tag_set:
        Pi[tag] = 0.0
        Count[tag] = 0


def get_tag_word_list(input_data):
    # text = open("train_pos.txt", "rb")
    text = open(input_data, "rb")
    while True:
        # 逐行读入
        line = text.readline()
        # 循环终止
        if not line:
            break
        # 设置为ignore，会忽略非法字符
        line = line.strip().decode("utf-8", "ignore") + " END/END"
        # 得到单词标注列表，以空格分割
        token_list = line.split(" ")
        for token in token_list:
            # 首先去掉不标注的token或者子token
            if "<sub>" or "<sup>" in token:
                token = token.replace("<sub>", "").replace("</sub>", "").replace("<sup>", "").replace("</sup>", "")
            # 遇到“//”直接将“/”作为word，第二个“/”之后的作为tag
            if token[:2] == "//":
                word = "/"
                tag = token[2:]
            # token中不包含“/”，则跳过本次循环
            elif "/" not in token:
                continue
            else:
                word_tag = token.split("/")
                if len(word_tag) > 2:
                    word = []
                    for wt in word_tag[:-2]:
                        word.append(wt)
                        word.append("/")
                    word.append(word_tag[-2])
                    word = "".join(word)
                    # 列表最后一个元素为tag
                    tag = word_tag[-1]
                else:
                    # 列表第一个元素为word
                    word = word_tag[0]
                    # 列表第二个元素为tag
                    tag = word_tag[1]
            # 得到所有的tag列表
            if tag not in tag_set:
                tag_set.append(tag)
            # 得到所有的word列表
            if word not in word_set:
                word_set.append(word)
    text.close()
    # 返回word、tag列表
    return tag_set, word_set


# 输出模型的三个参数：初始概率+转移概率+发射概率
def parameter():
    # 初始概率
    for key in Pi:
        Pi[key] = Pi[key] * 1.0 / line_num
        # print(key, end=" ")
        # print(Pi_dic[key])
    # 转移概率
    # key_list = []
    for tag in A:
        for tag1 in A[tag]:
            # if key1 not in key_list:
            #     key_list.append(key1)
            # print(key)
            A[tag][tag1] = A[tag][tag1] / Count[tag]
            # print(A_dic[key][key1])
        # print(key_list)
    # 发射概率
    for tag in B:
        for word in B[tag]:
            B[tag][word] = B[tag][word] / Count[tag]


def model(input_data):
    # text = open("train_pos.txt", "rb")
    text = open(input_data, "rb")
    init(input_data)
    global line_num
    while True:
        line = text.readline()
        if not line:
            break
        line_num += 1
        line = line.strip().decode("utf-8", "ignore") + " END/END"
        token_list = line.split(" ")
        word_list = []
        tag_list = []
        # 得到word列表和tag列表
        for token in token_list:
            if "<sub>" or "<sup>" in token:
                token = token.replace("<sub>", "").replace("</sub>", "").replace("<sup>", "").replace("</sup>", "")
            if token[:2] == "//":
                word = "/"
                tag = token[2:]
            elif "/" not in token:
                continue
            else:
                word_tag = token.split("/")
                if len(word_tag) > 2:
                    word = []
                    for wt in word_tag[:-2]:
                        word.append(wt)
                        word.append("/")
                    word.append(word_tag[-2])
                    word = "".join(word)
                    tag = word_tag[-1]
                else:
                    word = word_tag[0]
                    tag = word_tag[1]
            word_list.append(word)
            tag_list.append(tag)
        for i in range(len(tag_list)):
            if i == 0:
                # Pi记录句子第一个字的状态，用于计算初始状态概率
                Pi[tag_list[i]] += 1
                # 用于计算发射概率
                B[tag_list[i]][word_list[i]] += 1
                # 记录每一个状态的出现次数
                Count[tag_list[i]] += 1
            else:
                # 用于计算转移概率
                A[tag_list[i-1]][tag_list[i]] += 1
                # 用于计算发射概率
                B[tag_list[i]][word_list[i]] += 1
                # 记录每一个状态的出现次数
                Count[tag_list[i]] += 1
    parameter()
    text.close()
    return Pi, A, B, word_set, tag_set



