import json
import os
import re

def extract_first_two_numbers(s):
    # 检查格式
    # if not s.startswith('['):
    #     return None, None
    first_close = s.find(']')
    # if first_close == -1:
    #     return None, None
    # if len(s) <= first_close + 1 or s[first_close + 1] != '[':
    #     return None, None
    second_close = s.find(']', first_close + 2)
    # if second_close == -1:
    #     return None, None
    # 提取a和b
    a = s[1:first_close]
    b = s[first_close + 2:second_close]
    return a, b

def fix_json_string(s):
    # 只转义 `...` 里的双引号
    def replacer(match):
        inner = match.group(1)
        return '`' + inner.replace('"', '\\"') + '`'
    # 替换所有 `...` 里的内容
    s = re.sub(r'`([^`]*)`', replacer, s)
    return s

def get_index(all_line_number, element):
    if element in all_line_number:
        return all_line_number.index(element)
    a, b = extract_first_two_numbers(element)
    if a is not None:
        for aln in all_line_number:
            # c, d = extract_a_b(aln)
            c, d = extract_first_two_numbers(aln)
            if a == c:
                return all_line_number.index(aln)
    if b is not None:
        for aln in all_line_number:
            # c, d = extract_a_b(aln)
            c, d = extract_first_two_numbers(aln)
            if b == d:
                return all_line_number.index(aln)
    if a is not None and len(a) > 0:
        tmp = 1000000
        res_aln = all_line_number[0]
        for aln in all_line_number:
            c, d = extract_first_two_numbers(aln)
            if c is None or len(c) == 0:
                continue
            if abs(int(a) - int(c)) < tmp:
                tmp = abs(int(a) - int(c))
                res_aln = aln
        return all_line_number.index(res_aln)
    if b is not None and len(b) > 0:
        tmp = 1000000
        res_aln = all_line_number[0]
        for aln in all_line_number:
            c, d = extract_first_two_numbers(aln)
            if d is None or len(d) == 0:
                continue
            if abs(int(b) - int(d)) < tmp:
                tmp = abs(int(b) - int(d))
                res_aln = aln
        return all_line_number.index(res_aln)

    return -1

import re
def escape_reason_quotes(s):
    # 定义替换函数
    def replacer(match):
        prefix = match.group(1)  # "reason": "
        content = match.group(2) # XXX
        suffix = match.group(3)  # "
        # 替换内容里的 " 为 \"
        content_escaped = content.replace('"', r'\"')
        return f'{prefix}{content_escaped}{suffix}'
    # 匹配所有 "reason": "XXX"
    pattern = r'("reason":\s*")(.*)(")'
    # 需要支持内容里有双引号，所以用非贪婪匹配
    # pattern = r'("reason":\s*")((?:[^"\\]|\\.)*)(")'
    # 用re.sub替换所有匹配
    return re.sub(pattern, replacer, s)

for i in range(1,9):
    file_path = f'/data00/rdhu/ASE_data/run_llm/task2/prompt_{i}_answer_qwen2_5_coder_7b_instruct.json'
    right = 0
    res = 0
    cnt = 0
    cnt_perfect = 0
    with open(file_path, 'r') as r1:
        for line in r1.readlines():
            # try:
            # print(i)
            try:
                data = json.loads(line)
            except:
                continue
            # aws_claude35_sonnet gpt-3.5 gpt-4-32k-0613 gpt-4o-2024-05-13
            # qwen/qwen-2.5-coder-32b-instruct
            # qwen2.5-coder-14b-instruct
            # qwen2.5-coder-7b-instruct
            # deepseek/deepseek-chat
            # anthropic/claude-3.5-haiku
            # mistralai/codestral-2501
            ref_data = data['qwen2.5-coder-7b-instruct']
            # print(data['index'])
            if ref_data.splitlines()[0].startswith('```'):
                try:
                    answer = json.loads('\n'.join(ref_data.splitlines()[1:-1]).replace('\t', '\\t'))
                except:
                    continue
            else:
                # print(repr(escape_reason_quotes(ref_data)))
                # answer = json.loads(escape_reason_quotes(ref_data).replace('\t', '\\t'))
                try:
                    answer = json.loads(ref_data)
                except:
                    try:
                        answer = json.loads(escape_reason_quotes(ref_data))
                    except:
                        continue
            line_answer = answer['lines']
            # line_answer = json.loads(line_answer)
            if data['ground_truth'][0] in line_answer[:10]:
                cnt_perfect += 1
            cnt += 1
            # id = data['index']
            # with open(f'/data00/rdhu/ASE_data/final_json/{id}.json', 'r') as r1:
            #     data1 = json.load(r1)
            # all_line_number = data1['all_line_number']
            # try:
            #     index = get_index(all_line_number, line_answer)
            # except:
            #     continue
            # if index != -1:
            #     right_answer = all_line_number.index(data['ground_truth'][0])
            #     # res += (abs(index - right_answer) / len(all_line_number))
            #     res += abs(index - right_answer)
            #     cnt += 1
            # else:
            #     # res += len(all_line_number)
            #     res += 1
            #     cnt += 1
                # else:
                #     res += 1
                #     cnt += 1
            # except Exception as e:
            #     print(f'Error {e}')
            # finally:
            #     i += 1

    # print(res)
    # print(cnt)
    # print(res / cnt)
    # print(cnt)
    # print(cnt_perfect)
    print(cnt_perfect)