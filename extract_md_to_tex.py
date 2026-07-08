import json
import re

def main():
    with open('main.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'markdown':
            print("".join(cell.get('source', [])))
            print("---CELL_SEPARATOR---")
        elif cell['cell_type'] == 'code':
            source = "".join(cell.get('source', []))
            matches = re.findall(r'savefig\([\'"](plots/[^\'"]+\.png)[\'"]', source)
            if matches:
                for match in matches:
                    print(f"[IMAGE: {match}]")
                    print("---CELL_SEPARATOR---")

if __name__ == "__main__":
    main()
