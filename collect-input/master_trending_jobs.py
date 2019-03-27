import subprocess
import sys
import os
import pexpect
from time import sleep, time


STD_MSG_FILE_NOT_FOUND = 'WARNING - file: {}  not found'
STD_MSG_FILE_TOO_SMALL = 'WARNING - file: {}  has size ({} KB) below threshold ({} KB)'
STD_MSG_FILE_OK = 'file: {}  ok'

def check_file(fpath, fsize_min_kb,
            silent=False,
            msg_ok=STD_MSG_FILE_OK,
            msg_not_found=STD_MSG_FILE_NOT_FOUND,
            msg_too_small=STD_MSG_FILE_TOO_SMALL):
    """function validating copying from EOS to PLGRID

    Parameters
    ----------
    fpath : string
        name of file to be checked
    fsize_min_kb : float
        minimal accepted size of copied file (in KB)
    silent : bool
        stop printing
    Returns
    -------
    status : int
        0 = ok
        1 = file not found
        2 = file too small
    """
    fpath = fpath.strip()
    if os.path.isfile(fpath):
        fsize_kb = os.path.getsize(fpath) / 1024.
        if fsize_kb > fsize_min_kb:
            if not silent: print msg_ok.format(fpath)
            return 0
        else:
            if not silent: print msg_too_small.format(fpath, int(fsize_kb), fsize_min_kb)
            return 2
    else:
        if not silent: print msg_not_found.format(fpath)
        return 1


# create list of all QAresults to be processed - e.g. one period
def create_list_of_QAresults(eos_main_dir_path, period_hash):
    password='$tArstEk45'
    #> .tmp_qaresults_list_{}_MASTER
    cmd = 'ssh sbysiak@lxplus.cern.ch "find {} | grep QAresults.root | grep -v \"part\"" '.format(eos_main_dir_path)
    print 'Running: {}\t...'.format(cmd)
    child = pexpect.spawn(cmd)
    child.timeout = 300

    out_fname = '.tmp_qaresults_list_{}_MASTER'.format(period_hash)
    print 'saving result to {}'.format(out_fname)
    child.logfile = sys.stdout
    #child.logfile = open(out_fname, 'w')
    child.expect('Password: ')
    child.sendline(password)
    print 'before: ', child.before
    print 'after: ',  child.after

    with open(out_fname, 'w') as f:
        content = child.read().strip()+'\n'
        content = content.replace('\r\n','\n')
        f.writelines(content)
    child.expect(pexpect.EOF)
    return out_fname


def split_list_for_subjobs(fname_master, n_files_per_subjob):
    list_of_subjobs_infiles = []
    list_of_subjobs_lists = []
    current_subjob = 0

    # make list which elements are lists of QAresults.root to be processed
    with open(fname_master) as f:
        for line in f:
            fname_qa_results = line.replace('/eos', 'eos')
            fname_trending = fname_qa_results.replace('QAresults.root', 'trending.root')
            if check_file(fname_trending, fsize_min_kb=50, silent=True) > 0:
                if len(list_of_subjobs_lists) <= current_subjob:
                    list_of_subjobs_lists.append([])
                list_of_subjobs_lists[current_subjob].append(fname_qa_results)
                if len(list_of_subjobs_lists[current_subjob]) >= n_files_per_subjob:
                    current_subjob += 1

    # save each element of previous list to a separate file
    for subjob_id, subjob_list in enumerate(list_of_subjobs_lists):
        subjob_infile_name = fname_master.replace('MASTER', 'id'+str(subjob_id))
        with open(subjob_infile_name, 'w') as f_sub:
            f_sub.writelines(subjob_list)
        list_of_subjobs_infiles.append(subjob_infile_name)
    return list_of_subjobs_infiles


def run_subjob(infile):
    job_output = 'LOGS/slurm/' + infile.replace('.tmp_qaresults_list', 'trending') + '_%j.out'
    job_name = infile.replace('.tmp_qaresults_list', 'trend_')
    cmd = 'sbatch --output {} --job-name {} single_trending_job.py {} '.format(job_output, job_name, infile)
    print 'Running {} \t...'.format(cmd)
    subprocess.call(cmd, shell=True)


def get_n_running_subjobs():
    cmd = 'squeue -u plgsbysiak'
    output = subprocess.check_output(cmd, shell=True)
    # print 'output of {} \t :\n{}'.format(cmd, output)
    n_subjobs = len(output.strip().split('\n')) - 1
    return n_subjobs


def get_quota_percentage():
    out = subprocess.check_output('pro-fs | grep HOME', shell=True)
    percentage = float(' '.join(out.split('|')[0].split()).split(' ')[3].replace('%',''))
    return percentage



def run_locally(infile):
    cmd = 'time python single_trending_job.py {} '.format(infile)
    print 'Running {} \t...'.format(cmd)
    subprocess.call(cmd, shell=True)


def main(eos_main_dir_path, period_hash, max_n_subjobs=20, n_files_per_subjob=10, max_quota_perc=90):
    print '= = '*20 + '\nCREATE LIST OF QAresults\n' + '= = '*20
    fname_master = create_list_of_QAresults(eos_main_dir_path, period_hash)
    sleep(5)
    print '= = '*20 + '\nSPLIT LIST FOR SUBJOBS\n' + '= = '*20
    subjobs_infiles = split_list_for_subjobs(fname_master, n_files_per_subjob)
    print 'Files were split into {} jobs'.format(len(subjobs_infiles))
    sleep(5)
    print '= = '*20 + '\nRUN SUBJOBS\n' + '= = '*20
    for it,infile in enumerate(subjobs_infiles):
        n_running_subjobs = get_n_running_subjobs()
        if not (it % 5): current_quota_perc = get_quota_percentage()
        while n_running_subjobs >= max_n_subjobs or current_quota_perc > max_quota_perc:
            quota_str = 'WARNING ({}%)'.format(current_quota_perc) if current_quota_perc > max_quota_perc else 'OK'
            print 'there are {} running subjobs and quota_status = {} - sleeping ...'.format(n_running_subjobs, quota_str)
            sleep(20)
            n_running_subjobs = get_n_running_subjobs()
            current_quota_perc = get_quota_percentage()
        run_subjob(infile)


def main_local(eos_main_dir_path, period_hash, n_files_per_subjob=10):
    print '= = '*20 + '\nCREATE LIST OF QAresults\n' + '= = '*20
    fname_master = create_list_of_QAresults(eos_main_dir_path, period_hash)
    sleep(10)
    print '= = '*20 + '\nSPLIT LIST FOR SUBJOBS\n' + '= = '*20
    subjobs_infiles = split_list_for_subjobs(fname_master, n_files_per_subjob)
    sleep(10)
    print '= = '*20 + '\nRUN SUBJOBS\n' + '= = '*20
    for infile in reversed(subjobs_infiles):
        run_locally(infile)


################################################################################

if __name__ == '__main__':
    main(eos_main_dir_path='/eos/user/a/aliqat/www/qcml/data/2018/LHC18o',
         #period_hash='TEST_FLOATING_POINT_EXCEPTION',
         period_hash='LHC18o_i2',
         max_n_subjobs=200,
         n_files_per_subjob=3)

    # main_local(eos_main_dir_path='/eos/user/a/aliqat/www/qcml/data/2018/LHC18q',
    #      period_hash='LHC18q',
    #      n_files_per_subjob=10)
