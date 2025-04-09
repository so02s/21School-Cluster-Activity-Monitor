from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    name = Column(String, primary_key=True)
    tribe = Column(String)

    def __repr__(self):
        return f"User  (name='{self.name}', tribe='{self.tribe}')"

    @classmethod
    def get_tribe(cls, session, name):
        user = session.query(cls).filter(cls.name == name).first()
        if user:
            return user.tribe
        else:
            return None

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

class DatabaseManager:
    def __init__(self, db_url="sqlite:///peer.db"):
        self.engine = create_engine(db_url)
        self.Session = scoped_session(sessionmaker(bind=self.engine))
        self.inspector = inspect(self.engine)
        self.create_tables()
        
    def database_exists(self):
        """Проверяет существование самой базы данных"""
        try:
            self.engine.connect()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def tables_exist(self):
        """Проверяет существование всех необходимых таблиц"""
        existing_tables = self.inspector.get_table_names()
        return all(table in existing_tables for table in Base.metadata.tables.keys())

    def create_tables(self, check_first=True):
        """Создает таблицы с комплексной проверкой"""
        if not self.database_exists():
            raise RuntimeError("Database connection failed")
            
        if self.tables_exist():
            print("Все таблицы уже существуют")
            return False
            
        try:
            Base.metadata.create_all(self.engine, checkfirst=check_first)
            print(f"Успешно созданы таблицы: {list(Base.metadata.tables.keys())}")
            return True
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
            raise

    def add_user(self, name, tribe):
        """Добавляет нового пользователя в базу данных"""
        session = self.Session()
        try:
            if session.query(User).filter_by(name=name).first():
                raise ValueError(f"User {name} already exists")
                
            new_user = User(name=name, tribe=tribe)
            session.add(new_user)
            session.commit()
            return new_user
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_user(self, name):
        """Получает пользователя по имени"""
        session = self.Session()
        try:
            return session.query(User).filter_by(name=name).first()
        finally:
            session.close()

    def get_user_tribe(self, name):
        """Возвращает племя пользователя"""
        user = self.get_user(name)
        return user.tribe if user else None

    def update_user_tribe(self, name, new_tribe):
        """Обновляет племя пользователя"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(name=name).first()
            if not user:
                raise ValueError(f"User {name} not found")
                
            user.tribe = new_tribe
            session.commit()
            return user
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def delete_user(self, name):
        """Удаляет пользователя"""
        session = self.Session()
        try:
            user = session.query(User).filter_by(name=name).first()
            if not user:
                raise ValueError(f"User {name} not found")
                
            session.delete(user)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_all_users(self):
        """Получает всех пользователей"""
        session = self.Session()
        try:
            return session.query(User).all()
        finally:
            session.close()
