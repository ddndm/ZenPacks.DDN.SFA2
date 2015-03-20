# Import zenpacklib from the current directory (zenpacklib.py).
from . import zenpacklib

# Create a ZenPackSpec and name it CFG.

CFG = zenpacklib.ZenPackSpec(
    name=__name__,

    zProperties={
        'DEFAULTS': {'category': 'DDN SFA Storage Array'},
        # 'zSFAChosenIp': {
        #     'type': 'string',
        #     'default': 'None',
        # },
        'zSFASecondaryIp': {
            'type': 'string',
        },
    },
    classes={
        'SFADevice': {
            'base': zenpacklib.Device,
            'label': 'SFADevice',

            'properties': {
                'vdskcount_total': {
                    'label': 'VirtualDiskCount_Total',
                    'order': 4.0,
                },

                'vdskcount_awl': {
                    'label': 'VirtualDiskCount_AWL',
                    'order': 4.1,
                },

                'vdskcount_critical': {
                    'label': 'VirtualDiskCount_Critical',
                    'order': 4.2,
                },

                'vdskcount_inop': {
                    'label': 'VirtualDiskCount_INOP',
                    'order': 4.3,
                },

                'pdskcount_total': {
                    'label': 'PhysicalDiskCount_Total',
                    'order': 4.4,
                },

                'pdskcount_failed': {
                    'label': 'PhysicalDiskCount_Failed',
                    'order': 4.5,
                },

                'pdskcount_assigned': {
                    'label': 'PhysicalDiskCount_Assigned',
                    'order': 4.6,
                },

                'pdskcount_spare': {
                    'label': 'PhysicalDiskCount_Spare',
                    'order': 4.7,
                },

                'poolcount_total': {
                    'label': 'PoolCount_Total',
                    'order': 4.8,
                },

                'poolcount_degraded': {
                    'label': 'PoolCount_Degraded',
                    'order': 4.9,
                },

                'poolcount_nored': {
                    'label': 'PoolCount_NORED',
                    'order': 4.10,
                },

                'overall_health': {
                    'label': 'OverallHealth',
                    'order': 4.11,
                },
                'system_primary_ip': {
                    'label': 'Primary IP',
                    'order': 4.12,
                },
                'system_secondary_ip': {
                    'label': 'Secondary IP',
                    'order': 4.13,
                },
                'system_model': {
                    'label': 'Model',
                    'order': 4.14,
                },
            }
        },

        'Controller': {
            'base': zenpacklib.Component,
            'label': 'Controller',
            'properties': {
                'id': {
                    'label': 'id',
                    'order': 4.0,
                },

                'Primary': {
                    'label': 'Primary',
                    'order': 4.1,
                },

                'Local': {
                    'label': 'Local',
                    'order': 4.2,
                },

                'HealthState': {
                    'label': 'HealthState',
                    'order': 4.3,
                },

                'State': {
                    'label': 'State',
                    'order': 4.5,
                },

                'Description': {
                    'label': 'Description',
                    'order': 4.6,
                },

                'ID': {
                    'label': 'ID',
                    'order': 4.7,
                },
            },
        },

        'HostChannel': {
            'base': zenpacklib.Component,
            'label': 'HostChannel',
            'properties': {
                'id': {
                    'label': 'id',
                    'order': 4.0,
                },
                'Type': {
                    'label': 'Type',
                    'order': 4.0,
                },
                'LinkState': {
                    'label': 'LinkState',
                    'order': 4.1,
                },

                'PortID': {
                    'label': 'PortID',
                    'order': 4.2,
                },

                'Speed': {
                    'label': 'Speed',
                    'order': 4.3,
                },
                'ControllerIndex': {
                    'label': 'ControllerIndex',
                    'order': 4.4,
                },
                'Port': {
                    'label': 'Port',
                    'order': 4.5,
                },
                'VendorID': {
                    'label': 'VendorID',
                    'order': 4.6,
                },
                'ProductID': {
                    'label': 'ProductID',
                    'order': 4.7,
                },
            },
        },

        'Pool': {
            'base': zenpacklib.Component,
            'label': 'Pool',
            'properties': {
                'id': {
                    'label': 'id',
                    'order': 4.0,
                },
                'OID': {
                    'label': 'OID',
                    'order': 4.1,
                },
                'UUID': {
                    'label': 'UUID',
                    'order': 4.2,
                },
                'Type': {
                    'label': 'Type',
                    'order': 4.3,
                },
                'BlockSize': {
                    'label': 'BlockSize',
                    'order': 4.4,
                },
                'RawCapacity': {
                    'label': 'RawCapacity',
                    'order': 4.5,
                },
                'FreeCapacity': {
                    'label': 'FreeCapacity',
                    'order': 4.6,
                },
                'RAIDLevel': {
                    'label': 'RAIDLevel',
                    'order': 4.7,
                },
                'NumDisks': {
                    'label': 'NumDisks',
                    'order': 4.8,
                },
                'InitStatus': {
                    'label': 'InitStatus',
                    'order': 4.9,
                },
                'SparingPolicy': {
                    'label': 'SparingPolicy',
                    'order': 4.10,
                },
                'InitPolicy': {
                    'label': 'InitPolicy',
                    'order': 4.11,
                },
            },
        },

        'VirtualDisk': {
            'base': zenpacklib.Component,
            'label': 'VirtualDisk',
            'properties': {
                'id': {
                    'label': 'id',
                    'order': 4.0,
                },
                'OID': {
                    'label': 'OID',
                    'order': 4.1,
                },

                'UUID': {
                    'label': 'UUID',
                    'order': 4.2,
                },

                'PoolIndex': {
                    'label': 'PoolIndex',
                    'order': 4.5,
                },
                'Capacity': {
                    'label': 'Capacity',
                    'order': 4.6,
                },
                'Offset': {
                    'label': 'Offset',
                    'order': 4.7,
                },
                'BadBlockCount': {
                    'label': 'BadBlockCount',
                    'order': 4.8,
                },
                'State': {
                    'label': 'State',
                    'order': 4.9,
                },
                'HealthState': {
                    'label': 'HealthState',
                    'order': 4.10,
                },
                'CreatedOn': {
                    'label': 'CreatedOn',
                    'order': 4.11,
                },
            },
        },

        'PhysicalDisk': {
            'base': zenpacklib.Component,
            'label': 'PhysicalDisk',
            'properties': {
                'id': {
                    'label': 'id',
                    'order': 4.0,
                },
                'SerialNumber': {
                    'label': 'SerialNumber',
                    'order': 4.1,
                },
                'WWN': {
                    'label': 'WWN',
                    'order': 4.2,
                },

                'VendorID': {
                    'label': 'VendorID',
                    'order': 4.3,
                },
                'ProductID': {
                    'label': 'ProductID',
                    'order': 4.4,
                },
                'ProductRevision': {
                    'label': 'ProductRevision',
                    'order': 4.5,
                },
                'RawCapacity': {
                    'label': 'RawCapacity',
                    'order': 4.6,
                },
                'FormattedCapacity': {
                    'label': 'FormattedCapacity',
                    'order': 4.7,
                },
                'BlockSize': {
                    'label': 'BlockSize',
                    'order': 4.8,
                },
                'DiskHealthState': {
                    'label': 'DiskHealthState',
                    'order': 4.9,
                },
                'RotationSpeed': {
                    'label': 'RotationSpeed',
                    'order': 4.10,
                },
                'State': {
                    'label': 'State',
                    'order': 4.11,
                },
                'HealthState': {
                    'label': 'HealthState',
                    'order': 4.12,
                },
                'Spare': {
                    'label': 'Spare',
                    'order': 4.13,
                },
                'EnclosureIndex': {
                    'label': 'EnclosureIndex',
                    'order': 4.14,
                },
                'DiskSlotNumber': {
                    'label': 'DiskSlotNumber',
                    'order': 4.15,
                },
            },
        },

        'StorageSystem': {
            'base': zenpacklib.Component,
            'label': 'StorageSystem',
            'properties': {
                'id': {
                    'label': 'id',
                    'order': 4.0,
                },

                'SFXCapable': {
                    'label': 'SFXCapable',
                    'order': 4.2,
                },
                'SFXEnabled': {
                    'label': 'SFXEnabled',
                    'order': 4.3,
                },
                'UUID': {
                    'label': 'UUID',
                    'order': 4.4,
                },
                'HealthState': {
                    'label': 'HealthState',
                    'order': 4.5,
                },
                'ChildHealthState': {
                    'label': 'ChildHealthState',
                    'order': 4.6,
                },
            },
        },
    },

    class_relationships=zenpacklib.relationships_from_yuml(
        """[SFADevice]++-[Controller]
           [SFADevice]++-[HostChannel]
           [SFADevice]++-[Pool]
           [SFADevice]++-[VirtualDisk]
           [SFADevice]++-[PhysicalDisk]
           [SFADevice]++-[StorageSystem]"""
    )
)

# Create the specification.
CFG.create()
