class HTMLNode():
    def __init__(self,tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is not None:
            ret_str = ""
            for values in self.props:
                ret_str = f"{ret_str} {values}=\"{self.props[values]}\""
            return ret_str
    
    #def __repr__(self):
     #   return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"