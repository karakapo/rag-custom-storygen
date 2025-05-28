from database import db
from models import User

def check_user(user_id: int):
    with db.get_session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if user:
            print(f"Kullanıcı bulundu:")
            print(f"ID: {user.id}")
            print(f"Username: {user.username}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Is Active: {user.is_active}")
        else:
            print(f"ID={user_id} olan kullanıcı bulunamadı!")

if __name__ == "__main__":
    check_user(0)  # Test kullanıcısının ID'si 