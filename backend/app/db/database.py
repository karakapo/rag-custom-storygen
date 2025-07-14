from typing import Any, Dict, List, Optional, Union, Generator
import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class DatabaseConnection:
    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._engine is None:
            self._initialize_engine()

    def _initialize_engine(self):
        """Initialize the SQLAlchemy engine"""
        try:
            database_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"
            self._engine = create_engine(database_url, pool_size=10, max_overflow=20)
            self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        except Exception as e:
            raise Exception(f"Failed to initialize database engine: {str(e)}")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session"""
        session = self._SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise Exception(f"Database session error: {str(e)}")
        finally:
            session.close()

    def execute_query(self, query: str, params: dict = None) -> List[Dict]:
        """Execute a raw SQL query and return results"""
        with self.get_session() as session:
            result = session.execute(query, params or {})
            return [dict(row) for row in result]

    def execute_single(self, query: str, params: dict = None) -> Optional[Dict]:
        """Execute a raw SQL query and return single result"""
        with self.get_session() as session:
            result = session.execute(query, params or {})
            row = result.fetchone()
            return dict(row) if row else None

    def execute_many(self, query: str, params_list: List[dict]) -> None:
        """Execute multiple queries"""
        with self.get_session() as session:
            for params in params_list:
                session.execute(query, params)

    def execute_transaction(self, queries: List[tuple]) -> None:
        """Execute multiple queries in a transaction"""
        with self.get_session() as session:
            try:
                for query, params in queries:
                    session.execute(query, params or {})
            except Exception as e:
                raise Exception(f"Transaction failed: {str(e)}")

    def create_all(self):
        """Create all tables defined in models"""
        Base.metadata.create_all(bind=self._engine)

    def close(self):
        """Close all connections in the pool"""
        if self._engine:
            self._engine.dispose()

# Create a singleton instance
db = DatabaseConnection()

# Dependency
def get_db():
    session = db._SessionLocal()
    try:
        yield session
    finally:
        session.close()
