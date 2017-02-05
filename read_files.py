#!python

from Bio.PDB import *
from Bio.PDB import MMCIF2Dict
import time
import pdb2cif_header_reference as p2c
from texttable import *
import re


# Reads PDB file, returns structure returned by PDBParser and parsing time
def read_pdb_file(file_name):
    parser = PDBParser(QUIET=True)
    file_dir = 'data/' + file_name + '.pdb'
    start = time.time()
    structure = parser.get_structure(file_name, file_dir)
    end = time.time()
    dt = end-start
    return structure, dt


# Reads mmcif file, returns structure returned by MMCIFParser, dict returned by MMCIFDict and parsing time of both
def read_mmmcif_file(file_name):
    parser = MMCIFParser(QUIET=True)
    file_dir = 'data/' + file_name + '.cif'
    start = time.time()
    structure = parser.get_structure(file_name, file_dir)
    structure_dict = MMCIF2Dict.MMCIF2Dict(file_dir)
    end = time.time()
    dt = end - start
    return structure, structure_dict, dt


# Given a key of cif dictionary, returns strings of key and value
def get_value_from_cif(cif, cif_key):
    try:
        if type(cif_key) == type(list()):
            cif_value = []
            for key in cif_key:
                cif_value.append(cif[key])
            cif_value = str(cif_value)
            cif_key = str(cif_key)
        else:
            cif_value = cif[cif_key]
        return cif_key, cif_value
    except:
        return 'NOT FOUND', 'NOT FOUND'


# goes through all pdb header fields and tries to find corresponding cif dictionary structure fields
# returns 'not_found' dictionary of not found and not mapped values, and 'not_found_mapped' dictionary
# of values mapped as 'None'
def create_report(structure_pdb, structure_cif, report_file):
    table = Texttable()
    table.set_cols_align(["l", "l", "l"])
    table.set_cols_width([30, 40, 40])
    table.add_row(['PDB item name\n[CIF item name]', 'PDB item value', 'CIF item value'])
    pdb = structure_pdb.header
    cif = structure_cif
    pdb2cif = p2c.PDB2CIF_HEADER
    not_found = {}
    not_found_mapped = {}

    for pdb_key, pdb_value in pdb.items():
        if type(pdb_value) == type(str()):
            if pdb_key not in pdb2cif:
                not_found[pdb_key] = pdb_value
                continue
            cif_key = pdb2cif[pdb_key]
            cif_key, cif_value = get_value_from_cif(cif, cif_key)
            name_col = pdb_key + '\n[CIF: ' + cif_key + ']'
            table.add_row([name_col, pdb_value, cif_value])
        elif type(pdb_value) == type(list()):
            if pdb_key not in pdb2cif:
                not_found[pdb_key] = pdb_value
                continue
            cif_key = pdb2cif[pdb_key]
            cif_key, cif_value = get_value_from_cif(cif, cif_key)
            pdb_value = str(pdb_value)
            name_col = pdb_key + '\n[CIF: ' + cif_key + ']'
            table.add_row([name_col, pdb_value, cif_value])
        elif type(pdb_value) == type(dict()):
            for pdb_k, pdb_v in pdb_value.items():
                if type(pdb_v) == type(dict()):
                    for pdb_kk, pdb_vv in pdb_v.items():
                        if type(pdb_vv) == type(str()):
                            if re.match(r"\d+", pdb_k) and pdb_key == 'compound':
                                if pdb_key not in pdb2cif or pdb_kk not in pdb[pdb_key]:
                                    not_found[pdb_key+':'+pdb_k+':'+pdb_kk] = pdb_vv
                                    continue
                                cif_key = pdb2cif[pdb_key][pdb_kk]
                                if cif_key:
                                    if type(cif_key) == type(list()):
                                        cif_value = cif[cif_key][pdb_k]
                                        cif_value = str(cif_value)
                                        cif_key = str(cif_key) + pdb_k
                                    else:
                                        cif_value = cif[cif_key]
                                else:
                                    cif_key = 'NOT FOUND'
                                    cif_value = 'NOT FOUND'
                                    not_found_mapped[pdb_key+':'+pdb_k+':'+pdb_kk] = pdb_vv
                            else:
                                if pdb_key not in pdb2cif or pdb_k not in pdb[pdb_key] or pdb_kk not in pdb[pdb_key][pdb_k]:
                                    not_found[pdb_key+':'+pdb_k+':'+pdb_kk] = pdb_vv
                                    continue
                                try:
                                    cif_key = pdb2cif[pdb_key][pdb_k][pdb_kk]
                                except:
                                    continue
                                cif_key, cif_value = get_value_from_cif(cif, cif_key)
                            name_col = pdb_key + ':' + pdb_k + ':' + pdb_kk + '\n[CIF: ' + cif_key + ']'
                            table.add_row([name_col, pdb_vv, cif_value])

                elif type(pdb_v) == type(str()):
                    cif_key = pdb2cif[pdb_key][pdb_k]
                    cif_key, cif_value = get_value_from_cif(cif, cif_key)
                    name_col = pdb_key + ':' + pdb_k + '\n[CIF: ' + cif_key + ']'
                    table.add_row([name_col, pdb_v, cif_value])

    report_file.write(table.draw())
    if not_found:
        report_file.write('\n\nNOT MAPPED:')
        for name, value in not_found.items():
            report_file.write('\nPDB key: ' + str(name) + ', PDB value: ' + str(value))
    return not_found, not_found_mapped


# Analizes a single structure of a given name and creates a report in reports/ directory
def analize_structure(file_name):
    report_file = open('reports/report_' + file_name + '.txt', 'w')
    [structure_cif, structure_dict_cif, dt_cif] = read_mmmcif_file(file_name)
    [structure_pdb, dt_pdb] = read_pdb_file(file_name)
    report_file.write('PDB Parser time: ' + str(dt_pdb) + '\n')
    report_file.write('MMCIF Parser time: ' + str(dt_cif) + '\n\n')
    not_mapped, not_found = create_report(structure_pdb, structure_dict_cif, report_file)
    for name, value in not_found.items():
        not_mapped[name] = value
    return dt_pdb, dt_cif, not_mapped


# Writes the main report, containing average parsing times and fields that were not mapped successfully
def write_general_report(pdb_times, cif_times, missed_values):
    report_file = open('REPORT.txt', 'w')
    report_file.write('This is a general report of PDB and mmCif parser comparison in BioPython\n\n')
    pdb_av = sum(pdb_times) / float(len(pdb_times))
    cif_av = sum(cif_times) / float(len(cif_times))
    report_file.write('Average PDB parsing time: ' + str(pdb_av) + '\n')
    report_file.write('Average mmCif parsing time: ' + str(cif_av) + '\n')
    report_file.write('Positions missing/not mapped, that were found in the test files: \n')
    for name, value in missed_values.items():
        report_file.write(name + '\n')
    report_file.close()


# The main function goes through all the structures listed in test_structures.txt file.
# For each structure it runs the analize_structure() function, which produces the report_structname.txt file
# It creates the main REPORT.txt file, containing average parsing times and fields that could not be found
# in the Cif structure (mainly because they are not mapped)
def main():
    str_list_file = open('test_structures.txt', 'r')
    str_list = str_list_file.readlines()
    missed_values = {}
    pdb_times = []
    cif_times = []
    for line in str_list:
        dt_pdb, dt_cif, missed = analize_structure(line[0:4])
        if missed:
            missed_values.update(missed)
        pdb_times.append(dt_pdb)
        cif_times.append(dt_cif)
    write_general_report(pdb_times, cif_times, missed_values)


if __name__ == '__main__':
    main()
