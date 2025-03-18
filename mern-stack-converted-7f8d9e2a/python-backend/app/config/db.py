from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the SQLAlchemy engine
engine = create_engine('sqlite:///blog_app.db', echo=True)

# Create a sessionmaker
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

def init_db():
    try:
        # Create all tables
        Base.metadata.create_all(engine)
        print("Connected to the database!")
    except Exception as e:
        print(f"Error connecting to the database: {str(e)}")

# Initialize the database
init_db()