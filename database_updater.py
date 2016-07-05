from operator import itemgetter
import sys
import csv

sys.stdout = open('output.txt', 'w')


def get_data(file):
    data = []
    with open(file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for i in reader:
            ids = i
            break
        for i in reader:
            data.append(i)
    return data


def filter_data(data):
    # more formatting of data wrt to our needs
    roll = data[2]
    subjects = []
    i = 3
    id = 0
    while True:
        try:
            element = map(str, data[i].split(' '))
            element.pop(0)
            id = int(element[0])
            id = 1003  # started this new website at 1001
            i += 1
            subjects.append(tuple([element[1], element[-1], id]))
        except ValueError:
            break
    element = map(str, data[i].split(' '))
    element.pop(0)
    credit = int(element[2])
    sgpa = float(element[-1])
    return roll, id, subjects, sgpa, credit


def insert_sgpa(data2):
    # you could directly connect with db if it's locally available
    print 'INSERT INTO exam (student_id,semester_id,sgpa,credits) VALUES ',
    while len(data2) > 0:
        data = data2[0]
        print '("' + data[0] + '",' + str(data[1]) + ',' + str(data[3]) + ',' + str(data[-1]) + '),'
        data2.pop(0)


def insert_grades(data2):
    # you could directly connect with db if it's locally available
    print 'INSERT INTO `score` (student_id, subject_id, grade, semester_id) VALUES',
    while len(data2) > 0:
        data = data2[0]
        while len(data[2]) > 0:
            print '("' + data[0] + '","' + str(data[2][0][0]) + '","' + str(data[2][0][1]) + '",' + str(
                data[2][0][-1]) + '),'
            data[2].pop(0)
        data2.pop(0)


def main():
    data = get_data("./database8th.csv")
    data.sort(key=itemgetter(2))
    newdata = []
    for i in range(len(data)):
        newdata.append(filter_data(data[i]))
    insert_sgpa(newdata)
    insert_grades(newdata)


if __name__ == '__main__':
    main()
