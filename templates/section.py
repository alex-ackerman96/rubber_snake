import docx2txt


class Section:
    def __init__(self, title: str = None, file: str = None):
        self.filepath = file
        self.title = title
        self.content = docx2txt.process("sample/sections/Section 1.docx")

    def __str__(self):
        return f"{self.title}\n{self.content}"


# text = docx2txt.process("sample/sections/Section 1.docx")
# print(text)

