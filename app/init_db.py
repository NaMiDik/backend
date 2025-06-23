from app.database import engine
from app.models import Base

# Створення всіх таблиць у базі даних
print("🔧 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created.")