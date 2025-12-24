import os
import json

# type = 1表示base
# type = 2表示base + issue
# type = 3表示base + pr
# type = 4表示base + issue + pr
# type = 5表示base + content_before
# type = 6表示base + content_after
# type = 7表示base + content_before + content_after
# type = 8表示base + issue + pr + content_before + content_after

with open('task1_prefix.txt', 'r') as r1:
    task1_prefix = r1.read()

with open('task2_prefix.txt', 'r') as r2:
    task2_prefix = r2.read()

with open('task3_prefix.txt', 'r') as r3:
    task3_prefix = r3.read()

# with open('task2_prefix_multiple.txt', 'r') as r4:
#     task2_prefix_multiple = r4.read()

def get_task(data, task_type=1, type=1):
    # with open(json_path, 'r') as r1:
    #     data = json.load(r1)
    system_prompt = ''
    res = ''
    if task_type == 1:
        system_prompt = task1_prefix
        # res = task1_prefix
    elif task_type == 2:
        system_prompt = task2_prefix
        # res = task2_prefix
    elif task_type == 3:
        system_prompt = task3_prefix
        # res = task3_prefix
    # elif task_type == 4:
    #     system_prompt = task2_prefix_multiple

    res += "The full name of the repository is:\n"
    res += data['full_name']
    res += '\n'
    res += "It is a repository for the following programming language:\n"
    res += data['lang']
    res += '\n'
    if task_type == 1:
        res += "The diff hunk is:\n"
        res += data['diff_hunk']
    else:
        res += "The diff hunk with line number is:\n"
        res += data['diff_hunk_content_with_line_number']
    res += '\n'
    res += "The diff hunk head is:\n"
    res += data['diff_hunk_head']
    res += '\n'
    if task_type == 3:
        res += f'''You need to comment following line(s):
{data['comment_lines']}

Note:
- Here, each line is represented in the format `[][]`. The number in the left `[]` indicates the line number in the code before the change (leave it blank if the line did not exist before), and the number in the right `[]` indicates the line number in the code after the change (leave it blank if the line was deleted after the change).\n'''

    if type == 2:
        res += "The issue corresponding to this diff hunk is:\n"
        res += "issue title is:\n"
        res += data['issue_title']
        res += '\n'
        res += "issue body is:\n"
        res += data['issue_body'] if data['issue_body'] is not None else ''
        res += '\n'
    if type == 3:
        res += "The pull request corresponding to this diff hunk is:\n"
        res += "pull request title is:\n"
        res += data['pr_title']
        res += '\n'
        res += "pull request body is:\n"
        res += data['pr_body'] if data['pr_body'] is not None else ''
        res += '\n'
    if type == 4:
        res += "The issue corresponding to this diff hunk is:\n"
        res += "issue title is:\n"
        res += data['issue_title']
        res += '\n'
        res += "issue body is:\n"
        res += data['issue_body'] if data['issue_body'] is not None else ''
        res += '\n'
        res += "The pull request corresponding to this diff hunk is:\n"
        res += "pull request title is:\n"
        res += data['pr_title']
        res += '\n'
        res += "pull request body is:\n"
        res += data['pr_body'] if data['pr_body'] is not None else ''
        res += '\n'
    if type == 5:
        res += "The code context before the modification (the complete function/class or neighboring code containing the diff hunk) is:\n"
        res += data['snippet_before']
        res += '\n'
        res += 'Note:\n'
        res += '- The "context" refers to the complete function, class, or neighboring code where the diff hunk is located, both before and after the modification.\n'
    if type == 6:
        res += "The code context after the modification (the complete function/class or neighboring code containing the diff hunk) is:\n"
        res += data['snippet_after']
        res += '\n'
        res += 'Note:\n'
        res += '- The "context" refers to the complete function, class, or neighboring code where the diff hunk is located, both before and after the modification.\n'
    if type == 7:
        res += "The code context before the modification (the complete function/class or neighboring code containing the diff hunk) is:\n"
        res += data['snippet_before']
        res += '\n'
        res += "The code context after the modification (the complete function/class or neighboring code containing the diff hunk) is:\n"
        res += data['snippet_after']
        res += '\n'
        res += 'Note:\n'
        res += '- The "context" refers to the complete function, class, or neighboring code where the diff hunk is located, both before and after the modification.\n'
    
    if type == 8:
        res += "The issue corresponding to this diff hunk is:\n"
        res += "issue title is:\n"
        res += data['issue_title']
        res += '\n'
        res += "issue body is:\n"
        res += data['issue_body'] if data['issue_body'] is not None else ''
        res += '\n'
        res += "The pull request corresponding to this diff hunk is:\n"
        res += "pull request title is:\n"
        res += data['pr_title']
        res += '\n'
        res += "pull request body is:\n"
        res += data['pr_body'] if data['pr_body'] is not None else ''
        res += '\n'
        res += "The code context before the modification (the complete function/class or neighboring code containing the diff hunk) is:\n"
        res += data['snippet_before']
        res += '\n'
        res += "The code context after the modification (the complete function/class or neighboring code containing the diff hunk) is:\n"
        res += data['snippet_after']
        res += '\n'
        res += 'Note:\n'
        res += '- The "context" refers to the complete function, class, or neighboring code where the diff hunk is located, both before and after the modification.\n'
    if task_type == 2:
        res += 'The elements in the "lines" array can only be selected from the line markers below. No other formats or line markers are allowed; otherwise, they will not match.\n'
        id = data['id']
        with open(f'/data00/rdhu/ASE_data/final_json/{id}.json', 'r') as r1:
            x = json.load(r1)
        all_line_number = x['all_line_number']
        res += json.dumps(all_line_number)
        res += '\n'
    res += 'Note: Only output the JSON result. Do not output any other text, explanation, or formatting!'
    return system_prompt, res

# json_list = list()
# root_path = '/data00/rdhu/ASE_data/final_json'
# for file_path in [os.path.join(root_path, x) for x in os.listdir(root_path)]:
#     print(file_path)
#     with open(file_path, 'r') as r1:
#         data = json.load(r1)
#     json_list.append(file_path)


prompt = dict()
task = 1
type = 8

# with open('/data00/rdhu/ASE_data/sampled_unmerged_data_multiple_lines_task2.jsonl', 'r') as r1:
#     lines = r1.readlines()
# with open('/data00/rdhu/ASE_data/sampled_unmerged_data_single_lines_task2.jsonl', 'r') as r2:
#     lines.extend(r2.readlines())
with open('/data00/rdhu/ASE_data/run_llm/task1/final_task1.json', 'r') as r1:
    lines = r1.readlines()
for line in lines:
    data = json.loads(line)
    id = data['id']
    prompt[id] = dict()
    prompt[id]['system_prompt'], prompt[id]['user_prompt'] = get_task(data, task, type)
    # prompt[id]['ground_truth'] = data['review_comment']
    # prompt[id]['ground_truth'] = data['comment_lines']
    prompt[id]['ground_truth'] = data['merged']

if not os.path.exists(f'task{task}'):
    os.system(f'mkdir task{task}')
with open(f'task{task}/prompt_{type}.json', 'w') as w1:
    w1.write(json.dumps(prompt, indent=4))