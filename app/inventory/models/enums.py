from enum import Enum

class CustomerType(Enum):
    government_core = "government_core"
    government_op = "government_op"
    nilvim_core = "nilvim_core"
    nilvim_op = "nilvim_op"
    hcs = "hcs"


class ApplicationType(Enum):
    cucm = "cucm"
    imp = "imp"
    cuc = "cuc"
    uccx = "uccx"


class ServiceType(Enum):
    cpu = "cpu"
    sip = "sip"
    memory = "memory"
    disk = "disk"

class CredentialType(Enum):
    application = "application"
    platform = "platform"
    snmp = "snmp"


class SeverityType(Enum):
    critical = "critical"
    high = "high"
    low = "low"

class StatusType(Enum):
    good = "good"
    fail = "fail"

class EntityType(Enum):
    cucm = "cucm"
    imp = "imp"

class MaintenanceStatus(Enum):
    enabled = "enabled"
    disabled = "disabled"


class ExecutionStatus(str, Enum):

    SUCCESS = "success"

    FAILED = "failed"

    WARNING = "warning"

    UNKNOWN = "unknown"


class ExecutionStage(str, Enum):

    SSH = "ssh"

    PARSE = "parse"

    WRITE = "write"

    COMPLETE = "complete"

class HealthStatus(str, Enum):

    HEALTHY = "HEALTHY"

    WARNING = "WARNING"

    CRITICAL = "CRITICAL"

    UNKNOWN = "UNKNOWN"