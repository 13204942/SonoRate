# SonoRate

SonoRate is a lightweight clinician-centred pipeline for collecting and analysing clinician ratings of AI-generated predictions in medical imaging studies. The system provides a browser-based ranking interface for raters and automated scripts for processing rankings, conducting statistical analyses, and generating visualisations.

This repository accompanies our accepted MIUA 2026 paper:

> **SonoRate: A Clinician-Centred Pipeline for Annotation and Evaluation in Ultrasound AI Studies**

## Usage

### 1. Launch the rating interface

From the root directory, start a local HTTP server:
```bash
python3 -m http.server 8000
```

### 2. Open the rating interface

In a web browser, access one of the following pages:
```
http://161.116.4.112:8000/survey_app.html
```
or
```
http://161.116.4.112:8000/survey_app2.html
```
Clinicians can then complete the ranking tasks through the browser interface.

### 3. Organise collected results

After all ratings have been completed, place the exported rating files into the `data/` directory following the existing folder structure in this repository.
```text
data/
├── rater_1/
│   ├── hc18/
│   │   ├── results_case_1.txt
│   │   └── ...
│   ├── estt/
│       ├── results_case_1.txt
│       └── ...
│
├── rater_2/
│   ├── hc18/
│   │   ├── results_case_1.txt
│   │   └── ...
│   ├── estt/
│       ├── results_case_1.txt
│       └── ...
│
├── ...
```

* `hc18/`: clinician ratings collected on the HC18 dataset.
* `estcb/`: clinician ratings collected on the ES-TCB dataset.
* `expert/`: ratings from senior experts.
* `general/`: ratings from general clinicians.
* `non_expert/`: ratings from non-expert participants.
* Each CSV file should contain the ranking results exported from a single rater.


## Data Processing and Analysis

### Process ranking data
```bash
python src/rank_data_processor.py
```

### Perform statistical analysis
```bash
python rater_model_analysis_miua.py
```

### Generate visualisations
Subgroup ranking heatmaps:
```bash
python subgroup_ranking_heatmap.py
```

Top-1 selection frequency plots:
```bash
python top1_selection_frequency_plot.py
```

## Repository Structure
```
SonoRate/
├── data/                               # Collected rating results
├── src/
│   └── rank_data_processor.py          # Ranking data processing
├── survey_app.html                     # Rating interface
├── survey_app2.html                    # Alternative rating interface
├── rater_model_analysis_miua.py        # Statistical analysis
├── subgroup_ranking_heatmap.py         # Heatmap visualisation
└── top1 selection frequency plot.py    # Top-1 frequency plots
```

## Acknowledgements

We thank the developers of the VGG Image Annotator (VIA) for making their annotation framework openly available. The web-based rating interface in SonoRate was developed based on VIA and adapted for clinician-centred evaluation and ranking tasks in ultrasound AI studies.

VIA repository: https://github.com/ox-vgg/via


## Citation

If you use SonoRate in your research, please cite our MIUA 2026 paper.