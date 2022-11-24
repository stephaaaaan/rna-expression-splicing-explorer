import pandas as pd
import sys
import os
import json


def get_true_filename(filename):
    try:
        base = sys._MEIPASS
    except Exception:
        base = os.path.abspath(".")
    return os.path.join(base, filename)


class gene_count_table:
    def __init__(self) -> None:
        self.count_table = pd.read_csv(get_true_filename("count_table.csv"))
        self.count_table.index = self.count_table["Geneid"]
        self.alternative_splicing_table = pd.read_csv(
            get_true_filename("all_samples_psi.csv")
        )
        with open(get_true_filename("sample_metadata.json"), "r") as f:
            self.sample_metadata = json.load(f)
        self.default_list = [
            "CamK_1",
            "CamK_2",
            "CamK_3",
            "CamK_4",
            "CamK_W2",
            "CamK_W3",
            "CamK_W4",
            "CamK_W5",
            "Grik_W3",
            "Grik_W4",
            "Grik_W5",
            "Grik_W6",
            "PV_1",
            "PV_2",
            "PV_3",
            "PV_4",
            "Scnn_1",
            "Scnn_2",
            "Scnn_3",
            "Scnn_4",
            "SST_1",
            "SST_2",
            "SST_3",
            "SST_4",
            "SST_W2",
            "SST_W3",
            "SST_W5",
            "SST_W1",
            "VIP_W1",
            "VIP_W2",
            "VIP_W3",
            "VIP_W4",
        ]
        for col in self.default_list:
            self.count_table[col] = (
                self.count_table[col] / self.count_table[col].sum()
            ) * 1_000_000
        with open(get_true_filename("ensembl_to_gene_symbol.json"), "r") as f:
            self.ensembl_to_gene_symbol = json.load(f)
        self.gene_symbol_to_ensembl = {
            v: k for k, v in self.ensembl_to_gene_symbol.items()
        }
    
    def return_data_df(self, gene_list: list, columns_selected: list) -> pd.DataFrame:
        return self.count_table.loc[gene_list,columns_selected]

    def return_df(self, gene_list: list, columns_selected: list = []) -> pd.DataFrame:
        if columns_selected == []:
            columns_selected = self.default_list
        df_list = []
        for gene in gene_list:
            if gene not in self.count_table.index:
                raise ValueError("Gene not found")
            gene_count_data = self.count_table.loc[gene]
            genesym = gene_count_data.loc["gene symbol"]
            for col, val in zip(gene_count_data.index, gene_count_data):
                if col not in columns_selected:
                    continue
                df_list.append(
                    [
                        col,
                        gene,
                        genesym,
                        self.sample_metadata[col]["brainregion"],
                        self.sample_metadata[col]["type"],
                        val,
                    ]
                )
        return pd.DataFrame(
            df_list,
            columns=[
                "Sample",
                "ENSEMBL Gene ID",
                "Gene Symbol",
                "Brainregion",
                "Celltype",
                "gene count (counts per million)",
            ],
        )

    def return_alternative_splicing_df(
        self, parent, gene_list, columns_selected, splice_events_types_selected
    ) -> pd.DataFrame:
        df_list = []
        for gene in gene_list:
            gene_alternative_splice_events = self.alternative_splicing_table[
                (self.alternative_splicing_table["Ensembl Gene ID"] == gene)
                & (
                    self.alternative_splicing_table["splicing_event"].isin(
                        splice_events_types_selected
                    )
                )
            ]
            if gene_alternative_splice_events.shape[0] < 1:
                parent.no_splice_events(gene)
                continue
            # Ensembl Gene ID	splicing_event	chr	bp_position
            for _, splice_event in gene_alternative_splice_events.iterrows():
                genesym = self.ensembl_to_gene_symbol[gene]
                splice_event_type = splice_event["splicing_event"]
                chr = splice_event["chr"]
                bp_position = splice_event["bp_position"]
                strand = splice_event["strand"]
                for col, val in zip(splice_event.index, splice_event):
                    if col not in columns_selected:
                        continue
                    df_list.append(
                        [
                            col,
                            gene,
                            genesym,
                            self.sample_metadata[col]["brainregion"],
                            self.sample_metadata[col]["type"],
                            splice_event_type,
                            chr,
                            bp_position,
                            strand,
                            val,
                        ]
                    )
        return pd.DataFrame(
            df_list,
            columns=[
                "Sample",
                "ENSEMBL Gene ID",
                "Gene Symbol",
                "Brainregion",
                "Celltype",
                "splice event type",
                "chr",
                "event position",
                "strand",
                "psi",
            ],
        )
