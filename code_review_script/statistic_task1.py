import os
import json
import re
from sklearn.metrics import matthews_corrcoef

def extract_code_blocks(text):
    """
    提取被三反引号包围的内容（支持可选的格式标记）。
    返回一个列表，每个元素是一个代码块的内容。
    """
    # 正则说明：
    # - ``` 匹配三反引号
    # - (\w+)? 匹配可选的格式标记（如json、python等）
    # - [ \t]* 匹配可选的空格或制表符
    # - \n 匹配换行
    # - (.*?) 非贪婪匹配代码块内容
    # - ``` 匹配结尾的三反引号
    pattern = r"```(?:\w+)?[ \t]*\n(.*?)```"
    # re.DOTALL 让 . 匹配换行符
    return re.findall(pattern, text, re.DOTALL)

def f1_score(tp, fp, fn):
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    if precision + recall == 0:
        return 0
    return 2 * precision * recall / (precision + recall)

task = 1
for i in [1,2,3,4,5,6,7,8]:
    # print('*'*10 + str(i) + '*'*10)
    # model_name = 'gpt-4o-2024-05-13'
    # model_name = 'aws_claude35_sonnet'
    # model_name = 'gpt-4-32k-0613'
    model_name = 'gpt-3.5'
    # model_name = 'mistralai/codestral-2501'
    # model_name = 'deepseek/deepseek-chat'
    # model_name = 'qwen/qwen-2.5-coder-32b-instruct'
    # model_name = 'qwen2.5-coder-7b-instruct'
    # model_name = 'qwen2.5-coder-14b-instruct'
    # file_path = f'/data00/rdhu/ASE_data/run_llm/task{task}/prompt_{type}_answer_{model_name.replace("-", "_").replace(".", "_")}.json'
    file_path = f'/data00/rdhu/ASE_data/run_llm/task1/prompt_{i}_answer_gpt_3_5.jsonl'
    with open(file_path, 'r') as r1:
        lines = r1.readlines()

    # cnt = 0
    # num_line = len(lines)

    # for select_lang in ['rust', 'python', 'go', 'c', 'cpp', 'c_sharp', 'typescript', 'java', 'javascript']:
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    y_true = []
    y_pred = []
    for line in lines:
        try:
            x = json.loads(line)
            # index = x['index']
            # with open(f'/data00/rdhu/ASE_data/final_json/{index}.json', 'r') as r1:
            #     tmp = json.load(r1)
            # if tmp['lang'] != select_lang:
            #     continue
            ground_truth = x['ground_truth']
            # print(x['index'])
            is_merged = x[model_name]
            if x[model_name].startswith('```'):
                is_merged = extract_code_blocks(x[model_name])[0]
            # print(is_merged)
            is_merged = json.loads(is_merged)['is_merged']
            # print(str(ground_truth))
            if str(ground_truth).lower() == 'true' and str(is_merged).lower() == 'true':
                tp += 1
                y_true.append(1)
                y_pred.append(1)
            elif str(ground_truth).lower() == 'true' and str(is_merged).lower() == 'false':
                fn += 1
                y_true.append(1)
                y_pred.append(0)
            elif str(ground_truth).lower() == 'false' and str(is_merged).lower() == 'true':
                fp += 1
                y_true.append(0)
                y_pred.append(1)
            else:
                tn += 1
                y_true.append(0)
                y_pred.append(0)
        except Exception as e:
            continue
                # print(f'Error: {x["index"]} - {e}')
        # print(select_lang)
        # print(f1_score(tp, fp, fn))



        # print(cnt)

        # print(num_line)
        # print(cnt / num_line)
        # print(tp)
        # print(fp)
        # print(tn)
        # print(fn)
    print(f1_score(tp, fp, fn)*100)
    # print((tp+tn)/(tp+tn+fn+fp)*100) # accuracy
    # print(tp/(tp+fp)*100) # precision
    # print(tp/(tp+fn)) # recall
    # print(matthews_corrcoef(y_true, y_pred)) #mcc

        # print(model_name)
        # print(task)
        # print(type)