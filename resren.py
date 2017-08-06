#!/usr/bin/python

# resren.py -- renumber PDB files that have residue numbers with alphabetic suffixes or "inserted residues"
# 2017.08.03 -- first version -- John Saeger

# 2017.08.05 -- remove alternate coordinates for atoms (altLoc) -- just keep main and 'A' locations

from __future__ import print_function

infile = "5te4.pdb"
outfile = "5te4ren.pdb"

def read_pdb(fn):				# read selected chain in PDB file
	try:
		pdb = []						# clean it up a little
		for line in open(fn, 'r'):
			l=[]
			l.append(line[0:6].strip())		# atom
			if l[0] != 'ATOM': continue
			l.append(line[6:11].strip())	# serial
			l.append(line[12:16].strip())	# name
			l.append(line[16].strip())		# altLoc
			l.append(line[17:20].strip())	# resName
			l.append(line[21].strip())		# chainID
			l.append(line[22:26].strip())	# resSeq
			l.append(line[26].strip())		# iCode
			l.append(line[30:38].strip())	# x
			l.append(line[38:46].strip())	# y
			l.append(line[46:54].strip())	# z
			l.append(line[54:60].strip())	# occupancy
			l.append(line[60:66].strip())	# tempFactor
			l.append(line[76:78].strip())	# element
			l.append(line[78:80].strip())	# charge
			pdb.append(l)
	except:
		print("Couldn't read {}".format(fn))
		quit()
	return pdb

def write_pdb(fn, pdb):
	with open (fn, 'w') as out:
		for l in pdb:
			str = 'ATOM  '					# atom
			str += "%5s" % l[1]				# serial
			str += "  %-3s" % l[2]			# name (hmmm... why not %-4s ???)
			str += "%1s" % l[3]				# altLoc
			str += "%3s" % l[4]				# resName
			str += " %1s" % l[5]			# chainID
			str += "%4s" % l[6]				# resSeq
			str += "%1s" % l[7]				# iCode
			str += "   %8s" % l[8]			# x
			str += "%8s" % l[9]				# y
			str += "%8s" % l[10]			# z
			str += "%6s" % l[11]			# occupancy
			str += "%6s" % l[12]			# tempFactor
			str += "          %2s" % l[13]	# element
			str += "%2s" % l[14]			# charge
			str += '\n'
			if l[3] != '':					# skip over named alternative coordinates
				continue
			out.write(str)

def renumber_pdb(pdb):
	offset = 0								# keep track of how many iCodes
	prev_iCode = ''
	curr_iCode = ''
	prev_res = ''
	curr_res = ''
	prev_chain = ''
	curr_chain = ''
	for l in pdb:
		curr_res = l[6]
		curr_iCode = l[7]
		curr_chain = l[5]
		if curr_chain != prev_chain:
			prev_chain = curr_chain
			offset = 0
		if curr_iCode != prev_iCode:
			prev_iCode = curr_iCode
			if curr_iCode != '':
				print(curr_res)
				offset += 1
				print(offset)
		l[7] = ''
		resnum = int(l[6])
		resnum += offset
		l[6] = resnum
		if l[3] == 'A':						# we only want the 'A' coordinate of a residue
			l[3] = ''
	return pdb

pdb = read_pdb(infile)
pdb = renumber_pdb(pdb)
write_pdb(outfile, pdb)
