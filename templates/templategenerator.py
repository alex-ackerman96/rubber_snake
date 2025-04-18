import re

class TemplateParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.content = ""
        self.document_class = None
        self.options = None
        self.packages = []
        self.title = None
        self.subtitle = None
        self.authors = []

    def read_file(self):
        with open(self.filepath, 'r', encoding='utf-8') as file:
            self.content = file.read()

    def extract_document_class(self):
        # Extracts \documentclass[options]{class}
        pattern = r'\\documentclass(\[.*?\])?\{(.*?)\}'
        match = re.search(pattern, self.content)
        if match:
            self.options = match.group(1)[1:-1] if match.group(1) else None  # Remove brackets
            self.document_class = match.group(2)

    def extract_packages(self):
        # Extracts \usepackage[options]{package}
        pattern = r'\\usepackage(\[.*?\])?\{(.*?)\}'
        self.packages = []
        for match in re.findall(pattern, self.content):
            options = match[0][1:-1] if match[0] else None  # Remove brackets
            package = match[1]
            self.packages.append((package, options))

    def parse(self):
        self.read_file()
        self.extract_document_class()
        self.extract_packages()

    def get_document_class(self):
        return self.document_class, self.options

    def get_packages(self):
        # Returns list of tuples: (package_name, options)
        return self.packages

# Example usage:
parser = TemplateParser('templates/test.tex')
parser.parse()
print(parser.get_document_class())
print(parser.get_packages())
