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

run = '286454'
n_out_files = 50  # equals number of time chunks better set higher, unnecessary files are not created

sum_written = 0

fnames_out_lst = []

for time_id in range(1, n_out_files):
    tree = ET.parse('all_files_to_be_merged.xml')
    root = tree.getroot()
    print(f'starting loop for id={time_id} with len={len(root[0])}')
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
        tree.write(f'files_to_be_merged_{time_id}.xml')
        sum_written += len(root[0])
        
    print(f'after loop: removed {len(lst_torm)} elements, there are {len(root[0])} more, so far {sum_written}={len(fnames_out_lst)} were written')

print('\n\n\nList of files not included in any output file:')
all_fnames = []
tree = ET.parse('all_files_to_be_merged.xml')
root = tree.getroot()
for e in root[0]:
    if e.tag != 'event': continue
    fname = e[0].attrib['turl']
    all_fnames.append(fname)
    if fname not in fnames_out_lst: print(fname)
