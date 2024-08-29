import time
from fastapi import Body, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from src.model import user
from src.db import get_db
from src.repository.group import create_groups, get_groups_by_ids
from src.repository.group_member import get_user_groups, get_users_in_group
from src.repository.invites import accept_invite, all_my_invites, create_invite, reject_invite
from src.repository.todos import complete_todo, create_todos, delete_todo, get_created_todos, get_my_completed_todos, get_my_todos
from src.repository.user import create_user, get_user, get_user_by_id
from src.schema.group import CreateGroupSchema, GroupSchema
from src.schema.group_menber import GMUserDetails
from src.schema.invites import CreateInviteSchema, InviteSchema, UpdateInviteSchema
from src.schema.todos import CompleteTodoSchema, CreateTodosSchema, Todoschema
from src.schema.user import CreateUserSchema, UserLoginSchema, UserSchema
from src.util.jwt_util import token_middleware, verify_token

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
            user: str = Depends(token_middleware)):
    return get_user_by_id(session=session, id=user)

@app.post('/todos', response_model= Todoschema)
def create_todo(payload: CreateTodosSchema = Body(), 
          session: Session = Depends(get_db),
          user: str = Depends(token_middleware)):
    try:
        return create_todos(session= session, todos= payload, created_by= user)
    except:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Error creating todos")
    
@app.get("/mytodos", response_model=list[Todoschema])
def my_todos(session: Session = Depends(get_db), 
               user: str = Depends(token_middleware),
               group_id: str = None):
    list_todo = get_my_todos(session, assigned_to = user, group_id=group_id)
    return list_todo

@app.get("/completed_todos", response_model=list[Todoschema])
def my_todos(session: Session = Depends(get_db), 
               user: str = Depends(token_middleware),
               group_id: str = None):
    list_todo = get_my_completed_todos(session, assigned_to = user, group_id=group_id)
    return list_todo


@app.get("/createdTodos", response_model=list[Todoschema])
def created_todos(session: Session = Depends(get_db), 
               user_id: str = Depends(token_middleware),
               group_id: str = None):
    return get_created_todos(session, created_by = user_id, group_id=group_id)

@app.post("/complete_todo", response_model=dict )
def complete_todos(session: Session = Depends(get_db), 
               user: str = Depends(token_middleware),
               payload: CompleteTodoSchema = Body(),
               group_id: str = None):
    todo = complete_todo(session=session, id=payload.id, assigned_to=user, group_id=group_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found or assigned_to does not match")
    return {"id": todo.id, "is_completed": todo.is_completed}

@app.delete("/todo/{todo_id}", response_model=dict)
def delete_todos( todo_id:int, session: Session = Depends(get_db), 
                 user: str = Depends(token_middleware),
                 group_id: str = None):
    if delete_todo(session=session, id=todo_id, group_id=group_id) == 1:
        return {"deletion": True}
    else:
        return {"deletion": False}
    
@app.post("/group", response_model=GroupSchema)
def create_group( payload: CreateGroupSchema = Body(),
                 user: str = Depends(token_middleware),
                 session: Session = Depends(get_db)):
    try:
        return create_groups(session= session, group= payload, created_by= user)
    except:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Error creating Group")
    
@app.get("/group", response_model=list[GroupSchema])
def get_groups_user(user: str = Depends(token_middleware),
                 session: Session = Depends(get_db)):
    try:
        group_ids = get_user_groups(session=session, user_id=user)
        return get_groups_by_ids(session=session, ids=group_ids)
    except:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail="Error fetching Groups for user")

@app.get("/group_members/{id}", response_model= list[GMUserDetails])
def get_group_users(id: int, user: str = Depends(token_middleware),
                 session: Session = Depends(get_db)):
    try:
        return get_users_in_group(session=session, group_id=id, user_id=user)
    except Exception as e:
        raise e
        

@app.post("/invite", response_model=dict)
def invite_user(user: str = Depends(token_middleware),
                payload: CreateInviteSchema = Body(),
                session: Session = Depends(get_db)):
    try:
        create_invite(payload=payload, user_id=user, session= session)
        return {
            "status": "sent"
        }
    except Exception as e:
        raise e
   
@app.put("/invite/accept", response_model=dict) 
def accept_inv(payload:UpdateInviteSchema = Body(),
               user: str = Depends(token_middleware),
               session: Session = Depends(get_db)):
    try:
        accept_invite(id= payload.id, user_id=user, session=session)
        return {
            "status": "updated"
        }
    except:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating Invite for user")
    
@app.put("/invite/reject", response_model=dict)
def reject_inv(payload:UpdateInviteSchema = Body(),
               user: str = Depends(token_middleware),
               session: Session = Depends(get_db)):
    try:
        reject_invite(id= payload.id, user_id=user, session=session)
        return {
            "status": "updated"
        }
    except:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating Invite for user")
    
@app.get("/invite", response_model=list[InviteSchema])
def get_all_inv(user: str = Depends(token_middleware),
               session: Session = Depends(get_db)):
    return all_my_invites(user_id=user, session=session)