# pip install "trino[sqlalchemy]"

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, text
from trino.auth import OAuth2Authentication

engine = create_engine(
"trino://localhost:443/system",
    connect_args={
        "auth": OAuth2Authentication(),
        "http_scheme": "https",
        "verify": False
    }
)

connection = engine.connect()
rows = connection.execute(text("SELECT * FROM runtime.nodes")).fetchall()

print(rows)
