import sys

for line in open('numbers.txt', 'r'):

#   As recieve multiple value
    number1, number2 = line.split('\t')
    print "int:%d float:%f" % (int(number1), float(number2))


    
