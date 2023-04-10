import os
import argparse
import fileinput
import sys

def replacement(file, previousw, nextw):
    for line in fileinput.input(file, inplace=1):
        line = line.replace(previousw, nextw)
        sys.stdout.write(line)

def main(file):
    if os.path.exists(file.input):
        previousw = file.original
        nextw = file.new
        var1 = previousw
        var2 = nextw
        file = file.input
        try:
            replacement(file, var1, var2)
            print(str(file)+": "+str(var1)+" ➡️ "+str(var2))
        except:
            print("replacement wrong, check input and original words!")

    else:
        print("input invalid, check file input")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="check cif lattice, if not reach value, supercell it until to get it")
    parser.add_argument("-input", help="File path")
    parser.add_argument("-original", help="Original Words Shows in pdb")
    parser.add_argument("-new", help="Replacement Shows in pdb")
    file = parser.parse_args()
    main(file)
