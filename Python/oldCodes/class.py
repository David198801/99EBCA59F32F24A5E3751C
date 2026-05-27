class Student(object):
    def __init__(self,name,score,height,money = 'unknow'):
        self.name = name
        self.score = score
        self.__height = height # can not directly access it form outside
        self.money = money
    def learn(self):
        print 'learning'
    def print_score(self):
        print '%s: %s' % (self.name, self.score)
    def printHeight(self):
        print self.__height
Sam=Student('Sam',95,175)
Sam.print_score()
print Sam.name,Sam.score,Sam.money
Sam.score = 96
print Sam.score
Sam.printHeight()