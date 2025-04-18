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
        return ""
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self,tag, value,props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag is None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
class ParentNode(HTMLNode):
    def __init__(self,tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have at least one child")
        
        props_html = self.props_to_html()
        str_to_return = f"<{self.tag}{props_html}>"
        
        for child in self.children:
           str_to_return = f"{str_to_return}{child.to_html()}" 

        return f"{str_to_return}</{self.tag}>"
           
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"

    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html