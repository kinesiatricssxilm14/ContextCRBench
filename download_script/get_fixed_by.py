import os
import json
from package import PACKAGE_NAME

PACKAGE_NAME_1 = PACKAGE_NAME.split('/')[-1]
if not os.path.exists(f'paring/{PACKAGE_NAME_1}'):
    os.system(f"mkdir -p pairing/{PACKAGE_NAME_1}")

all_json = [os.path.join('data', PACKAGE_NAME_1, x) for x in os.listdir(f'data/{PACKAGE_NAME_1}')]

for aj in all_json:
    with open(aj, 'r') as r1:
        try:
            raw_data = json.load(r1)
            if 'fixed_by' in raw_data and len(raw_data['fixed_by']) > 0:
                print(f'{PACKAGE_NAME_1} {raw_data["number"]}')
                os.system(f'cp data/{PACKAGE_NAME_1}/{raw_data["number"]}.json pairing/{PACKAGE_NAME_1}')
                for fix in raw_data['fixed_by']:
                    os.system(f'cp data/{PACKAGE_NAME_1}/{fix}.json pairing/{PACKAGE_NAME_1}')
        except Exception as e:
            print(f'Error: {aj} -- {e}')