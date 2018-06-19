"""add missing id column between MANU_STATE and Revision Number (3rd last field)"""

import re


def find_all(line, sub_str):
    return [m.start() for m in re.finditer(sub_str, line)]


def has_few_columns(line):
    return len(find_all(line, '¬')) < 13


def add_id_column(line):
    index = find_all(line, '¬')
    replace = '¬'
    return line[:index[10]] + replace + line[index[10]:]


def correct_export(filename):
    with open(filename, "r+") as f:
        lines = f.readlines()
        if has_few_columns(lines[0]):
            output = ''
            for line in lines:
                output += add_id_column(line)

            f.seek(0)
            f.write(output)
            f.truncate()


if __name__ == '__main__':
    correct_export("C:/cooptemp2/teamworks.txt")
