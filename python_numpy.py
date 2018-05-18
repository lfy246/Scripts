# #numpy实现矩阵相加相乘
# import numpy
#
# a = numpy.matrix([ [1, 2, 3, 4],
#                 [5, 6, 7, 8],
#                 [9, 10, 11, 12],
#                 [13, 14, 15, 16] ])
# b = numpy.matrix([ [16, 15, 14, 13],
#                 [12, 11, 10, 9],
#                 [8, 7, 6, 5],
#                 [4, 3, 2, 1] ])
# print('a+b:',a+b)
# print('a*b:',a*b)


#矩阵相加
def count_and(X,Y):
    result = [[0]*len(X[0]) for row in range(n)]

    for i in range(len(X)):
        for j in range(len(X[0])):
            result[i][j] = X[i][j] + Y[i][j]

    return result

# sum = 0
# for i in range(3):
#     print(i)
# print(sum)

# i=1
# while i+1:
#     if i>4:
#         print(i)
#         i+=1
#         break
#     print(i)
#     i+=2
# print(i)


# x  =input()
# print(isinstance(x,int))
a,b=3,4
a,b=b,a
print(a,b)