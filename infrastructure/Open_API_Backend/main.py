from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import subprocess
import uuid

app = FastAPI()

# Модель данных для пользователя
class User(BaseModel):
    name: str
    email: str

# Модель данных для пользователя с ID
class UserWithID(User):
    id: str

# Хранилище пользователей
users_db: Dict[str, UserWithID] = {}

# Метод для создания пользователя
@app.post("/users/", response_model=UserWithID)
async def create_user(user: User):
    user_id = str(uuid.uuid4())
    user_with_id = UserWithID(id=user_id, **user.dict())

    if user_with_id.id in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user_with_id.id] = user_with_id

    return user_with_id

# Метод для просмотра всех пользователей
@app.get("/users/", response_model=List[UserWithID])
async def read_users():
    return list(users_db.values())

# Метод для удаления пользователя по имени
@app.delete("/users/name/{user_name}")
async def delete_user_by_name(user_name: str):
    user_ids_to_delete = [user_id for user_id, user in users_db.items() if user.name == user_name]
    if not user_ids_to_delete:
        raise HTTPException(status_code=404, detail="User not found")

    for user_id in user_ids_to_delete:
        del users_db[user_id]

    return {"message": "User deleted"}

# Метод для получения OpenAPI спецификации
@app.get("/openapi.json")
async def get_openapi_json():
    return app.openapi()

def run_server():
    # Запуск сервера Uvicorn
    subprocess.run(["uvicorn", "main:app", "--reload", "--port", "8082"])

if __name__ == "__main__":
    run_server()
