from twisted.internet import reactor
import logging

from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap


log = logging.getLogger('zen.zenpymodeler')

from ZenPacks.DDN.SFA2.lib.sfa_help import chn_makedict, chnstat_makedict, \
    pd_makedict, pdstat_makedict, vd_makedict, vdstat_makedict

from ZenPacks.DDN.SFA2.lib.DDNMetricPlugin import DDNMetricPlugin


class HcPlugin(DDNMetricPlugin):
    """HcPlugin collects SFA Host Channel metrics."""

    # List of device attributes you'll need to do collection.
    @classmethod
    def params(cls, datasource, context):
        return {}

    def __init__(self):
        super(HcPlugin, self).__init__()

    def collect(self, config):
        """
        No default collect behavior. You must implement this method.

        This method must return a Twisted deferred. The deferred results will
        be sent to the onResult then either onSuccess or onError callbacks
        below.
        """

        log.info("Collecting Metrics for Device __class__ : %s ",
                 self.__class__.__name__)

        self.initConnectionParams(config)
        conn = self.connect()
        from ZenPacks.DDN.SFA2.lib.DDNConnPlugin import fetch_data

        func = 'get_all_hcstats'
        stats = fetch_data(conn, func)

        func = 'get_all_hcerrors'
        errors = fetch_data(conn, func)

        func = 'get_all_hostchn'
        chans = fetch_data(conn, func)

        reactor.callLater(0, self.assemble, chans, stats, errors)
        log.debug("Deferred Obj: %s ", self.ext_defer)
        return self.ext_defer

    def prepare_values(self, stats, errors):
        values = {}
        for item, eitem in zip(stats, errors):
            index = 'HostChannel_{0}'.format(str(item.Index))
            values[index] = chnstat_makedict(item, eitem)
        return values

    def prepare_alert(self, chn):
        if chn['LinkState'] == 'DOWN':
            alert = {}
            alert['summary'] = 'Host Channel {0} link is down.'.format(
                chn['id'])
            alert['eventKey'] = chn['id']
            alert['severity'] = 4
            alert['eventClass'] = '/Perf'
            alert['component'] = chn['id']  # associates with component
            return alert
        return None

    # Return a dictionary... empty dictionary is fine too.
    def prepare_map(self, chans):
        events = []
        maps = []
        for c in chans:
            model = chn_makedict(c)
            comp = model.get('id')
            maps.append(ObjectMap(data=model,
                                  modname='ZenPacks.DDN.SFA2.HostChannel'))
            log.debug('XXX updated model for component %s', comp)
            alert = self.prepare_alert(model)
            if alert:
                events.append(alert)
                log.debug('XXX updated events for component %s', comp)
        rmap = RelationshipMap(relname="hostChannels",
                               modname="ZenPacks.DDN.SFA2.HostChannel",
                               objmaps=maps)
        return {'events': events, 'maps': [rmap]}

    def assemble(self, chans, stats, errors):
        result = self.prepare_map(chans)
        result['values'] = self.prepare_values(stats, errors)
        self.ext_defer.callback(result)

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


class PdPlugin(DDNMetricPlugin):
    """PdPlugin collects SFA Physical disk metrics."""

    # List of device attributes you'll need to do collection.
    @classmethod
    def params(cls, datasource, context):
        return {}

    def __init__(self):
        super(PdPlugin, self).__init__()

    def collect(self, config):
        """
        No default collect behavior. You must implement this method.

        This method must return a Twisted deferred. The deferred results will
        be sent to the onResult then either onSuccess or onError callbacks
        below.
        """

        log.info("Collecting Metrics for Device __class__ : %s ",
                 self.__class__.__name__)
        self.initConnectionParams(config)
        conn = self.connect()
        from ZenPacks.DDN.SFA2.lib.DDNConnPlugin import fetch_data

        func = 'get_all_pdstats'
        stats = fetch_data(conn, func)

        func = 'get_all_pds'
        pds = fetch_data(conn, func)

        reactor.callLater(0, self.assemble, pds, stats)
        return self.ext_defer

    def onError(self, result, config):
        """
        Called only on error. After onResult, before onComplete.
        """
        log.error('XXXX onError result=%r', result)
        data = self.new_data()
        data['events'] = [{
                              'summary': 'error: %s' % result,
                              'eventKey': 'SFAPhysicalDisk',
                              'severity': 3,
                          }]
        return data

    def prepare_alert(self, d):
        alert = {}
        if d['DiskHealthState'] == 'FAILED':
            alert['summary'] = \
                'Physical Disk Drive {2} failed. Enclosure {0}, SlotNumber {' \
                '1}' \
                    .format(d['EnclosureIndex'], d['DiskSlotNumber'], d['id'])
            alert['eventKey'] = d['id']
            alert['severity'] = 4
            alert['eventClass'] = '/Perf'
            alert['component'] = d['id']  # associates with component
            return alert
        if d['DiskHealthState'] == 'FAILURE_PREDICTED':
            alert['summary'] = \
                'Physical Disk Drive {2} predicted to fail. Enclosure {0}, ' \
                'SlotNumber {1}' \
                    .format(d['EnclosureIndex'], d['DiskSlotNumber'], d['id'])
            alert['eventKey'] = d['id']
            alert['severity'] = 3
            alert['eventClass'] = '/Perf'
            alert['component'] = d['id']  # associates with component
            return alert
        return None

    def prepare_map(self, pds):
        events = []
        maps = []
        for d in pds:
            model = pd_makedict(d)
            comp = model.get('id')
            maps.append(ObjectMap(data=model,
                                  modname='ZenPacks.DDN.SFA2.PhysicalDisk'))
            log.debug('XXX updated model for component %s', comp)
            alert = self.prepare_alert(model)
            if alert:
                events.append(alert)
                log.debug('XXX updated events for component %s', comp)
        rmap = RelationshipMap(relname="physicalDisks",
                               modname="ZenPacks.DDN.SFA2.PhysicalDisk",
                               objmaps=maps)
        return {'events': events, 'maps': [rmap]}

    def prepare_values(self, stats):
        log.debug('XXX prepare values for updating metrics, stats = %r', stats)
        values = {}
        for d in stats:
            index = 'PD_{0}'.format(str(d.Index))
            log.debug('XXX collecting metrics for phydrv %s', index)
            values[index] = pdstat_makedict(d)
        log.debug('XXX collected metrics for %d components', len(values))
        return values

    def assemble(self, pds, stats):
        aggregate = self.prepare_map(pds)
        aggregate['values'] = self.prepare_values(stats)
        self.ext_defer.callback(aggregate)
        log.debug('XXXX final assembled result %r', aggregate)


class VdPlugin(DDNMetricPlugin):
    """VdPlugin collects SFA Virtual disk metrics."""

    # List of device attributes you'll need to do collection.
    @classmethod
    def params(cls, datasource, context):
        log.debug("XXX GsMetricPlugin params(cls=%r, datasource=%r, context=%r"
                  % (cls, datasource, context))
        return {}

    def __init__(self):
        super(VdPlugin, self).__init__()

    def collect(self, config):
        """
        No default collect behavior. You must implement this method.

        This method must return a Twisted deferred. The deferred results will
        be sent to the onResult then either onSuccess or onError callbacks
        below.
        """

        log.info("Collecting Metrics for Device __class__ : %s ",
                 self.__class__.__name__)
        self.initConnectionParams(config)
        conn = self.connect()
        from ZenPacks.DDN.SFA2.lib.DDNConnPlugin import fetch_data

        func = 'get_all_vdstats'
        stats = fetch_data(conn, func)

        func = 'get_all_vds'
        vds = fetch_data(conn, func)

        reactor.callLater(0, self.assemble, vds, stats)
        return self.ext_defer

    def onError(self, result, config):
        """
        Called only on error. After onResult, before onComplete.
        """
        log.error('XXXX onError result=%r', result)
        data = self.new_data()
        data['events'] = [{
                              'summary': 'error: %s' % result,
                              'eventKey': 'SFAVirtualDisk',
                              'severity': 3,
                          }]
        return data


    def prepare_alert(self, d):
        state = d['State']
        if state == 'NONE' or state == 'NOT_READY' or state == 'INOPERATIVE' \
                or state == 'AUTO_WRITE_LOCKED' or state == 'CRITICAL' or \
                        state == 'DELETED' or state == \
                'FORCED_WRITE_THROUGH' or \
                        state == 'INIT_FAILED':
            alert = {}
            alert['summary'] = \
                'Virtual Disk Drive {0} is in non optimal state-{1}.' \
                    .format(d['id'], state)
            alert['eventKey'] = d['id']
            alert['severity'] = 4
            alert['eventClass'] = '/Perf'
            alert['component'] = d['id']  # associates with component
            return alert
        return None

    def prepare_map(self, vds):
        events = []
        maps = []
        for d in vds:
            model = vd_makedict(d)
            comp = model.get('id')
            maps.append(ObjectMap(data=model,
                                  modname='ZenPacks.DDN.SFA2.VirtualDisk'))
            log.debug('XXX updated model for component %s', comp)
            alert = self.prepare_alert(model)
            if alert:
                events.append(alert)
                log.debug('XXX updated events for component %s', comp)
        rmap = RelationshipMap(relname="virtualDisks",
                               modname="ZenPacks.DDN.SFA2.VirtualDisk",
                               objmaps=maps)
        return {'events': events, 'maps': [rmap]}

    def prepare_values(self, stats):
        values = {}
        for d in stats:
            index = 'VD_{0}'.format(str(d.Index))
            log.debug('XXX collecting metrics for phydrv %s', index)
            values[index] = vdstat_makedict(d)
        return values

    def assemble(self, vds, stats):
        aggregate = self.prepare_map(vds)
        aggregate['values'] = self.prepare_values(stats)
        self.ext_defer.callback(aggregate)
        log.debug('XXXX final assembled result %r', aggregate)

