"""Models SFA physical disk using local SFA API scripts."""

# Zenoss Imports
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin


class ModelSFAPhysicalDisk(PythonPlugin):
    """ Models SFA Host Channel """

    relname = 'physicalDisks'
    modname = 'ZenPacks.DDN.SFA2.PhysicalDisk'

    requiredProperties = (
        'zCommandUsername',
        'zCommandPassword',
        'zSFASecondaryIp',
    )

    deviceProperties = PythonPlugin.deviceProperties + requiredProperties

    def collect(self, device, log):
        """Synchronously collect data from device. """
        log.info("%s: collecting Physical disk data", device.id)

        rm = self.relMap()
        try:
            from ZenPacks.DDN.SFA2.lib.sfa_help import pd_makedict
            from ZenPacks.DDN.SFA2.lib.DDNConnPlugin import fetch_data, connect

            conn_parms = {}
            conn_parms['user'] = getattr(device, 'zCommandUsername', 'user')
            conn_parms['pass'] = getattr(device, 'zCommandPassword', 'pass')
            conn_parms['target'] = device.id
            conn_parms['alt_target'] = getattr(device, 'zSFASecondaryIp', None)
            conn = connect(conn_parms)
            func = 'get_all_pds'
            disks = fetch_data(conn, func)

            for d in disks:
                model = pd_makedict(d)
                log.debug('XXX modeled physical disk[%d]=%r', int(d.Index), rm)
                rm.append(self.objectMap(model))
            log.debug('XXX modeled physical disk as %r', rm)
            return rm
        except Exception as e:
            log.error('SFAPhysicalDisk exception %s' % str(e))
            return None

    def process(self, device, results, log):
        """Process results. Return iterable of datamaps or None."""
        return results
