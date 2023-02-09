#/bin/python
from pathlib import Path
import re
import sys

def get_max_size_in_column(table : list[list[str]], column : int) -> int:
    max_size = 0
    for line in table:
        size = len(line[column])
        if size > max_size:
            max_size = size
    if column != 1:
        return max_size
    return max(max_size, 3)

def table_is_valid(table : list[list[str]]) -> bool:
    first_len = len(table[0])
    for l in table:
        if len(l) != first_len:
            return False
    return True

def dump_table(file, table : list[list[str]]) -> None:
    sizes = [ get_max_size_in_column(table, i) for i in range(len(table[0]))]
    first_line = True
    for line in table:
        file.write("|")
        for c in range(len(line)):
            file.write(" " + line[c] + (" " * (sizes[c] - len(line[c])) + " |"))
        file.write("\n")
        if first_line:
            file.write("|")
            for c in range(len(line)):
                if c != 1:
                    file.write(" " + ("-" * (sizes[c]) + " |"))
                else:
                    file.write(" :" + ("-" * (sizes[c] - 2) + ": |"))
            file.write("\n")

            first_line = False

def collect_table(lines: list[str], from_line : int) -> tuple[list[list[str]], int]:
    res = []
    nb_lines = len(lines)
    origin = from_line

    while from_line < nb_lines and re.match('^(\|[^|]*\|)([^|]*\|)*$', lines[from_line]):
        collumns = lines[from_line].split("|")
        collumns.pop()
        collumns.pop(0)
        for i in range(len(collumns)):
            collumns[i] = collumns[i].strip()
        res.append(collumns)
        from_line += 1
        # Skip the |---|----|-|
        if len(res) == 1:
            from_line += 1
    if not table_is_valid(res):
        return None, origin
    return res, from_line

def is_table(lines : list[str], from_line : int) -> bool:
    # If it is the last line, it cannot be a table
    if from_line + 1 >= len(lines):
        return False
    if re.match('^(\|[^|]*\|)([^|]*\|)*$', lines[from_line]) and re.match('^(\|( ?)-*( ?)\|)(( ?)(:?)-*(:?)( ?)\|)?(( ?)-+( ?)\|)*$', lines[from_line + 1]):
        return True
    return False

def format_tables_in_file(file) -> None:
    f = open(file)
    lines = f.readlines()
    f.close()
    f = open("test_out", "w")
    nb_lines = len(lines)
    i = 0
    while i < nb_lines:
        if is_table(lines, i):
            table, i = collect_table(lines, i)
            if table == None:
                f.write(lines[i])
                i += 1
            else:
                dump_table(f, table)
        else:
            f.write(lines[i])
            i += 1
    f.close()

def main(argv):
    for file in argv:
        format_tables_in_file(file)

if __name__ == "__main__":
    main(sys.argv)
