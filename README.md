## Site Finder

### Introduction

This script will take a protein-protein complex as PDB file and outputs a multi-fasta aligned file containing the possible binding site between these two protein residues

This is the very first step in any protein engineering tasks, is to find the site of possible binding that forms any electrostatic noncovalent interaction.

## How to Install

- Install dependencies
- This script requires pyrosetta only as python dependency.
- You have to install pyrosetta in your python environment.

## How to Use

- You can issue the following command : `python sitefinder.py --help`

#### Output

```text
usage: sitefinder.py [-h] [-l LIGAND] [-p PROTEIN] [-c PDB] [-g [GETPROTEIN]]
                     [-d DISTANCE] [-o OUTPUT]

Site Finder, It is a tool to extract protein fragment which essentially
contributes to the binding between two protein complexes

optional arguments:
  -h, --help            show this help message and exit
  -l LIGAND, --ligand LIGAND
                        The chain identifier of the protein ligand
  -p PROTEIN, --protein PROTEIN
                        The chain identifier of the interacting protein
  -c PDB, --pdb PDB     Protein-Protein(ligand) complex PDB file location
  -g [GETPROTEIN], --getprotein [GETPROTEIN]
                        Return The binding fragment from the interacting
                        protein not from the ligand. Defaults: True,
                        Otherwise, it returns the fragment from the ligand not
                        from the interacting protein.
  -d DISTANCE, --distance DISTANCE
                        Inclusive Cutoff distance to use in order to consider
                        the presence of noncovalent bonding. Defaults: 5
                        Angstroms
  -o OUTPUT, --output OUTPUT
                        Output directory at which to store the FastQ file
                        containing the protein fragment.


```
Let's take an example, `6lzg.pdb` file, this file contains SARS-COV 2 RBD of Spike S protein in complex with ACE2 (Angiotensen converting Enzyme 2).

We knew that RBD (Receptor Binding Domain) of SARS-COV2 is in Chain `B` while ACE2 of human epithelia is represented in chain `A`

- If you want to extract the binding site in RBD, then, we put `--protein B` and `--ligand A` whereas, if we want to get the binding site in ACE2 that binds to RBD of SARS-COV2 , we put `--protein A` and `--ligand B`.

- By default, the script calculates all atoms in both chains which probably can share any electrostatic interaction between each others with a cutoff distance specified by `--distance` which defaults to 5 Angstroms by default, if you want to specify other value like 3A, you can do this `--distance 3`

- You can output the binding fragment in aligned multiple fasta format, which you can display at any genome editor/viewer by specifying `--output`, the default is the standard output if not specified.

- You don't have to clean the PDB from any solvents as the script is going to do this anyway.

#### Ex.

`python sitefinder.py --ligand B --protein A --pdb 6lzg.pdb --output /where/you/want/to/save/yourfile.fa`



### Improvements

- I will improve the script later, to work on HPC and multicore environments.
- I will introduce Coulomb electrostatic calculations taking into account different dielectric constants of biological environments as the electrostatic forces depends on the nature of the environment.



 
