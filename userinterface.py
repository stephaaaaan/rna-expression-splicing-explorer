import os

import plotly.express as px
from PyQt5 import QtGui, QtWebEngineWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (QButtonGroup, QCheckBox, QGridLayout, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QMessageBox,
                             QPushButton, QRadioButton, QVBoxLayout, QWidget)

from export_dialog import export_dialog
from gene_table import gene_count_table, get_true_filename


class ui_window(QWidget):
    def __init__(
        self, width: int, height: int
    ):  
        super().__init__()
        myFont = QtGui.QFont()
        myFont.setBold(True)
        # load gene table
        self.gene_count_table = gene_count_table()
        self.selected_genes = []
        # --------------------------- initalize main window -------------------------- #
        self.setWindowTitle("Gene Expression Data")
        self.resize(width,height)
        # define layout
        self.mainwindowlayout = QGridLayout()
        self.setLayout(self.mainwindowlayout)
        self.leftcolumn = QVBoxLayout()
        self.rightcolumn = QVBoxLayout()
        # ---------------------------------------------------------------------------- #
        #                                    Widgets                                   #
        # ---------------------------------------------------------------------------- #
        # -------------------------------- input field ------------------------------- #
        self.input_layout = QGridLayout()
        # description for fields
        self.input_field_desc = QLabel("Enter ENSEMBL ID")
        self.input_field_desc.setFont(myFont)
        self.input_layout.addWidget(self.input_field_desc, 0, 0)
        self.gene_id_desc = QLabel("Gene ID")
        self.gene_id_desc.setFont(myFont)
        self.input_layout.addWidget(self.gene_id_desc, 0, 1)
        # input for gene id
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.add_to_list_func)
        self.input_field.textChanged.connect(self.input_changed)
        self.input_layout.addWidget(self.input_field, 1, 0)
        #
        self.gene_id = QLineEdit()
        self.gene_id.returnPressed.connect(self.add_to_list_func)
        self.gene_id.textChanged.connect(self.geneid_changed)
        self.input_layout.addWidget(self.gene_id, 1, 1)
        # button add to list
        self.add_to_list = QPushButton("Add Gene", self)
        self.add_to_list.clicked.connect(self.add_to_list_func)
        self.input_layout.addWidget(self.add_to_list, 1, 2)
        self.input_layout.setVerticalSpacing(10)
        self.leftcolumn.addLayout(self.input_layout)
        # ---------------------------- gene selection list --------------------------- #
        self.selected_genes_list_desc = QLabel("Selected Genes")
        self.selected_genes_list_desc.setFont(myFont)
        self.leftcolumn.addWidget(self.selected_genes_list_desc)
        # list showing selection
        self.selected_genes_list = QListWidget()
        self.leftcolumn.addWidget(self.selected_genes_list)
        self.selected_genes_list.clicked.connect(self.activate_delete)
        # button delete
        self.delete = QPushButton("Delete", self)
        self.delete.setEnabled(False)
        self.delete.clicked.connect(self.delete_item)
        self.leftcolumn.addWidget(self.delete)
        # output selection
        self.output_selection = QGridLayout()
        # ------------------------------ example picture ----------------------------- #
        self.overview = QLabel(self)
        self.pixmap = QPixmap(get_true_filename("overview_figure.png"))
        self.image_width = int(round(width/3,0))
        self.pixmap_scaled = self.pixmap.scaledToWidth(self.image_width)
        self.overview.setPixmap(self.pixmap_scaled)
        self.rightcolumn.addWidget(self.overview)
        # ------------------------------- splice graph ------------------------------- #
        self.splice_graph_pix = QPixmap(get_true_filename("splicegraphs_5'.svg"))
        self.splice_graph_pix_scaled = self.splice_graph_pix.scaledToWidth(self.image_width)
        self.splice_graph = QLabel(self)
        self.splice_graph.setPixmap(self.splice_graph_pix_scaled)
        self.rightcolumn.addWidget(self.splice_graph)
        self.splicegraph_switch = QButtonGroup()
        self.splicegraph_layout = QHBoxLayout()
        self.splicegraph_switch_label = QLabel('Choose Strand')
        self.splicegraph_switch_label.setFont(myFont)
        self.splicegraph_layout.addWidget(self.splicegraph_switch_label)
        self.five_dash = QRadioButton("5' direction")
        self.five_dash.setChecked(True)
        self.five_dash.clicked.connect(self.change_splicegraph)
        self.splicegraph_switch.addButton(self.five_dash)
        self.splicegraph_layout.addWidget(self.five_dash)
        self.three_dash = QRadioButton("3' direction")
        self.three_dash.clicked.connect(self.change_splicegraph)
        self.splicegraph_switch.addButton(self.three_dash)
        self.splicegraph_layout.addWidget(self.three_dash)
        self.rightcolumn.addLayout(self.splicegraph_layout)
        self.rightcolumn.addStretch(100)
        # ------------------------------- brain region ------------------------------- #
        self.brainregion_layout = QHBoxLayout()
        self.brainregion_button_group = QButtonGroup()
        self.brainregion_label = QLabel("Brainregion")
        self.brainregion_label.setFont(myFont)
        self.brainregion_layout.addWidget(self.brainregion_label)
        self.both_select = QRadioButton("both")
        self.brainregion_button_group.addButton(self.both_select)
        self.both_select.clicked.connect(self.radiobutton_pressed)
        self.both_select.setChecked(True)
        self.brainregion_layout.addWidget(self.both_select)
        self.crtx_select = QRadioButton("Cortex")
        self.brainregion_button_group.addButton(self.crtx_select)
        self.crtx_select.clicked.connect(self.radiobutton_pressed)
        self.brainregion_layout.addWidget(self.crtx_select)
        self.hipp_select = QRadioButton("Hippocampus")
        self.brainregion_button_group.addButton(self.hipp_select)
        self.hipp_select.clicked.connect(self.radiobutton_pressed)
        self.brainregion_layout.addWidget(self.hipp_select)
        self.output_selection.addLayout(self.brainregion_layout, 0, 0)
        # --------------------------------- cell type -------------------------------- #
        self.celltype_layout = QHBoxLayout()
        self.celltype_button_group = QButtonGroup()
        self.type_label = QLabel("Celltype")
        self.type_label.setFont(myFont)
        self.celltype_layout.addWidget(self.type_label)
        self.all_other_select = QRadioButton("all/custom")
        self.celltype_button_group.addButton(self.all_other_select)
        self.all_other_select.clicked.connect(self.radiobutton_pressed)
        self.all_other_select.setChecked(True)
        self.celltype_layout.addWidget(self.all_other_select)
        self.inhibitory_select = QRadioButton("inhibitory")
        self.celltype_button_group.addButton(self.inhibitory_select)
        self.inhibitory_select.clicked.connect(self.radiobutton_pressed)
        self.celltype_layout.addWidget(self.inhibitory_select)
        self.excitatory_select = QRadioButton("excitatory")
        self.celltype_button_group.addButton(self.excitatory_select)
        self.excitatory_select.clicked.connect(self.radiobutton_pressed)
        self.celltype_layout.addWidget(self.excitatory_select)
        self.output_selection.addLayout(self.celltype_layout, 1, 0)
        self.leftcolumn.addLayout(self.output_selection)
        # ---------------------------------- samples --------------------------------- #
        self.samples_layout = QGridLayout()
        self.samples_label = QLabel("Samples")
        self.samples_label.setFont(myFont)
        self.samples_layout.addWidget(self.samples_label, 0, 0)
        self.camk = QCheckBox("CamK2")
        self.camk.setChecked(True)
        self.samples_layout.addWidget(self.camk, 0, 1)
        self.grik = QCheckBox("Grik4")
        self.grik.setChecked(True)
        self.samples_layout.addWidget(self.grik, 0, 2)
        self.pv = QCheckBox("PV")
        self.pv.setChecked(True)
        self.samples_layout.addWidget(self.pv, 1, 1)
        self.scnn = QCheckBox("Scnn1a")
        self.scnn.setChecked(True)
        self.samples_layout.addWidget(self.scnn, 1, 2)
        self.sst = QCheckBox("SST")
        self.sst.setChecked(True)
        self.samples_layout.addWidget(self.sst, 2, 1)
        self.vip = QCheckBox("VIP")
        self.vip.setChecked(True)
        self.samples_layout.addWidget(self.vip, 2, 2)
        self.leftcolumn.addLayout(self.samples_layout)
        # ---------------------------------------------------------------------------- #
        #                             alternative splicing                             #
        # ---------------------------------------------------------------------------- #
        # --------------------------- choose analysis type --------------------------- #
        self.switch_gene_expression_layout = QHBoxLayout()
        self.switch_gene_expression_label = QLabel("Analysis Type")
        self.switch_gene_expression_label.setFont(myFont)
        self.switch_gene_expression_layout.addWidget(self.switch_gene_expression_label)
        self.switch_gene_expression = QButtonGroup()
        self.gene_expression = QRadioButton("gene expression")
        self.switch_gene_expression.addButton(self.gene_expression)
        self.gene_expression.clicked.connect(self.switch_gene_expression_clicked)
        self.gene_expression.setChecked(True)
        self.switch_gene_expression_layout.addWidget(self.gene_expression)
        self.alternative_splicing = QRadioButton("alternative splicing")
        self.switch_gene_expression.addButton(self.alternative_splicing)
        self.alternative_splicing.clicked.connect(self.switch_gene_expression_clicked)
        self.switch_gene_expression_layout.addWidget(self.alternative_splicing)
        self.leftcolumn.addLayout(self.switch_gene_expression_layout)
        # -------------------- select splicing events of interest -------------------- #
        self.splicing_events_layout = QGridLayout()
        self.splicing_events_label = QLabel("Splicing Events")
        self.splicing_events_label.setFont(myFont)
        self.splicing_events_layout.addWidget(self.splicing_events_label, 0, 0)
        self.ie = QCheckBox("Including Exon (IE)")
        self.splicing_events_layout.addWidget(self.ie, 0, 1)
        self.se = QCheckBox("Skipping Exon (SE)")
        self.splicing_events_layout.addWidget(self.se, 0, 2)
        self.me = QCheckBox("Mutually exclusive exon (MX)")
        self.splicing_events_layout.addWidget(self.me, 1, 1)

        self.ri = QCheckBox("Retained Intron (RI)")
        self.splicing_events_layout.addWidget(self.ri, 1, 2)
        self.a5 = QCheckBox("Alternative 5' splice-site (A5)")
        self.splicing_events_layout.addWidget(self.a5, 2, 1)
        self.a3 = QCheckBox("Alternative 3' splice-site (A3)")
        self.splicing_events_layout.addWidget(self.a3, 2, 2)
        self.af = QCheckBox("Alternative first exon (AF)")
        self.splicing_events_layout.addWidget(self.af, 3, 1)
        self.splicing_events_checkboxes = [
            self.ie,
            self.se,
            self.me,
            self.ri,
            self.a5,
            self.a3,
            self.af,
        ]
        for checkbox in self.splicing_events_checkboxes:
            checkbox.setChecked(True)
            checkbox.setCheckable(False)
            checkbox.setToolTip("Select Analysis Type 'alternative splicing'")
        self.leftcolumn.addLayout(self.splicing_events_layout)

        # ---------------------------------- export ---------------------------------- #
        self.export_btn = QPushButton("export")
        self.export_btn.clicked.connect(self.export)
        self.leftcolumn.addWidget(self.export_btn)
        # --------------------------------- Citation --------------------------------- #
        self.citationlayout = QGridLayout()
        smallFont = QtGui.QFont()
        smallFont.setPointSize(10)
        self.original_study_label = QLabel("Original Study")
        self.original_study_label.setFont(myFont)
        self.citationlayout.addWidget(self.original_study_label,0,0)
        urlLink = '<a href="https://doi.org/10.1038/s41593-019-0465-5">Furlanis et al., Nat Neurosci 22 (2019)</a>'
        self.original_study = QLabel(urlLink)
        self.original_study.setOpenExternalLinks(True)
        self.original_study.setFont(smallFont)
        self.citationlayout.addWidget(self.original_study,0,1)
        self.citationlayout.rowStretch(0)
        self.original_data_label = QLabel("Raw Data")
        self.original_data_label.setFont(myFont)
        self.citationlayout.addWidget(self.original_data_label,1,0)
        urlLink2 = '<a href="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE133291">GSE133291</a>'
        self.original_data = QLabel(urlLink2)
        self.original_data.setOpenExternalLinks(True)
        self.original_data.setFont(smallFont)
        self.citationlayout.addWidget(self.original_data,1,1)
        smallerFont = smallFont
        smallerFont.setPointSize(8)
        smallerFont.setItalic(True)
        self.copyright = QLabel("© Stephan Weißbach, 2022 - version 0.02")
        self.copyright.setFont(smallerFont)
        self.citationlayout.addWidget(self.copyright,2,0)
        self.rightcolumn.addLayout(self.citationlayout)
        self.mainwindowlayout.addLayout(self.leftcolumn, 0, 0)
        self.mainwindowlayout.addLayout(self.rightcolumn, 0, 1)
        # ---------------------------------------------------------------------------- #
        #                            gene expression heatmap                           #
        # ---------------------------------------------------------------------------- #
        self.browser = QtWebEngineWidgets.QWebEngineView(self)
        self.browser.setMinimumSize(self.image_width,int(height*0.9))
        self.browser.setMaximumSize(self.image_width,int(height*0.9))
        #self.browser.setMinimumSize(500,100)
        self.mainwindowlayout.addWidget(self.browser,0,2)

    # ---------------------------------------------------------------------------- #
    #                                Button Methods                                #
    # ---------------------------------------------------------------------------- #
    def input_changed(self) -> None:
        if len(self.input_field.text()) == 18:
            if (
                self.input_field.text()
                in self.gene_count_table.ensembl_to_gene_symbol.keys()
            ):
                self.gene_id.setText(
                    self.gene_count_table.ensembl_to_gene_symbol[
                        self.input_field.text()
                    ]
                )
        else:
            self.gene_id.setText("")

    def geneid_changed(self) -> None:
        if self.gene_id.text() in self.gene_count_table.gene_symbol_to_ensembl.keys():
            self.input_field.setText(
                self.gene_count_table.gene_symbol_to_ensembl[self.gene_id.text()]
            )
        else:
            self.input_field.setText("")

    def add_to_list_func(self) -> None:
        if (
            self.input_field.text()
            not in self.gene_count_table.ensembl_to_gene_symbol.keys()
        ):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Gene is not in the data.")
            msg.setInformativeText(
                "Please select valid gene. Make sure to use the ENSMBL Gene ID for mouse."
            )
            msg.setWindowTitle("Gene not found.")
            msg.exec_()
            return
        if self.input_field.text() not in self.selected_genes:
            self.selected_genes.append(self.input_field.text())
            self.selected_genes_list.addItem(
                f"{self.input_field.text()} ({self.gene_count_table.ensembl_to_gene_symbol[self.input_field.text()]})"
            )
        self.input_field.setText("")
        self.gene_id.setText("")
        self.plotly_graph_update()

    def delete_item(self) -> None:
        idx = self.selected_genes_list.currentRow()
        gene = self.selected_genes_list.currentItem().text().split(" ")[0]
        _ = self.selected_genes_list.takeItem(idx)
        self.selected_genes.remove(gene)
        self.delete.setEnabled(False)
        self.plotly_graph_update()

    def activate_delete(self) -> None:
        self.delete.setEnabled(True)
    
    def change_splicegraph(self) -> None:
        self.rightcolumn.itemAt(1).widget().deleteLater()
        if self.five_dash.isChecked():
            self.splice_graph_pix = QPixmap(get_true_filename("splicegraphs_5'.svg"))
        else:
            self.splice_graph_pix = QPixmap(get_true_filename("splicegraphs_3'.svg"))
        self.splice_graph_pix_scaled = self.splice_graph_pix.scaledToWidth(self.image_width)
        self.splice_graph = QLabel(self)
        self.splice_graph.setPixmap(self.splice_graph_pix_scaled)
        self.rightcolumn.insertWidget(1,self.splice_graph)

    def radiobutton_pressed(self) -> None:
        if self.inhibitory_select.isChecked() and self.crtx_select.isChecked():
            # pv,vip,sst
            for button in [self.pv, self.vip, self.sst]:
                button.setCheckable(True)
                button.setChecked(True)
            for button in [self.grik, self.scnn, self.camk]:
                button.setChecked(False)
                button.setCheckable(False)
        elif self.inhibitory_select.isChecked() and self.hipp_select.isChecked():
            for button in [self.sst]:
                button.setCheckable(True)
                button.setChecked(True)
            for button in [self.grik, self.scnn, self.camk, self.pv, self.vip]:
                button.setChecked(False)
                button.setCheckable(False)
        elif self.inhibitory_select.isChecked() and self.both_select.isChecked():
            for button in [self.sst, self.pv, self.vip]:
                button.setCheckable(True)
                button.setChecked(True)
            for button in [self.grik, self.scnn, self.camk]:
                button.setChecked(False)
                button.setCheckable(False)
        elif self.excitatory_select.isChecked() and self.crtx_select.isChecked():
            for button in [self.scnn, self.camk]:
                button.setCheckable(True)
                button.setChecked(True)
            for button in [self.grik, self.sst, self.pv, self.vip]:
                button.setChecked(False)
                button.setCheckable(False)
        elif self.excitatory_select.isChecked() and self.hipp_select.isChecked():
            for button in [self.grik, self.camk]:
                button.setCheckable(True)
                button.setChecked(True)
            for button in [self.scnn, self.sst, self.pv, self.vip]:
                button.setChecked(False)
                button.setCheckable(False)
        elif self.excitatory_select.isChecked() and self.both_select.isChecked():
            for button in [self.scnn, self.grik, self.camk]:
                button.setCheckable(True)
                button.setChecked(True)
            for button in [self.sst, self.pv, self.vip]:
                button.setChecked(False)
                button.setCheckable(False)
        elif self.all_other_select.isChecked() and self.hipp_select.isChecked():
            for button in [self.sst, self.grik, self.camk]:
                button.setCheckable(True)
                button.setChecked(True)
            for button in [self.scnn, self.pv, self.vip]:
                button.setChecked(False)
                button.setCheckable(False)
        elif self.all_other_select.isChecked() and self.crtx_select.isChecked():
            for button in [self.pv, self.scnn, self.sst, self.camk, self.vip]:
                button.setCheckable(True)
                button.setChecked(True)
            for button in [self.grik]:
                button.setChecked(False)
                button.setCheckable(False)
        else:
            for button in [
                self.pv,
                self.scnn,
                self.sst,
                self.camk,
                self.vip,
                self.grik,
            ]:
                button.setCheckable(True)
                button.setChecked(True)
        self.plotly_graph_update()

    def switch_gene_expression_clicked(self):
        to_set = False if self.gene_expression.isChecked() else True
        for checkbox in self.splicing_events_checkboxes:
            if not to_set:
                checkbox.setChecked(False)
            checkbox.setCheckable(to_set)
            checkbox.setChecked(True)
            if to_set:
                checkbox.setToolTip("")
            else:
                checkbox.setToolTip("Select Analysis Type 'alternative splicing'")

    def no_splice_events(self, gene):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("No splice-variants")
        msg.setText(
            f"No splice-variants for {gene} ({self.gene_count_table.ensembl_to_gene_symbol[gene]}) with your current selection."
        )
        msg.exec_()
    
    def plotly_graph_update(self) -> None:
        selected_samples = self.get_selected_samples()
        df = self.gene_count_table.return_data_df(self.selected_genes, selected_samples).T
        if df.shape[0] == 0:
            return
        fig = px.imshow(df, labels={'Geneid': 'Ensembl Gene ID',
                                     'y': 'Sample ID',
                                     'color': 'cpm'})
        fig.update_layout({'yaxis_title':None,'xaxis_title':None, 'xaxis': {'tickfont':{'size':10},'tickangle':90}, 'yaxis': {'tickfont':{'size':10}}})
        fig.update_layout(coloraxis_showscale=False)
        self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


    def export(self, _):
        # ----------------------- check if any sample selected ----------------------- #
        any_sample_selected = False
        for button in [self.pv, self.scnn, self.sst, self.camk, self.vip, self.grik]:
            if button.isChecked():
                any_sample_selected = True
                break
        if not any_sample_selected:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Select at least one cell type!")
            msg.setWindowTitle("No cell type selected.")
            msg.exec_()
            return
        # ------------------------ check if any genes selected ----------------------- #
        if len(self.selected_genes) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Select at least one gene.")
            msg.setWindowTitle("No genes selected")
            msg.exec_()
            return
        self.export_window = export_dialog(self)
        self.export_window.show()

    def get_selected_samples(self):
        selected_samples = []
        if self.pv.isChecked():
            selected_samples += ["PV_1", "PV_2", "PV_3", "PV_4"]
        if self.scnn.isChecked():
            selected_samples += ["Scnn_1", "Scnn_2", "Scnn_3", "Scnn_4"]
        if self.sst.isChecked():
            if self.hipp_select.isChecked():
                selected_samples += ["SST_1", "SST_2", "SST_3", "SST_4"]
            elif self.crtx_select.isChecked():
                selected_samples += ["SST_W2", "SST_W3", "SST_W5", "SST_W1"]
            else:
                selected_samples += [
                    "SST_1",
                    "SST_2",
                    "SST_3",
                    "SST_4",
                    "SST_W2",
                    "SST_W3",
                    "SST_W5",
                    "SST_W1",
                ]
        if self.camk.isChecked():
            if self.hipp_select.isChecked():
                selected_samples += ["CamK_W2", "CamK_W3", "CamK_W4", "CamK_W5"]
            elif self.crtx_select.isChecked():
                selected_samples += ["CamK_1", "CamK_2", "CamK_3", "CamK_4"]
            else:
                selected_samples += [
                    "CamK_1",
                    "CamK_2",
                    "CamK_3",
                    "CamK_4",
                    "CamK_W2",
                    "CamK_W3",
                    "CamK_W4",
                    "CamK_W5",
                ]
        if self.vip.isChecked():
            selected_samples += ["VIP_W1", "VIP_W2", "VIP_W3", "VIP_W4"]
        if self.grik.isChecked():
            selected_samples += ["Grik_W3", "Grik_W4", "Grik_W5", "Grik_W6"]
        return selected_samples

    def save(self, filepath: str, filename: str, fileformat: str) -> None:
        self.export_window.close()
        # ------------------------- export count table as csv ------------------------ #
        selected_samples = self.get_Selected_samples()
        if self.gene_expression.isChecked():
            df = self.gene_count_table.return_df(self.selected_genes, selected_samples)

        else:
            selected_splice_events = []
            for button in self.splicing_events_checkboxes:
                if not button.isChecked():
                    continue
                selected_splice_events.append(button.text().split("(")[1][:-1])
            if len(selected_splice_events) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("No Splice Events selected")
                msg.setText(f"Select at least one splice event for export.")
                msg.exec_()
                return
            df = self.gene_count_table.return_alternative_splicing_df(
                self, self.selected_genes, selected_samples, selected_splice_events
            )
        if fileformat == "csv":
            df.to_csv(os.path.join(filepath, f"{filename}.csv"), index=False)
        else:
            df.to_excel(os.path.join(filepath, f"{filename}.xlsx"), index=False)

        # --------------------------- empty all selections --------------------------- #
        self.selected_genes = []
        self.selected_genes_list.clear()
        # -------------------- message to inform successful export ------------------- #
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Export successful")
        msg.setText(
            f"The file was exported to {os.path.join(filepath,f'{filename}.{fileformat}')}"
        )
        msg.exec_()