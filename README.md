#### Overview
This repository contains the data and scripts for the ContextCRBench dataset.
#### 🔗 Quick Links
- Dataset Access: https://drive.google.com/file/d/1pEvBisl0komPDG9Tb91B6L1SaR696Np2/view?usp=drive_link
- Raw Data from GitHub: 
- Experiment Scripts: [code_review_script](https://github.com/kinesiatricssxilm14/ContextCRBench/tree/main/code_review_script)
- Experiment Results: [Link to the directory or file with results]

#### 📂 Data Structure
Here is an overview of the directory and data structure:
```
/
├── data/
│   ├── processed_data/           # Processed data used in experiments
│   └── raw_data/                 # Raw data crawled from GitHub
├── scripts/
│   ├── run_experiments.sh        # Main script to run all experiments
│   └── data_crawler.py           # Script for crawling GitHub data
├── results/
│   └── experiment_summary.csv    # Summary of experiment results
└── README.md
```

#### ⚙️ Scripts
- Data Crawling Script: `scripts/data_crawler.py`
  - This script is used to crawl the raw data from GitHub.
  - Usage: `python scripts/data_crawler.py --output_dir data/raw_data`
- Experiment Script: `scripts/run_experiments.sh`
  - This script runs the main experiments.
  - Usage: `bash scripts/run_experiments.sh`
#### 📊 Results
The results of our experiments are located in the `results/` directory. For a detailed summary, please see `results/experiment_summary.csv`.
