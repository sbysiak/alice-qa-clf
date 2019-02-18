# script exporting time statistics of time intervals (1 interval correspond to single ROOT file) to *.csv file
# it can also draw a plot with run id on horizontal and time on vertical axis
# run with "-i" option in order to keep the canvas open

# one can select whether to use POSIX/UNIX/PYTHON timestamps using (make_time_shift=False)
# or ROOT timestamps (starting from 2010) using (make_time_shift=True)

# use ROOT timestamps for plotting

import ROOT
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import csv
from array import array

# ***  PARAMETERS  ***
make_time_shift = 1
main_dir = 'OUTPUTS/data/2018/LHC18d/'
csv_fname = 'time-stats-LHC18d.csv'
# ***      ***     ***


def shift_cetTimeLHC(cetTimeLHC):
    return cetTimeLHC+1262304000.+3600.

def extract_time_interval_id(file_path):
    # /user/a/aliqat/www/qcml/data/2018/LHC18d/000285978/pass1/time_interval_01
    str_just_before = 'time_interval_'
    id_start = file_path.find(str_just_before)+len(str_just_before) 
    return int(file_path[id_start : id_start+2])

def extract_run(file_path):
    run_str_start = file_path.find('000')
    run = file_path[run_str_start : run_str_start+9]
    return int(run)

var_name = "cetTimeLHC"
run_lst, time_id_lst, mean_lst, std_lst, median_lst, min_lst, max_lst = [], [], [], [], [], [], []

files_list = []
for root, subdirs, files in os.walk(main_dir):
    if len(files) < 1: continue
    if files[0] == 'QAresults.root':
        file_path = os.path.join(root,files[0])
        if os.path.getsize(file_path) < 1000: continue
        files_list.append(file_path)


for file_path in sorted(files_list, key=extract_time_interval_id):
        # print file_path
        root_file = ROOT.TFile.Open(file_path)
        root_file.cd('Vertex_Performance')

        cOutputVtxESD = ROOT.gROOT.FindObject("cOutputVtxESD")
        tree = cOutputVtxESD.FindObject("fTreeBeamSpot")

        tree.Draw(var_name + " >> htime", "", "goff")
        htime = tree.GetHistogram()
        std = htime.GetStdDev()
        mean_orig = htime.GetMean()
        min_orig = tree.GetMinimum(var_name)
        max_orig = tree.GetMaximum(var_name)

        q = array('d', [0.5])
        median_orig = array('d', [-1.])
        htime.GetQuantiles(1, median_orig, q)
        median_orig = median_orig[0]

        # print 'fpath={}, mean={}, std={}, min={}, max={}'.format(file_path, mean, std, mini, maxi)
        run = extract_run(file_path)
        run_lst.append(run)
        time_interval_id = extract_time_interval_id(file_path)
        time_id_lst.append(time_interval_id)
        mean_lst.append(mean_orig)
        std_lst.append(std)
        median_lst.append(median_orig)
        min_lst.append(min_orig)
        max_lst.append(max_orig)

        time_zero = ROOT.TDatime(2010,1,1,1,0,0)
        htime.GetXaxis().SetTimeOffset(time_zero.Convert())
        htime.GetXaxis().SetTimeDisplay(1)
        htime.GetXaxis().SetTimeFormat('<%y%m%d %H:%M:%S>')
        # htime.Draw()

# OPTIONAL CONVERTION OF TIMESTAMPS TO ROOT CONVENTION
if make_time_shift:
    # shift for python datetime.date.fromtimestamp
    print 'USING POSIX TIMESTAMPS (from 1970)'
    csv_comment = '# timestamps in POSIX/UNIX convention, with time zero in 1970 \n# read with e.g. PY:datetime.datetime.fromtimestamp() or ROOT:TTimeStamp\n'
    mean_lst    = [shift_cetTimeLHC(m_orig) for m_orig in mean_lst]
    median_lst  = [shift_cetTimeLHC(m_orig) for m_orig in median_lst]
    min_lst     = [shift_cetTimeLHC(m_orig) for m_orig in min_lst]
    max_lst     = [shift_cetTimeLHC(m_orig) for m_orig in max_lst]
else:
    # no shift for ALICE/ROOT TDatime starting from (2010,1,1,1,0,0)
    # used in graph plotting
    print 'USING ROOT TIMESTAMPS (from 2010)'
    csv_comment = '# timestamps in ALICE/ROOT convention, with time zero in 2010 \n# use e.g. on ROOT plots with SetTimeOffset() and TDatime(2010,1,1,1,0,0)\n'



# WRITE TO CSV
with open(csv_fname, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    csvfile.write(csv_comment)
    writer.writerow(['run', 'time_interval_id', 'mean', 'std', 'mini', 'median', 'maxi'])
    for row in zip(run_lst, time_id_lst, mean_lst, std_lst, min_lst, median_lst, max_lst):
        writer.writerow(row)


# MAKE GRAPH

# lst -> arr for TGraphErrors
time_id_arr = array('d', time_id_lst)
mean_arr   = array('d', mean_lst)
std_arr    = array('d', std_lst)
median_arr = array('d', median_lst)
min_arr    = array('d', min_lst)
max_arr    = array('d', max_lst)
width_arr  = array('d', [(maxi-mini)/2 for mini,maxi in zip(min_arr, max_arr)])
half_arr   = array('d', [(maxi+mini)/2 for mini,maxi in zip(min_arr, max_arr)])
zeros_arr  = array('d', [0.]*len(time_id_arr) )

# graph = ROOT.TGraphErrors(len(half_arr), time_id_arr, half_arr, zeros_arr ,width_arr)
# graph.SetTitle('Errorbars = min:max')
graph = ROOT.TGraphErrors(len(half_arr), time_id_arr, mean_arr, zeros_arr, std_arr)
graph.SetTitle('Errorbars = +/-stddev')

dt = ROOT.TDatime(2010,1,1,1,0,0);
graph.GetYaxis().SetTimeOffset(dt.Convert())
graph.GetYaxis().SetTimeDisplay(1)
graph.GetYaxis().SetTimeFormat('<%Y-%m-%d %H:%M:%S>')

graph.GetXaxis().SetTitle('time interval ID')
graph.GetYaxis().SetTitle('time')
graph.Draw()
