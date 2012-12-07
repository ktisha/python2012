class Error(Exception):
    pass


class Stanza(object):
    def __init__(self, name=None, attr=None, text=None, children=None):
        super(Stanza, self).__init__()
        self.__is_closed_ = False
        self.__name_ = name
        if attr:
            self.__attr_ = attr
        else:
            self.__attr_ = {}
        if text:
            self.__text_ = text
        else:
            self.__text_ = ""
        if children:
            self.__children_ = children
        else:   self.__children_ = []


    def get_text(self):
        return self.__text_

    def get_attr(self, key):
        return self.__attr_[key]

    def get_attrs(self):
        return self.__attr_

    def get_children(self):
        return self.__children_

    def get_name(self):
        return self.__name_

    def set_name(self, name):
        self.__name_ = name

    def add_text(self, test):
        self.__text_ = test

    def add_child(self, child):
        self.__children_.append(child)

    def add_atr(self, name, value):
        self.__attr_[name] = value

    def close(self):
        self.__is_closed_ = True

    def is_closed(self):
        return self.__is_closed_

    def to_xml(self):
        res = []
        if not self.__name_:
            raise Error()
        res.append("<")
        res.append(self.__name_)
        res.append(" ")
        for name, value in self.__attr_.items():
            res.append(name)
            res.append("=")
            res.append("'")
            res.append(value)
            res.append("'")
            res.append(" ")
        res.append(">")
        if self.__text_:
            res.append(self.__text_)
            # res.append("\n")
        for child in self.__children_:
            res.append(child.to_xml())
        res.append("</")
        res.append(self.__name_)
        res.append(">")
        return "".join(res)
