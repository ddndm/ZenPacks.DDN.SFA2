# -*- coding: utf-8 -*-
"""
Created on 18/3/15 1:11 PM

@author: Naveen Subramani
"""
__author__ = 'Naveen Subramani'


import logging
from twisted.internet.defer import maybeDeferred, Deferred, DeferredList

from Products.ZenEvents import ZenEventClasses
from Products.ZenUtils.Executor import TwistedExecutor
from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSourcePlugin
import DDNConnPlugin


log = logging.getLogger('zen.zenpymetrics')

class DDNMetricPlugin(PythonDataSourcePlugin):
    # List of device attributes you'll need to do collection.
    proxy_attributes = (
        'zCommandUsername',
        'zCommandPassword',
        'zSFASecondaryIp',
    )

    def __init__(self):
        self.config = None
        self.ext_defer = Deferred()

    # called when collect() method gets called.
    def initConnectionParams(self, config):
        self.config = config
        ## Pick info only from device component.
        for ds in config.datasources:
            if not ds.component:  # device has no component defined
                break
        else:
            ds = config.datasources[0]

        # templateId = ds.template
        self._config_key = ds.config_key
        self._config_params = ds.params
        self.conn_params = {'user': ds.zCommandUsername,
                            'pass': ds.zCommandPassword,
                            'target': config.id,  # targets
                            'alt_target': ds.zSFASecondaryIp,  # targets
                            }
        return self.conn_params


    @classmethod
    def config_key(cls, datasource, context):
        """
        Return a tuple defining collection uniqueness.

        This is a classmethod that is executed in zenhub. The datasource and
        context parameters are the full objects.

        This example implementation is the default. Split configurations by
        device, cycle time, template id, datasource id and the Python data
        source's plugin class name.

        You can omit this method from your implementation entirely if this
        default uniqueness behavior fits your needs. In many cases it will.
        """
        return (
            context.device().id,
            datasource.getCycleTime(context),
            datasource.rrdTemplate().id,
            datasource.id,
            datasource.plugin_classname,
        )

    @classmethod
    def params(cls, datasource, context):
        """
        Return params dictionary needed for this plugin.

        This is a classmethod that is executed in zenhub. The datasource and
        context parameters are the full objects.

        This example implementation will provide no extra information for
        each data source to the collect method.

        You can omit this method from your implementation if you don't require
        any additional information on each of the datasources of the config
        parameter to the collect method below. If you only need extra
        information at the device level it is easier to just use
        proxy_attributes as mentioned above.
        """
        raise NotImplementedError

    def connect(self,conn_params=None):
        """
        create a connection to object the remote device.
        Make a new SSH connection object if there isn't one available.
        This doesn't actually connect to the device.
        """
        if conn_params is None:
            conn_params = self.conn_params
        # log.debug("XXXX _connect instance %r, param %s",
        # self, str(conn_params))
        conn = None

        try:
            connection = DDNConnPlugin.DDNConnection(conn_params['user'],  # target
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
                connection = DDNConnPlugin.DDNConnection(conn_params['user'],  # target
                                                       conn_params['pass'],
                                                       target,
                                                       conn_params['alt_target'])
                conn = connection.get_conn()

        return conn

    def onSuccess(self, result, config):
        """
        Called only on success. After onResult, before onComplete.

        You should return a data structure with zero or more events, values
        and maps.
        """
        log.info("Successfully Collected Metrics for Device __class__ : %s ",
                 self.__class__.__name__)
        log.debug("On success result %s",result)

        return result

    def onError(self, result, config):
        """
        Called only on error. After onResult, before onComplete.
        """
        log.error('XXXX onError result=%r', result)
        data = self.new_data()
        data['events'] = [{
                              'summary': 'error: %s' % result,
                              'eventKey': 'SFAHostChannel',
                              'severity': 3,
                          }]
        return data

    def onComplete(self, result, config):
        """
        Called last for success and error.

        You can omit this method if you want the result of either the
        onSuccess or onError method to be used without further processing.
        """
        self.ext_defer = Deferred()  # oncomplete: Clear the commands list bcoz it leads
        # error while we run zenpython in background
        return result



