"""Utility class for some common functions"""
__author__ = "Madhur Nawandar"
__email__ = "mnawandar@ddn.com"
__date__ = "Aug 26, 2013"
__copyright__ = "(c) 2013 DataDirect Networks, Inc. All rights reserved."

# Import system modules
import subprocess
import time
import sys
#import cherrypy
import tempfile
import os
# Import local module
from sfa_api import SfaAPI
#from sfa_test_api import SfaAPI as SfaTestAPI
#from config import Config, LUSTRE_FS_TYPE, GPFS_FS_TYPE

TIMEOUT = 1000
#log = cherrypy.log

def run_cmd_stdout(cmd, store_op_in_file=False):
    if store_op_in_file:
        (fd, name) = tempfile.mkstemp(dir='/tmp/', prefix='sfxoob-')
        fp = os.fdopen(fd, 'w')
        cmd = subprocess.Popen(cmd, close_fds=True, stdout=fp, stderr=subprocess.PIPE)
    else:
        cmd = subprocess.Popen(cmd, close_fds=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    poll_seconds = .250
    deadline = time.time() + TIMEOUT
    while time.time() < deadline and cmd.poll() == None:
        time.sleep(poll_seconds)

    if cmd.poll() == None:
        #log.error("Error: Command failed with timeout: %s" % ' '.join(cmd))
        cmd.terminate()
        sys.exit(1)

    if cmd.poll() != 0 :
        #log.error("Error: Command '%s' failed with exit status: %s Error: %s" % (' '.join(cmd), cmd.poll(), cmd.communicate()[1]))
        sys.exit(1)
    if store_op_in_file:
        fp.close()
        fp = open(name, 'r')
        output = fp.read()
        fp.close()
        os.remove(name)
        return output
    return cmd.communicate()[0]

def filter_extentsdo_from_frag_extents(extentsdo, frag_extents):
    filtered_extentsdo = []
    for frag_extent in frag_extents:
        for extentdo in extentsdo:
            if (frag_extent.start_lba >= extentdo.start_block and
                frag_extent.start_lba <= (extentdo.start_block + extentdo.num_block) and
                frag_extent.vdi == extentdo.vdi):
                filtered_extentsdo.append(extentdo)
                break
    return filtered_extentsdo

def get_sfa_api(sfa_user, sfa_passwd, sfa_host, sfa_alt_host=None):
    #config = Config()
    return SfaAPI(sfa_user, sfa_passwd, sfa_host, sfa_alt_host)

def get_mount_pt_from_fs_name_and_type(fs_name, fs_type):
    mounts = run_cmd_stdout(['mount', '-t', fs_type])
    mounts = mounts.splitlines()
    if fs_type == LUSTRE_FS_TYPE:
        for mount in mounts:
            if mount.find(":/%s" % fs_name) > -1:
                result = mount.split(' ')
                return result[2]
    elif fs_type == GPFS_FS_TYPE:
        for mount in mounts:
            if mount.find("dev=%s" % fs_name) > -1:
                result = mount.split(' ')
                return result[2]
    raise Exception("Unable to find mount point for filesystem %s of type %s" % (fs_name, fs_type))
