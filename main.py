

from thompsonTools.Bridge import Bridge
import pydot

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'    

class Compilador:
    def __init__(self, regex):
        self.regex = regex
        self.sims = {'(': 1, '|': 2, '.': 3, '*': 4, '+': 4, '?': 4}
        self.statesNo = 0
        self.transitions = {}

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


    def MYT(self):
        stringg = self.infixPostfix()
        stack = []

        for value in stringg:
            if value.isalnum(): 
                # Definiendo estados iniciales y finales
                start = self.statesNo
                end = self.statesNo + 1
                
                # Generando transicion
                transitions = {}
                transitions[start] = {value: [end]}
                
                stack.append(Bridge(start, end, transitions))
                self.statesNo += 2

            elif value == '.':
                # # Obteniendo los dos ultimos elementos de la pila
                el2 = stack.pop()
                el1 = stack.pop()
                el1.trs.update(el2.trs)

                for k, v in el1.trs.items():    
                    for el in v.values():
                        if el1.end in el:
                            dict1 = el1.trs[k]
                            key = list(dict1.keys())[0]
                            change = el1.trs[k][key].index(el1.end)
                            el1.trs[k][key][change] = el2.start
                            
                # Creando nuevo estado
                stack.append(Bridge(el1.start, el2.end, el1.trs))
                

            elif value == '|':
                # Obteniendo los dos ultimos elementos de la pila
                el2 = stack.pop()
                el1 = stack.pop()
                el1.trs.update(el2.trs)

                # Generando transicion
                start = self.statesNo
                end = self.statesNo + 1
                el1.trs[start] = {'ε': [el1.start, el2.start]}
                el1.trs[el1.end] = {'ε': [end]}
                el1.trs[el2.end] = {'ε': [end]}

                # Creando nuevo estado
                stack.append(Bridge(start, end, el1.trs))
                self.statesNo += 2

            elif value == '*':
                # Obteniendo el ultimo elemento de la pila
                el1 = stack.pop()

                # Generando transicion
                start = self.statesNo
                end = self.statesNo + 1
                self.statesNo += 2

                el1.trs[start] = {'ε': [el1.start, end]}
                el1.trs[el1.end] = {'ε': [el1.start, end]}

                # Creando nuevo transicion
                stack.append(Bridge(start, end, el1.trs))

            elif value == '+':
                # Obteniendo el ultimo elemento de la pila
                el1 = stack.pop()

                # Generando transicion
                start = self.statesNo
                end = self.statesNo + 1
                el1.trs[start] = {'ε': [el1.start]}
                el1.trs[el1.end] = {'ε': [el1.start, end]}

                # Creando nuevo estado
                stack.append(Bridge(start, end, el1.trs))
                self.statesNo += 2
            
            elif value == '?':
                start = self.statesNo
                end = self.statesNo + 1
                    
                # Generando transicion
                transitions = {}
                transitions[start] = {'ε': [end]}
                self.statesNo += 2
                
                el1 = stack.pop()
                el2 = Bridge(start, end, transitions)
                el1.trs.update(el2.trs)

                # Generando transicion
                start = self.statesNo
                end = self.statesNo + 1
                el1.trs[start] = {'ε': [el1.start, el2.start]}
                el1.trs[el1.end] = {'ε': [end]}
                el1.trs[el2.end] = {'ε': [end]}

                # Creando nuevo estado
                stack.append(Bridge(start, end, el1.trs))
                self.statesNo += 2

        return stack.pop()


    def graph_myt(self):
        myt = self.MYT()
        graph = pydot.Dot(graph_type='digraph', strict=True)
        graph.set_rankdir('LR')

        for k, v in myt.trs.items():
            for k2, v2 in v.items():
                for i in range(len(v2)):
                    if k == myt.start:
                        graph.add_node(pydot.Node(str(k), color='orange'))
                    if v2[i] == myt.end:
                        graph.add_node(pydot.Node(str(v2[i]), shape='doublecircle'))
                    else:
                        graph.add_node(pydot.Node(str(v2[i])))

                    graph.add_edge(pydot.Edge(str(k), str(v2[i]), label=k2))
        
        graph.write_png('output.png', encoding='utf-8')






# compi = Compilador("0?(1?)?0*") 
compi = Compilador("ab*ab*")
compi.graph_myt()
