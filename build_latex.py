import json
import re

def process_text(text):
    # Hide math
    math_blocks = []
    def math_repl(m):
        math_blocks.append(m.group(0))
        return f"__MATH_{len(math_blocks)-1}__"
    text = re.sub(r'(\$.*?\$)', math_repl, text)

    # Escape chars
    text = text.replace('\\', '\\\\')
    text = text.replace('%', '\\%')
    text = text.replace('&', '\\&')
    text = text.replace('_', '\\_')
    text = text.replace('#', '\\#')

    # Bold and Italic
    text = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'\*(.*?)\*', r'\\textit{\1}', text)

    # Restore math
    for i, math_block in enumerate(math_blocks):
        # Because we escaped _, the placeholder became \_\_MATH\_i\_\_
        text = text.replace(f"\\_\\_MATH\\_{i}\\_\\_", math_block)

    return text

def md_to_latex(text):
    text = process_text(text)
    lines = text.split('\n')
    out = []
    in_table = False
    
    for line in lines:
        if line.startswith('\\#\\#\\# '):
            out.append('\\subsubsection*{' + line[7:].strip() + '}')
            continue
        elif line.startswith('\\#\\# '):
            out.append('\\subsection*{' + line[5:].strip() + '}')
            continue
        elif line.startswith('\\# '):
            out.append('\\section*{' + line[3:].strip() + '}')
            continue
            
        if re.match(r'^\|.*\|$', line.strip()):
            if not in_table:
                in_table = True
                out.append('\\begin{center}\n\\begin{tabular}{lll}\n\\toprule')
            row = line.strip().strip('|').split('|')
            if '---' in row[0] or (len(row) > 1 and '---' in row[1]):
                out.append('\\midrule')
                continue
            clean_row = [c.strip() for c in row if c.strip() != '']
            latex_row = " & ".join(clean_row) + " \\\\"
            out.append(latex_row)
            continue
        else:
            if in_table:
                in_table = False
                out.append('\\bottomrule\n\\end{tabular}\n\\end{center}')
                
        out.append(line)
        
    if in_table:
        out.append('\\bottomrule\n\\end{tabular}\n\\end{center}')
        
    return "\n".join(out)

def main():
    with open('main.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)

    latex_doc = [
        "\\documentclass{article}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage[spanish]{babel}",
        "\\usepackage{graphicx}",
        "\\usepackage{hyperref}",
        "\\usepackage{booktabs}",
        "\\usepackage{float}",
        "\\begin{document}",
        ""
    ]

    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            source = "".join(cell.get('source', []))
            latex_doc.append(md_to_latex(source))
            latex_doc.append("\n\n")
        elif cell['cell_type'] == 'code':
            source = "".join(cell.get('source', []))
            matches = re.findall(r'savefig\([\'"](plots/[^\'"]+\.png)[\'"]', source)
            if matches:
                for match in matches:
                    latex_doc.append("\\begin{figure}[H]")
                    latex_doc.append("\\centering")
                    latex_doc.append(f"\\includegraphics[width=0.8\\textwidth]{{{match}}}")
                    latex_doc.append("\\end{figure}")
                    latex_doc.append("\n")

    latex_doc.append("\\end{document}")

    with open('informe_proyecto.tex', 'w', encoding='utf-8') as f:
        f.write("\n".join(latex_doc))
    print("informe_proyecto.tex regenerado con éxito y fórmulas corregidas.")

if __name__ == "__main__":
    main()
