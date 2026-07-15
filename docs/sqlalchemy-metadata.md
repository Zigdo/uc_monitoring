# Canonical SQLAlchemy metadata

Leolan has one SQLAlchemy declarative Base:

```python
from app.db.base import Base
```

Every ORM model must inherit from this object. No other module may construct a
second `declarative_base()` or `DeclarativeBase` subclass.

## Compatibility imports

The following historical import paths re-export the same canonical object:

```python
from app.db.session import Base
from app.inventory.models.base import Base
```

They exist to avoid breaking older imports. New model code must import directly
from `app.db.base`.

## Model registration

SQLAlchemy registers a mapped table when its model module is imported. Before
performing a metadata-wide operation, import the model package entry point:

```python
import app.inventory.models
from app.db.base import Base
```

`app.inventory.models` currently imports every mapped model. The existing
`app.db.create_tables` helper follows this registration pattern before calling
`Base.metadata.create_all()`.

## PR 2 boundaries

Canonical metadata consolidation does not:

- alter tables, columns, constraints, relationships, or entity names;
- create, drop, or migrate a database;
- introduce Alembic;
- repair model configuration defects;
- change engine, session, or transaction behavior.

Schema corrections belong to PR 3, and migrations belong to PR 4 in the frozen
Leolan V1 PRD.
