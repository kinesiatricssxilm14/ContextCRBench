# -*- coding: utf-8 -*-
# pip install nltk rouge-score python-Levenshtein

import Levenshtein
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
import json
import os

for i in [1,2,3,4,5,6,7,8]:
    bleu = 0
    rouge1 = 0
    rouge2 = 0
    rougeL = 0
    edit_sim = 0
    file_path = f'task3/prompt_{i}_answer_aws_claude35_sonnet.jsonl'
    # aws_claude35_sonnet gpt-3.5 gpt-4-32k-0613 gpt-4o-2024-05-13
    # qwen/qwen-2.5-coder-32b-instruct
    # qwen2.5-coder-14b-instruct
    # qwen2.5-coder-7b-instruct
    # deepseek/deepseek-chat
    # anthropic/claude-3.5-haiku
    # mistralai/codestral-2501
    model_name = 'aws_claude35_sonnet'
    with open(file_path, 'r') as r1:
        lines = r1.readlines()
    for line in lines:
        data = json.loads(line)
        try:
            s1 = json.loads(data[model_name])['comment']
            s2 = '\n'.join(data['ground_truth'])
        except:
            s1 = data[model_name]
            s2 = '\n'.join(data['ground_truth'])

        bleu += sentence_bleu([s1.split()], s2.split(), smoothing_function=SmoothingFunction().method1)

        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        rouge = scorer.score(s1, s2)

        rouge1 += rouge['rouge1'].fmeasure
        rouge2 += rouge['rouge2'].fmeasure
        rougeL += rouge['rougeL'].fmeasure
        edit_sim += (1 - Levenshtein.distance(s1, s2) / max(len(s1), len(s2)))
    # print(bleu/len(lines)*100)
    # print(rouge1/len(lines)*100)
    # print(rouge2/len(lines)*100)
    print(rougeL/len(lines)*100)
    # print(edit_sim/len(lines)*100)
        # print(f"BLEU: {bleu:.4f}")
        # print(f"ROUGE-1: {rouge['rouge1'].fmeasure:.4f}")
        # print(f"ROUGE-2: {rouge['rouge2'].fmeasure:.4f}")
        # print(f"ROUGE-L: {rouge['rougeL'].fmeasure:.4f}")
        # print(f"Edit Similarity: {edit_sim:.4f}")
