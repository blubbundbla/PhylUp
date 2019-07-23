import pandas as pd
from pandas_filter import pandas_numpy_try1, config, aln_updater


def test_filterlen():
    workdir = "tests/test_runs"
    trfn = "data/tiny_test_example/test.tre"
    schema_trf = "newick"
    id_to_spn = "data/tiny_test_example/test_nicespl.csv"
    seqaln = "data/tiny_test_example/test_extralongseq.fas"
    mattype = "fasta"
    configfi = "data/localblast.config"

    conf = config.ConfigObj(configfi, workdir, interactive=False)
    test = pandas_numpy_try1.Update_data(id_to_spn, seqaln, mattype, trfn, schema_trf, conf, mrca=18794)

    aln = test.read_in_aln()

    extra_long = {'ncbi_txn': ['extra_long'],
                  'ncbi_txid': [123],
                  'org_sp_name': ['extra_long'],
                  'tip_name': ['extra_long'],
                  'status': ['test'], 'status_note': ['note'], "date": ['2001'],
                  'index': [5], 'accession': ['532342.1'],
                  'pident': [99.533], 'evalue': [0], 'bitscore': [1175],
                  'sseq': [
                      'TCGAAACCTGCATAGCAGAACGACCTGTGAACATGTAAAAACAATTGGGTGTTCTAAGTATTGGGCTCTTGTYCGATTYCTAGGATGCCATGTTGACGTGCGTCTTTGGCAAGCCCCTTGGGTGTCTAAGGACGTCACGTCGACGCAACAACAAACCCCCGGCACGGCATGTGCCAAGGAAATATAAACTTAATAAGGGCTTGTTCCATGCATTGCCGTTCGCGGTGATTGCATTGAAACTTGCTTCTTTATAATCATAAACGACTCTCGGCAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCCGAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACACATCGCGTCGCCCCCATCACACCTCTTGACGGGGATGTTTGAATGGGGACGGAGATTGGTCTCCCGTTCCTAAGGTGCGGTTGGCTGAATTTTGAGTCCTCTTCGACGGACGCACGATTAGTGGTGGTTGACAAGACCTTCTTTCGAGTTGTGTGTTCCAAGAAGTAAGGAATATCTCTTTAACGACCCTAAAGTGTTGTCTCATGACGATGCTTCGACTGCTCGAAACCTGCATAGCAGAACGACCTGTGAACATGTAAAAACAATTGGGTGTTCTAAGTATTGGGCTCTTGTYCGATTYCTAGGATGCCATGTTGACGTGCGTCTTTGGCAAGCCCCTTGGGTGTCTAAGGACGTCACGTCGACGCAACAACAAACCCCCGGCACGGCATGTGCCAAGGAAATATAAACTTAATAAGGGCTTGTTCCATGCATTGCCGTTCGCGGTGATTGCATTGAAACTTGCTTCTTTATAATCATAAACGACTCTCGGCAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCCGAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACACATCGCGTCGCCCCCATCACACCTCTTGACGGGGATGTTTGAATGGGGACGGAGATTGGTCTCCCGTTCCTAAGGTGCGGTTGGCTGAATTTTGAGTCCTCTTCGACGGACGCACGATTAGTGGTGGTTGACAAGACCTTCTTATCGAGTTGTGTGTTCCAAGAAGTAAGGAATATCTCTTTAACGACCCTAAAGTGTTGTCTCATGACGATGCTTCGACTGCTTGTCTCATGACGATGCTTCGACTGCTCGAAACCTGCATAGCAGAACGACCTGTGAACATGTAAAAACAATTGGGTGTTCTAAGTATTGGGCTCTTGTYCGATTYCTAGGATGCCATGTTGACGTGCGTCTTTGGCAAGCCCCTTGGGTGTCTAAGGACGTCACGTCGACGCAACAACAAACCCCCGGCACGGCATGTGCCAAGGAAATATAAACTTAATAAGGGCTTGTTCCATGCATTGCCGTTCGCGGTGATTGCATTGAAACTTGCTTCTTTATAATCATAAACGACTCTCGGCAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCCGAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACACATCGCGTCGCCCCCATCACACCTCTTGACGGGGATGTTTGAATGGGGACGGAGATTGGTCTCCCGTTCCTAAGGTGCGGTTGGCTGAATTTTGAGTCCTCTTCGACGGACGCACGATTAGTGGTGGTTGACAAGACCTTCTTATCGAGTTGTGTGTTCCAAGAAGTAAGGAATATCTCTTTAACGACCCTAAAGTGTTGTCTCATGACGATGCTTCGACTGC'],
                  'title': ['no title']
                  }

    new_seqs = pd.DataFrame(extra_long)
    before = len(new_seqs)

    f = pandas_numpy_try1.FilterLength(test.config, aln)
    f.filter(new_seqs)
    new_seqs = f.upd_new_seqs

    del_tab = len(f.del_table)
    after = len(new_seqs)

    assert before > after
    assert del_tab > 0

    extra_short = {'ncbi_txn': ['extra_long'],
                  'ncbi_txid': [123],
                  'org_sp_name': ['extra_long'],
                  'tip_name': ['extra_long'],
                  'status': ['test'], 'status_note': ['note'], "date": ['2001'],
                  'index': [5], 'accession': ['532342.1'],
                  'pident': [99.533], 'evalue': [0], 'bitscore': [1175],
                  'sseq': [
                      'TCGAAACCTGCATAGCAGAACGACCTGTGAACATGTAAAAACAATTGGGTGTTCTAAGTATTGGGCTCTTGTYCGATTYCTAGGATGCCATGTTGA'],
                  'title': ['no title']
                  }

    new_seqs = pd.DataFrame(extra_short)
    before = len(new_seqs)

    f = pandas_numpy_try1.FilterLength(test.config, aln)
    f.filter(new_seqs)
    new_seqs = f.upd_new_seqs

    del_tab = len(f.del_table)
    after = len(new_seqs)

    assert before > after
    assert del_tab > 0