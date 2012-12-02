__author__ = 'derketzer'

class STATE:
    def __init__(self, out0 = 0, out1 = 0, action0 = 3, action1 = 3):
        self.outState0 = out0
        self.outState1 = out1
        self.actionToMove0 = action0
        self.actionToMove1 = action1

    def getOutState(self, id):
        return self.outState0 if (id == 0) else self.outState1

    def getAction(self, id):
        return self.actionToMove0 if (id == 0) else self.actionToMove1
