
#this code requires dcm2niix installed

import os
import shlex
from subprocess import Popen, PIPE
import time as time
from os.path import join
import shutil
def get_exitcode_stdout_stderr(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    return exitcode, out, err

inpath= ''#input path
opath= ''#output path for the nifti files
if not os.path.exists(opath): os.makedirs(opath)
for path, imdir, files in os.walk(inpath):
    if files:
        if len(files)<10:
            continue
        # for timepoint in os.listdir(join(inpath,pt)):
        idir = path
        pt = idir.split('/')[-3]
        tp = idir.split('/')[-2]
        batch = idir.split('/')[-4]
        odir = join(opath,pt,tp)
        # set output directory   
        os.chdir(idir)
        # if os.path.exists(odir): 
        #     shutil.rmtree(odir)
        if not os.path.exists(odir):
            os.makedirs(odir)

        print('*************************************') 
        print('Image conversion DCM -> NIIX') 
        print('*************************************')  
        st = time.time()
        dcm_exe = r'dcm2niix'
        dir_io = ' '.join(['"'+odir+'"', '"'+idir+'"'])
        params_str = ' '.join(['-ba', 'y', '-i y', '-f', f'ICO_{pt}_{tp}_%s', '-w y','-o']) #CT
        call_str = " ".join([dcm_exe, params_str, dir_io])
        print(call_str)
        exitcode, out, err = get_exitcode_stdout_stderr(call_str)
        if exitcode: print('Terminated with error code:',exitcode,err); del exitcode
        elapsed_time = time.time() - st
        print('Done. Elapsed (time %.2fs)' % elapsed_time)
            