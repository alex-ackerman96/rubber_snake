import docx2txt


class Section:
    def __init__(self, title: str = None, file = filepath):
        self.title = title
        self.content = content

    def __str__(self):
        return f"{self.title}\n{self.content}"


text = docx2txt.process("sample/sections/Section 1.docx")
print(text)

