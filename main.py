

class Compilador:
    def __init__(self, regex):
        self.regex = regex
        self.sims = {'(': 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}
        self.statesNo = 0


    def concat(self):
        newRegex, ops = "", list(self.sims.keys())
        ops.remove('(')

        for i in range(len(self.regex)):
            val = self.regex[i]
            if i+1 < len(self.regex):
                val_p1 = self.regex[i+1]
                newRegex += val

                if val != '(' and val_p1 != ')' \
                   and val != '|' \
                   and val_p1 not in ops:
                    newRegex += '.'

        newRegex += self.regex[-1]
        return newRegex


    def prec(self, value):
        return 5 if value.isalnum() else self.sims[value]


    def infixPostfix(self):
        postfix, stack = '', []
        concatRegex = self.concat()

        for value in concatRegex:
            if value == '(':
                stack.append(value)

            elif value == ')':
                while stack[-1] != '(':
                    postfix += stack.pop()
                stack.pop()

            else:
                while stack and self.prec(stack[-1]) >= self.prec(value):
                    postfix += stack.pop()
                stack.append(value)
                
        while stack:
            postfix += stack.pop()
        return postfix





compi = Compilador("0?(1?)?0*") 
print(compi.infixPostfix())
