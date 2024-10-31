import Player

class StateMachine:
    def __init__(self, o):
        self.o = o
        self.eventQue = []

    def update(self):
        self.curState.do(self.o)
        if self.eventQue:   #list에 요소가 있으면, list 값은 True
            e = self.eventQue.pop(0)   #list의 첫 번째 요소를 꺼냄
            for check_event, next_state in self.transitions[self.curState].items():
                if check_event(e):  # e가 지금 check_event이면? space_down(e) ?
                    self.curState.exit(self.o, e)
                    print(f'EXIT from {self.curState}')
                    self.curState = next_state
                    self.curState.enter(self.o, e)
                    print(f'ENTER into {next_state}')
                    return

    def start(self, startState):
        self.curState = startState
        startState.enter('START', 0)

    def render(self):
        self.curState.render(self.o)

    def setTransitions(self, transitions):
        self.transitions = transitions

    def addEvent(self, e):
        self.eventQue.append(e)
        print(f'    DEBUG: new event {e} is added.')