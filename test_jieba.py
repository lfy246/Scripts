import jieba

str = '徐州艾迪热能工程有限公司'
result1 = jieba.cut(str)
for i in result1:
    print(i)
