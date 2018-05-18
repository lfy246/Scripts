# list = [1,2,3,4,5,6,7]
# list2 = [8,9]
# for i in list:
#     print(i)
#     if(i==2):
#         list.extend(list2)
#
# print(list)

# str = '南京鹤龄药事服务有限公司\n· 统一社会信用代码/注册号：91320100585084405E'
# list = str.split('\n')
# print(list[0])
def del_same():
    file = open("F:\python\公司名录\江苏1.txt", 'r',encoding='utf-8')
    data = file.readlines()
    print(len(data))
    data_s = set(data)
    print(len(data_s))
    file.close()
    file_w = open("F:\python\公司名录\江苏.txt", 'w',encoding='utf-8')
    for i in data_s:
        file_w.write(i)
    file_w.close()

del_same()
