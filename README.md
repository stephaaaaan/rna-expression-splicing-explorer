# rna-expression-splicing-explorer
A simple programm to access RNA expression and alternative splicing profiles for different celltypes of mouse cortex and hippocampus. 

## Functionality
1. Select genes of interest via Genesymbol or ENSEMBL ID
2. Select Brainregion and/or celltypes or samples directly
3. Select analysis type (gene expression / alternative splicing)
The programm will export a csv/xlsx file including the <b>counts per million</b> (gene expression) or <b>percentage spliced in</b> (alternative splicing) 
values for all selected genes. An interactive heatmap representing gene expression values of all selected genes is generated within the programm.
![Screenshot of the GUI](https://github.com/stephaaaaan/rna-expression-splicing-explorer/blob/main/src/pics/gui_screenshot.png)

## Celltypes included
The celltypes are:
- excitatory
  - CamK2 (Hippocampus, Cortex)
  - Grik4 (Hippocampus)
  - Scnn1a (Cortex)
- inhibitory
  - SST (Hippocampus, Cortex)
  - PV (Cortex)
  - VIP (Cortex)

![celltypes included](https://github.com/stephaaaaan/rna-expression-splicing-explorer/blob/main/src/pics/overview_figure.png)
Raw data is available at: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE133291 (Furlanis et al., 2019)

## Gene Expression
The gene expression analysis was done with [STAR Aligner](https://github.com/alexdobin/STAR). 
In the output file there are the following columns:
- Sample: The sample id is build as `<celltype>_<celltype_samplenumber>`
- ESEMBL Gene ID
- Gene Symbol
- Brainregion: `hipp` for hippocampus and `crtx` for cortex
- Celltype: `excitatory` and `inhibitory`
- gene count: in counts per million

## Alternative Splicing 
The alternative splicing analysis was done with [SUPPA 2](https://github.com/comprna/SUPPA). There are seven splicing events that can be detected.
In the output file each event is defined as:
- Sample: The sample id is build as `<celltype>_<celltype_samplenumber>`
- ESEMBL Gene ID
- Gene Symbol
- Brainregion: `hipp` for hippocampus and `crtx` for cortex
- Celltype: `excitatory` and `inhibitory` 
- Splice Event: 
  - `IE`: Including Exon
  - `SE`: Skipping Exon
  - `MX`: Mutually exclusive exon
  - `RI`: Retained Intron
  - `A5`: Alternative 5' splice-site
  - `A3`: Alternative 3' splice-site
  - `AF`: Alternative first exon
- chr: chromsome
- event position: exact position of splice event (and its alternative version) on the chromsome. See the image below describing how to read the coordinates for each splicing event
- strand: `+` for 5'->3' direction and `-` for 5'<-3' direction
- psi: percentage spliced in of the orange pathway in the splice graph depicted below
![5' Splice Graphs](https://github.com/stephaaaaan/rna-expression-splicing-explorer/blob/main/src/pics/splicegraphs_5'.svg)
![3' Splice Graphs](https://github.com/stephaaaaan/rna-expression-splicing-explorer/blob/main/src/pics/splicegraphs_3'.svg)
