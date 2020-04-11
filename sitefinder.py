#!/usr/bin/env python
from __future__ import print_function
from pyrosetta import *
import argparse, sys, os
from math import sqrt
from pyrosetta.rosetta.core.pose import Pose
from pyrosetta.toolbox import cleanATOM


def get_bond_length(fa, sa):
    fa_x, fa_y, fa_z = fa
    sa_x, sa_y, sa_z = sa
    dx, dy, dz = (fa_x - sa_x) ** 2, (fa_y - sa_y) ** 2, (fa_z - sa_z) ** 2
    return sqrt(dx + dy + dz)


class SiteFinder(object):
    def __init__(self):
        self.p = argparse.ArgumentParser(
            description="Site Finder, It is a tool to extract protein fragment which essentially contributes to the "
                        "binding between two protein complexes")
        self.args = None
        self.pose = None
        self.info = None
        self.ligand = []
        self.protein = []
        self.fragment = []

    def parse(self):
        self.p.add_argument("-l", "--ligand", help="The chain identifier of the protein ligand")
        self.p.add_argument("-p", "--protein", help="The chain identifier of the interacting protein")
        self.p.add_argument("-c", "--pdb", help="Protein-Protein(ligand) complex PDB file location")
        self.p.add_argument("-g", "--getprotein", const=True, nargs="?", default=True,
                            help="Return The binding fragment from the interacting protein not from the ligand. "
                                 "Defaults: True, Otherwise, it returns the "
                                 " fragment from the ligand not from the interacting protein.")
        self.p.add_argument("-d", "--distance", default=5, type=int,
                            help="Inclusive Cutoff distance to use in order to "
                                 "consider the presence of noncovalent bonding. "
                                 "Defaults: 5 Angstroms")
        # self.p.add_argument("-t", "--temperature", default=25, type=int,
        #                     help="Temperature in Celesius to use in order to "
        #                          "calculate the cutoff kinetic energy. "
        #                          "Defaults: 25C room temperature.")
        self.p.add_argument("-o", "--output", default=None,
                            help="Output directory at which to store the FastQ file containing the "
                                 "protein fragment.")
        self.args = self.p.parse_args()
        if len(sys.argv) <= 1:
            self.p.print_help()
            return

        self.extract()

    def has_noncovalent_bonding(self, first, second):
        first_atoms = [i for i in range(1, len(first.atoms())) if not first.atom_is_backbone(i)]
        second_atoms = [j for j in range(1, len(second.atoms())) if not second.atom_is_backbone(j)]
        result = False
        for i in first_atoms:
            first_atom_type = first.atom_type(i)
            for j in second_atoms:
                second_atom_type = second.atom_type(j)
                first_condition = any([(first_atom_type.is_acceptor() and second_atom_type.is_donor()),
                                       (first_atom_type.is_donor() and second_atom_type.is_acceptor()),
                                       (first_atom_type.is_hydrogen() and second_atom_type.is_acceptor()),
                                       (first_atom_type.is_acceptor() and second_atom_type.is_hydrogen())])
                second_condition = get_bond_length(first.atom(i).xyz(), second.atom(j).xyz()) <= int(self.args.distance)
                if first_condition and second_condition:
                    result = True

        return result

    def print_fragment(self):
        if self.fragment is not None:
            if len(self.fragment) <= 0:
                print("No Binding Fragment found.")
            else:
                seq = ""
                for item in self.fragment:
                    if isinstance(item, str):
                        seq += item
                    else:
                        seq += item.annotated_name()
                stdout = sys.stdout if self.args.output is None else open(os.path.join(self.args.output,"ligand.fa"), 'w')
                print(">SEQUENCE;{0}\r".format(self.info.name()), file=stdout)
                print(self.pose.sequence() + "\r", file=stdout)
                print(">FRAGMENT;{0}\n".format("PROTEIN" if self.args.getprotein else "LIGAND"), file=stdout)
                print(seq, file=stdout)

    def extract(self):
        print("Starting Rosetta environment. Please wait....")
        init()
        if self.args.pdb is None or len(self.args.pdb) <= 0:
            self.p.print_help()
            return
        print("Cleaning PDB. Please Wait...")
        filename, _ = os.path.splitext(os.path.basename(self.args.pdb))
        cleanATOM(self.args.pdb)
        print("Loading cleaned PDB file. Please wait....")
        self.pose = pose_from_pdb("{0}.clean.pdb".format(filename))
        if not isinstance(self.pose, Pose):
            print("PDB file doesn't contain a valid pose object.")
            self.p.print_help()
            return
        self.info = self.pose.pdb_info()
        print("Building ligand and the interacting protein.")
        for resId in range(1, self.pose.total_residue() + 1):
            res = self.pose.residue(resId)
            chainid = self.info.chain(resId)
            if str(chainid) == self.args.ligand:
                self.ligand.append((resId, res))
            elif str(chainid) == self.args.protein:
                self.protein.append((resId, res))
        print("Building Fragment. Please Wait....")
        self.fragment = ["-" for i in range(self.pose.total_residue())]
        for i in range(0, len(self.protein)):
            fr_pos, first_residue = self.protein[i]
            for j in range(0, len(self.ligand)):
                sec_pos, second_residue = self.ligand[j]
                if self.has_noncovalent_bonding(first_residue, second_residue):
                    if self.args.getprotein:
                        self.fragment[fr_pos] = first_residue
                    else:
                        self.fragment[sec_pos] = second_residue
        self.print_fragment()


if __name__ == '__main__':
    finder = SiteFinder()
    finder.parse()