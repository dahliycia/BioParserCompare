# BioParserCompare
Comparison of molecular structures parsers (PDB, mmCif) available in biopython


# What you need
Python 2.7 or 3, BioPython, texttable and PDB and mmCif files for your structure(s).

# What it does

BioParserCompare compares PDB.PDBParser and PDB.MMCIFDict modules output (header info)
It creates a report for single structures, and if run in test mode, a general report of average times and missing values.
You can use it to quickly find placement of some data in the structures returned by PDBParser and MMCIFDict.
You can also use it to see human-friendly form of data from your structure files.

- Why not PDB.MMCIFParser()?
PDB.MMCIFParser does not support the header info. In general, it does not contain many info, and it is advised to used PDB.MMCIFDict instead.
You can still use read_files.read_mmmcif_file(file_name) to get the MMCIFParser result :)

- What is in the report file for a single structure?
PDB parsing time, mmCif parsing time (MMCIFParser + MMCIFDict)
Table comapring the values available in both structures
List of fields from PDB header not found in Cif (mostly not mapped)

- What is in the main report file?
Average PDB parsing time, average mmCif parsing time (MMCIFParser + MMCIFDict)
List of fields not found for any of the structures

- Why is not everything mapped?
Some fields that have non-deterministic values were hard to map, and some are not mapped yet. You can always contribute by adding your mappings to the pdb2cif_header_reference.py file!

- How to download files? Why it does not download PDB and mmCif files instead?
You can download both mmcif and PDB files at:
http://www.rcsb.org/pdb/home/home.do#Subcategory-download_structures

I did not yet found a solution to download mmCif automatically.
You can download PDB files in your code using:
```
pdbl = PDBList()
pdbl.retrieve_pdb_file('1FAT')
```
Find more at: http://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ


# Usage

Download this repo and install BioPython and texttable :)

- For single structure

Import the BioParserCompare read_files.py and analyse a single structure:
You must add your structure PDB and mmCif files to 'data/' directory!
```
import read_files as bpc
my_struct = 'abcd'
bcp.analize_structure(my_struct)
```
It will produce the report for a single structure under 'reports/'

- For many structures
You must add your structure PDB and mmCif files to 'data/' directory!
List your structures names in the `test_structures.txt` file (some are there already, just remove if not needed). Then run `read_files.py`. It will create a report for every structure in 'reports/' and a main report in the main BioParserCompare directory.

- For testing parsers
Run `pick_structures.py`, it will pick a few structures from the 'author.idx' file. Then tun `read_files.py`, it will create a report for every structure in 'reports/' and a main report in the main BioParserCompare directory. All needed files are in the repo.
You can edit the picking algorythm if you want. You must add any new PDB and mmCif files to 'data/' directory!

- For getting PDBParser or MMCIFParser/MMCIFDict structures
You must add your structure PDB and mmCif files to 'data/' directory!
```
import read_files as bpc
my_struct = 'abcd'
pdb_struct, pdb_parsing_time = bpc.read_pdb_file(my_struct)
cif_struct, cif_dict, cif_parsing_time = bpc.read_mmmcif_file(my_struct)
```
