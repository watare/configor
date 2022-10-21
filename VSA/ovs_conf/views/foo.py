from lxml import etree as ET

class Elem():

    def __init__(self,name):
        super().__init__()
        self.name = name
        self.attributes = {}
        self.children = []
        self.text = None
    def serialFirst(self):
        node = ET.Element(self.name)
        for k,v in self.attributes.items():
            node.set(k,v)
        if not self.text :
            for child in self.children:
                Elem.serialize(child,node)
        else :
            node.text = self.text
        return node
                    
    def serialize(self,parentnode):
        node = ET.SubElement(parentnode,self.name)
        for k,v in self.attributes.items():
            node.set(k,v)
        if not self.text :
            for child in self.children:
                Elem.serialize(child,node)
        else :
            # print(self.text)
            node.text = self.text
            
            
root = ET.Element('root')
print(root)      
first = Elem('first')
first.attributes['toto'] ='tutu'
# print(first.attributes.key())

second = Elem('second')
second2 = Elem('second')
third = Elem('third')
third.attributes['jul'] ='lie'
third.text = 'My own way'
first.children.append(second)
second.children.append(third)


first.serialize(root)
print(ET.tostring(root,encoding='Unicode',pretty_print=True))

   