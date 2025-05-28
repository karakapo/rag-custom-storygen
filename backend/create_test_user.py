from database import db
from models import User, UserRole
from werkzeug.security import generate_password_hash

def create_test_user():
    with db.get_session() as session:
        # Test kullanıcısını oluştur
        test_user = User(
            id=0,  # ID'yi 0 olarak ayarla
            username="test_user",
            email="test@example.com",
            password_hash=generate_password_hash("test123"),
            role=UserRole.USER,
            is_active=True
        )
        
        try:
            session.add(test_user)
            session.commit()
            print("Test kullanıcısı başarıyla oluşturuldu!")
            print(f"Kullanıcı ID: {test_user.id}")
            print(f"Kullanıcı adı: {test_user.username}")
            print(f"E-posta: {test_user.email}")
        except Exception as e:
            session.rollback()
            print(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    create_test_user() 