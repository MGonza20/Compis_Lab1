


class Syntax:
    def __init__(self, string): 
        self.string = string
        self.sims = {'(': 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}
        

    def checkParenthesis(self):
        stack = []
        for i in range(len(self.string)):
            if self.string[i] == '(': 
                stack.append(self.string[i])
            elif self.string[i] == ')':
                if not stack:
                    return False
                stack.pop()
        return not stack


    def checkOperator(self):
        for i in range(len(self.string)):
            if self.string[i] in self.sims.keys():
                if i == 0:
                    return False
        return True


    def checkOperatorValid(self):
        for i in range(len(self.string)):
            if self.string[i] in self.sims.keys():
                if i+1 == len(self.string):
                    return False
        return True

