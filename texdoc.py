

class Document():
    
    def __init__(self, template = None, documentclass : str = "report", font : float = 12, columnformat : str = None, sheetsize : str = "letterpaper"):
        
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
            
    def save_doc_to_file(self, filename : str = "untitled"):
        
        filename += ".tex"
        self.filename = filename 
        with open(filename, 'w') as file:
            for line in self.content:
                file.write(line + "\n")
        
          
if __name__ == "__main__":
    doc = Document(columnformat="twocolumn")
    
    print(doc.documenthead)
    print(doc.documentstart)
    print(doc.documentend)
    doc.save_doc_to_file()