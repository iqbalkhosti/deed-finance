from app import app, Session, Client, bcrypt
from datetime import datetime

with app.app_context():
    with Session() as session:
        # Check if user exists
        user = session.query(Client).filter_by(email="ui_test@example.com").first()
        if user:
            print("User already exists")
            user.is_verified = True # Ensure verified
            session.commit()
        else:
            hashed_pw = bcrypt.generate_password_hash("password123").decode('utf-8')
            new_user = Client(
                first_name="Alex",
                surname="Designer",
                email="ui_test@example.com",
                password=hashed_pw,
                is_verified=True
            )
            session.add(new_user)
            session.commit()
            print("Test user created: ui_test@example.com / password123")
