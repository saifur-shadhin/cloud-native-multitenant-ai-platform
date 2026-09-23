from backend.app.core.database import SessionLocal
from backend.app.models import Organization, User


db = SessionLocal()

try:
    organization1 = db.query(Organization).filter_by(name="DIU").first()
    organization2 = db.query(Organization).filter_by(name="TechCorp").first()

    user1 = User(
        name="Saifur",
        email="saifur@example.com",
        age=22,
        organization_id=organization1.id
    )

    user2 = User(
        name="Rahim",
        email="rahim@example.com",
        age=23,
        organization_id=organization1.id
    )

    user3 = User(
        name="Karim",
        email="karim@example.com",
        age=24,
        organization_id=organization2.id
    )

    user4 = User(
        name="Hasan",
        email="hasan@example.com",
        age=25,
        organization_id=organization2.id
    )

    db.add_all([user1, user2, user3, user4])
    db.commit()

    print("Users created successfully!")

except Exception as e:
    db.rollback()
    print("Error:", e)

finally:
    db.close()
