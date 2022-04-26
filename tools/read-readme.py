#!/usr/bin/python3

import pprint
import csv
import argparse

parser = argparse.ArgumentParser(description="Parse README to question/answer pair and append the result to csv file")
parser.add_argument("--file", type=str, help="file's path")
parser.add_argument("--component", type=str, help="component's name")
parser.add_argument("--csv_file", type=str, required=False, help="target csv file that the result is appended to")
parser.add_argument("--dry_run", type=bool, required=False, help="only print the result", default=False)
args = parser.parse_args()
file = args.file
component = args.component
dry_run = args.dry_run
csv_file = args.csv_file

with open(file) as f:
    lines = f.readlines()
a = []
question = ''
answer = ''
command_start = True
for line in lines:
    line = line.strip(" ")
    if line.startswith("##"):
        if question and answer:
            a.append([question, answer])
            answer = ''
        line = line.replace("#", "").strip(" ")
        question = f"{component}'s \"{line}\""
    elif line.startswith("#"):
        line = line.replace("#", "").strip(" ")
        question = f"What is {line}?"
    else:
        if line:
            answer += f"{line}"
if question and answer:
    a.append([question, answer])

if dry_run:
    print(a)
else:
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(a)
        print(f"write {len(a)} qa paris to {csv_file}")
        pprint.pprint(a[:3])
