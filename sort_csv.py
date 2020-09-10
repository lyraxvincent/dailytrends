import os, operator, sys
import pandas as pd

dirpath = os.path.abspath(sys.argv[0])
dirpath = "/".join(dirpath.split("/")[:-1]) + "/csv files"

# make a generator for all file paths within dirpath
all_files = (os.path.join(basedir, filename) for basedir, dirs, files in os.walk(dirpath) for filename in files)

# sort files
sorted_files = sorted(all_files, key=os.path.getsize, reverse=True)
sorted_files.pop(-1)    # remove topics.csv

# pass the 5-10 largest files and store the result to a dataframe
topics = []
for file in sorted_files[:10]:
    topics.append(file.split("/")[-1])
final_topics = pd.DataFrame({'topics': topics})
final_topics.to_csv("csv files/sortopics.csv", index=False)