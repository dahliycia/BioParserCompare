#!python

from Bio.PDB import *
from Bio.PDB import MMCIF2Dict
import time
import pdb2cif_header_reference as p2c

def read_pdb_file(file_name):
  parser = PDBParser(QUIET=True)
  file_dir = 'data/' + file_name + '.pdb'
  start = time.time()
  structure = parser.get_structure(file_name, file_dir)
  end = time.time()
  dt = end-start
  return structure, dt


def read_mmmcif_file(file_name):
  parser = MMCIFParser(QUIET=True)
  file_dir = 'data/' + file_name + '.cif'
  start = time.time()
  structure = parser.get_structure(file_name, file_dir)
  end = time.time()
  dt = end-start
  structure_dict = MMCIF2Dict.MMCIF2Dict(file_dir)
  return structure, structure_dict, dt
  
def get_pdb_file(file_name):
  pdb1 = PDBList()
  
def get_header(structure, report_file):

  for name, value in structure.header.items():
    report_file.write('  - ' + name + '\n    ' + str(value) + '\n\n')
  
def get_ref_val_from_cif(structure_dict_cif):
  for pdb_key, key in p2c.PDB2CIF_HEADER.items():
    if type(key) == type(str()):
      get_value_from_cif(structure_dict_cif, key)
    elif type(key) == type(dict()):
      for pdb_k, k in key.items():
        if type(k) == type(dict()):
          for pdb_kk, kk in k.items():
            get_value_from_cif(structure_dict_cif, kk)
        else:
          get_value_from_cif(structure_dict_cif, k)
        
    elif type(key) == type(list()):
      for i in key:
        get_value_from_cif(structure_dict_cif, i)
  
def get_value_from_cif(structure_dict_cif, key):
  if key:
    print structure_dict_cif[key]
  
  
def main ():

  file_name = '3wgx'
  report_file = open('report_' + file_name + '.txt', 'w')
  [structure_cif, structure_dict_cif, dt_cif] = read_mmmcif_file(file_name)
  [structure_pdb, dt_pdb] = read_pdb_file(file_name)
  report_file.write('PDB Parser time: ' + str(dt_pdb) + '\n')
  report_file.write('MMCIF Parser time: ' + str(dt_cif) + '\n\n')
  report_file.write('PDB HEADER:\n')
  get_header(structure_pdb, report_file)
  report_file.write('CIF HEADER:\n')
  for name, value in structure_dict_cif.items():
    report_file.write('  - ' + name + '\n    ' + str(value) + '\n\n')

  get_ref_val_from_cif(structure_dict_cif)

if __name__ == '__main__':
    main()    