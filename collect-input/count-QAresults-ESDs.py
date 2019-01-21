# script counting number of QAresults.root and ESDs.root files 
# in certain periods / runs inside pass1 directory


import subprocess
import os
import numpy as np
import pickle
import pprint
from time import time

# # BENCHMARK
# for 5 files per run, year 2010-18:  77min


def mycheck_output(cmd):
    return subprocess.check_output(cmd, shell=True).split('\n')

def position_report(path):
    print('current location = {}'.format(path))

def process_output(cmd):
    '''returns no. files found by alien_find command
       returns -1 in case of `Exceeded maximum number of columns` error
       returns -2 in case of other error
    '''
    try:
        output = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == -11:
            return -1
        else:
            return -2
    if output == '\n':
        return 0
    if output.endswith('files found\n'):
        return int(output.split('\n')[-2].split()[0])
    # should never be called
    return -3


pp = pprint.PrettyPrinter(indent=4)



main_dir = '/alice/data/'
# ls_cmd = 'alien_ls \"/alice/data/2018/LHC18e/000286380/pass1/18000286380038.102\"'

ls = 'alien_ls '
result = {}
total_runs_number = 0
output_empty = '\n'


for year in reversed(mycheck_output(ls + main_dir)):
    year_path = os.path.join(main_dir, year)
    position_report(year_path)
    #if not year.startswith('201') or 'i' in year: continue
    if year not in ['2013', '2014', '2015', '2016', '2017', '2018']: continue
    result[year] = {}
    pp.pprint(result)

    for period in mycheck_output(ls + year_path):
        period_path = os.path.join(year_path, period)
        position_report(period_path)
        if (not period.startswith('LHC')) or '_' in period: continue  # only runs with working TPC <=> no "_Muon" etc
        result[year][period] = {}

        runs_lst = mycheck_output(ls + period_path)
        print('There are {} runs in {}'.format(len(runs_lst)-1, period))
        n_runs_per_period = min(30, len(runs_lst))
        #n_runs_per_period = len(runs_lst)
        selected_runs = [''] + np.random.choice(runs_lst, n_runs_per_period, replace=False).tolist()
        for run in selected_runs:
            #continue
            run_path = os.path.join(period_path, run)
            position_report(run_path)

            tic = time()
            find_qa_cmd = 'alien_find {} \"/pass1/*000*/QAresults.root\"'.format(run_path)
            output_qa = process_output(find_qa_cmd)

            find_esd_cmd = 'alien_find {} \"/pass1/*000*/AliESDs.root\"'.format(run_path)
            output_esd = process_output(find_esd_cmd)
            output_to_print = (str(output_qa) + ' ' + str(output_esd)).replace('\n', ' \\n ') + '\t\t exec. time: {} sec '.format(time()-tic)
            print(output_to_print)

            if not run: run = '<ALL>'  # replace empty strings for pickle
            result[year][period][run] = {'qa':output_qa, 'esd':output_esd}
            if result[year][period]['<ALL>'] == {'qa':0, 'esd':0} and len(result[year][period]) > 5:
                print 'Interrupting empty period'
                break
        result[year][period]['n_runs'] = len(runs_lst)-1


        pp.pprint(result)

        with open('counts.pickle', 'wb') as f:
            pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)
