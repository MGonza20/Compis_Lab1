
from thompsonTools.Syntax import Syntax
from thompsonTools.AFN import AFN

class Compilador:
    def __init__(self):
        pass

    def menu(self):
        print("1. AFN")
        print("2. Salir\n")
    
    def run(self):
        while True:
            self.menu()
            option = input("Opcion: ")
             
            if option == "1":
                string = input("Ingrese la expresion regular: ")
                syntax = Syntax(string)
                if syntax.checkParenthesis() and syntax.checkOperator():
                    a = AFN(string)
                    a.graph_myt()
                else:
                    print("Expresion regular incorrecta\n")
            elif option == "2":
                break
            else:
                print("Opcion incorrecta\n")

if __name__ == "__main__":
    c = Compilador()
    c.run()

