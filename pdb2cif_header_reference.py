PDB2CIF_HEADER = {
  'structure_method': '_exptl.method',
  'head': '_struct_keywords.pdbx_keywords',
  'journal': ['_citation_author.name', '_citation.title', '_citation.journal_abbrev', '_citation.journal_volume', '_citation.year', '_citation.page_first', '_citation.journal_id_ISSN', '_citation.pdbx_database_id_PubMed', '_citation.pdbx_database_id_DOI'],
  'journal_reference': ['_citation_author.name', '_citation.title', '_citation.journal_abbrev', '_citation.journal_volume', '_citation.year', '_citation.page_first', '_citation.journal_id_ISSN', '_citation.pdbx_database_id_PubMed', '_citation.pdbx_database_id_DOI'],
  'compound': {'synonym': '_entity_name_com.name', 'chain': None, 'fragment': '_entity.pdbx_fragment', 'misc': None, 'molecule': '_struct.pdbx_descriptor', 'engineered': None, 'mutation': None},
  'keywords': '_struct_keywords.text',
  'name': '_struct.title',
  'author': '_audit_author.name',
  'deposition_date': '_database_PDB_rev.date_original',
  'release_date': '_database_PDB_rev.date',
  'source': {
    '1':
      {'expression_system_vector_type': '_entity_src_gen.pdbx_host_org_vector_type', 'expression_system': '_entity_src_gen.pdbx_host_org_scientific_name', 'expression_system_taxid': '_entity_src_gen.pdbx_host_org_ncbi_taxonomy_id', 'organism_taxid': '_entity_src_gen.pdbx_gene_src_ncbi_taxonomy_id',
      'organism_scientific': '_entity_src_gen.pdbx_gene_src_scientific_name',
      'misc': None,
      'expression_system_plasmid': '_entity_src_gen.plasmid_name',
      'expression_system_strain': '_entity_src_gen.pdbx_host_org_strain',
      'gene': '_entity_src_gen.pdbx_gene_src_gene',
      'organism_common': '_entity_src_gen.gene_src_common_name'
      },
    '2':
      {'organism_scientific': '_pdbx_entity_src_syn.organism_scientific',
      'other_details': '_pdbx_entity_src_syn.details',
      'misc': None,
      'organism_taxid': '_pdbx_entity_src_syn.ncbi_taxonomy_id',
      'organism_common': '_pdbx_entity_src_syn.organism_common_name'
      }
    },
  'resolution': '_reflns.d_resolution_high',
  'structure_reference': None,
  }
    # - _entity.pdbx_fragment
    # ['Trx2 domain, UNP residues 190-298', 'c-term domain, UNP residues 244-263', '?', '?']
    # - _entity_name_com.name
    # ['ERp46, Endoplasmic reticulum resident protein 46, ER protein 46, Thioredoxin-like protein p46', 'Prx4', '?', '?']

  
    # - _citation_author.name
    # ['Kojima, R.', 'Okumura, M.', 'Masui, S.', 'Kanemura, S.', 'Inoue, M.', 'Saiki, M.', 'Yamaguchi, H.', 'Hikima, T.', 'Suzuki, M.', 'Akiyama, S.', 'Inaba, K.']