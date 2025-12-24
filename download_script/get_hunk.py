import re
import json
import os
import sys
from package import PACKAGE_NAME

def add_lines_number(content, minus_start_number, minus_lines, add_start_number, add_lines):
    minus_start_number, minus_lines, add_start_number, add_lines = int(minus_start_number), int(minus_lines), int(add_start_number), int(add_lines)
    res = list()
    minus_number = minus_start_number
    add_number = add_start_number
    for line in content.splitlines():
        if line.startswith('+'):
            res.append(f'[][{add_number}] ' + line)
            add_number += 1
        elif line.startswith('-'):
            res.append(f'[{minus_number}][] ' + line)
            minus_number += 1
        else:
            res.append(f'[{minus_number}][{add_number}] ' + line)
            add_number += 1
            minus_number += 1
    return '\n'.join(res)
    
def extract_diff_hunks(content):
    file_blocks = re.split(r"^diff --git ", content, flags=re.MULTILINE)
    
    file_blocks = file_blocks[1:]
    
    result_files = []
    
    for block in file_blocks:
        file_path_match = re.match(r"a/(.*?) b/(.*?)\n", block)
        if file_path_match:
            file_path = file_path_match.group(1)
        else:
            file_path = None
        
        diff_hunks_matches = re.finditer(r"(@@ -\d+,\d+ \+\d+,\d+ @@.*?)(?=\n@@|\ndiff --git|\Z)", block, re.DOTALL)

        diff_hunks = []
        for match in diff_hunks_matches:
            hunk = match.group(1)
            nums = re.findall(r"-([\d]+),([\d]+) \+([\d]+),([\d]+)", hunk)
            lines_modified = nums[0] if nums else ()

            hunk_lines = hunk.splitlines()
            hunk_head = ''.join(hunk_lines[0].split('@@')[2:])
            content = '\n'.join(hunk_lines[1:])  
            content_with_line_number = add_lines_number(content, lines_modified[0], lines_modified[1], lines_modified[2], lines_modified[3])
            diff_hunks.append({
                "hunk": hunk,
                "lines_modified": lines_modified,
                "hunk_head": hunk_head,
                "content": content,
                "content_with_line_number": content_with_line_number,
            })
        
        result_files.append({
            "file_path": file_path,
            "diff_hunks": diff_hunks
        })
    
    return result_files

package = f'data/{PACKAGE_NAME.split("/")[1]}'

all_files = [os.path.join(package, x) for x in os.listdir(package) if x.endswith('.json')]
for file in all_files:
    print(f'Start {file}')
    try:
        with open(file, 'r') as r1:
            data = json.load(r1)
        if 'pull_request' not in data:
            continue
        processed_diff = extract_diff_hunks(data['pull_request']['diff'])
        data['processed_diff'] = processed_diff
        with open(file, 'w') as w1:
            w1.write(json.dumps(data, indent=4, ensure_ascii=False))
        print(f'Finsih {file}')
    except Exception as e:
        print(f'Error: {file} {e}')
        # sys.exit()
