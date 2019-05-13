#!/bin/python
#SBATCH --mail-type=ALL
#SBATCH --mail-user="sbysiak@cern.ch"
#SBATCH -A aliceo2qa

#SBATCH --output="LOGS/slurm/trending-%j.out"
#SBATCH --error="LOGS/slurm/trending-%j_error.out"
#SBATCH --mem-per-cpu=5GB
#SBATCH --mem=5GB
#SBATCH --time=10
# /// SBATCH -p plgrid-short




import subprocess
import sys
import os
import pexpect
from time import sleep, time

sys.path.append(os.getcwd()) # for slurm to find custom modules
from master_trending_jobs import check_file, check_file_root


def copy_from_eos_single(fpath_eos):
    if fpath_eos.startswith('eos'):
        fpath_eos = fpath_eos.replace('eos', '/eos')
    password='$tArstEk45'
    cmd = 'rsync -R --progress sbysiak@lxplus.cern.ch:{} .'.format(fpath_eos)
    print 'Running: {}\t...'.format(cmd)
    child = pexpect.spawn(cmd)
    child.timeout = 1200
    child.logfile = sys.stdout
    child.expect('Password: ')
    child.sendline(password)
    print 'before: ', child.before
    print 'after: ',  child.after
    child.expect(pexpect.EOF)


def copy_from_eos(infile, fsize_min_kb=10000):
    msg_not_found = 'WARNING - file: {} has not been copied!'
    with open(infile) as f:
        for fpath_eos in f:
            fpath_eos = fpath_eos.strip()
            n_trials_left = 3
            while True:
                if n_trials_left < 1: break
                try:
                    copy_from_eos_single(fpath_eos)
                except pexpect.exceptions.TIMEOUT:
                    print 'timeout exception, try once again ({} trial left)'.format(n_trials_left)
                    n_trials_left -= 1
                else:
                    status_std_check = check_file(fpath_eos, fsize_min_kb, msg_not_found=msg_not_found)
                    status_root_check = check_file_root(fpath_eos)
                    if status_std_check > 0 or status_root_check > 0:
                        print 'check_file failed, try once again ({} trial left)'.format(n_trials_left)
                        n_trials_left -= 1
                    else:
                        break


def validate_copying(infile, fsize_min_kb=10000):
    """function validating copying from EOS to PLGRID

    Parameters
    ----------
    infile : string
        name of file containing list of files to be copied
    fsize_min_kb : float
        minimal accepted size of copied file (in KB)
    Returns
    -------
    not_OK : int
        # issues (0 means all fine)
    """
    not_OK = 0
    msg_not_found = 'WARNING - file: {} has not been copied!'
    with open(infile) as f:
        for fpath_eos in f:
            fpath_eos = fpath_eos.strip()
            status_std_check = check_file(fpath_eos, fsize_min_kb, msg_not_found=msg_not_found)
            status_root_check = check_file_root(fpath_eos)
            if status_std_check > 0 or status_root_check > 0:
                not_OK += 1
    return not_OK


def validate_trending(infile, fsize_min_kb=50):
    """function validating generation of trending.root files

    Parameters
    ----------
    infile : string
        name of file containing list of files to be copied
    fsize_min_kb : float
        minimal accepted size of copied file (in KB)
    Returns
    -------
    not_OK : int
        # issues (0 means all fine)
    """
    not_OK = 0
    msg_not_found = 'WARNING - file: {} has not been generated!'
    with open(infile) as f:
        for fpath_eos in f:
            fpath_eos = fpath_eos.strip()
            fpath_trending = fpath_eos.replace('QAresults.root', 'trending.root')
            status = check_file(fpath_trending, fsize_min_kb, msg_not_found=msg_not_found)
            if status > 0:
                not_OK += 1
    return not_OK


def generate_trendings(infile):
    """ function executing make_trendings_parallel.sh - actual trendings extraction """
    cmd = 'bash make_trendings_parallel.sh {}'.format(infile)
    print 'Running {}\t...'.format(cmd)
    status = subprocess.call(cmd, shell=True)
    return status


def rm_QAresults(infile):
    """function removing processed QAresults.root
    """
    with open(infile) as f:
        for fpath_eos in f:
            fpath_eos = fpath_eos.strip()
            cmd = 'rm {}'.format(fpath_eos)
            subprocess.call(cmd, shell=True)


def load_aliroot():
    cmd = 'alienv load AliPhysics/latest-master-user-next-root6'
    print 'Running {}  ...'.format(cmd)
    subprocess.call(cmd, shell=True)

################################################################################


def main(infile):
    tic = time()
    # print '---' *20 + '\m LOAD ALIROOT\n' + '---'*20
    # load_aliroot()
    print '---' *20 + '\nCOPY FROM EOS\n' + '---'*20
    copy_from_eos(infile)
    print '---' *20 + '\nVALIDATE COPYING\n' + '---'*20
    n_issues_copying = validate_copying(infile)

    print '---' *20 + '\nGENERATE TRENDING\n' + '---'*20
    generate_trendings(infile)
    print '---' *20 + '\nVALIDATE TRENDING\n' + '---'*20
    n_issues_trending = validate_trending(infile)
    print '---' *20 + '\nREMOVE QARESULTS\n' + '---'*20
    rm_QAresults(infile)

    n_files_processed = subprocess.check_output('wc -l {}'.format(infile), shell=True).split()[0]
    print '\n\n'
    print 'Execution completed'
    print 'exec. time = {}'.format(time() - tic)
    print 'number of files processed: {}'.format(n_files_processed)
    print 'number of issues:\n\tcopying: {}\n\ttrending: {}'.format(n_issues_copying, n_issues_trending)
    return n_issues_trending


if __name__ == '__main__':
    exit_status = main(sys.argv[1])
    if exit_status: sys.exit(exit_status+1000)


# copy files from EOS

# generate trendings
#make_trendings_parallel.sh ".tmp_files_list_HASH"

# check if everything is processed

# if yes - remove QAresults.root

# if no - ALARM
