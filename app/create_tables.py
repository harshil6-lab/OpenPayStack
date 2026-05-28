from app.core.database import Base , engine
from app.models.user import User
from app.models.wallet import Wallet

print("Creating DB")

Base.metadata.create_all(bind=engine)

print("DB tables created succcessfully!")

