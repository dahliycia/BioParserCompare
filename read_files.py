#!python

from Bio.PDB import *
from Bio.PDB import MMCIF2Dict
import time
import pdb2cif_header_reference as p2c
from texttable import *
import re


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


# def get_ref_val_from_cif(structure_dict_cif):
    # cif_ref_values = {}
    # for pdb_key, key in p2c.PDB2CIF_HEADER.items():
    #     if type(key) == type(str()):
    #         cif_ref_values[pdb_key] = get_value_from_cif(structure_dict_cif, key)
    #     elif type(key) == type(dict()):
    #         cif_ref_values[pdb_key] = {}
    #         for pdb_k, k in key.items():
    #             if type(k) == type(dict()):
    #                 cif_ref_values[pdb_key][pdb_k] = {}
    #                 for pdb_kk, kk in k.items():
    #                     cif_ref_values[pdb_key][pdb_k][pdb_kk] = get_value_from_cif(structure_dict_cif, kk)
    #             else:
    #                 cif_ref_values[pdb_key][pdb_k] = get_value_from_cif(structure_dict_cif, k)
    #
    #     elif type(key) == type(list()):
    #         cif_ref_values[pdb_key] = []
    #         for i in key:
    #             temp = get_value_from_cif(structure_dict_cif, i)
    #             cif_ref_values[pdb_key].append(temp)
    # # print cif_ref_values
    # return cif_ref_values


def get_value_from_cif(cif, cif_key):
    if cif_key:
        if type(cif_key) == type(list()):
            cif_value = []
            for key in cif_key:
                cif_value.append(cif[key])
            cif_value = str(cif_value)
            cif_key = str(cif_key)
        else:
            cif_value = cif[cif_key]
        return cif_key, cif_value
    else:
        return 'NOT FOUND', 'NOT FOUND'


def create_report(structure_pdb, structure_cif, report_file):
    table = Texttable()
    table.set_cols_align(["l", "l", "l"])
    table.set_cols_width([30, 40, 40])
    table.add_row(['PDB item name\n[CIF item name]', 'PDB item value', 'CIF item value'])
    pdb = structure_pdb.header
    cif = structure_cif
    pdb2cif = p2c.PDB2CIF_HEADER
    not_found = {}

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
                            else:
                                if pdb_key not in pdb2cif or pdb_k not in pdb[pdb_key] or pdb_kk not in pdb[pdb_key][pdb_k]:
                                    not_found[pdb_key+':'+pdb_k+':'+pdb_kk] = pdb_vv
                                    continue
                                cif_key = pdb2cif[pdb_key][pdb_k][pdb_kk]
                                cif_key, cif_value = get_value_from_cif(cif, cif_key)
                            name_col = pdb_key + ':' + pdb_k + ':' + pdb_kk + '\n[CIF: ' + cif_key + ']'
                            table.add_row([name_col, pdb_vv, cif_value])

                elif type(pdb_v) == type(str()):
                    cif_key = pdb2cif[pdb_key][pdb_k]
                    cif_key, cif_value = get_value_from_cif(cif, cif_key)
                    name_col = pdb_key + ':' + pdb_k + '\n[CIF: ' + cif_key + ']'
                    table.add_row([name_col, pdb_v, cif_value])
    #
    # for pdb_key, cif_key in p2c.PDB2CIF_HEADER.items():
    #     if type(cif_key) == type(str()):
    #         name_col = pdb_key + '\n[CIF: ' + cif_key + ']'
    #         table.add_row([name_col, pdb[pdb_key], cif[pdb_key]])
    #     elif type(cif_key) == type(list()):
    #         print 'LIST ' + pdb_key
    #         cif_key = str(cif_key)
    #         cif_value = str(cif[pdb_key])
    #         name_col = pdb_key + '\n[CIF: ' + cif_key + ']'
    #         table.add_row([name_col, pdb[pdb_key], cif_value])
    #     elif type(cif_key) == type(dict()):
    #         print 'DICT ' + pdb_key
    #         for pdb_k, cif_k in cif_key.items():
    #             if type(cif_k) == type(str()):
    #                 cif_value = cif[pdb_key][pdb_k]
    #                 pdb_value = pdb[pdb_key][pdb_k]
    #                 name_col = pdb_key + ': ' + pdb_k + '\n[CIF: ' + cif_k + ']'
    #                 table.add_row([name_col, pdb_value, cif_value])
    #             elif type(cif_k) == type(dict()):
    #                 for pdb_kk, cif_kk in cif_k.items():
    #                     cif_value = cif[pdb_key][pdb_k][pdb_kk]
    #                     pdb_value = pdb[pdb_key][pdb_k][pdb_kk]
    #                     name_col = pdb_key + ': ' + pdb_k + ': '+ pdb_kk + '\n[CIF: ' + cif_k + ']'
    #                     table.add_row([name_col, pdb_value, cif_value])

    report_file.write(table.draw())
    if not_found:
        report_file.write('\n\nNOT MAPPED:')
        for name, value in not_found.items():
            report_file.write('\nPDB key: ' + str(name) + ', PDB value: ' + str(value))


def analize_structure(file_name):
    report_file = open('report_' + file_name + '.txt', 'w')
    [structure_cif, structure_dict_cif, dt_cif] = read_mmmcif_file(file_name)
    [structure_pdb, dt_pdb] = read_pdb_file(file_name)
    report_file.write('PDB Parser time: ' + str(dt_pdb) + '\n')
    report_file.write('MMCIF Parser time: ' + str(dt_cif) + '\n\n')
    create_report(structure_pdb, structure_dict_cif, report_file)


def main():
    analize_structure('3wgx')


if __name__ == '__main__':
    main()
