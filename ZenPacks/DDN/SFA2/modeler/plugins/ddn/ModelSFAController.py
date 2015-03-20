"""Models SFA Controllers using local SFA API scripts."""

# stdlib Imports

# Zenoss Imports
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin


class ModelSFAController(PythonPlugin):
    """ Models SFA Controllers """

    relname = 'controllers'
    modname = 'ZenPacks.DDN.SFA2.Controller'

    requiredProperties = (
        'zCommandUsername',
        'zCommandPassword',
        'zSFASecondaryIp',
    )

    deviceProperties = PythonPlugin.deviceProperties + requiredProperties

    def collect(self, device, log):
        """Synchronously collect data from device. """
        log.info("%s: collecting data", device.id)
        rm = self.relMap()
        try:
            from ZenPacks.DDN.SFA2.lib.DDNConnPlugin import fetch_data, connect
            from ZenPacks.DDN.SFA2.lib.sfa_help import ctrl_makedict

            conn_parms = {}
            conn_parms['user'] = getattr(device, 'zCommandUsername', 'user')
            conn_parms['pass'] = getattr(device, 'zCommandPassword', 'pass')
            conn_parms['target'] = device.id
            conn_parms['alt_target'] = getattr(device, 'zSFASecondaryIp', None)
            conn = connect(conn_parms)
            func = 'get_all_ctlr'
            ctrls = fetch_data(conn, func)

            for ctrl in ctrls:
                model = ctrl_makedict(ctrl)
                rm.append(self.objectMap(model))
            return rm
        except Exception as e:
            log.error('SFAController Exception %s' % str(e))
            return None

    def process(self, device, results, log):
        """Process results. Return iterable of datamaps or None."""
        return results
