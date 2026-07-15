import unittest

from sqlalchemy import create_mock_engine

from app.db.base import Base as CanonicalBase
from app.db.session import Base as SessionBase
from app.inventory.models.base import Base as InventoryModelBase

# Import the package entry point so every current ORM model is registered.
import app.inventory.models  # noqa: F401, E402


EXPECTED_TABLES = {
    "alerts",
    "audit_logs",
    "credentials",
    "cucm",
    "customers",
    "customers_contacts",
    "health_score",
    "incident_alert",
    "incidents",
    "maintenance_event",
    "monitoring_capabilities",
    "monitoring_execution_state",
    "monitoring_job_implementations",
    "monitoring_profile_jobs",
    "monitoring_profiles",
    "node_base",
    "node_credentials_mapping",
    "node_health",
    "node_health_component",
    "node_metric_state",
    "node_monitoring_overrides",
    "services",
    "systems",
    "users",
}

EXPECTED_MAPPERS = {
    "Alert",
    "AuditLog",
    "CUCM",
    "Credential",
    "Customer",
    "CustomerContact",
    "HealthScore",
    "Incident",
    "IncidentAlert",
    "MaintenanceEvent",
    "MonitoringCapability",
    "MonitoringExecutionState",
    "MonitoringJobImplementation",
    "MonitoringProfile",
    "MonitoringProfileJob",
    "NodeBase",
    "NodeCredentialMapping",
    "NodeHealth",
    "NodeHealthComponent",
    "NodeMetricState",
    "NodeMonitoringOverride",
    "Service",
    "System",
    "User",
}


class CanonicalMetadataTests(unittest.TestCase):
    def test_compatibility_imports_reexport_canonical_base(self):
        self.assertIs(SessionBase, CanonicalBase)
        self.assertIs(InventoryModelBase, CanonicalBase)

    def test_all_registered_mappers_use_canonical_metadata(self):
        mappers = list(CanonicalBase.registry.mappers)

        self.assertEqual(
            {mapper.class_.__name__ for mapper in mappers},
            EXPECTED_MAPPERS,
        )

        for mapper in mappers:
            with self.subTest(model=mapper.class_.__name__):
                self.assertIs(
                    mapper.local_table.metadata,
                    CanonicalBase.metadata,
                )

    def test_all_current_tables_are_registered(self):
        self.assertEqual(
            set(CanonicalBase.metadata.tables),
            EXPECTED_TABLES,
        )

    def test_canonical_metadata_supports_mock_create_all(self):
        emitted_ddl = []
        mock_engine = create_mock_engine(
            "postgresql+psycopg2://",
            lambda statement, *args, **kwargs: emitted_ddl.append(statement),
        )

        CanonicalBase.metadata.create_all(bind=mock_engine)

        self.assertGreaterEqual(len(emitted_ddl), len(EXPECTED_TABLES))


if __name__ == "__main__":
    unittest.main()
