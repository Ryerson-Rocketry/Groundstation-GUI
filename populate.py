import time

def populateFile():

    with open('dateUpdate.txt', "w") as f, open('data.txt', "r") as f1:
        

        arrayList = f1.readlines()

        for i in arrayList:
            f.write(i)
            f.flush()

            time.sleep(1)

populateFile()