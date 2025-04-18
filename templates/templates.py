
import os
import shutil
import subprocess
import json
from datetime import datetime
from typing import Union

class Document:
    def __init__(self, documentclass : str = "article", fontsize : Union[int, float] = 12, sheetsize : str = "a4", columnformat : str = None, packages : list[tuple[str, str]] = [], title : str = None, subtitle : str = None, authors : list[str] = [], date : str = None, sectionfiles = [], appendixfiles = []):
        
        self.projectpath = os.getcwd()
        
        self.documentclass = documentclass
        self.fontsize = fontsize
        self.sheetsize = sheetsize
        self.columnformat = columnformat
        self._default_packages = []
        self.packages = self._default_packages + packages
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        if date is not None:
            self.date = date
        else:
            self.date = datetime.now().strftime("%Y-%m-%d")
        self.sections = sectionfiles
        self.appendices = appendixfiles
        self.watermark = None
        self.setup = []
        self.customcommands = []
    
    def set_documentclass(self, documentclass):
        self.documentclass = documentclass

    def set_fontsize(self, fontsize):
        self.fontsize = fontsize

    def set_sheetsize(self, sheetsize):
        self.sheetsize = sheetsize

    def set_columnformat(self, columnformat):
        self.columnformat = columnformat

    def add_package(self, package, options=None):
        self.packages.append((package, options))

    def set_title(self, title):
        self.title = title

    def set_subtitle(self, subtitle):
        self.subtitle = subtitle

    def add_author(self, author):
        self.authors.append(author)

    def set_date(self, date):
        self.date = date

    def add_section(self, section):
        self.sections.append(section)

    def add_appendix(self, appendix):
        self.appendices.append(appendix)
        
    def add_custom_command(self, command):
        self.customcommands.append(command)
        
    def add_watermark(self, watermark):
        self.watermark = watermark
        
    def synthesize(self):
        # Document class
        doc_str = f"\\documentclass[{self.fontsize}pt, {self.columnformat}]{{{self.documentclass}}}\n"
        # Packages
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n% Packages %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
        for package, options in self._default_packages:
            if options:
                doc_str += f"\\usepackage[{options}]{{{package}}}\n"
            else:
                doc_str += f"\\usepackage{{{package}}}\n"
        # Setup
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n% Setup %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
        for setup in list(self.setup.keys()):
            if self.setup[setup]:
                doc_str += f"% {setup}\n"
            for command, *args in self.setup[setup]:
                line = f"\\{command}"
                for arg in args:
                    if arg:
                        line += f"{arg}"
                doc_str += line + "\n"
            doc_str += "\n"
        # Custom commands
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n% Custom commands %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
        
        # Page style commands
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n% Page style %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
        doc_str += f"\\pagestyle{{{self.pagestyle}}}\n"
        print(doc_str)
        
        # Document
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n% Document %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
        doc_str += "\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n"
        doc_str += f"\\title{{{self.title}}}\n"
        if self.subtitle:
            doc_str += f"\\subtitle{{{self.subtitle}}}\n"
        if self.authors:
            doc_str += "\\author{"
            for i, author in enumerate(self.authors):
                doc_str += author
                if i < len(self.authors) - 1:
                    doc_str += ", "
            doc_str += "}\n"
        doc_str += f"\\date{{{self.date}}}\n\n\n"
        doc_str += "\\begin{document}\n\n"
        doc_str += "\\maketitle\n"
        doc_str += "\\tableofcontents\n"
        doc_str += "\\newpage\n"
        
        # Sections
        doc_str += "\n\\end{document}\n"
        # self.texfile = doc_str
        return doc_str
        
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
        self.texfile = os.path.join(self.projectpath, self.filename)
        with open(self.texfile, 'w') as file:
            file.write(f"{self.synthesize()}\n")

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


class Datasheet(Document):
    def __init__(self, watermark = None, **kwargs):
        super().__init__(**kwargs)
        self.pagestyle = "fancy"
        self.watermark = watermark
        self._default_packages = [("geometry", "left=1.5cm, right=1.5cm, top=2.0cm, bottom=2.0cm"), ("graphicx", None), ("tabularx", None), ("fancyhdr", None), ("caption", None), ("subcaption", None), ("float", None), ("booktabs", None), ("fancyhdr", None), ("draftwatermark", None)]
        self.customcommands = []
        
        self.setup_fancyhdr = [("fancyhf", None), ("fancyhead", "[L]", "{\\leftmark}"), ("fancyhead", "[R]", "{\\rightmark}"), ("fancyfoot", "[C]", "{\\thepage}")]
        self.setup_toc = [("setcounter", "{tocdepth}", "{2}")]
        self.setup_watermark = []
        
        if self.watermark is not None:
            self.setup_watermark = [("SetWatermarkText", f"{{{self.watermark}}}"), ("SetWatermarkScale", f"{{{2.25}}}"), ("SetWatermarkColor", "[gray]", f"{{{0.85}}}"), ("SetWatermarkAngle", f"{{{45}}}")] # 
            
        self.setup_caption = [("captionsetup", "{font=small, labelfont=bf, labelsep=colon, justification=centering}")]
            
        self.setup = {
                            "header":self.setup_fancyhdr, 
                            "contents":self.setup_toc, 
                            "watermark":self.setup_watermark,
                            "caption":self.setup_caption
                      }

if __name__ == "__main__":
    # Example usage
    doc = Datasheet(documentclass="article", fontsize=12, sheetsize="a4", columnformat="twocolumn", watermark="Sample Watermark")
    doc.set_title("Sample Document")
    doc.set_subtitle("An example of a LaTeX document")
    doc.add_author("John Doe")
    doc.set_date("2023-10-01")
    doc.add_package("graphicx", "pdftex")
    doc.add_section("introduction.tex")
    doc.add_appendix("appendix.tex")

    # doc.synthesize()
    doc.save_to_file()
    doc.compile("C:\\Users\\admin\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64")
