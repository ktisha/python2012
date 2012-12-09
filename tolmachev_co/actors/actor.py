class Actor:
    def accept_visitor(self, visitor):
        raise NotImplementedError("Abstract method is called")

    def get_name(self):
        raise NotImplementedError("Abstract method is called")