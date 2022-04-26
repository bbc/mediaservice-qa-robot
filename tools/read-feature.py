#!/usr/bin/python3

import pprint
import os
import csv
import argparse

parser = argparse.ArgumentParser(description="Parse cucumber test feature files to question/answer pair"
                                             " and append the result to csv file")
parser.add_argument("--folder", type=str, help="feature files' folder")
parser.add_argument("--component", type=str, help="component's name")
parser.add_argument("--csv_file", type=str, required=False, help="target csv file that the result is appended to")
parser.add_argument("--dry_run", type=bool, required=False, help="only print the result", default=False)
args = parser.parse_args()
folder = args.folder
component = args.component
dry_run = args.dry_run
csv_file = args.csv_file


def parse_feature_file(file, a):
    with open(file) as f:
        lines = f.readlines()
    question = ""
    answer = ""
    for line in lines:
        line = line.strip(" ")
        if line.startswith("Scenario:"):
            if question and answer:
                a.append([question, answer])
                answer = ""
            line = line.replace("Scenario:", "").strip()
            question = f"{component} {line}?"
        else:
            if question and line and not line.startswith('|') and not line.startswith("@"):
                answer += line
    if question and answer:
        a.append([question, answer])
    return a


result = []
for filename in os.listdir(folder):
    if filename.endswith(".feature"):
        f = os.path.join(folder, filename)
        parse_feature_file(f, result)

if dry_run:
    print(result)
else:
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(result)
        print(f"write {len(result)} qa paris to {csv_file}")
        pprint.pprint(result[:3])

