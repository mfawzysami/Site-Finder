#!/usr/bin/python
from __future__ import print_function
from argparse import ArgumentParser
import sys , os

def main():
    p = ArgumentParser()
    p.add_argument("-p","--positionFile",help="Position File to load")
    p.add_argument("-g","--mutagen",default="a",type=str,help="Mutating all residues in the above mentioned position file to this Amino acids group.")
    args = p.parse_args()
    if len(sys.argv) <= 1:
        p.print_help()
        return

    with open(args.positionFile,'r') as reader:
        contents = reader.readlines()
        contents = contents[1:]
        mutagens = []
        for line in contents:
            res,location,chain,chain_pos = line.replace('\r','').replace('\n','').split('\t')
            mutation = "{0}{1}{2}{3}".format(res,chain,chain_pos,args.mutagen)
            mutagens.append(mutation)
        print(",".join(mutagens))



if __name__ == '__main__':
    main()