# Database Connection Utility

This repository includes a small Python utility (`db_connect.py`) for
establishing a database connection.

## Quick Start

### SQLite (no extra dependencies)

```python
from db_connect import get_connection, close_connection

conn = get_connection()
# use conn ...
close_connection(conn)
```

By default the utility connects to `database.db` in the current directory.
Override the path with the `DB_PATH` environment variable:

```bash
DB_PATH=/path/to/my.db python db_connect.py
```

### Other Databases (PostgreSQL, MySQL, …)

Install the required packages:

```bash
pip install sqlalchemy psycopg2-binary   # PostgreSQL example
```

Then pass a connection URL:

```python
from db_connect import get_connection, close_connection

conn = get_connection("postgresql://user:password@localhost:5432/mydb")
close_connection(conn)
```

See `requirements.txt` for a full list of optional driver packages.
