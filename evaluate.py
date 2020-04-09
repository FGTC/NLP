# -*- coding: utf-8 -*-

# 结果
# def evaluate():
#     count = 0
#     count1 = 0
#     # 验证集
#     vp = open("val_pos.txt", "r", encoding="utf-8")
#     # 标注结果集
#     pr = open("pos_res.txt", "r", encoding="utf-8")
#     while True:
#         line1 = vp.readline()
#         line2 = pr.readline()
#         if not line1:
#             break
#         token_list1 = line1.split()
#         token_list2 = line2.split()
#         count += len(token_list2)
#         newtoken_list1 = []
#         for i in range(len(token_list1)):
#             if token_list1[i] not in token_list2:
#                 continue
#             else:
#                 newtoken_list1.append(token_list1[i])
#         for j in range(len(newtoken_list1)):
#             if newtoken_list1[j] == token_list2[j]:
#                 count1 += 1
#             else:
#                 continue
#     vp.close()
#     pr.close()
#     recall = count1 / count
#     print("召回率为：{:03.2f}".format(recall))
#
#
# evaluate()
