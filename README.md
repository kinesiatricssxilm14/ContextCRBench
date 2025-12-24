#### Overview
This repository contains the data and scripts for [ContextCRBench](https://arxiv.org/pdf/2511.07017).
#### 🔗 Quick Links
- Dataset Access: [data](https://drive.google.com/file/d/1pEvBisl0komPDG9Tb91B6L1SaR696Np2/view?usp=drive_link) (1.56G)
- Raw Data Access: [raw data](https://drive.google.com/file/d/1v774ZN4K6izWiHC8Oug6yl_NOcZL4W-w/view?usp=sharing) (6.16G)
- Experiment Results: [LLM results](https://drive.google.com/file/d/1UxA1OCJpBM5slACCeVCa3SG73svyZonR/view?usp=sharing) (72.7M)

#### 📂 Data Structure
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

#### 📊Data Distribution
### C

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| espressif/esp-idf | https://github.com/espressif/esp-idf | 15k+ | 95%+ | 6347 | 15619 |
| micropython/micropython | https://github.com/micropython/micropython | 16k+ | 85%+ | 6747 | 16979 |
| mpv-player/mpv | https://github.com/mpv-player/mpv | 16k+ | 85%+ | 8433 | 16085 |
| netdata/netdata | https://github.com/netdata/netdata | 19k+ | 70%+ | 10437 | 19932 |
| openssl/openssl | https://github.com/openssl/openssl | 27k+ | 75%+ | 13761 | 27110 |
| redis/redis | https://github.com/redis/redis | 13k+ | 70%+ | 8278 | 13870 |
| Genymobile/scrcpy | https://github.com/Genymobile/scrcpy | 5k+ | 60%+ | 2002 | 5941 |
| swaywm/sway | https://github.com/swaywm/sway | 8k+ | 95%+ | 5923 | 8623 |
| systemd/systemd | https://github.com/systemd/systemd | 36k+ | 85%+ | 18117 | 36820 |
| zephyrproject-rtos/zephyr | https://github.com/zephyrproject-rtos/zephyr | 87k+ | 90%+ | 31067 | 87462 |

### C++

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| aseprite/aseprite | https://github.com/aseprite/aseprite | 15k+ | 90%+ | 2606 | 5069 |
| duckdb/duckdb | https://github.com/duckdb/duckdb | 16k+ | 80%+ | 1256 | 16773 |
| godotengine/godot | https://github.com/godotengine/godot | 104k+ | 85%+ | 44847 | 104430 |
| grpc/grpc | https://github.com/grpc/grpc | 39k+ | 70%+ | 25081 | 39037 |
| hyprwm/Hyprland | https://github.com/hyprwm/Hyprland | 9k+ | 95%+ | 1 | 9687 |
| ocornut/imgui | https://github.com/ocornut/imgui | 8k+ | 85%+ | 3687 | 8505 |
| opencv/opencv | https://github.com/opencv/opencv | 27k+ | 85%+ | 19242 | 27117 |
| osquery/osquery | https://github.com/osquery/osquery | 8k+ | 65%+ | 6878 | 8574 |
| microsoft/terminal | https://github.com/microsoft/terminal | 18k+ | 90%+ | 8688 | 18707 |
| xbmc/xbmc | https://github.com/xbmc/xbmc | 26k+ | 85%+ | 19004 | 26558 |

### C#

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| dotnet/aspnetcore | https://github.com/dotnet/aspnetcore | 61k+ | 90%+ | 28965 | 61087 |
| duplicati/duplicati | https://github.com/duplicati/duplicati | 6k+ | 85%+ | 4407 | 6070 |
| files-community/Files | https://github.com/files-community/Files | 16k+ | 95%+ | 2805 | 16970 |
| QuantConnect/Lean | https://github.com/QuantConnect/Lean | 8k+ | 90%+ | 5109 | 8646 |
| OpenRA/OpenRA | https://github.com/OpenRA/OpenRA | 21k+ | 80%+ | 18987 | 21813 |
| dotnet/orleans | https://github.com/dotnet/orleans | 9k+ | 95%+ | 6867 | 9399 |
| ppy/osu | https://github.com/ppy/osu | 32k+ | 100% | 11386 | 32514 |
| PowerShell/PowerShell | https://github.com/PowerShell/PowerShell | 25k+ | 80%+ | 14527 | 25212 |
| microsoft/PowerToys | https://github.com/microsoft/PowerToys | 38k+ | 60%+ | 8869 | 38091 |
| dotnet/runtime | https://github.com/dotnet/runtime | 113k+ | 80%+ | 46493 | 113784 |

### Go

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| cli/cli | https://github.com/cli/cli | 10k+ | 95%+ | 2719 | 10650 |
| cockroachdb/cockroach | https://github.com/cockroachdb/cockroach | 143k+ | 90%+ | 58398 | 143321 |
| go-gitea/gitea | https://github.com/go-gitea/gitea | 33k+ | 80%+ | 14207 | 33972 |
| ethereum/go-ethereum | https://github.com/ethereum/go-ethereum | 31k+ | 80%+ | 22098 | 31455 |
| kubernetes/kubernetes | https://github.com/kubernetes/kubernetes | 130k+ | 95%+ | 97643 | 130996 |
| moby/moby | https://github.com/moby/moby | 49k+ | 95%+ | 41848 | 49683 |
| ollama/ollama | https://github.com/ollama/ollama | 9k+ | 90%+ | 1 | 9937 |
| prometheus/prometheus | https://github.com/prometheus/prometheus | 16k+ | 85%+ | 8334 | 16257 |
| hashicorp/terraform | https://github.com/hashicorp/terraform | 36k+ | 90%+ | 27390 | 36748 |
| pingcap/tidb | https://github.com/pingcap/tidb | 60k+ | 90%+ | 22138 | 60221 |

### Java

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| bazelbuild/bazel | https://github.com/bazelbuild/bazel | 25k+ | 80%+ | 12764 | 25652 |
| elastic/elasticsearch | https://github.com/elastic/elasticsearch | 125k+ | 95%+ | 66906 | 125232 |
| bumptech/glide | https://github.com/bumptech/glide | 5k+ | 90%+ | 4459 | 5484 |
| oracle/graal | https://github.com/oracle/graal | 10k+ | 90%+ | 3099 | 10893 |
| TeamNewPipe/NewPipe | https://github.com/TeamNewPipe/NewPipe | 12k+ | 80%+ | 5325 | 12111 |
| netty/netty | https://github.com/netty/netty | 14k+ | 95%+ | 10906 | 14952 |
| redisson/redisson | https://github.com/redisson/redisson | 6k+ | 100% | 3322 | 6506 |
| apache/rocketmq | https://github.com/apache/rocketmq | 9k+ | 95%+ | 2540 | 9267 |
| spring-projects/spring-boot | https://github.com/spring-projects/spring-boot | 44k+ | 95%+ | 24625 | 44814 |
| spring-projects/spring-framework | https://github.com/spring-projects/spring-framework | 34k+ | 95%+ | 26332 | 34628 |

### JavaScript

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| expressjs/express | https://github.com/expressjs/express | 6k+ | 95%+ | 4500 | 6408 |
| fastify/fastify | https://github.com/fastify/fastify | 6k+ | 90%+ | 2771 | 6020 |
| jquery/jquery | https://github.com/jquery/jquery | 5k+ | 90%+ | 4821 | 5641 |
| nodejs/node | https://github.com/nodejs/node | 57k+ | 60%+ | 5560 | 10121 |
| parcel-bundler/parcel | https://github.com/parcel-bundler/parcel | 10k+ | 80%+ | 36716 | 57586 |
| mozilla/pdf.js | https://github.com/mozilla/pdf.js | 19k+ | 70%+ | 12802 | 19703 |
| facebook/react | https://github.com/facebook/react | 32k+ | 65%+ | 20528 | 32711 |
| sveltejs/svelte | https://github.com/sveltejs/svelte | 15k+ | 70%+ | 5843 | 15589 |
| mrdoob/three.js | https://github.com/mrdoob/three.js | 30k+ | 60%+ | 20987 | 30778 |
| webpack/webpack | https://github.com/webpack/webpack | 19k+ | 95%+ | 12300 | 19351 |

### Python

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| apache/airflow | https://github.com/apache/airflow | 48k+ | 90%+ | 13417 | 48107 |
| ansible/ansible | https://github.com/ansible/ansible | 84k+ | 85%+ | 73092 | 84880 |
| comfyanonymous/ComfyUI | https://github.com/comfyanonymous/ComfyUI | 7k+ | 95%+ | 1 | 7357 |
| home-assistant/core | https://github.com/home-assistant/core | 141k+ | 100% | 44722 | 141168 |
| python/cpython | https://github.com/python/cpython | 131k+ | 60%+ | 24032 | 131601 |
| keras-team/keras | https://github.com/keras-team/keras | 21k+ | 100% | 14340 | 21082 |
| tensorflow/models | https://github.com/tensorflow/models | 13k+ | 85%+ | 9599 | 13556 |
| pandas-dev/pandas | https://github.com/pandas-dev/pandas | 61k+ | 90%+ | 38871 | 61167 |
| huggingface/transformers | https://github.com/huggingface/transformers | 36k+ | 95%+ | 9373 | 36910 |
| vllm-project/vllm | https://github.com/vllm-project/vllm | 15k+ | 85%+ | 1 | 15353 |

### Rust

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| bevyengine/bevy | https://github.com/bevyengine/bevy | 18k+ | 90%+ | 1182 | 18473 |
| meilisearch/meilisearch | https://github.com/meilisearch/meilisearch | 5k+ | 95%+ | 1153 | 5450 |
| pola-rs/polars | https://github.com/pola-rs/polars | 21k+ | 65%+ | 247 | 21890 |
| astral-sh/ruff | https://github.com/astral-sh/ruff | 16k+ | 95%+ | 1 | 16908 |
| rustdesk/rustdesk | https://github.com/rustdesk/rustdesk | 11k+ | 60%+ | 9 | 11208 |
| swc-project/swc | https://github.com/swc-project/swc | 10k+ | 95%+ | 1308 | 10247 |
| tauri-apps/tauri | https://github.com/tauri-apps/tauri | 13k+ | 80%+ | 1132 | 13049 |
| vercel/turborepo | https://github.com/vercel/turborepo | 10k+ | 75%+ | 1 | 10218 |
| astral-sh/uv | https://github.com/astral-sh/uv | 12k+ | 95%+ | 1 | 12387 |
| zed-industries/zed | https://github.com/zed-industries/zed | 27k+ | 95%+ | 1 | 27292 |

### TypeScript

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| angular/angular | https://github.com/angular/angular | 60k+ | 85%+ | 40290 | 60501 |
| excalidraw/excalidraw | https://github.com/excalidraw/excalidraw | 9k+ | 90%+ | 2693 | 9289 |
| n8n-io/n8n | https://github.com/n8n-io/n8n | 14k+ | 90%+ | 1298 | 14089 |
| nuxt/nuxt | https://github.com/nuxt/nuxt | 31k+ | 95%+ | 8575 | 31488 |
| microsoft/playwright | https://github.com/microsoft/playwright | 35k+ | 90%+ | 4862 | 35306 |
| strapi/strapi | https://github.com/strapi/strapi | 23k+ | 80%+ | 9024 | 23202 |
| supabase/supabase | https://github.com/supabase/supabase | 34k+ | 60%+ | 464 | 34318 |
| Eugeny/tabby | https://github.com/Eugeny/tabby | 10k+ | 75%+ | 3277 | 10383 |
| typeorm/typeorm | https://github.com/typeorm/typeorm | 11k+ | 95%+ | 7238 | 11350 |
| vitejs/vite | https://github.com/vitejs/vite | 19k+ | 80%+ | 1277 | 19690 |

### Ruby (Not used in the paper because the number after filtering is not enough)

| full_name | link | issue# | programming purity | issue# after 2021 | last number till crawling |
|---|---|---:|---:|---:|---:|
| Homebrew/brew | https://github.com/Homebrew/brew | 19k+ | 90%+ | 10192 | 19572 |
| chef/chef | https://github.com/chef/chef | 14k+ | 95%+ | 10811 | 14914 |
| fastlane/fastlane | https://github.com/fastlane/fastlane | 29k+ | 80%+ | 17890 | 29511 |
| jekyll/jekyll | https://github.com/jekyll/jekyll | 9k+ | 70%+ | 8528 | 9790 |
| mastodon/mastodon | https://github.com/mastodon/mastodon | 34k+ | 60%+ | 15474 | 34240 |
| rails/rails | https://github.com/rails/rails | 54k+ | 95%+ | 40990 | 54802 |
| rubocop/rubocop | https://github.com/rubocop/rubocop | 14k+ | 95%+ | 9321 | 14023 |
| sidekiq/sidekiq | https://github.com/sidekiq/sidekiq | 6k+ | 85%+ | 4772 | 6656 |
| spree/spree | https://github.com/spree/spree | 12k+ | 75%+ | 10639 | 12544 |
| hashicorp/vagrant | https://github.com/hashicorp/vagrant | 13k+ | 80%+ | 12126 | 13630 |

#### 📖Citation Format
```
@article{hu2025benchmarking,
  title={Benchmarking LLMs for Fine-Grained Code Review with Enriched Context in Practice},
  author={Hu, Ruida and Wang, Xinchen and Wen, Xin-Cheng and Zhang, Zhao and Jiang, Bo and Gao, Pengfei and Peng, Chao and Gao, Cuiyun},
  journal={arXiv preprint arXiv:2511.07017},
  year={2025}
}
```
