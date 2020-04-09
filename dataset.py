# -*- coding: utf-8 -*-


# 数据预处理，输入是原始数据，输出是供模型使用的格式
def ori_to_res(origin_data, result_data):
    # text = open("val_pos.txt", "rb")
    text = open(origin_data, "rb")
    while True:
        line = text.readline()
        if not line:
            break
        line = line.strip().decode("utf-8", "ignore")
        token_list = line.split(" ")
        word_list = []
        for token in token_list:
            if token[:2] == "//":
                word = "/ "
            elif token == "$$_":
                word = "$$_ "
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
                    word = "".join(word) + " "
                else:
                    word = word_tag[0] + " "
            word_list.append(word)
            line = "".join(word_list)
            line = line.strip()
            # tag_list.append(tag)
        # with open("ori_pos.txt", "a", encoding="utf-8") as f:
        with open(result_data, "a", encoding="utf-8") as f:
            f.write(line + "\n")


# def ori_to_res():
#     text = open("test_pos1.txt", "rb")
#     # text = open(origin_data, "rb")
#     while True:
#         line = text.readline()
#         if not line:
#             break
#         line = line.strip()
#         line = line.decode("utf-8", "ignore")
#         token_list = line.split(" ")
#         word_list = []
#         for token in token_list:
#             if token[:2] == "//":
#                 word = "/ "
#             elif token == "$$_":
#                 word = "$$_ "
#             elif "/" not in token:
#                 continue
#             else:
#                 word_tag = token.split("/")
#                 if len(word_tag) > 2:
#                     word = []
#                     for wt in word_tag[:-2]:
#                         word.append(wt)
#                         word.append("/")
#                     word.append(word_tag[-2])
#                     word = "".join(word) + " "
#                 else:
#                     word = word_tag[0] + " "
#             word_list.append(word)
#             line = "".join(word_list)
#             line = line.strip()
#             # tag_list.append(tag)
#         with open("ori_pos.txt", "a", encoding="utf-8") as f:
#         # with open(result_data, "a", encoding="utf-8") as f:
#             f.write(line + "\n")
#
# ori_to_res()


