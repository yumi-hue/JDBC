

import easygui as e
import random
import  math

class Question:
    number_range = 10
    expression_array = []#表达式列表
    expression = " "     #表达式表示
    answer = 0           #答案
    answer_char = " "    #答案表示
    probability = 0.5    #分数出现的概率
    count = 4            #操作数
    def __init__(self,number_range,count,probability):

        self.number_range = number_range
        self.count = count
        self.probability = probability

        result = self.new_exp(self.count)
        self.expression_array = result['expression_array']
        self.expression = result['expression']
        self.answer = result['answer']
        self.answer_char = str(self.fraction_char(result['answer']))

    def fraction_char(self,figure_array):#获得分数的表示形式
        figure1 = figure_array[0]
        figure2 = figure_array[1]
        if figure2 == 1:
            return figure1
        elif(figure1>figure2):
            quotient = int (figure1/figure2)
            figure1 = figure1 - (quotient*figure2)
            return  str(quotient) +"'" + str(figure1) + "/" + str(figure2)
        else:
            return  str(figure1) + "/" + str(figure2)

    def random_fraction(self):#获得随机分数
        number_range = self.number_range
        while True:
            figure1 = self.new_random(number_range)
            figure2 = self.new_random(number_range)
            if (figure1 % figure2)== 0 or figure2 == 0:
                continue
            else :
                break
        return self.Simple_fraction(figure1,figure2)

    def new_num(self) : # 获得随机运算数字
        number_range = self.number_range
        probability= self.probability

        probability *= 100
        probability = int(probability)

        result = { }
        if self.new_random(100) <= probability:
            figure = self.random_fraction()
            result['figure'] = figure[0]/figure[1]
            result['figure_char'] =self.fraction_char(figure)
            result['figure_array'] =  [figure[0],figure[1]]
        else :
            figure = self.new_random(number_range-1)
            result['figure'] = figure
            result['figure_char'] = str(figure)
            result['figure_array'] =  [figure,1]
        return result
    def operator_char(self,operator) :# 获取运算符号表示形式
        operatorArray = ['+','-','×','÷']
        return operatorArray[operator-1]

    def new_random(self,range): # 获取一个随机数
        return random.randint(1,range)

    def Calculation(self,figure1,figure2,operate):#计算算式的结果
        if operate == 1:
            numerator = figure1[0]*figure2[1]+figure2[0]*figure1[1]
            denominator = figure1[1]*figure2[1]
        elif operate == 2:
            numerator = figure1[0]*figure2[1]-figure2[0]*figure1[1]
            denominator = figure1[1]*figure2[1]
            if numerator < 0:
                return [numerator,denominator]
        elif operate == 3:
            numerator = figure1[0]*figure2[0]
            denominator = figure1[1]*figure2[1]
        elif operate == 4 :
            numerator = figure1[0]*figure2[1]
            denominator = figure1[1]*figure2[0]
        result = self.Simple_fraction(numerator,denominator)
        return result

    def Simple_fraction(self,numerator,denominator):#化为最简分数
            flage = self.Common_factor(numerator,denominator )
            numerator = int (numerator/flage)
            denominator = int (denominator/flage)
            return [numerator,denominator]

    def Common_factor(self,numerator,denominator):#辗转相除获得最大公约数
        numerator,denominator = denominator,numerator%denominator
        if denominator == 0:
            return numerator
        else:
            return self.Common_factor( numerator, denominator)

    def new_exp(self,count):#生成式子
        if count == 1:
            figure = self.new_num()
            return{
                'expression_array': figure['figure'],
                'expression':       figure['figure_char'],
                'answer':           figure['figure_array']
            }
        else :
            leftcount = self.new_random(count -1)
            rightcount = count - leftcount

            left = self.new_exp(leftcount)
            right = self.new_exp(rightcount)

            operate = self.new_random(4)

            if operate == 4 and right['answer'][0] == 0:
                 t = left
                 left = right
                 right = t
            answer = self.Calculation(left['answer'],right['answer'],operate)
            if answer[0] < 0:
                 t = left
                 left = right
                 right = t
                 answer = self.Calculation(left['answer'],right['answer'],operate)

            leftvalue = left['answer'][0]/left['answer'][1]
            rightvalue = right['answer'][0]/right['answer'][1]
            expression_array = [left['expression_array'],operate,right['expression_array']]
            if type(left['expression_array'])!=list and type(right['expression_array'])!=list: #两个子树都为值
                if (operate == 1 or operate == 3) and leftvalue < rightvalue:
                    expression_array = [right['expression_array'],operate,left['expression_array']]
            elif  type(left['expression_array'])==list and type(right['expression_array'])==list:# 两个子树都为树
                if operate == 1 or operate == 3:
                    if leftvalue == rightvalue and left['expression_array'][1] < right['expression_array'][1]:#树的值相等时，运算符优先级高的在左边
                        expression_array = [right['expression_array'],operate,left['expression_array']]
                    elif leftvalue < rightvalue :
                        expression_array = [right['expression_array'],operate,left['expression_array']]
                if operate in [3,4] :
                    if left['expression_array'][1] in [1,2]:
                        left['expression'] = '(' + left['expression'] + ')'
                    if right['expression_array'][1] in [1,2]:
                        right['expression'] = '(' + right['expression'] + ')'
            else:#一边的子树为树
                if operate == 1 or operate == 3:
                    if type(right['expression_array']) == list:
                        expression_array = [right['expression_array'],operate,left['expression_array']]
                if operate in [3,4] :
                    if type(left['expression_array']) == list and left['expression_array'][1] in [1,2] :
                        left['expression'] = '(' + left['expression'] + ')'
                    if type(right['expression_array']) == list and right['expression_array'][1] in[1,2]:
                        right['expression'] = '(' + right['expression'] + ')'
            expression = left['expression']+' '+self.operator_char(operate)+' '+right['expression']
            return {
                'expression_array':  expression_array,
                'expression':        expression,
                'answer':            answer
            }
class Parameter :
    number_range = 10
    expression_count = 5 
    probability = 0.5    #分数出现的概率
    expressionlist = []  #算式列表
    count = 4            #操作数
    boolean = True
    
    def get_parameter(self,ret):
        self.expression_count = int(ret[0])
        self.number_range = int(ret[1])
        return
        
    def __init__(self,ret):
        self.get_parameter(ret)
        self.expressionlist = self.getexpression_list(self.expression_count,self.number_range,self.count,self.probability)
        if self.boolean == True:
            self.write_file(self.expressionlist)


    def getexpression_list(self, expression_count, number_range, count, probability) :# 算式
        List = []
        i = 0
        while i < expression_count:
            expression = Question(number_range,count,probability)
            while self.check(expression,List):
                expression = Question(number_range,count,probability)
            List.append({
                'expression_array': expression.__dict__['expression_array'],#二叉树表示
                'expression':       expression.__dict__['expression'],#算式表达形式
                'answer':           expression.__dict__['answer'],#答案
                'answer_char':      expression.__dict__['answer_char']#答案表达形式

            })
            i += 1
        return List

    def check(self,expression,List):#查重方法
        expressionarray = expression.__dict__['expression_array']
        for i in List:
            if expressionarray == i['expression_array']:
                return True
        return False
    def write_file(self,expressionlist):#写入到文件
        i = 0
        E = open("Exercises.txt","w")
        A = open("Answers.txt","w")
        while i < len(expressionlist):
            E.write(str((i + 1)) + '. ' + expressionlist[i]['expression'] + ' =\n')
            A.write(str((i+1)) + '. ' + expressionlist[i]['answer_char'] + '\n')
            i += 1
        E.close()
        A.close()
    def check_answers(path1,path2):
        
        list = Parameter.get_answers(path1)
        grade = Parameter.checks(list,path2)
        Parameter.write_grade(grade)
        
    def write_grade(grade):#写入做题结果文件
        G = open('Grade.txt',"w")
        G.write('Correct:'+ str(len(grade[0])) + str(grade[0])+'\n'+ 'Wrong:'+ str(len(grade[1])) + str(grade[1])+'\n')
        G.close()
    def get_answers(path2):#获得用户答案
        with open(path2,"r",encoding="gbk") as file:
            lines = file.readlines()

            list = []
            for line in lines:
                answer = line.split('.')[1]
                answer1 = answer.replace(' ','')
                list.append(answer1)
        return list
    def checks(list,path1):#比对答案
        with open(path1,"r",encoding="gbk") as f:
            lines = f.readlines()
            listA =[]
            correct=[]
            wrong=[]
            grade=[]
            for line in lines:
                right_answer = line.split('.')[1]
                right_answer1 = right_answer.replace(' ','')
                listA.append(right_answer1)
            i = 0
            if (i) < len(listA):
                for char in listA:
                    if char != list[i]:
                        wrong.append(i+1)
                        i+=1
                    elif char == list[i]:
                        correct.append(i+1)
                        i+=1
                grade.append(correct)
                grade.append(wrong)
            return grade

# 图形界面
    def gui():
        order = e.ccbox(msg='请选择', title='小学四则运算', choices=['生成题目', '批改题目'])
        if order:
            msg = '请输入'
            title = '小学四则运算'
            fields = ['生成题目的个数', '生成参数的范围']
            try:
                ret = e.multenterbox(msg, title, fields, values=[1, 1])
                if int(ret[0]) <= 0 or int(ret[1]) <= 0:
                    e.msgbox(msg='参数错误，请重试新输入！', title='参数错误', ok_button='好耶！')
                    Parameter.gui()
                add = Parameter(ret)
            except:
                e.exceptionbox()
            order2 = e.ccbox(msg='请选择', title='小学四则运算', choices=['继续', '退出'])
            if order2:
                Parameter.gui()
            elif not order2:
                e.msgbox(msg='退出', title='退出', ok_button='好耶！')
        elif not order:
            e.msgbox(msg='根据提示选择文件路径', title='批改作业', ok_button='好耶！')
            msg1 = '选择一个文件，将会返回该文件的完整的目录'
            title1 = '用户答案文件路径'
            title2 = '题目答案文件路径'
            try:
                path1 = e.fileopenbox(msg1, title1, filetypes=["*.txt"])
                path2 = e.fileopenbox(msg1, title2, filetypes=["*.txt"])
                # path1 用户答案路径 path2原答案
                Parameter.check_answers(path1, path2)
                e.msgbox(msg='批改完成', title='退出', ok_button='好耶！')
            except:
                e.exceptionbox()

            order2 = e.ccbox(msg='请选择', title='小学四则运算', choices=['继续', '退出'])
            if order2:
                Parameter.gui()
            elif not order2:
                e.msgbox(msg='退出', title='退出', ok_button='好耶！')


def main():
    Parameter.gui()


main()
