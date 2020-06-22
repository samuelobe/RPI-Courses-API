import pandas as pd
import time
import csv
import json
import sys
import os
from collections import defaultdict


def get_courses():

    temp_csvfile = open('/tmp/data.csv', 'w')

    # The webpage URL whose table we want to extract
    url = 'https://sis.rpi.edu/reg/zs20200501.htm'

    # Assign the table data to a Pandas dataframe
    table = pd.read_html(url)

    for i in range(len(table)):
        # Remove unneeded strings and replace them with blank strings
        table[i].rename({"Unnamed: 1_level_0": "", "Unnamed: 2_level_0": "", "Unnamed: 8_level_0": "",
                         "Unnamed: 10_level_0": ""}, axis="columns", inplace=True)

        # Remove column that contains unneeded data
        table[i] = table[i][table[i].columns.drop(
            list(table[i].filter(regex='Unnamed: 12_level_1')))]

    # Convert table data to csv formart and add it to temp file
    df = pd.concat(table, ignore_index=True)
    df.to_csv("/tmp/data.csv", index=False)

    time.sleep(1)

    temp_csvfile = open('/tmp/data.csv', 'r')

    # Open csvfile and convert file to a list of lists
    r = csv.reader(temp_csvfile)
    csv_lines = list(r)
    length = len(csv_lines)

    for i in range(length):
        if i >= 2:
            if csv_lines[i][0] == '' and csv_lines[i][1] == '':
                csv_lines[i][0] = csv_lines[i-1][0]
                csv_lines[i][1] = csv_lines[i-1][1]
            elif csv_lines[i][2] == '':
                csv_lines[i][2] = 'LEC'
    # Remove the headers
    csv_lines.remove(csv_lines[0])
    csv_lines.remove(csv_lines[0])

    key_tuple = ('CRN Course-Sec', 'Course Title', 'Class Type', 'Credit Hrs', 'Gr Tp',
                 'Class Days', 'Start Time', 'End Time', 'Instructor', 'Max Enrl', 'Enrl', 'Sts Rmng')

    for line in csv_lines:
        if 'NOTE:' in line[1]:
            csv_lines.remove(line)
        else:
            print(line)



    fields = ['CRN Course-Sec', 'Course Title', 'Class Type', 'Credit Hrs', 'Gr Tp',
                 'Class Days', 'Start Time', 'End Time', 'Instructor', 'Max Enrl', 'Enrl', 'Sts Rmng']

    with open('data.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for line in csv_lines:
            writer.writerow(line)


if __name__ == "__main__":
    get_courses()
    os.remove("/tmp/data.csv")
