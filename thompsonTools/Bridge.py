
# Description: Esta clase es usada para representar una transicion
# entre dos estados en un AFN.
class Bridge():
    def __init__(self, start, final, transition):
        self.start = start
        self.final = final
        self.transition = transition
