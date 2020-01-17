#!/usr/bin/env python3 
from nltk.tokenize import RegexpTokenizer
import fileinput
import argparse
import os

def westToEastConversion(filename, terminalArgs):
    expr_to_find = RegexpTokenizer("const +[^*&]+\s*[*&]+")
    if(terminalArgs.convert):
        backup_file = filename + ".bak"
        backup = open(backup_file, "w")       
    with open(filename, "r") as f:
        file = f.readlines()
    line_count = 0
    changes_done = 0
    try:
        for line in file:
            if(terminalArgs.convert):
                backup.write(line)
            line_count += 1
            match = expr_to_find.tokenize(line)
            if (match):
                sep_match = match[0].split()
                type_name = sep_match[0]                
                if(len(sep_match) == 3):
                    ref_or_pointer = sep_match[2] + " "
                    qualifier = sep_match[1]
                else:
                    qualifier = sep_match[1][:-1]
                    ref_or_pointer = sep_match[1][-1]
                new_expr = qualifier + " " + type_name + ref_or_pointer
                if(terminalArgs.print):
                    print("Change at line " + str(line_count) + ": " + line + "--> " + line.replace(match[0], new_expr))
                elif(terminalArgs.convert):
                    line = line.replace(match[0], new_expr)  
                    file[line_count-1] = line                  
                changes_done += 1                
        if(terminalArgs.convert):
            with open(filename, "w") as f:
                f.writelines(file)
            backup.close()
            print(str(changes_done) + " conversions done!")
            if(terminalArgs.nobackup):
                os.remove(backup_file)
            else:
                print("Backup made as " + backup_file) #.bak extension
            
        elif(terminalArgs.print):
            print("---- " + str(changes_done) + " possible conversions to do. ----")
    except FileNotFoundError:
        print("Error: No such file exists (" + filename + ")")



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File to be edited.")
    parser.add_argument("-print", help="Prints out the conversion, if any.",
                        action="store_true")
    parser.add_argument("-convert", help="Executes and saves the conversion to the file.",
                        action="store_true")
    parser.add_argument("-reverse", help="\033[93mDO NOT USE, NOT FULLY IMPLEMENTED\033[0m Reverses the process, copying the .bak file to the original.",
                        action="store_true")
    parser.add_argument("-nobackup", help="Turns off the backup option, making no backup of edited file.",
                        action="store_true", default=False)

    args = parser.parse_args()

    if(args.reverse):
        os.rename(args.filename + ".bak", args.filename)
        return
    westToEastConversion(args.filename, args)

if __name__ == "__main__":
    main()
    
