class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str:
        raise NotImplementedError
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None: 
            raise ValueError("Error")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    
class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_list = []
        for child in self.children:
            children_list.append(child.to_html())
        children_string = "".join(children_list)
        return f"<{self.tag}{self.props_to_html()}>{children_string}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"