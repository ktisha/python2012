class Actor:
    def accept_visitor(self, visitor):
        raise NotImplementedError("Abstract method is called")

    def draw(self):
        raise NotImplementedError("Abstract method is called")
