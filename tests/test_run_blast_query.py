import datetime
import pandas as pd
import os
from pandas_filter import pandas_numpy_try1, config, blast
from pandas_filter import cd

taxon = 'Senecio_test'
query_seq = 'GATTGCATTGAAACTTGCTTCTTTATAATCATAAACGACTCTCGGCAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCCGAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACACATCGCGTCGCCCCCATCACACCTCTTGACGGGGATGTT'

workdir = "tests/test_runs"
configfi = "data/localblast.config"
conf = config.ConfigObj(configfi, workdir, interactive=False)

db_path = conf.blastdb

input_fn = "{}/blast/{}_tobeblasted.fas".format(conf.workdir, taxon)
input_fn = os.path.abspath(input_fn)
toblast = open(input_fn, "w")
toblast.write(">{}\n".format(taxon))
toblast.write("{}\n".format(query_seq))
toblast.close()

outfmt = " -outfmt '6 sseqid staxids sscinames pident evalue bitscore sseq salltitles sallseqid'"

out_fn = os.path.abspath('{}/testfile.blastn'.format(workdir))


with cd(db_path):
    # this format (6) allows to get the taxonomic information at the same time
    # outfmt = " -outfmt 5"  # format for xml file type
    # TODO MK: update to blast+ v. 2.8 code - then we can limit search to taxids: -taxids self.mrca_ncbi
    blastcmd = "blastn -query " + input_fn + \
               " -db {}/nt_v5 -out ".format(db_path) + out_fn + \
               " {} -num_threads {}".format(outfmt, conf.num_threads) + \
               " -max_target_seqs {} -max_hsps {}".format(conf.hitlist_size,
                                                          conf.hitlist_size)
    # needs to run from within the folder:
    print('run blastcmd')
    if not os.path.isfile(out_fn):

        print(blastcmd)
        os.system(blastcmd)
    elif not os.stat(out_fn).st_size > 0:
        print(blastcmd, 'xxxx')
        os.system(blastcmd)
    assert os.path.isfile(out_fn)




def test_run_blast_query():
    workdir = "tests/test_runs"
    trfn = "data/tiny_test_example/test.tre"
    schema_trf = "newick"
    id_to_spn = "data/tiny_test_example/test_nicespl.csv"
    seqaln = "data/tiny_test_example/test.fas"
    mattype = "fasta"
    configfi = "data/localblast.config"

    conf = config.ConfigObj(configfi, workdir, interactive=False)
    test = pandas_numpy_try1.Update_data(id_to_spn, seqaln, mattype, trfn, schema_trf, conf, mrca=18794)

    # create list of indice of subset list
    today = datetime.date.today()
    min_date_blast = today - datetime.timedelta(days=90)
    present_subset_df = test.table['status'] != "excluded"
    present_subset_df = test.table[present_subset_df == True]
    present_subset_df = present_subset_df[(present_subset_df.date <= min_date_blast)]
    present_subset = present_subset_df


    for index in present_subset.index:
        print('blast table seq')

        tip_name = test.table.loc[index, 'tip_name']

        query_seq = test.table.loc[index, 'sseq']
        print()
        test.table.loc[index, 'date'] = today  # TODO: is here the blast date the issue???
        print(query_seq, tip_name, test.config.blastdb, "Genbank", test.config)
        # new_seq_tax = blast.get_new_seqs(query_seq, tip_name, test.config.blastdb, "Genbank", test.config)
        blast.run_blast_query(query_seq, tip_name, test.config.blastdb, "Genbank", test.config)
        new_blastseqs = blast.read_blast_query(tip_name, test.config, 'Genbank')
        assert len(new_blastseqs) > 0


def test_run_blast():
    taxon = 'Senecio_test'
    query_seq = 'GATTGCATTGAAACTTGCTTCTTTATAATCATAAACGACTCTCGGCAACGGATATCTCGGCTCACGCATCGATGAAGAACGTAGCAAAATGCGATACTTGGTGTGAATTGCAGAATCCCGTGAACCATCGAGTTTTTGAACGCAAGTTGCGCCCGAAGCCTTTTGGTTGAGGGCACGTCTGCCTGGGCGTCACACATCGCGTCGCCCCCATCACACCTCTTGACGGGGATGTT'

    workdir = "tests/test_runs"
    configfi = "data/localblast.config"
    conf = config.ConfigObj(configfi, workdir, interactive=False)

    db_path = conf.blastdb

    input_fn = "{}/blast/{}_tobeblasted.fas".format(conf.workdir, taxon)
    input_fn = os.path.abspath(input_fn)
    toblast = open(input_fn, "w")
    toblast.write(">{}\n".format(taxon))
    toblast.write("{}\n".format(query_seq))
    toblast.close()

    outfmt = " -outfmt '6 sseqid staxids sscinames pident evalue bitscore sseq salltitles sallseqid'"

    out_fn = os.path.abspath('{}/testfile.blastn'.format(workdir))

    with cd(db_path):
        # this format (6) allows to get the taxonomic information at the same time
        # outfmt = " -outfmt 5"  # format for xml file type
        # TODO MK: update to blast+ v. 2.8 code - then we can limit search to taxids: -taxids self.mrca_ncbi
        blastcmd = "blastn -query " + input_fn + \
                   " -db {}/nt_v5 -out ".format(db_path) + out_fn + \
                   " {} -num_threads {}".format(outfmt, conf.num_threads) + \
                   " -max_target_seqs {} -max_hsps {}".format(conf.hitlist_size,
                                                              conf.hitlist_size)
        # needs to run from within the folder:
        print('run blastcmd')
        if not os.path.isfile(out_fn):
            os.system(blastcmd)
        elif not os.stat(out_fn).st_size > 0:
            os.system(blastcmd)
        assert os.path.isfile(out_fn)
