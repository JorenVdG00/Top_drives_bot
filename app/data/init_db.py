from app.data.db_setup import engine
from app.models import Base

def create_tables():
    Base.metadata.create_all(engine)
    print("Tables created successfully!")

def delete_tables():
    Base.metadata.drop_all(engine)
    print("Tables deleted successfully!")

if __name__ == "__main__":
    delete_tables()  # Optional: Clear old tables before recreating
    create_tables()
