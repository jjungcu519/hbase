from fastapi import FastAPI
import happybase
from pydantic import BaseModel
from datetime import datetime

app = FastAPI() #fastapi = 작은 django~

connection = happybase.Connection('localhost')
connection.open()

class User(BaseModel):
    username: str
    email: str

class Chatroom(BaseModel):
    room_name: str

class Chat(BaseModel):
    user_id: str
    room_id: str
    message: str


# @app.get("/")   # => urls.py
# def read_root():    # => views.py
#     return {"Hello": "World"}   # => context return이 한 과정에~

# @app.get('/index')
# def index():
#     return {"asdf":"asdf"}

# @app.get('/items/{item_id}')
# def read_item(item_id:int):
#     return {"item": item_id}

@app.post('/user')
def create_user(user:User):
    table = connection.table('user')
    user_id = user.username
    table.put(
        user_id,
        {'info:username' : user.username,
        'info:email' : user.email

        }
        )

    return{
        'user_id':user_id,
        'username':user.username,
        'email':user.email
    }

@app.get('/user/{user_id}')
def get_user(user_id:str):
    table = connection.table('user')
    row = table.row(user_id)

    return {
        'user_id' : user_id,
        'username' : row[b'info:username'].decode('utf-8'),
        'email' : row[b'info:email'].decode('utf-8')
        }


@app.post('/chatroom')
def create_chatroom(chatroom:Chatroom):
    table = connection.table('chatroom')
    chatroom_id = chatroom.room_name
    table.put(chatroom_id, {'info:room_name': chatroom.room_name})
    return{'chatroom_id':chatroom_id, 'room_name':chatroom.romm_name}

@app.post('/chat')
def create_chat(chat: Chat):
    table = connection.table('chat')
    timestamp = datetime.now().timestamp()
    MAX_TIMESTAMP = 2**63 - 1

    chat_id = f'{chat.room_id}_{int(MAX_TIMESTAMP-timestamp)}'
    table.put(chat_id,{
        'info:user_id' : chat.user_id,
        'info:room_id' : chat.room_id,
        'info:message' : chat.message,
    })

    return {
        'chat_id' : chat_id,
        'user_id' : chat.user_id,
        'room_id' : chat.roomm_id,
        'message' : chat.message

    }

@app.get('/chatroom/{room_id}')
def get_chatroom(room_id: str):
    table = connection.table('chat')

    rows = table.scan(filter=f"SingleColumnValueFilter('info', 'roo_id', =, '{room_id}')")

    chats = []

    for k, v in rows:
        chats.append({
            'chat_id': k,
            'room_id': v[b'info:room_id'],
            'user_id': v[b'info:user_id'],
            'message': v[b'info:message'],
        })

    return chats
