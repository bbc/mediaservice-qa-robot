#!/usr/bin/python3

import pprint
import csv
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description="add id column")
parser.add_argument("--csv_in", type=str, help="input csv file's path")
parser.add_argument("--csv_out", type=str, help="target csv file ")
args = parser.parse_args()
csv_in = args.csv_in
csv_out = args.csv_out

df = pd.read_csv(csv_in, header=None)
df.to_csv(csv_out, header=["question", "answer"], index_label="id")

