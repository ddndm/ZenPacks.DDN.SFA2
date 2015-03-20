"""Models SFA storage pool using local SFA API scripts."""

# stdlib Imports

# Zenoss Imports
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin


class ModelSFAPool(PythonPlugin):
    """ Models SFA Host Channel """

    relname = 'pools'
    modname = 'ZenPacks.DDN.SFA2.Pool'

    requiredProperties = (
        'zCommandUsername',
        'zCommandPassword',
        'zSFASecondaryIp',
    )

    deviceProperties = PythonPlugin.deviceProperties + requiredProperties

    def collect(self, device, log):
        """Synchronously collect data from device. """
        log.info("%s: collecting Storage Pool data", device.id)
        rm = self.relMap()
        try:
            from ZenPacks.DDN.SFA2.lib.DDNConnPlugin import fetch_data, connect
            from ZenPacks.DDN.SFA2.lib.sfa_help import pool_makedict

            conn_parms = {}
            conn_parms['user'] = getattr(device, 'zCommandUsername', 'user')
            conn_parms['pass'] = getattr(device, 'zCommandPassword', 'pass')
            conn_parms['target'] = device.id
            conn_parms['alt_target'] = getattr(device, 'zSFASecondaryIp', None)
            conn = connect(conn_parms)
            func = 'get_all_pools'
            pools = fetch_data(conn, func)

            log.debug("Pools are : %s", str(pools))
            for pool in pools:
                model = pool_makedict(pool)
                rm.append(self.objectMap(model))
            return rm
        except Exception as e:
            log.error('SFAPool Exception : %s', str(e))
            return None

    def process(self, device, results, log):
        """Process results. Return iterable of datamaps or None."""
        return results
