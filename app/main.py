from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from .database import SessionLocal, User

# --- Настройки JWT ---
SECRET_KEY = "your-super-secret-key-change-in-production"  # ← Замените в продакшене!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Инициализация ---
app = FastAPI(
    title="Auth Service with JWT",
    description="API для регистрации, входа и защиты маршрутов с JWT",
    version="1.0.0"
)

# --- OAuth2 ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

# --- Хэширование паролей ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Зависимость для БД ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Pydantic модели ---
class UserLogin(BaseModel):
    username: str = Field(..., min_length=1, max_length=32)
    password: str = Field(..., min_length=12, max_length=32)

class UserRegister(UserLogin):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserOut(BaseModel):
    username: str

# --- Вспомогательные функции ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учётные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# --- Эндпоинты ---
@app.get("/")
def home():
    return {"message": "Работодателю - привет)"}

@app.post("/register", summary="Регистрация нового пользователя")
def register(user: UserRegister, db: Session = Depends(get_db)):
    db_user = get_user(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким логином уже существует"
        )
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Пользователь успешно зарегистрирован", "username": new_user.username}

@app.post("/auth", response_model=Token, summary="Авторизация и получение JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/profile", response_model=UserOut, summary="Защищённый эндпоинт")
def read_users_me(current_user: User = Security(get_current_user)):
    return current_user