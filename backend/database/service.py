from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
import json
import uuid
from config import settings
from database.models import Contact

class DatabaseService(ABC):
    """Abstract base class for database services"""
    
    @abstractmethod
    async def create_contact(self, contact_data: dict) -> str:
        """Create a new contact record"""
        pass
    
    @abstractmethod
    async def get_contact(self, contact_id: str) -> Optional[dict]:
        """Get a contact by ID"""
        pass
    
    @abstractmethod
    async def list_contacts(self, limit: int = 100, offset: int = 0) -> List[dict]:
        """List contacts with pagination"""
        pass
    
    @abstractmethod
    async def initialize(self):
        """Initialize the database connection and schema"""
        pass

class InMemoryDatabaseService(DatabaseService):
    """In-memory database service for development"""
    
    def __init__(self):
        self.contacts = {}
    
    async def create_contact(self, contact_data: dict) -> str:
        contact_id = str(uuid.uuid4())
        self.contacts[contact_id] = {
            "id": contact_id,
            "full_name": contact_data["full_name"],
            "email": contact_data["email"],
            "phone_number": contact_data.get("phone_number"),
            "country_code": contact_data["country_code"],
            "message": contact_data["message"],
            "created_at": datetime.utcnow().isoformat()
        }
        return contact_id
    
    async def get_contact(self, contact_id: str) -> Optional[dict]:
        return self.contacts.get(contact_id)
    
    async def list_contacts(self, limit: int = 100, offset: int = 0) -> List[dict]:
        contacts_list = list(self.contacts.values())
        return contacts_list[offset:offset + limit]
    
    async def initialize(self):
        # No initialization needed for in-memory storage
        pass

class PostgreSQLDatabaseService(DatabaseService):
    """PostgreSQL database service"""
    
    def __init__(self):
        self.engine = None
        self.SessionLocal = None
    
    async def initialize(self):
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        from database.models import Base
        import asyncpg
        
        # Create database URL
        database_url = (
            f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}"
            f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
        )
        
        # Create engine
        self.engine = create_async_engine(database_url, echo=False)
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Create tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def create_contact(self, contact_data: dict) -> str:
        async with self.SessionLocal() as session:
            contact = Contact(
                full_name=contact_data["full_name"],
                email=contact_data["email"],
                phone_number=contact_data.get("phone_number"),
                country_code=contact_data["country_code"],
                message=contact_data["message"]
            )
            session.add(contact)
            await session.commit()
            await session.refresh(contact)
            return contact.id
    
    async def get_contact(self, contact_id: str) -> Optional[dict]:
        from sqlalchemy import select
        
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(Contact).where(Contact.id == contact_id)
            )
            contact = result.scalar_one_or_none()
            return contact.to_dict() if contact else None
    
    async def list_contacts(self, limit: int = 100, offset: int = 0) -> List[dict]:
        from sqlalchemy import select
        
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(Contact).offset(offset).limit(limit)
            )
            contacts = result.scalars().all()
            return [contact.to_dict() for contact in contacts]

class DynamoDBDatabaseService(DatabaseService):
    """DynamoDB database service using sync boto3 with async wrapper"""
    
    def __init__(self):
        self.dynamodb = None
        self.table = None
    
    async def initialize(self):
        import boto3
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        
        # Create thread pool for sync operations
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Initialize boto3 session and DynamoDB resource
        session = boto3.Session(
            region_name=settings.dynamodb_region,
            aws_access_key_id=settings.aws_access_key_id or None,
            aws_secret_access_key=settings.aws_secret_access_key or None,
        )
        
        self.dynamodb = session.resource('dynamodb')
        
        # Get or create table
        try:
            self.table = self.dynamodb.Table(settings.dynamodb_table_name)
            # Try to access table to verify it exists
            await asyncio.get_event_loop().run_in_executor(
                self.executor, lambda: self.table.table_status
            )
        except Exception:
            # Create table if it doesn't exist
            await self._create_table()
    
    async def _create_table(self):
        import asyncio
        
        def create_table_sync():
            table = self.dynamodb.create_table(
                TableName=settings.dynamodb_table_name,
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Wait for table to be created
            table.wait_until_exists()
            return table
        
        self.table = await asyncio.get_event_loop().run_in_executor(
            self.executor, create_table_sync
        )
    
    async def create_contact(self, contact_data: dict) -> str:
        import asyncio
        
        contact_id = str(uuid.uuid4())
        item = {
            "id": contact_id,
            "full_name": contact_data["full_name"],
            "email": contact_data["email"],
            "phone_number": contact_data.get("phone_number", ""),
            "country_code": contact_data["country_code"],
            "message": contact_data["message"],
            "created_at": datetime.utcnow().isoformat()
        }
        
        def put_item_sync():
            return self.table.put_item(Item=item)
        
        await asyncio.get_event_loop().run_in_executor(
            self.executor, put_item_sync
        )
        return contact_id
    
    async def get_contact(self, contact_id: str) -> Optional[dict]:
        import asyncio
        
        def get_item_sync():
            response = self.table.get_item(Key={"id": contact_id})
            return response.get("Item")
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, get_item_sync
        )
    
    async def list_contacts(self, limit: int = 100, offset: int = 0) -> List[dict]:
        import asyncio
        
        def scan_sync():
            # Note: DynamoDB doesn't support traditional offset-based pagination
            # This is a simplified implementation
            response = self.table.scan(Limit=limit)
            return response.get("Items", [])
        
        return await asyncio.get_event_loop().run_in_executor(
            self.executor, scan_sync
        )

# Factory function to create the appropriate database service
def create_database_service() -> DatabaseService:
    if settings.database_type == "memory":
        return InMemoryDatabaseService()
    elif settings.database_type == "postgres":
        return PostgreSQLDatabaseService()
    elif settings.database_type == "dynamodb":
        return DynamoDBDatabaseService()
    else:
        raise ValueError(f"Unsupported database type: {settings.database_type}")

# Global database service instance
db_service = create_database_service()
