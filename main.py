import csv
import matplotlib.pyplot as plt
import math


class Point:
    def __init__(self, x1: float, x2: float, belong: list):
        self.x1 = x1
        self.x2 = x2
        self.belong = belong


"""this method is for calculating the antropy which shows the disorder of belonging datas to clusters"""


def antropy():
    sum = 0
    i = 0
    while i < c:
        j = 0
        while j < len(points):
            temp = points[j].belong[i]
            sum += temp * math.log(temp) / c
            j += 1
        i += 1
    return -sum


#
# def repair():
#     i = 0
#     sum1x = 0
#     sum1y = 0
#     while i < len(points):
#         sum2x = 0
#         sum2y = 0
#         j = 0
#         while j < c:
#             sum2x += points[i].belong[j] * cv[j][0]
#             sum2y += points[i].belong[j] * cv[j][1]
#             j += 1
#         sum1x += (abs(sum2x - points[i].x1)) ** 2
#         sum1y += (abs(sum2y - points[i].x2)) ** 2
#         i += 1
#     return math.sqrt(sum1x ** 2 + sum1y ** 2)

"""this method is for calculating the centers of clusters"""


def calculate_cv():
    j = 0
    while j < c:
        sumx1 = 0
        sumx2 = 0
        sum2 = 0
        i = 0
        while i < len(points):
            sumx1 += points[i].x1 * (points[i].belong[j] ** m)
            sumx2 += points[i].x2 * (points[i].belong[j] ** m)
            sum2 += (points[i].belong[j] ** m)
            i += 1
        cv[j] = [sumx1 / sum2, sumx2 / sum2]
        j += 1


"""this method is for calculating the belonging of each data to each cluster"""


def calculate_u():
    k = 0
    while k < c:
        i = 0
        while i < len(points):
            x1 = abs(points[i].x1 - cv[k][0])
            x2 = abs(points[i].x2 - cv[k][1])
            sumx1 = 0
            sumx2 = 0
            j = 0
            while j < c:
                sumx1 += (x1 / abs(points[i].x1 - cv[j][0])) ** (2 / (m - 1))
                sumx2 += (x2 / abs(points[i].x2 - cv[j][1])) ** (2 / (m - 1))
                j += 1
            # belong = math.sqrt((1 / sumx1)**2 + (1/sumx2)**2)
            belong = 1 / math.sqrt(sumx1 ** 2 + sumx2 ** 2)
            points[i].belong[k] = belong

            i += 1
        k += 1


m = 1.5
"""c is the number of clusters"""
c = 1
"""cv is the array which keeps the centers of clusters"""
cv = []
if __name__ == "__main__":

    points = []

    with open('sample3.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if not line_count == 0:
                points.append(Point(float(row[0]), float(row[1]), [0 for i in range(c)]))
            line_count += 1

        c = 1

        antropy_number_c = 999999
        while c < 100:
            cv.append([1 / (c + 1), 1 / (c + 1)])
            for j in points:
                j.belong = [0 for k in range(c)]

            antropy_center_v = 999999
            while True:
                calculate_u()
                calculate_cv()
                s = antropy()
                """if the antropy hasn't changed a lot this means we found the optimal centers of clusters"""
                if abs(s - antropy_center_v) < 0.005:
                    antropy_center_v = s
                    break
                antropy_center_v = s
            """if the antropy hasn't changed a lot this means we found the optimal number of clusters"""
            if abs(antropy_number_c - antropy_center_v) < 5:
                antropy_number_c = antropy_center_v
                break
            antropy_number_c = antropy_center_v
            c += 1
        print(antropy_number_c)
        print(c)

        listx1 = []
        listx2 = []
        for i in cv:
            listx1.append(i[0])
            listx2.append(i[1])
        plt.scatter(listx1, listx2, marker='o', color='blue')

        # create plot for training data
        x_array, y_array = [], []
        for point in points:
            x_array.append(point.x1)
            y_array.append(point.x2)
        plt.scatter(x_array, y_array, marker='*', color='red')

        plt.xlabel('x1', fontsize=16)
        plt.ylabel('x2', fontsize=16)
        plt.title('FCM - sample3', fontsize=20)
        plt.show()
