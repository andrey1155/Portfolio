
class MacroManager:

    def __init__(self,lm):
        self.macro_dict = {}
        self.lm = lm

    def invoke(self,name,args,line):
        return self.macro_dict[name].invoke(args,self.lm,line)

    def add_macro(self,node):
        self.macro_dict.update({node.name:node})

    def update(self, mm):
        if isinstance(mm, MacroManager):
            self.macro_dict.update(mm.macro_dict)
        else: raise Exception()


class MacroLabelManager:

    def __init__(self,name = ""):
        self.macro_name = name
        self.inv_labels = {}
        self.labels = {}
        self.id = 0

    def invoke(self):
        self.id += 1


    #instr id / name
    def add_label(self,name,id):
        self.inv_labels.update({id:name})
        self.labels.update({name: id})


    def get_label_id(self,name):
        return self.labels[name]


    def get_name(self, id):

        return  f"{self.macro_name}_{self.inv_labels[id]}_{self.id}"

        pass

    def __repr__(self):
        return self.labels.__repr__()