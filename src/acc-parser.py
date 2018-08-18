import csv
from os import listdir, path, makedirs, rename
from operator import attrgetter
from rowhandlers import OutputRow, ResolveProcessor

def ensuredirectory(directory): 
    if not path.exists(directory):
        makedirs(directory)

rootPath = path.abspath(path.dirname(path.dirname(__file__)))
inputfolder     = path.join(rootPath, "data")
outputFolder    = path.join(rootPath, "output")
processedFolder = path.join(rootPath, "processed")

files = listdir(inputfolder)
outputs = []

for f in files:
    filepath = path.join(inputfolder, f)
    if path.isfile(filepath):
        with open(filepath) as csvfile:
            transactions = csv.reader(csvfile)
            headers = next(transactions)
            processor = ResolveProcessor(headers)
            if processor is not None:
                for row in transactions:
                    transformedRow = processor.ToOutputRow(row)
                    outputs.append(transformedRow)

sortedoutput = sorted(outputs, key=attrgetter('date'))
mindate = sortedoutput[0].date
maxdate = sortedoutput[len(sortedoutput)-1].date

ensuredirectory(outputFolder)
outputfile = path.join(outputFolder, f'{mindate.isoformat()} - {maxdate.isoformat()}.csv')

with open(outputfile, 'w+', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(OutputRow._fields)
    writer.writerows(sortedoutput)

ensuredirectory(processedFolder)
for f in files:
    source = path.join(inputfolder, f)
    destination = path.join(processedFolder, f)
    rename(source,destination)
