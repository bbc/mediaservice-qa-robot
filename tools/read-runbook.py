#!/usr/bin/python3

import pprint
import csv
import requests
import argparse
import pandas as pd
from bs4 import BeautifulSoup
from requests_pkcs12 import get


USEFUL_TITLES = ["purpose", "inputs and outputs", "architecture", "deployment", "configuration and licensing", "database",
                 "dependencies", "changes, maintenance and outages", "backup and recovery"]

parser = argparse.ArgumentParser(description="read runbook")
parser.add_argument("--url", type=str, help="url of runbook")
parser.add_argument("--csv_out", type=str, help="target csv file ")
parser.add_argument("--p12cert_path", type=str, help="p12 path")
parser.add_argument("--p12_password", type=str, help="p12 password")
parser.add_argument("--component", type=str, help="component name")
parser.add_argument("--dry_run", type=bool, required=False, help="only print the result", default=False)
args = parser.parse_args()
url = args.url
csv_out = args.csv_out
p12cert_path = args.p12cert_path
p12_password = args.p12_password
component = args.component
dry_run = args.dry_run

r = get(url, verify=False, pkcs12_filename=p12cert_path, pkcs12_password=p12_password)
s = BeautifulSoup(r.text, features="html.parser")

title = url.split("/")[-1].replace("+", "").replace("-", "")

titles = s.find_all("h1", id=lambda value: value and value.startswith(title))

a = []

for child in titles:
    if child.text.lower() in USEFUL_TITLES:
        question = f"{component}'s {child.text.lower()}"
        c = child.next_element
        answer = ""
        while c and c.name != "h1":
            if c.name == "p":
                answer += c.text
            c = c.next_element
        a.append([question, answer])
    elif child.text.lower() == "ispy events":
        c = child.next_element
        rows_index = 0
        while c and c.name != "h1":
            if c.name == "tr":
                answer = ""
                question = ""
                if rows_index != 0:
                    columns = c.find_all("td")
                    td_index = 0
                    for td in columns:
                        td_contents = td.getText()

                        if td_contents:
                            if td_index == 0:
                                question = f"{component} ispy event '{td_contents}'"
                            else:
                                answer += td_contents
                        td_index += 1

                rows_index += 1
                if question != "":
                    a.append([question, answer])
            c = c.next_element


if dry_run:
    pprint.pprint(a)
else:
    with open(csv_out, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(a)
        print(f"write {len(a)} qa paris to {csv_out}")
        pprint.pprint(a[:3])

