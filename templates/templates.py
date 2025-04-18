from datetime import datetime
from typing import Union

class Document:
    def __init__(self, documentclass : str = "article", fontsize : Union[int, float] = 12, sheetsize : str = "a4", columnformat : str = None, packages : list[tuple[str, str]] = [], title : str = None, subtitle : str = None, authors : list[str] = [], date : str = None, sectionfiles = [], appendixfiles = []):
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

class DataSheet(Document):
    def __init__(self, watermark, **kwargs):
        self.watermark = watermark
        self._default_packages = [("geometry", "left=1.5cm, right=1.5cm, top=2.0cm, bottom=2.0cm"), ("graphicx", None), ("tabularx", None), ("fancyhdr", None), ("caption", None), ("subcaption", None), ("float", None), ("booktabs", None), ("fancyhdr", None), ("draftwatermark", None)]
        self.customcommands = []
        setup_watermark = [("SetWatermarkText", self.watermark), ("SetWatermarkScale", 2.25), ("SetWatermarkColor", "gray", 0.85), ("SetWatermarkAngle", 45)] # 
        super().__init__(**kwargs)


if __name__ == "__main__":
    # Example usage
    doc = Document(documentclass="article", fontsize=12, sheetsize="a4", columnformat="twocolumn")
    doc.set_title("Sample Document")
    doc.set_subtitle("An example of a LaTeX document")
    doc.add_author("John Doe")
    doc.set_date("2023-10-01")
    doc.add_package("graphicx", "pdftex")
    doc.add_section("introduction.tex")
    doc.add_appendix("appendix.tex")

    print(f"Document class: {doc.documentclass}")
    print(f"Title: {doc.title}")
    print(f"Authors: {', '.join(doc.authors)}")
    print(f"Date: {doc.date}")
    print(f"Sections: {', '.join(doc.sections)}")
    print(f"Appendices: {', '.join(doc.appendices)}")
    print(f"Packages: {', '.join([pkg[0] for pkg in doc.packages])}")
