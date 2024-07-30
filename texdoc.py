import json
from typing import Union

class Document():
    
    def __init__(self, template = None, documentclass : str = "report", font : float = 12, columnformat : str = None, sheetsize : str = "letterpaper"):
        
        if template != None:
            try:
                self.load_json(f"{template}.json")
                print(f"Successfully loaded '{template}.json'")
            except Exception as e:
                print(f"Unable to load template '{template}.json': {e}")
        
        # Document class options
        documentclasses = ["article", "proc", "minimal", "report", "book", "slides", "memoir", "letter", "beamer"]
        if documentclass in documentclasses:
            self.documentclass = documentclass
        else:
            self.documentclass = "report"
        
        self.font = font
            
        # Column format options
        columnformats = ["twocolumn"]
        if columnformat in columnformats:
            self.columnformat = columnformat
        else:
            self.columnformat = None
        
        # Sheet size options
        sheetsizes = ["letterpaper", "a4paper"]
        if sheetsize in sheetsizes:
            self.sheetsize = sheetsize
        else:
            self.sheetsize = "letterpaper"
        # Column formatting options
        if self.columnformat != None:    
            self.documenthead = f"\documentclass[{self.font}pt, {self.sheetsize}, {self.columnformat}]{{{self.documentclass}}}"
        else:
            self.documenthead = f"\documentclass[{self.font}pt, {self.sheetsize}]{{{self.documentclass}}}"
        
        
        self.documentstart = f"\\begin{{document}}"
        self.documentend = f"\end{{document}}"
        
        self.content = [self.documenthead, self.documentstart, self.documentend]
    
    def load_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
            
    def save_doc_to_file(self, filename : str = "untitled"):
        
        filename += ".tex"
        self.filename = filename 
        with open(filename, 'w') as file:
            for line in self.content:
                file.write(line + "\n")

    class Package(str):
        
        def __new__(self, name : str, options : Union[str, list, dict] = None):
            
            if options == None:
                content = f"\\usepackage{{{name}}}"
            else:
                if type(options) == str:
                    options = [options]
                elif type(options) == dict:
                    option_list = []
                    for key in options.keys():
                        option_list.append(options[key])   
                    options = option_list
                
                content = f"\\usepackage["
                for option in options:
                    content += f"{option}"
                    if option != options[-1]:
                        content += ", "
                content += f"]{{{name}}}"
                    
            
            return super().__new__(self, content)
        
    class Figure():
        pass
    
    class Table():
        pass
                        
          
if __name__ == "__main__":
    # doc = Document(columnformat="twocolumn")
    doc = Document(template="templates/whitepaper")
    
    print(doc.documenthead)
    print(doc.documentstart)
    print(doc.documentend)
    package = Document.Package("xcolor", ["table","xcdraw"])
    print(package)
    doc.save_doc_to_file()