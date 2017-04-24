#!/usr/bin/python
# -*- coding: utf-8 -*-

from re import search
import sys, getopt


def write_out(text: str, prefix: str, fout) -> None:
    if search('^\s*$', text) is not None:
        fout.write('\n')
    elif text[0] == '#':
        fout.write(prefix + text)
    elif prefix == '':
        fout.write(text)
    else:
        fout.write(prefix + ' ' + text)


def write_lines_out(text: str, fout) -> None:
    cont = 0
    mystring = ''

    for mychar in list(text):
        mystring += mychar
        cont += 1

        if cont > 80 and mychar == ' ':
            write_out(mystring + '\n', '#', fout)
            cont = 0
            mystring = ''

    write_out(mystring, '#', fout)


def change_status(linea: str, estado: str) -> str:
    prefix = linea[0:3]
    
    if estado in ['formula', 'block'] and prefix == '```':
        return ('formula_end')

    if estado in ['head_end', 'formula_end', 'block_end']:
        return('text')

    if estado == 'formula_start':
        return('formula')
        
    if estado == 'block_start':
        return('block')

    if estado in ['head_start', 'author', 'date']:
        estado = 'head'

    if estado == 'head':
        if prefix == 'dat':
            return ('date')
        elif prefix == 'aut':
            return ('author')
        elif prefix == '---':
            return ('head_end')

    if estado == 'text':
        if prefix == '---':
            return ('head_start')
        elif linea[0:5] == '```{r':
            return ('formula_start')
        elif linea[0:6] == '```{bl':
            return ('block_start')

    return (estado)

def main(argv):

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('Rmd2R.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Rmd2R.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            fin_name = arg
        elif opt in ("-o", "--ofile"):
            fout_name = arg

    fin = open(fin_name, 'r')
    fout = open(fout_name, 'w')
    lineas = fin.readlines()
    estado = 'text'

    for linea in lineas:
        estado = change_status(linea, estado)

        if estado in ['author', 'date']:
            write_out(linea, '##', fout)

        elif estado == 'formula':
            write_out(linea, '', fout)

        elif estado == 'block':
            write_lines_out(linea, fout)
            
        elif estado == 'formula_end':
            write_out('\n', '', fout)
            
        elif estado == 'text' and linea[0] == '#':
            write_out('#----------------------------------------\n', '', fout)
            write_out(linea, '', fout)
            write_out('#----------------------------------------\n\n', '', fout)

    fin.close()
    fout.close()

if __name__ == "__main__":
   main(sys.argv[1:])
