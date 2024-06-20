import csv

with open("test.csv", "w") as file:
    spamwriter = csv.writer(file)

    spamwriter.writerow([1,2,3,3])