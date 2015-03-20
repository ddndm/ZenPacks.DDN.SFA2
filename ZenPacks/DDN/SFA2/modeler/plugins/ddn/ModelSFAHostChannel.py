"""Models SFA Host Channel using local SFA API scripts."""

# Zenoss Imports
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin


class ModelSFAHostChannel(PythonPlugin):
    """ Models SFA Host Channel """

    relname = 'hostChannels'
    modname = 'ZenPacks.DDN.SFA2.HostChannel'

    requiredProperties = (
        'zCommandUsername',
        'zCommandPassword',
        'zSFASecondaryIp',
    )

    deviceProperties = PythonPlugin.deviceProperties + requiredProperties

    def collect(self, device, log):
        """Synchronously collect data from device. """
        log.info("%s: collecting SFAHostChannel data", device.id)
        rm = self.relMap()
        try:
            from ZenPacks.DDN.SFA2.lib.DDNConnPlugin import fetch_data, connect
            from ZenPacks.DDN.SFA2.lib.sfa_help import chn_makedict

            conn_parms = {}
            conn_parms['user'] = getattr(device, 'zCommandUsername', 'user')
            conn_parms['pass'] = getattr(device, 'zCommandPassword', 'pass')
            conn_parms['target'] = device.id
            conn_parms['alt_target'] = getattr(device, 'zSFASecondaryIp', None)
            conn = connect(conn_parms)
            func = 'get_all_hostchn'
            host_chnls = fetch_data(conn, func)

            for chn in host_chnls:
                model = chn_makedict(chn)
                model['id'] = model.get('title')
                rm.append(self.objectMap(model))
        except Exception as e:
            log.error("Exception : %s", str(e))
            return None
        return rm

    def process(self, device, results, log):
        """Process results. Return iterable of datamaps or None."""
        return results
