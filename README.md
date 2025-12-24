#### Overview
This repository contains the data and scripts for the ContextCRBench dataset.
#### 🔗 Quick Links
- Dataset Access: [data](https://drive.google.com/file/d/1pEvBisl0komPDG9Tb91B6L1SaR696Np2/view?usp=drive_link)
- Raw Data Access: [raw data](https://drive.google.com/file/d/1v774ZN4K6izWiHC8Oug6yl_NOcZL4W-w/view?usp=sharing)
- Experiment Results: [LLM results](https://drive.google.com/file/d/1UxA1OCJpBM5slACCeVCa3SG73svyZonR/view?usp=sharing)

#### 📂 Data Structure
Here is an overview of the directory and data structure:
```
/
├── id                            # ID number
├── full_name                     # repository name, e.g., bevyengine/bevy
├── lang                          # programming language, e.g., rust
├── issue_number                  # issue number
├── issue_tilte                   # issue title
├── issue_body                    # issue body
├── issue_comment                 # issue comments(list)
│   ├── comment_1
│   ├── comment_2
│   ├── ...
│   └── comment_n
├── pr_number                     # pull request number
├── pr_title                      # pull request title
├── pr_body                       # pull request body
├── pr_comment                    # pull request comments(list)
│   ├── comment_1
│   ├── comment_2
│   ├── ...
│   └── comment_n
├── merged                        # if the pull request merged(true or false)
├── created_at                    # issue creation time
├── commit_id                     # commit sha
├── original_commit_id            # original commit sha
├── path                          # file path after
├── start_line                    # start line(if one line, it is null)
├── original_start_line           # original start line(if one line, it is null)
├── start_side                    # comment side(left means original side, right means new side, null means only one line)
├── line                          # line number of new side
├── original_line                 # line number of original side
├── side                          # left means original side, and right means new side
├── original_position             # line number of the original patch
├── position                      # line number of the patch
├── subject_type                  # comment type, line or file
├── review_comment                # review comment list
│   ├── comment_1
│   ├── comment_2
│   ├── ...
│   └── comment_n
├── diff_hunk                     # diff hunk
├── diff_hunk_head                # diff hunk head
├── diff_hunk_content             # diff hunk minus head
├── diff_hunk_content_with_line_number  # diff hunk content with line number
├── diff_hunk_original_start_line # original diff hunk start line
├── diff_hunk_original_end_line   # original diff hunk end line
├── diff_hunk_start_line          # diff hunk start line
├── diff_hunk_end_line            # diff hunk end line
├── file_path_before              # file path before
├── file_path_after               # file path after
├── comment_lines                 # comment line list
│   ├── line_number_1             # e.g., [][253], [254][], [255][254]
│   ├── line_number_2
│   ├── ...
│   └── line_number_n
├── content_before                # file before content
├── content_after                 # file after content
├── snippet_before                # corresponding function before
├── snippet_start_line_before     # corresponding function before start line
├── snippet_end_line_before       # corresponding function before end line
├── snippet_after                 # corresponding function after
├── snippet_start_line_after      # corresponding function after start line
├── snippet_end_line_after        # corresponding function after end line
└── all_line_number               # all possible line number list
    ├── line_number_1             # e.g., [][253], [254][], [255][254]
    ├── line_number_2
    ├── ...
    └── line_number_n
```

#### ⚙️ Scripts
- Data Crawling Script: [data_crawler](https://github.com/kinesiatricssxilm14/ContextCRBench/tree/main/download_script)
  - It is used to crawl the raw data from GitHub.
- Experiment Script: [code_review_script](https://github.com/kinesiatricssxilm14/ContextCRBench/tree/main/code_review_script)
  - It runs the main experiments and ablation study.
