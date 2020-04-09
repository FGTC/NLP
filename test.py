# -*- coding: utf-8 -*-

# 二元隐马尔科夫模型（Bigram HMMs）

import re
# 状态转移概率
A_dic = {}
# 发射概率
B_dic = {}
# 统计计数
Count_dic = {}
# 初始状态概率
Pi_dic = {}
# 状态列表
state_set = []
# 单词列表
word_set = []
line_num = -1


# 初始化字典
def init():
    get_state_word_list()
    for state in state_set:
        A_dic[state] = {}
        for state1 in state_set:
            A_dic[state][state1] = 0.0
    for state in state_set:
        B_dic[state] = {}
        for word in word_set:
            B_dic[state][word] = 0.0
    for state in state_set:
        Pi_dic[state] = 0.0
        Count_dic[state] = 0


def get_state_word_list():
    text = open("train_pos.txt", "rb")
    while True:
        line = text.readline()
        if not line:
            break
        line = line.strip()
        line = line.decode("utf-8", "ignore")
        line = line + " END/END"
        token_list = line.split(" ")
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
            if tag not in state_set:
                state_set.append(tag)
            if word not in word_set:
                word_set.append(word)
    text.close()
    # 返回word、tag列表
    return state_set, word_set


# 输出模型的三个参数：初始概率+转移概率+发射概率
def parameter():
    # 初始概率
    for key in Pi_dic:
        Pi_dic[key] = Pi_dic[key] * 1.0 / line_num
        # print(key, end=" ")
        # print(Pi_dic[key])
    # 转移概率
    key_list = []
    for key in A_dic:
        for key1 in A_dic[key]:
            # if key1 not in key_list:
            #     key_list.append(key1)
            # print(key)
            A_dic[key][key1] = A_dic[key][key1] / Count_dic[key]
            # print(A_dic[key][key1])
        # print(key_list)
    # 发射概率
    for key in B_dic:
        for word in B_dic[key]:
            B_dic[key][word] = B_dic[key][word] / Count_dic[key]


def viterbi(line):
    line = line.replace("<sub>", "").replace("</sub>", "").replace("<sup>", "").replace("</sup>", "").replace("$$_ ", "")
    sentence = line.split()
    # 每次都找出以tag X为最终节点，长度为i的tag链
    viterbi = []
    # 把所有tag X前一个Tag记下来
    backpointer = []
    first_viterbi = {}
    first_backpointer = {}
    for state in state_set:
        if sentence[0] not in word_set:
            first_viterbi[state] = Pi_dic[state] * (1 / len(word_set))
        else:
            first_viterbi[state] = Pi_dic[state]*B_dic[state][sentence[0]]
        first_backpointer[state] = "START"
    viterbi.append(first_viterbi)
    backpointer.append(first_backpointer)
    for wordindex in range(1, len(sentence)):
        if sentence[wordindex] not in word_set:
            continue
        this_viterbi = {}
        this_backpointer = {}
        prev_viterbi = viterbi[-1]
        for tag in state_set:
            # 如果现在这个tag是X，现在的单词是w，
            # 我们想找前一个tag Y，并且让最好的tag sequence以Y X结尾。
            # 也就是说
            # Y要能最大化：
            # prev_viterbi[ Y ] * P(X | Y) * P( w | X)
            best_previous = max(prev_viterbi.keys(), key=lambda prevtag: prev_viterbi[prevtag] * A_dic[prevtag][tag] * B_dic[tag][sentence[wordindex]])
            this_viterbi[tag] = prev_viterbi[best_previous] * A_dic[best_previous][tag] * B_dic[tag][sentence[wordindex]]
            this_backpointer[tag] = best_previous
        viterbi.append(this_viterbi)
        backpointer.append(this_backpointer)
    prev_viterbi = viterbi[-1]
    best_previous = max(prev_viterbi.keys(), key=lambda prevtag: prev_viterbi[prevtag] * A_dic[prevtag]["END"])
    # 我们这会儿是倒着存的。。。。因为。。好的在后面
    best_tagsequence = [best_previous]
    # 同理 这里也有倒过来
    backpointer.reverse()
    current_best_tag = best_previous
    # 回溯
    for bp in backpointer:
        best_tagsequence.append(bp[current_best_tag])
        current_best_tag = bp[current_best_tag]
    best_tagsequence.reverse()
    del best_tagsequence[0]
    return best_tagsequence


def test():
    op = open("ori_pos.txt", "r", encoding="utf-8")
    pt = open("pos_res.txt", "a", encoding="utf-8")
    while True:
        line = op.readline()
        if not line:
            break
        line = line.strip()
        tag_list = viterbi(line)
        token_list = line.split()
        newline = ""
        newtoken_list = []
        for token in token_list:
            if "$$_" in token:
                continue
            else:
                newtoken_list.append(token)
        m = 0
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
        pt.write(newline + "\n")
    op.close()
    pt.close()


def main():
    text = open("train_pos.txt", "rb")
    init()
    global line_num
    while True:
        line = text.readline()
        if not line:
            break
        line_num += 1
        line = line.strip()
        line = line.decode("utf-8", "ignore")
        line = line + " END/END"
        token_list = line.split(" ")
        word_list = []
        tag_list = []
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
                Pi_dic[tag_list[i]] += 1      # Pi_dic记录句子第一个字的状态，用于计算初始状态概率
                B_dic[tag_list[i]][word_list[i]] += 1  # 用于计算发射概率
                Count_dic[tag_list[i]] += 1   # 记录每一个状态的出现次数
            else:
                A_dic[tag_list[i-1]][tag_list[i]] += 1    # 用于计算转移概率
                B_dic[tag_list[i]][word_list[i]] += 1  # 用于计算发射概率
                Count_dic[tag_list[i]] += 1   # 记录每一个状态的出现次数
    parameter()
    text.close()


if __name__ == "__main__":
    main()
    test()



