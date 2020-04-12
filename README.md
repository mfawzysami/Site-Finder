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

```
Let's take an example, `6lzg.pdb` file, this file contains SARS-COV 2 RBD of Spike S protein in complex with ACE2 (Angiotensen converting Enzyme 2).

We knew that RBD (Receptor Binding Domain) of SARS-COV2 is in Chain `B` while ACE2 of human epithelia is represented in chain `A`

- If you want to extract the binding site in RBD, then, we put `--protein B` and `--ligand A`

- `--getligand` will output the binding fragment in the ligand not in the protein. By default, it outputs the binding fragment in protein.

- By default, the script calculates all atoms in both chains which probably can share any electrostatic interaction between each others with a cutoff distance specified by `--distance` which defaults to 5 Angstroms by default, if you want to specify other value like 3A, you can do this `--distance 3`

- You can output the binding fragment in aligned multiple fasta format, which you can display at any genome editor/viewer by specifying `--output`, the default is the standard output if not specified.

- You don't have to clean the PDB from any solvents as the script is going to do this anyway.

- The script also outputs a positions.tsv file which contain the relative locations and chain identifiers for each residue in the binding fragment

#### Ex.

`python sitefinder.py --ligand B --protein A --pdb 6lzg.pdb --output /where/you/want/to/save/`



### Improvements

- I will improve the script later, to work on HPC and multicore environments.
- I will introduce Coulomb electrostatic calculations taking into account different dielectric constants of biological environments as the electrostatic forces depends on the nature of the environment.



 
