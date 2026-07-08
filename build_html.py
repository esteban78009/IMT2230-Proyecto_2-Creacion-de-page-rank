import json
import re
import subprocess

def main():
    with open('main.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)

    new_cells = []
    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            new_cells.append(cell)
        elif cell['cell_type'] == 'code':
            source = "".join(cell.get('source', []))
            matches = re.findall(r'savefig\([\'"](plots/[^\'"]+\.png)[\'"]', source)
            if matches:
                for match in matches:
                    md_cell = {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [f"<img src='{match}' width='80%'>\n"]
                    }
                    new_cells.append(md_cell)

    nb['cells'] = new_cells

    with open('temp_md_only.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

    print("Ejecutando nbconvert...")
    subprocess.run(['python', '-m', 'jupyter', 'nbconvert', '--to', 'html', 'temp_md_only.ipynb', '--output', 'informe_final.html'])
    print("informe_final.html generado.")

if __name__ == "__main__":
    main()
