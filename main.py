
from treeComponents import Nodo

class Compilador:
    def __init__(self, regex):
        self.regex = regex
        self.sims = {'(': 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 5}

    def concat(self):
        newRegex = ""
        for i in range(len(self.regex)):
            value_i = self.regex[i]
            if (i+1 < len(self.regex)):
                value_ip1 = self.regex[i+1]
                newRegex += value_i

                if (value_i != "(" \
                    and value_ip1 != ")" \
                    and value_i != '|' \
                    and value_ip1 not in list(self.sims.keys())):
                        newRegex += '.'
        newRegex += self.regex[-1]
        return newRegex

    def infix_postfix(self):
        postfix, stack = "", []
        concatExp = self.concat()

        for value in concatExp:
            if value == '(':
                stack.append(value)

            elif value == ')':
                while stack[0] != '(':
                    poppedValue = stack.pop(0)
                    postfix += poppedValue
                stack.pop(0)
            else:
                while stack:
                    topValKey = stack[0]
                    topVal = 5 if topValKey.isalnum() else self.sims[topValKey]
                    cValue = 5 if value.isalnum() else self.sims[value]

                    if topVal >= cValue:
                        poppedValue = stack.pop(0)
                        postfix += poppedValue
                    else:
                        break
                stack.insert(0, value)
        while stack:
            postfix += stack.pop(0)
        return postfix


compi = Compilador("a?(b?)?b") 
print(compi.infix_postfix())
