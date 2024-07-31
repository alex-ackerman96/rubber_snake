import os
import shutil
import subprocess
import json
from typing import Union

class Document():
    
    def __init__(self, template = None, documentclass : str = "report", font : float = 12, columnformat : str = None, sheetsize : str = "letterpaper", sourcedir : str = None):
        
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
        
        if sourcedir == None:
            self.sourcedir = os.getcwd()
        else:
            self.sourcedir = sourcedir
            
        self.projectpath = os.getcwd()
            
        self.packages = []
        self.content = [f"\section{{Introduction}}"]
    
    def load_json(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    
    def add(self, item):
        if type(item) == self.Package:
            self.packages.append(item)
        else:
            self.content.append(item)
     
    def new_figure(self, imgfile : str, label : str = None, caption : str = None, options : Union[str, list, dict] = None):
        
        figure = self.Figure(imgfile, label, caption, options, sourcedir = self.sourcedir, figdir = os.path.join(self.projectpath, "figures"))
        return figure
               
    def create_directory(self, path : str = None, dirname : str = "New_TeX_Project"):

        if path == None:
            path = os.getcwd()

        fullpath = os.path.join(path, dirname)
        figspath = os.path.join(fullpath, "figures")
        
        self.projectpath = fullpath

        # Check if the directory exists
        if not os.path.isdir(fullpath):
            # Create the directory
            os.makedirs(fullpath)
            print(f"Directory '{fullpath}' created.")
            if not os.path.isdir(figspath):
                # Create the directory
                os.makedirs(figspath)
                print(f"Directory '{figspath}' created.")
        else:
            print(f"Directory '{fullpath}' already exists.")
    
    def save_to_file(self, filename : str = "main"):
        
        filename += ".tex"
        self.filename = filename 
        with open(filename, 'w') as file:
            file.write(f"{self.documenthead}\n")
            for i in range(len(self.packages)):
                file.write(self.packages[i] + "\n")
            file.write(f"\\begin{{document}}\n")
            for i in range(len(self.content)):
                file.write(self.content[i] + "\n")
            file.write(f"\\end{{document}}")   

    def save_to_directory(self, path : str = None, dirname : str = "New_TeX_Project"):

        if path == None:
            path = self.projectpath

        fullpath = os.path.join(path, dirname)
        figspath = os.path.join(fullpath, "figures")
        
        self.projectpath = fullpath

        # Check if the directory exists
        if not os.path.isdir(fullpath):
            # Create the directory
            os.makedirs(fullpath)
            print(f"Directory '{fullpath}' created.")
            if not os.path.isdir(figspath):
                # Create the directory
                os.makedirs(figspath)
                print(f"Directory '{figspath}' created.")
        else:
            print(f"Directory '{fullpath}' already exists.")
        
        self.texfile = os.path.join(self.projectpath, "main")
        self.save_to_file(self.texfile)
        
        
    def compile(self, miktex_path):
        os.environ["PATH"] += os.pathsep + miktex_path
        # Run pdflatex
        subprocess.run(["pdflatex", f"--output-directory={self.projectpath}", self.texfile], check=True)

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
        
    class Equation():
        pass
        
    class Figure():
        
        def __new__(self, imgfile : str, label : str = None, caption : Union[str, list, dict] = None, options : Union[str, list, dict] = None, sourcedir = None, figdir = None):
            
            if sourcedir == None:
                self.sourcedir = os.getcwd()
            else:
                self.sourcedir = sourcedir
                
            try:
                os.makedirs(figdir, exist_ok=True)
                img = os.path.join(figdir, os.path.basename(imgfile))
                shutil.copy(os.path.join(sourcedir, os.path.basename(imgfile)), img)
            except Exception as e:
                pass
            
            alignment = "\\centering"
            
            self.content = {    
                                "begin":f"\\begin{{figure}}\n    ",
                                "alignment":f"{alignment}\n",
                                "graphics":"",
                                "caption":"",
                                "label":"",
                                "end":f"\\end{{figure}}"
                            }
            
            width = 10
            
            self.content.update({"graphics":f"        \\includegraphics[width={width}cm]{{figures/{imgfile}}}\n"})
            
            outstr = ""
            
            outstr += self.content["begin"]
            outstr += self.content["alignment"]
            outstr += self.content["graphics"]
            outstr += self.content["caption"]
            outstr += self.content["label"]
            outstr += self.content["end"]
            
            return outstr
    
    class Table():
        pass
                        
          
if __name__ == "__main__":
    # doc = Document(columnformat="twocolumn")
    doc = Document(template="templates/whitepaper", sourcedir="sample")
    doc.create_directory()
    fig1 = doc.new_figure("Wavelength.png")
    # package1 = Document.Package("xcolor", ["table","xcdraw"])
    # doc.add(package1)
    # package2 = Document.Package("graphicx")
    # doc.add(package2)
    # print(doc.packages)
    # image = Document.Figure("Wavelength.png")
    # doc.add(image)
    # doc.save_to_directory()
    # doc.compile("C:\\Users\\aackerman\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64")