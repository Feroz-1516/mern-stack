from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Set strict query to False (equivalent to mongoose.set('strictQuery', false))
# Note: In PyMongo, there's no direct equivalent, but we can handle this in our queries

# Connect to MongoDB
try:
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["BlogApp"]
    print("Connected to MongoDB!")
except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")

# Function to get the database connection
def get_db():
    return db