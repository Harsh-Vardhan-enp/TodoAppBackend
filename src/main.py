import time
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from src.model import user
from src.db import get_db
from src.repository.todos import create_todos, get_created_todos, get_my_todos
from src.repository.user import create_user, get_user, get_user_by_id
from src.schema.todos import CreateTodosSchema, Todoschema
from src.schema.user import CreateUserSchema, UserBaseSchema, UserLoginSchema, UserSchema
from src.util.jwt_util import verify_token

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

@app.get("/ping")
def pingpong():
    return "pong"

@app.post('/signup',response_model= UserSchema)
async def signup(payload: CreateUserSchema = Body(),
           session: Session = Depends(get_db)):
    payload.hashed_pass = user.User.hash_password(payload.hashed_pass)
    return create_user(session, payload)

@app.post('/login', response_model= dict)
def login(payload: UserLoginSchema, 
          session: Session = Depends(get_db)):
    try:
        curr_user: user.User = get_user(session=session, email= payload.email)
    except:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid Username")
    if not curr_user.validate_password(payload.password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
    return curr_user.gen_token()

@app.get("/profile", response_model=UserSchema)
def profile(session:Session=Depends(get_db),
            token: str = Depends(oauth2_scheme)):
    id = verify_token(token)
    return get_user_by_id(session=session, id=id)

@app.post('/todos', response_model= Todoschema)
def create_todo(payload: CreateTodosSchema = Body(), 
          session: Session = Depends(get_db),
          token: str = Depends(oauth2_scheme)):
    id = verify_token(token)
    try:
        return create_todos(session= session, todos= payload, created_by= id)
    except:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Error creating todos")
    
@app.get("/todos", response_model=list[Todoschema])
def my_todos(session: Session = Depends(get_db), 
               token: str = Depends(oauth2_scheme)):
    id = verify_token(token=token)
    return get_my_todos(session, assigned_to = id)

@app.get("/createdTodos", response_model=list[Todoschema])
def created_todos(session: Session = Depends(get_db), 
               token: str = Depends(oauth2_scheme)):
    id = verify_token(token=token)
    return get_created_todos(session, created_by = id)