import os

if os.listdir("csv files/"):
    print("Deleting previous files...")
    for file in os.listdir("csv files/"):
        file = "csv files/{}".format(file)
        os.remove(file)
