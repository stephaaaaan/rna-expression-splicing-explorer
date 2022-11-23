import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QButtonGroup, QCheckBox, QVBoxLayout,
                             QFileDialog, QFrame, QGridLayout, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QMessageBox,
                             QPushButton, QRadioButton, QWidget)

from gene_table import gene_count_table, get_true_filename


class ui_window(QWidget):
    def __init__(self):
        super().__init__()
        myFont=QtGui.QFont()
        myFont.setBold(True)
        # load gene table
        self.gene_count_table = gene_count_table()
        self.selected_genes = []
        # --------------------------- initalize main window -------------------------- #
        self.setWindowTitle("Gene Expression Data")
        #self.resize(1000, 500)
        # define layout
        self.mainwindowlayout = QGridLayout()
        self.setLayout(self.mainwindowlayout)
        self.leftcolumn = QGridLayout()
        self.rightcolumn = QGridLayout()
        # ---------------------------------------------------------------------------- #
        #                                    Widgets                                   #
        # ---------------------------------------------------------------------------- #
        # -------------------------------- input field ------------------------------- #
        self.input_layout = QGridLayout()
        #description for fields
        self.input_field_desc = QLabel('Enter ENSEMBL ID')
        self.input_field_desc.setFont(myFont)
        self.input_layout.addWidget(self.input_field_desc,0,0)
        self.gene_id_desc = QLabel('Gene ID')
        self.gene_id_desc.setFont(myFont)
        self.input_layout.addWidget(self.gene_id_desc,0,1)
        # input for gene id
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.add_to_list_func)
        self.input_field.setMaximumWidth(200)
        self.input_field.textChanged.connect(self.input_changed)
        self.input_layout.addWidget(self.input_field,1,0)
        # 
        self.gene_id = QLineEdit()
        self.gene_id.returnPressed.connect(self.add_to_list_func)
        self.gene_id.textChanged.connect(self.geneid_changed)
        self.input_layout.addWidget(self.gene_id,1,1)
        # button add to list
        self.add_to_list = QPushButton('Add Gene',self)
        self.add_to_list.clicked.connect(self.add_to_list_func)
        self.input_layout.addWidget(self.add_to_list,1,2)
        self.input_layout.setVerticalSpacing(10)
        self.leftcolumn.addLayout(self.input_layout,0,0,1,3)
        # ---------------------------- gene selection list --------------------------- #
        self.selected_genes_list_desc = QLabel('Selected Genes')
        self.selected_genes_list_desc.setFont(myFont)
        self.leftcolumn.addWidget(self.selected_genes_list_desc,1,0)
        # list showing selection
        self.selected_genes_list = QListWidget()
        self.leftcolumn.addWidget(self.selected_genes_list,2,0,2,2)
        self.selected_genes_list.clicked.connect(self.activate_delete)
        # button delete
        self.delete = QPushButton('Delete', self)
        self.delete.setEnabled(False)
        self.delete.clicked.connect(self.delete_item)
        self.leftcolumn.addWidget(self.delete,2,2,1,1)
        # output selection
        self.output_selection = QGridLayout()
        # ------------------------------ example picture ----------------------------- #
        self.overview = QLabel(self)
        self.pixmap = QPixmap(get_true_filename('overview_figure.png'))
        self.pixmap_scaled = self.pixmap.scaled(700, 700, Qt.KeepAspectRatio)
        self.overview.setPixmap(self.pixmap_scaled)
        self.rightcolumn.addWidget(self.overview,0,0,2,3)
        self.splice_graph = QLabel()
        self.pixmap_splice_graph = QPixmap(get_true_filename('splice_graphs.png'))
        self.pixmap_splice_graph_scaled = self.pixmap_splice_graph.scaled(700, 700, Qt.KeepAspectRatio)
        self.splice_graph.setPixmap(self.pixmap_splice_graph_scaled)
        self.rightcolumn.addWidget(self.splice_graph,3,0,2,3)
        # ------------------------------- brain region ------------------------------- #
        self.brainregion_layout = QHBoxLayout()
        self.brainregion_button_group = QButtonGroup()
        self.brainregion_label = QLabel('Brainregion')
        self.brainregion_label.setFont(myFont)
        self.brainregion_layout.addWidget(self.brainregion_label)
        self.both_select = QRadioButton('both')
        self.brainregion_button_group.addButton(self.both_select)
        self.both_select.clicked.connect(self.radiobutton_pressed)
        self.both_select.setChecked(True)
        self.brainregion_layout.addWidget(self.both_select)
        self.crtx_select = QRadioButton('Cortex')
        self.brainregion_button_group.addButton(self.crtx_select)
        self.crtx_select.clicked.connect(self.radiobutton_pressed)
        self.brainregion_layout.addWidget(self.crtx_select)
        self.hipp_select = QRadioButton('Hippocampus')
        self.brainregion_button_group.addButton(self.hipp_select)
        self.hipp_select.clicked.connect(self.radiobutton_pressed)
        self.brainregion_layout.addWidget(self.hipp_select)
        self.output_selection.addLayout(self.brainregion_layout,0,0)
        # --------------------------------- cell type -------------------------------- #
        self.celltype_layout = QHBoxLayout()
        self.celltype_button_group = QButtonGroup()
        self.type_label = QLabel('Celltype')
        self.type_label.setFont(myFont)
        self.celltype_layout.addWidget(self.type_label)
        self.all_other_select = QRadioButton('all/custom')
        self.celltype_button_group.addButton(self.all_other_select)
        self.all_other_select.clicked.connect(self.radiobutton_pressed)
        self.all_other_select.setChecked(True)
        self.celltype_layout.addWidget(self.all_other_select)
        self.inhibitory_select = QRadioButton('inhibitory')
        self.celltype_button_group.addButton(self.inhibitory_select)
        self.inhibitory_select.clicked.connect(self.radiobutton_pressed)
        self.celltype_layout.addWidget(self.inhibitory_select)
        self.excitatory_select = QRadioButton('excitatory')
        self.celltype_button_group.addButton(self.excitatory_select)
        self.excitatory_select.clicked.connect(self.radiobutton_pressed)
        self.celltype_layout.addWidget(self.excitatory_select)
        self.output_selection.addLayout(self.celltype_layout,1,0)
        self.leftcolumn.addLayout(self.output_selection,4,0,1,3)
        # ---------------------------------- samples --------------------------------- #
        self.samples_layout = QGridLayout()
        self.samples_label = QLabel('Samples')
        self.samples_label.setFont(myFont)
        self.samples_layout.addWidget(self.samples_label,0,0)
        self.camk = QCheckBox('CamK2')
        self.camk.setChecked(True)
        self.samples_layout.addWidget(self.camk,0,1)
        self.grik = QCheckBox('Grik4')
        self.grik.setChecked(True)
        self.samples_layout.addWidget(self.grik,0,2)
        self.pv = QCheckBox('PV')
        self.pv.setChecked(True)
        self.samples_layout.addWidget(self.pv,0,3)
        self.scnn = QCheckBox('Scnn1a')
        self.scnn.setChecked(True)
        self.samples_layout.addWidget(self.scnn,1,1)
        self.sst = QCheckBox('SST')
        self.sst.setChecked(True)
        self.samples_layout.addWidget(self.sst,1,2)
        self.vip = QCheckBox('VIP')
        self.vip.setChecked(True)
        self.samples_layout.addWidget(self.vip,1,3)
        self.leftcolumn.addLayout(self.samples_layout,5,0,1,3)
        # ---------------------------------------------------------------------------- #
        #                             alternative splicing                             #
        # ---------------------------------------------------------------------------- #
        # ---------------------------- chose analysis type --------------------------- #
        self.switch_gene_expression_layout = QHBoxLayout()
        self.switch_gene_expression_label = QLabel('Analysis Type')
        self.switch_gene_expression_label.setFont(myFont)
        self.switch_gene_expression_layout.addWidget(self.switch_gene_expression_label)
        self.switch_gene_expression = QButtonGroup()
        self.gene_expression = QRadioButton('gene expression')
        self.switch_gene_expression.addButton(self.gene_expression)
        self.gene_expression.clicked.connect(self.switch_gene_expression_clicked)
        self.gene_expression.setChecked(True)
        self.switch_gene_expression_layout.addWidget(self.gene_expression)
        self.alternative_splicing = QRadioButton('alternative splicing')
        self.switch_gene_expression.addButton(self.alternative_splicing)
        self.alternative_splicing.clicked.connect(self.switch_gene_expression_clicked)
        self.switch_gene_expression_layout.addWidget(self.alternative_splicing)
        self.leftcolumn.addLayout(self.switch_gene_expression_layout,6,0)
        # -------------------- select splicing events of interest -------------------- #
        self.splicing_events_layout = QGridLayout()
        self.splicing_events_label = QLabel('Splicing Events')
        self.splicing_events_label.setFont(myFont)
        self.splicing_events_layout.addWidget(self.splicing_events_label,0,0)
        self.ie= QCheckBox('Including Exon (IE)')
        self.splicing_events_layout.addWidget(self.ie,0,1)
        self.se = QCheckBox('Skipping Exon (SE)')
        self.splicing_events_layout.addWidget(self.se,0,2)
        self.me = QCheckBox('Mutually exclusive exon (MX)')
        self.splicing_events_layout.addWidget(self.me,0,3)
        
        self.ri = QCheckBox('Retained Intron (RI)')
        self.splicing_events_layout.addWidget(self.ri,1,1)
        self.a5= QCheckBox("Alternative 5' splice-site (A5)")
        self.splicing_events_layout.addWidget(self.a5,1,2)
        self.a3 = QCheckBox("Alternative 3' splice-site (A3)")
        self.splicing_events_layout.addWidget(self.a3,1,3)
        self.af = QCheckBox('Alternative first exon (AF)')
        self.splicing_events_layout.addWidget(self.af,2,1)
        self.splicing_events_checkboxes = [self.ie,self.se,self.me,self.ri,self.a5,self.a3,self.af]
        for checkbox in self.splicing_events_checkboxes:
            checkbox.setChecked(True)
            checkbox.setCheckable(False)
            checkbox.setToolTip("Select Analysis Type 'alternative splicing'")
        self.leftcolumn.addLayout(self.splicing_events_layout,7,0,1,4)


        # ---------------------------------- export ---------------------------------- #
        msg = QMessageBox()
        msg.setText('Select export folder')
        msg.setIcon(QMessageBox.Information)
        msg.setInformativeText('The gene count table will be saved in this folder..')
        msg.exec_()
        self.filepath_label = QLabel('Export Folder')
        self.filepath_label.setFont(myFont)
        self.leftcolumn.addWidget(self.filepath_label,8,0)
        self.filename_label = QLabel('Filename')
        self.filename_label.setFont(myFont)
        self.leftcolumn.addWidget(self.filename_label,8,2)
        self.filepath = QFileDialog.getExistingDirectory()
        self.filepath_show = QLabel(self.filepath)
        self.leftcolumn.addWidget(self.filepath_show,9,0)
        self.filepath_change = QPushButton('change')
        self.filepath_change.clicked.connect(self.change_filepath)
        self.leftcolumn.addWidget(self.filepath_change,9,1)
        self.filename = QLineEdit('gene_count_data')
        self.leftcolumn.addWidget(self.filename,9,2)
        self.save_btn = QPushButton('export')
        self.save_btn.clicked.connect(self.save)
        self.leftcolumn.addWidget(self.save_btn,9,3)
        # --------------------------------- Citation --------------------------------- #
        self.citationlayout = QVBoxLayout()
        smallFont=QtGui.QFont()
        smallFont.setPointSize(10)
        self.original_study_label = QLabel('Original Study')
        self.original_study_label.setFont(myFont)
        self.citationlayout.addWidget(self.original_study_label)
        urlLink="<a href=\"https://doi.org/10.1038/s41593-019-0465-5\">Furlanis, E., Traunmüller, L., Fucile, G. et al., Nat Neurosci 22 (2019)</a>" 
        self.original_study = QLabel(urlLink)
        self.original_study.setOpenExternalLinks(True)
        self.original_study.setFont(smallFont)
        self.citationlayout.addWidget(self.original_study)
        self.original_data_label = QLabel('Raw Data')
        self.original_data_label.setFont(myFont)
        self.citationlayout.addWidget(self.original_data_label)
        urlLink2="<a href=\"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE133291\">FASTA files</a>" 
        self.original_data = QLabel(urlLink2)
        self.original_data.setOpenExternalLinks(True)
        self.original_data.setFont(smallFont)
        self.citationlayout.addWidget(self.original_data)
        smallerFont = smallFont
        smallerFont.setPointSize(8)
        smallerFont.setItalic(True)
        self.copyright = QLabel('© Stephan Weißbach, 2022 - version 0.02')
        self.copyright.setFont(smallerFont)
        self.citationlayout.addWidget(self.copyright)
        self.rightcolumn.addLayout(self.citationlayout,6,2)
        self.mainwindowlayout.addLayout(self.leftcolumn,0,0)
        self.mainwindowlayout.addLayout(self.rightcolumn,0,1)
    # ---------------------------------------------------------------------------- #
    #                                Button Methods                                #
    # ---------------------------------------------------------------------------- #
    def input_changed(self) -> None:
        if len(self.input_field.text()) == 18:
            if self.input_field.text() in self.gene_count_table.ensembl_to_gene_symbol.keys():
                self.gene_id.setText(self.gene_count_table.ensembl_to_gene_symbol[self.input_field.text()])
        else:
            self.gene_id.setText('')
    
    def geneid_changed(self) -> None:
        if self.gene_id.text() in self.gene_count_table.gene_symbol_to_ensembl.keys():
            self.input_field.setText(self.gene_count_table.gene_symbol_to_ensembl[self.gene_id.text()])
        else:
            self.input_field.setText('')

    def add_to_list_func(self) -> None:
        if self.input_field.text() not in self.gene_count_table.ensembl_to_gene_symbol.keys():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Gene is not in the data.")
            msg.setInformativeText('Please select valid gene. Make sure to use the ENSMBL Gene ID for mouse.')
            msg.setWindowTitle("Gene not found.")
            msg.exec_()
            return
        if self.input_field.text() not in self.selected_genes:
            self.selected_genes.append(self.input_field.text())
            self.selected_genes_list.addItem(f'{self.input_field.text()} ({self.gene_count_table.ensembl_to_gene_symbol[self.input_field.text()]})')
        self.input_field.setText('')
        self.gene_id.setText('')
    
    def delete_item(self) -> None:
        idx = self.selected_genes_list.currentRow()
        gene = self.selected_genes_list.currentItem().text().split(' ')[0]
        _ = self.selected_genes_list.takeItem(idx)
        self.selected_genes.remove(gene)
        self.delete.setEnabled(False)
    
    def activate_delete(self) -> None:
        self.delete.setEnabled(True)

    def radiobutton_pressed(self) -> None:
        if self.inhibitory_select.isChecked() and self.crtx_select.isChecked():
            #pv,vip,sst
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
            for button in [self.pv, self.scnn, self.sst, self.camk, self.vip, self.grik]:
                button.setCheckable(True)
                button.setChecked(True)
        
    def change_filepath(self):
        self.filepath = QFileDialog.getExistingDirectory()
        self.filepath_show.setText(self.filepath)
    
    def switch_gene_expression_clicked(self):
        to_set = False if self.gene_expression.isChecked() else True
        for checkbox in self.splicing_events_checkboxes:
            checkbox.setCheckable(to_set)
            checkbox.setChecked(True)
            if to_set:
                checkbox.setToolTip('')
            else:
                checkbox.setToolTip("Select Analysis Type 'alternative splicing'")
    
    def no_splice_events(self,gene):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("No splice-variants")
        msg.setText(f'No splice-variants for {gene} ({self.gene_count_table.ensembl_to_gene_symbol[gene]}) with your current selection.')
        msg.exec_()

    def save(self):
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
        # ----------------------- check if export filename set ----------------------- #
        if self.filename.text() == '':
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Filename cannot be empty.")
            msg.setWindowTitle("Filename empty")
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
        # ------------------------- export count table as csv ------------------------ #
        selected_samples = []
        if self.pv.isChecked():
            selected_samples += ['PV_1', 'PV_2','PV_3', 'PV_4']
        if self.scnn.isChecked():
            selected_samples += ['Scnn_1', 'Scnn_2', 'Scnn_3', 'Scnn_4']
        if self.sst.isChecked():
            if self.hipp_select.isChecked():
                selected_samples += ['SST_1','SST_2', 'SST_3', 'SST_4']
            elif self.crtx_select.isChecked():
                selected_samples += ['SST_W2', 'SST_W3', 'SST_W5', 'SST_W1']
            else:
                selected_samples += ['SST_1','SST_2', 'SST_3', 'SST_4','SST_W2', 'SST_W3', 'SST_W5', 'SST_W1']
        if self.camk.isChecked():
            if self.hipp_select.isChecked():
                selected_samples += ['CamK_W2', 'CamK_W3', 'CamK_W4', 'CamK_W5']
            elif self.crtx_select.isChecked():
                selected_samples += ['CamK_1', 'CamK_2', 'CamK_3', 'CamK_4']
            else:
                selected_samples += ['CamK_1', 'CamK_2', 'CamK_3', 'CamK_4','CamK_W2', 'CamK_W3', 'CamK_W4', 'CamK_W5']
        if self.vip.isChecked():
            selected_samples += ['VIP_W1', 'VIP_W2', 'VIP_W3', 'VIP_W4']
        if self.grik.isChecked():
            selected_samples += ['Grik_W3', 'Grik_W4', 'Grik_W5', 'Grik_W6']
        if self.gene_expression.isChecked():
            df = self.gene_count_table.return_df(self.selected_genes,selected_samples)
            df.to_csv(os.path.join(self.filepath,f'{self.filename.text()}.csv'),index=False)
                
        else:
            selected_splice_events = []
            for button in self.splicing_events_checkboxes:
                if not button.isChecked(): continue
                selected_splice_events.append(button.text().split('(')[1][:-1])
            if len(selected_splice_events) == 0:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("No Splice Events selected")
                msg.setText(f"Select at least one splice event for export.")
                msg.exec_()
                return
            df = self.gene_count_table.return_alternative_splicing_df(self,self.selected_genes,selected_samples,selected_splice_events)
            df.to_csv(os.path.join(self.filepath,f'{self.filename.text()}.csv'),index=False)
        # --------------------------- empty all selections --------------------------- #
        self.selected_genes = []
        self.selected_genes_list.clear()
        # -------------------- message to inform successful export ------------------- #
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Export successful")
        msg.setText(f"The file was exported to {os.path.join(self.filepath,f'{self.filename.text()}.csv')}")
        msg.exec_() 
    
