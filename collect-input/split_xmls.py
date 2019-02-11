# script for splitting xml file containing all QAresults.root from given RUN
# into a set of output xml files among which each file contains only files which are to be merged together
# based on the timestamp which is coded in last digits of the path (3rd or 3rd and 4th from the end), e.g.
# 18 in /alice/data/2018/LHC18e/000286454/pass1/18000286454039.1811/QAresults.root or 
#  9 in /alice/data/2018/LHC18e/000286454/pass1/18000286454038.906/QAresults.root
# 
# example command to get the output:
# alien_find -x files_to_be_merged /alice/data/2018/LHC18e/000286454/pass1/ QAresults.root > outputFileName.xml
# time benchmark: on lxplus-1:26; locally in alidock-4:10

import xml.etree.ElementTree as ET
import re
import sys
import os
from time import time 

tic = time()
input_fname = sys.argv[1]
run = input_fname.split('/')[-3][-6:]

n_out_files = 0
with open(input_fname) as f: 
    maxi = 0
    for i_line,line in enumerate(f): 
        if 'turl' not in line: continue 
        if 'Stage' in line or 'QA/QAres' in line: continue 
        fpath = line.split()[-3] 
        time_interval = int(fpath.split('.')[1].split('/')[0])  
        maxi = max(maxi, time_interval) 
n_out_files = int(maxi/100)

if i_line < 10: sys.exit()

sum_written = 0
fnames_out_lst = []

for time_id in range(1, n_out_files+1):
    output_fname = input_fname.replace('.xml', '_{0:02}.xml'.format(time_id))
    tree = ET.parse(input_fname)
    root = tree.getroot()
    #print('starting loop for id={0} with len={1}'.format(time_id, len(root[0])))
    lst_torm = []
    for ie, e in enumerate(root[0]):
        if e.tag != 'event': continue
        fname = e[0].attrib['turl']
        remove = not re.match(r'.+' + run + '...\.' + str(time_id) + '../QAresults.root', fname)
        #print(ie, fname,'REGEX done',)
        #if remove: print('\t-> remove')
        #else: print ('\t-> keep')
        if remove: lst_torm.append(e)
        else: fnames_out_lst.append(fname)
    
    for e_torm in lst_torm:
        root[0].remove(e_torm)
   
   
    if len(root[0]) > 1:
        tree.write( output_fname )
        sum_written += len(root[0])
        
    #print 'after loop: removed {0} elements, there are {1} more, so far {2}={3} were written'.format(len(lst_torm), len(root[0]), sum_written, len(fnames_out_lst))

all_fnames = []
tree = ET.parse(input_fname)
root = tree.getroot()

printed=0
for e in root[0]:
    if e.tag != 'event': continue
    fname = e[0].attrib['turl']
    all_fnames.append(fname)
    if fname not in fnames_out_lst: 
        if not printed: 
            print '\nList of files not included in any output file:'
            printed=1
        print fname

print 'exec. time: {0} sec ({1} lines - {2} time intervals)'.format(time()-tic, i_line, n_out_files)
