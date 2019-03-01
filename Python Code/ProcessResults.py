import pandas as pd
import numpy as np

files = ["10dimension100.csv","30dimension100.csv","50dimension100.csv","100dimension100.csv",
"10dimension500.csv","30dimension500.csv","50dimension500.csv","100dimension500.csv"]

for i in range(len(files)):
    print("File : %s"%files[i])
    data = pd.read_csv("Results/"+files[i])
    headers = list(data)
    newData = []
    for index,row in data.iterrows():
        ran = len(row)
        for x in range(5,ran):
            newData.append(row[headers[x]]-500)

    array = np.array(newData)

    print("Min : %d"%np.min(array))
    print("Max : %d"%np.max(array))
    print("Mean : %d"%np.mean(array))
    print("Median : %d"%np.median(array))
    print("Standard Deviation : %d"%np.std(array))
