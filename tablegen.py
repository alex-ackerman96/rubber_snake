import pandas as pd
import openpyxl
from openpyxl.styles import Border

import pandas as pd

def excel_to_latex(excel_path, sheet_name=0, output_path=None):
    """
    Convert Excel to LaTeX table with exact format:
    - 7 specific columns with vertical bars in header
    - Fixed multicolumn headers
    - Empty rows template when no data
    """
    # Load Excel data (ignore headers)
    df = pd.read_excel(excel_path, sheet_name=sheet_name, header=None)
    
    # Define fixed header structure
    header = (
        r'\multicolumn{1}{|c|}{\textbf{Parameter}} & '
        r'\multicolumn{1}{c|}{\textbf{Symbol}} & '
        r'\multicolumn{1}{c|}{\textbf{Min.}} & '
        r'\multicolumn{1}{c|}{\textbf{Typ.}} & '
        r'\multicolumn{1}{c|}{\textbf{Max.}} & '
        r'\multicolumn{1}{c|}{\textbf{Units}} & '
        r'\multicolumn{1}{c|}{\textbf{Conditions}} \\ \hline'
    )
    
    # Build LaTeX table
    latex = [
        r'\begin{table}[]',
        r'\begin{tabular}{lllllll}',
        r'\hline',
        header
    ]
    
    # Add data rows or empty template
    if df.empty:
        for _ in range(3):
            latex.append(' & ' * 6 + r' \\')
    else:
        for _, row in df.iterrows():
            # Truncate/pad to 7 columns
            cells = [str(cell) if pd.notnull(cell) else '' for cell in row][:7]
            cells += [''] * (7 - len(cells))
            latex.append(' & '.join(cells) + r' \\')
    
    latex.append(r'\end{tabular}')
    latex.append(r'\end{table}')
    
    # Output handling
    result = '\n'.join(latex)
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
    return result

# Example usage:
# latex_table = excel_to_spec_latex_table('input.xlsx', output_path='output.tex')


# Example usage:
latex_code = excel_to_latex('table.xlsx', sheet_name=0)
print(latex_code)
