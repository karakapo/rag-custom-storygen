import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
import sys
import os

# Add parent directory to path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import DatabaseConnection
from rag.vectorstore import client as qdrant_client

def test_postgres_connection():
    """Test PostgreSQL connection"""
    try:
        # Test using our DatabaseConnection class
        db = DatabaseConnection()
        with db.get_session() as session:
            # Try a simple query
            result = session.execute(text("SELECT 1")).scalar()
            print("✅ PostgreSQL connection successful!")
            print(f"Test query result: {result}")
            return True
    except Exception as e:
        print("❌ PostgreSQL connection failed!")
        print(f"Error: {str(e)}")
        return False

def test_qdrant_connection():
    """Test Qdrant connection"""
    try:
        # Test Qdrant connection
        collections = qdrant_client.get_collections()
        print("✅ Qdrant connection successful!")
        print(f"Available collections: {[col.name for col in collections.collections]}")
        return True
    except Exception as e:
        print("❌ Qdrant connection failed!")
        print(f"Error: {str(e)}")
        return False

def test_embedding_model():
    """Test sentence transformer model"""
    try:
        # Test embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        test_text = "This is a test sentence."
        embedding = model.encode(test_text)
        print("✅ Embedding model loaded successfully!")
        print(f"Embedding dimension: {len(embedding)}")
        return True
    except Exception as e:
        print("❌ Embedding model failed!")
        print(f"Error: {str(e)}")
        return False

def main():
    """Run all connection tests"""
    print("🔍 Testing database connections...\n")
    
    # Load environment variables
    load_dotenv()
    
    # Print current configuration
    print("Current Configuration:")
    print(f"PostgreSQL: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    print(f"Qdrant: {os.getenv('QDRANT_URL')}")
    print("-" * 50 + "\n")
    
    # Run tests
    postgres_ok = test_postgres_connection()
    print()
    qdrant_ok = test_qdrant_connection()
    print()
    embedding_ok = test_embedding_model()
    
    # Print summary
    print("\n" + "=" * 50)
    print("Connection Test Summary:")
    print(f"PostgreSQL: {'✅' if postgres_ok else '❌'}")
    print(f"Qdrant: {'✅' if qdrant_ok else '❌'}")
    print(f"Embedding Model: {'✅' if embedding_ok else '❌'}")
    print("=" * 50)
    
    # Return overall status
    return all([postgres_ok, qdrant_ok, embedding_ok])

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 