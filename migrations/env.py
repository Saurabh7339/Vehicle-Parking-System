from sqlmodel import SQLModel
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from models.database import engine  # Import your engine if defined elsewhere

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Use your engine or specify your connection URL
config.set_main_option("sqlalchemy.url", "sqlite:////home/dante/Desktop/fastapi_sample/sql_fastapi_db/db.db")

# Set target_metadata to your models' metadata
target_metadata = SQLModel.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
