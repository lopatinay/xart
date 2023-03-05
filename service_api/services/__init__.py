from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from service_api.configs import RuntimeConfig


_url = (
    "postgresql+psycopg2://"
    f"{RuntimeConfig.pg_user}:{RuntimeConfig.pg_pass}@"
    f"{RuntimeConfig.pg_host}:{RuntimeConfig.ph_port}/"
    f"{RuntimeConfig.pg_name}"
)

_psql_engine = create_engine(
    _url,
    echo_pool=RuntimeConfig.pg_echo,
    connect_args={
        "application_name": f"{RuntimeConfig.app_name}:{RuntimeConfig.app_runtime_id}"
    },
    pool_size=RuntimeConfig.pg_pool_size,
    pool_recycle=RuntimeConfig.pg_pool_recycle,
    max_overflow=RuntimeConfig.pg_max_overflow,
)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=_psql_engine)


def db_conn():
    session = db_session()
    try:
        yield session
    finally:
        session.close()
