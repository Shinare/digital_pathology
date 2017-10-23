## Calculate mean for each unique patient ID exported from QuPath into a tab separeted values from single or multiple files. 
## Contact rkacprzyk01@qub.ac.uk

import csv, argparse, os, statistics
from glob import glob


## Define arguments form the console input
parser = argparse.ArgumentParser(description="Provide [input files] then [output files].")
parser.add_argument('allin', nargs='?', type=str, metavar="Input files(s)", help="Relative or absolute string. Can include wildcards")
parser.add_argument('fresults', nargs='?', type=str, metavar="Output file", help="Relative or absolute string")
parser.add_argument('-k', '--keep', action='store_true', default=False)
args = parser.parse_args()

files = glob(args.allin)
allout = "output.txt"

## Remove old intermediate file
if os.path.isfile(allout):
	os.remove(allout)
	print("Old ", allout, "file removed")	

## Create intermediate file where all separate TMA results will be read into
with open(allout, 'a', newline = '') as tsvout:
	tsvout = csv.writer(tsvout, delimiter='\t')
	for file in files:
		with open(file, 'r') as tsvin:
			tsvin = csv.reader(tsvin, delimiter='\t')
			if file == files[0]:
				header = next(tsvin)
				header = [w.replace('Unique ID', 'Description') for w in header]
				header.append("Unique ID")
				tsvout.writerow(header)
			if file != files[0]:
				next(tsvin, None)
			for line in tsvin:
				if any(line):
					line.append(line[header.index("Description")].partition(' ')[0])
					tsvout.writerow(line)
print("Individual files parsed")

## Create results file which where uniqe ids will be inserted alongside with the means corresponding to the patient
with open(allout, 'r') as tsvoutf:
	tsvout = csv.reader(tsvoutf, delimiter='\t')
	next(tsvout)
	uids =[]
	## Create list with unique ids 
	for row1 in tsvout:
		if uids.count(row1[header.index("Unique ID")])<1:
			uids.append(row1[header.index("Unique ID")])
	## go through intermediate csv and pull out each postitive cell per um2 measuerement and average it, delete intermediate file
	tsvoutf.seek(1)
	sender=[]
	for uid in uids:
		one_mean=[]
		for row2 in tsvout:
			if uid == row2[header.index("Unique ID")]:
				one_mean.append(float(row2[header.index("Num Positive per mm^2")]))
		tsvoutf.seek(1)
		sender.append([uid, statistics.mean(one_mean)])
	## Create final file and write out unique ids and means
	if os.path.isfile(args.fresults):
		os.remove(args.fresults)
		print("Old ", args.fresults, "file removed")	
	with open(args.fresults, 'a', newline = '') as results:
		results = csv.writer(results, delimiter='\t')
		results.writerow(["Unique ID", "Num Positive per mm^2 Mean"])
		for i in sender:
			results.writerow(i)
if args.keep!=True:
	if os.path.isfile(allout):
		os.remove(allout)
		print("Intermediate:", allout, "file removed")
print("Done")