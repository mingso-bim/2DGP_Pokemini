
class StateMachine:
    def __init__(self, o):
        self.o = o
        self.eventQue = []

    def update(self):
        self.curState.do()

    def start(self, startState):
        self.curState = startState;
        startState.enter()

    def render(self):
        self.curState.render()

    def setTransitions(self, transitions):
        self.transition = transitions

    def addEvent(self, e):
        self.eventQue.append(e)