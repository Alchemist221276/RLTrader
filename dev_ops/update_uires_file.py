import sys
import argparse
import os


def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('in_filename', nargs='?')
    parser.add_argument('res_filename', nargs='?')
    parser.add_argument('out_filename', nargs='?')

    return parser


def process_res_filename(res_filename_full):
    res_filename_path = os.path.dirname(res_filename_full)
    res_filename = os.path.basename(res_filename_full).split('.')[0]
    result = ""
    for symbol_index in range(len(res_filename_path)):
        symbol = res_filename_path[symbol_index]
        if symbol == "\\" or symbol == "/":
            if len(result) > 0:
                result += "."
        else:
            if symbol != ".":
                result += symbol
    return res_filename + "_rc", result + "." + res_filename


def main():
    argparser = create_argparser()
    arguments = argparser.parse_args()

    #++DEBUG
    #print("arguments.in_filename: {}".format(arguments.in_filename))
    #print("arguments.res_filename: {}".format(arguments.res_filename))
    #print("arguments.out_filename: {}".format(arguments.out_filename))
    #--DEBUG

    in_filename_full = arguments.in_filename
    res_filename_full = arguments.res_filename
    out_filename_full = arguments.out_filename

    if in_filename_full is None and res_filename_full is None:
        print("Syntax: update_uires_filename <in_filename> <res_filename> [out_filename]")
        return -1

    errors = False
    if in_filename_full is None:
        print("in_filename parameter is not specified")
        errors = True
    if not os.path.isfile(in_filename_full):
        print("Can't find file '{}'".format(in_filename_full))
        errors = True

    if res_filename_full is None:
        print("res_filename parameter is not specified")
        errors = True
    if not os.path.isfile(in_filename_full):
        print("Can't find file '{}'".format(res_filename_full))
        errors = True

    if out_filename_full is None:
        out_filename_full = in_filename_full
    if not os.path.isfile(in_filename_full):
        print("Can't find file '{}'".format(out_filename_full))
        errors = True

    if errors:
        return -2

    source_res_filename, corrected_res_filename = process_res_filename(res_filename_full)
    source_res_line = "import {}\n".format(source_res_filename)
    corrected_res_line = "import {}\n".format(corrected_res_filename)
    #++DEBUG
    #print("source_res_line: {}".format(source_res_line))
    #print("corrected_res_line: {}".format(corrected_res_line))
    #--DEBUG

    in_file = open(in_filename_full, mode="r")
    in_file_lines = in_file.readlines()
    in_file.close()

    #++DEBUG
    #for in_file_line in in_file_lines:
    #    sys.stdout.write(in_file_line)
    #--DEBUG

    updated = False
    out_file_lines = []
    for in_file_line in in_file_lines:
        if in_file_line == source_res_line:
            out_file_lines.append(corrected_res_line)
            updated = True
        else:
            out_file_lines.append(in_file_line)

    if updated:
        out_file = open(out_filename_full, mode="w")
        out_file.writelines(out_file_lines)
        print("update_uires_file: '{}' successfully updated".format(out_filename_full))
    else:
        print("update_uires_file: '{}' not updated: source line not found".format(out_filename_full))


if __name__ == "__main__":
    main()
