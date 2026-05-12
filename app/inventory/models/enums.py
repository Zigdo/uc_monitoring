import enum

class CustomerType(enum.Enum):
    government_core = "government_core"
    government_op = "government_op"
    nilvim_core = "nilvim_core"
    nilvim_op = "nilvim_op"
    hcs = "hcs"


class ApplicationType(enum.Enum):
    cucm = "cucm"
    imp = "imp"
    cuc = "cuc"
    uccx = "uccx"


class ServiceType(enum.Enum):
    cpu = "cpu"
    sip = "sip"
    memory = "memory"
    disk = "disk"

class CredentialType(enum.Enum):
    application = "application"
    platform = "platform"
    snmp = "snmp"


class SeverityType(enum.Enum):
    critical = "critical"
    high = "high"
    low = "low"

class StatusType(enum.Enum):
    good = "good"
    fail = "fail"

class EntityType(enum.Enum):
    cucm = "cucm"
    imp = "imp"

class MaintenanceStatus(enum.Enum):
    enabled = "enabled"
    disabled = "disabled"