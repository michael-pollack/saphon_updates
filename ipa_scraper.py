import json
import os

with open("ipa.json", 'r', encoding='utf-8') as ipa_file:
    ipa = json.load(ipa_file)

for category in ipa:
    print(category["category"])