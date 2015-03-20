# -*- coding: utf-8 -*-
"""
Created on 19/2/15 3:23 PM

@author: Naveen Subramani
"""
__author__ = 'Naveen Subramani'

import sys
import getopt
import logging

from sfa_api import SfaAPI

log = logging.getLogger('zen.zenpymodeler')

class DDNConnection(object):
    def __init__(self, sfa_user, sfa_passwd, sfa_host, sfa_alt_host=None):
        self.sfa_host = sfa_host
        self.sfa_alt_host = sfa_alt_host
        self.sfa_user = sfa_user
        self.sfa_passwd = sfa_passwd
        self.conn = None

    def get_conn(self):
        if self.conn is None:
            self.conn = SfaAPI(self.sfa_user,
                               self.sfa_passwd,
                               self.sfa_host,
                               self.sfa_alt_host)
        log.debug("Conn obj %s", self.conn)
        return self.conn


class GETData(object):
    def __init__(self,conn, func):
        self.dConn = conn
        self.func = func

    # def __init__(self, *args, **kargs):
        # if kargs.get('func'):
        #     self.func = kargs.get('func')
        #     del kargs['func']
        # self.dConn = (DDNConnection(*args, **kargs)).get_conn()

    def get_results(self):
        return getattr(self, self.func)()

    def get_all_ctlr(self):
        r = self.dConn.context.execute(self.dConn.get_all_ctlr)
        return r

    def get_all_hcerrors(self):
        r = self.dConn.context.execute(self.dConn.get_all_hcerrors)
        return r

    def get_all_hcstats(self):
        r = self.dConn.context.execute(self.dConn.get_all_hcstats)
        return r

    def get_all_hostchn(self):
        r = self.dConn.context.execute(self.dConn.get_all_hostchn)
        return r

    def get_all_pdstats(self):
        r = self.dConn.context.execute(self.dConn.get_all_pdstats)
        return r

    def get_all_pds(self):
        r = self.dConn.context.execute(self.dConn.get_all_pds)
        return r

    def get_all_pools(self):
        r = self.dConn.context.execute(self.dConn.get_all_pools)
        return r

    def get_all_vdstats(self):
        r = self.dConn.context.execute(self.dConn.get_all_vdstats)
        return r

    def get_all_vds(self):
        r = self.dConn.context.execute(self.dConn.get_all_vds)
        return r


def fetch_data(conn, func):
    try:
        result = GETData(conn=conn,
                        func=func).get_results()
        log.debug("From Conn File : %r ",result)
        return result
    except Exception as e:
        log.error("Failed to Remote Get data Exception: %s Method : %s", e,
                  func)
        # sys.exit(0)

    return None

def connect(conn_params=None):
    """
    create a connection to object the remote device.
    Make a new SSH connection object if there isn't one available.
    This doesn't actually connect to the device.
    """
    if conn_params is None:
        conn_params = conn_params
    # log.debug("XXXX _connect instance %r, param %s",
    # self, str(conn_params))
    conn = None

    try:
        connection = DDNConnection(conn_params['user'],  # target
                                               conn_params['pass'],
                                               conn_params['target'],
                                               conn_params['alt_target'])
        conn = connection.get_conn()
        log.info("Trying to collect Metrics using target : %s",conn_params['target'])
    except Exception as e:
        log.warn("Error in conncetion connecting with sec Ip %s E: %s",
                 conn_params['alt_target'], e)
        if conn_params['target'] != conn_params['alt_target']:
            target = conn_params['alt_target']
            connection = DDNConnection(conn_params['user'],  # target
                                                   conn_params['pass'],
                                                   target,
                                                   conn_params['alt_target'])
            conn = connection.get_conn()

    return conn

def usage():
    print "Usage is : "
    print 'DDNConnPlugin.py -f <function to call> -u <user> [-p <passwd>] -k ' \
          '<keyfile> -t <target>'
    sys.exit(0)


def main(argv):
    username = ''
    password = ''
    keyfile = '~/.ssh/id_rsa'  # default key file
    target = ''

    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    try:
        opts, args = getopt.getopt(argv, "hf:u:p:k:t:")
    except getopt.GetoptError as e:
        print "Error: Failed to parse Args: ", e
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-f"):
            func = arg
        elif opt in ("-u"):
            username = arg
        elif opt in ("-p"):
            password = arg
        elif opt in ("-k"):
            keyfile = arg
        elif opt in ("-t"):
            target = arg

    if not target or not username or not func:
        usage()

    if password: keyfile = ''  # ignore keyfile if password preferred

    # result =  GETData(sfa_user=username, sfa_passwd=password, sfa_host=target,
    #               func=func).get_results()
    # result = fetch_data(username,password,target,func)
    # import pdb; pdb.set_trace()
    # print result


if __name__ == "__main__":
    main(sys.argv[1:])