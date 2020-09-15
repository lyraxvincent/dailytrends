import pandas as pd

topics = pd.read_csv("csv files/sortopics.csv")
topics = list(topics.topics)

for topic in topics:
    df = pd.read_csv("csv files/{}".format(topic))
    print(f"Cleaning [{topic}]...")
    df.dropna(axis=0, subset=['text'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    for i in range(len(df)):
        if type(df.text[i]) != str:
            df.drop(i, inplace=True)
        else:
            pass
    df.to_csv("csv files/{}".format(topic))