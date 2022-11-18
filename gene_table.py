import pandas as pd
import yaml


class gene_count_table:
    def __init__(self) -> None:
        self.count_table = pd.read_csv('count_table.txt')
        print('count table')
        self.count_table.index = self.count_table['Geneid']
        with open('sample_metadata.yaml','r') as f:
            self.sample_metadata = yaml.load(f,yaml.Loader)
        print('meta data')
        self.default_list = ['CamK_1',
            'CamK_2', 'CamK_3', 'CamK_4', 'CamK_W2', 'CamK_W3', 'CamK_W4',
            'CamK_W5', 'Grik_W3', 'Grik_W4', 'Grik_W5', 'Grik_W6', 'PV_1', 'PV_2',
            'PV_3', 'PV_4', 'Scnn_1', 'Scnn_2', 'Scnn_3', 'Scnn_4', 'SST_1',
            'SST_2', 'SST_3', 'SST_4', 'SST_W2', 'SST_W3', 'SST_W5', 'SST_W1',
            'VIP_W1', 'VIP_W2', 'VIP_W3', 'VIP_W4']
        for col in self.default_list:
            self.count_table[col] = (self.count_table[col] / self.count_table[col].sum()) * 1_000_000
        with open('ensembl_to_gene_symbol.yaml','r') as f:
            self.ensembl_to_gene_symbol = yaml.load(f,yaml.Loader)
  
    def return_df(self, gene_list: list, columns_selected: list = []) -> pd.DataFrame:
        if columns_selected == []:
            columns_selected = self.default_list
        df_list = []
        for gene in gene_list:
            if gene not in self.count_table.index:
                raise ValueError('Gene not found')
            gene_count_data = self.count_table.loc[gene]
            print(gene_count_data.loc['Geneid'])
            genesym = gene_count_data.loc['gene symbol']
            for col, val in zip(gene_count_data.index,gene_count_data):
                if col not in columns_selected: continue
                df_list.append([col,gene,genesym,self.sample_metadata[col]['brainregion'],self.sample_metadata[col]['type'],val])
        return pd.DataFrame(df_list, columns=['Sample','ENSEMBL Gene ID', 'Gene Symbol','Brainregion','Celltype','gene (counts per million)'])
