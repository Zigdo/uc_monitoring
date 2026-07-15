import unittest

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import CreateTable

import app.inventory.models  # noqa: F401, E402
from app.inventory.models.monitoring_execution_state import (
    MonitoringExecutionState,
)
from app.inventory.models.system import System


class SystemSchemaTests(unittest.TestCase):
    def test_system_sequence_constraint_has_intended_columns(self):
        constraints = [
            constraint
            for constraint in System.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
            and constraint.name == "uq_system_sequence"
        ]

        self.assertEqual(len(constraints), 1)
        self.assertEqual(
            tuple(constraints[0].columns.keys()),
            ("customer_id", "type", "sequence_number"),
        )

    def test_existing_customer_index_is_preserved(self):
        indexes = {
            index.name: tuple(index.columns.keys())
            for index in System.__table__.indexes
        }

        self.assertEqual(
            indexes["idx_system_customer"],
            ("customer_id",),
        )

    def test_system_code_remains_unique(self):
        unique_column_sets = {
            tuple(constraint.columns.keys())
            for constraint in System.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
        }

        self.assertIn(("system_code",), unique_column_sets)

    def test_postgresql_ddl_contains_system_sequence_constraint(self):
        ddl = str(
            CreateTable(System.__table__).compile(
                dialect=postgresql.dialect()
            )
        )

        normalized = " ".join(ddl.split())
        self.assertIn(
            "CONSTRAINT uq_system_sequence UNIQUE (customer_id, type, sequence_number)",
            normalized,
        )


class MonitoringExecutionStateSchemaTests(unittest.TestCase):
    FOREIGN_KEY_TARGETS = {
        "node_id": "node_base.id",
        "system_id": "systems.id",
        "customer_id": "customers.id",
        "implementation_id": "monitoring_job_implementations.id",
    }

    def test_foreign_keys_explicitly_match_referenced_uuid_types(self):
        for column_name, expected_target in self.FOREIGN_KEY_TARGETS.items():
            with self.subTest(column=column_name):
                column = MonitoringExecutionState.__table__.c[column_name]
                foreign_key = next(iter(column.foreign_keys))

                self.assertIsInstance(column.type, UUID)
                self.assertTrue(column.type.as_uuid)
                self.assertIsInstance(foreign_key.column.type, UUID)
                self.assertTrue(foreign_key.column.type.as_uuid)
                self.assertEqual(
                    type(column.type),
                    type(foreign_key.column.type),
                )
                self.assertEqual(foreign_key.target_fullname, expected_target)
                self.assertFalse(column.nullable)
                self.assertTrue(column.index)

    def test_execution_state_uniqueness_is_preserved(self):
        constraint = next(
            constraint
            for constraint in MonitoringExecutionState.__table__.constraints
            if isinstance(constraint, UniqueConstraint)
            and constraint.name == "uq_node_implementation_state"
        )

        self.assertEqual(
            tuple(constraint.columns.keys()),
            ("node_id", "implementation_id"),
        )

    def test_postgresql_ddl_uses_uuid_for_affected_foreign_keys(self):
        ddl = str(
            CreateTable(MonitoringExecutionState.__table__).compile(
                dialect=postgresql.dialect()
            )
        )
        normalized = " ".join(ddl.split())

        for column_name in self.FOREIGN_KEY_TARGETS:
            with self.subTest(column=column_name):
                self.assertIn(f"{column_name} UUID NOT NULL", normalized)


if __name__ == "__main__":
    unittest.main()
