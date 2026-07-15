# PR 3 schema integrity corrections

PR 3 corrects two active ORM schema definitions. It does not modify a live
database and does not introduce migrations.

## System sequence uniqueness

The `systems` table has one named composite uniqueness constraint:

```text
uq_system_sequence(customer_id, type, sequence_number)
```

The existing `idx_system_customer` index remains on `customer_id`, and
`system_code` remains independently unique. The constraint uses the existing
database column named `type`; no table or column was renamed.

## Monitoring execution foreign keys

These `monitoring_execution_state` columns explicitly use PostgreSQL
`UUID(as_uuid=True)` and Python `uuid.UUID` values:

- `node_id` -> `node_base.id`
- `system_id` -> `systems.id`
- `customer_id` -> `customers.id`
- `implementation_id` -> `monitoring_job_implementations.id`

The execution-state primary key remains a UUID-formatted string stored in a
`VARCHAR`. Relationships, indexes, nullability, and
`uq_node_implementation_state` are unchanged.

## Fresh and existing databases

A fresh PostgreSQL schema generated from the canonical metadata includes the
correct system uniqueness constraint and explicit UUID foreign-key columns.

Changing ORM definitions does not alter an existing database. PR 4 must inspect
the deployed schema before producing migrations:

1. Check for duplicate `(customer_id, type, sequence_number)` rows before
   adding `uq_system_sequence`.
2. Inspect the four execution-state column types.
3. If they are already UUID, no data conversion is needed.
4. If any are text, validate every value and referenced row before converting
   with an explicit PostgreSQL UUID cast and recreating affected constraints.

PR 3 intentionally does not fix unrelated annotations, relationships,
constraints, sequence-allocation concurrency, APIs, or deprecated queries.
