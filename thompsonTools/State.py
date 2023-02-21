
# Description: Esta clase es usada para representar un estado en un AFN.
class State():
    def __init__(self, stateNo, prev=None, next=None, initial=False, accept=False):
        self.stateNo = stateNo
        self.prev = prev if prev else []
        self.next = next if next else []
        self.initial = initial
        self.accept = accept

    def addPrev(self, prev):
        self.prev.append(prev)

    def addNext(self, next):
        self.next.append(next)

