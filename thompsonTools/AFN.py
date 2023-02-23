

from .Bridge import Bridge
from .Format import Format
import pydot

import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin'    

class AFN:
    def __init__(self, regex):
        self.regex = regex
        self.statesNo = 0

    def MYT(self):
        formatt = Format(self.regex)
        stringg = formatt.infixPostfix()
        stack = []

        for value in stringg:
            if value.isalnum(): 
                # Definiendo estados iniciales y finales
                start = self.statesNo
                end = self.statesNo + 1
                
                # Generando transicion
                transitions = {}
                # Formato: {estado inicial: {simbolo: [estado final]}}
                # Ejemplo: {0: {'a': [1]}}
                # Cuando se trata de un caracter solo hay un estado final e inicial
                transitions[start] = {value: [end]}
                
                # Se crea un objeto de tipo Bridge que es la transicion 
                # del caracter
                stack.append(Bridge(start, end, transitions))
                # Dado que se crearon dos estados se aumenta el contador en dos
                self.statesNo += 2

            elif value == '.':
                # # Obteniendo los dos ultimos elementos de la pila
                el2 = stack.pop()
                el1 = stack.pop()
                # Se realiza la union de los dos diccionarios para tomar 
                # en cuenta todas las transiciones
                el1.trs.update(el2.trs)

                # El objetivo de este ciclo es reemplazar el estado final
                # del primer elemento por el estado inicial del segundo
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
                
                # Dado que para la union ... 
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
                        graph.add_node(pydot.Node(str(k), color='green', style='filled', shape='circle'))                                               
                    if v2[i] == myt.end:
                        graph.add_node(pydot.Node(str(v2[i]), shape='doublecircle'))
                    else:
                        graph.add_node(pydot.Node(str(v2[i])))
                    graph.add_edge(pydot.Edge(str(k), str(v2[i]), label=k2))
        graph.write_png('output.png', encoding='utf-8')


