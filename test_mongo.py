import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

async def test_connection():
    load_dotenv()
    mongo_url = os.getenv("MONGO_DETAILS")
    
    print("=" * 60)
    print("🧪 Testing MongoDB Atlas Connection")
    print("=" * 60)
    print(f"URL: {mongo_url[:50]}...")
    
    try:
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        print("✅ SUCCESS! MongoDB Atlas is connected!")
        
        # Test database access
        db = client.trinetra_db
        collections = await db.list_collection_names()
        print(f"\n📊 Database: trinetra_db")
        print(f"📁 Collections: {len(collections)}")
        for coll in collections:
            count = await db[coll].count_documents({})
            print(f"   - {coll}: {count} documents")
        
        client.close()
        return True
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
