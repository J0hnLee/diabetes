from typing import Union
from fastapi import FastAPI
import redis
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4


app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379)


class UserInfo(BaseModel):
    id: str
    name: str
    phone: str
    line_id: Optional[str] = None


class BloodSugarRecord(BaseModel):
    user_id: str
    blood_sugar: float
    timestamp: str
    meal_status: str


user_data = []
blood_sugar_data = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    redis_client.set(item_id, q)
    return {"item_id": item_id, "q": q}

# 建立一般民眾的基本資料


@app.post("/users/")
async def create_user(user: UserInfo):
    user.id = str(uuid4())  # 使用uuid生成唯一id
    user_data.append(user)
    return {"message": "User created successfully", "user_id": user.id}

# 輸入一般民眾的血糖數值及測量時間


@app.post("/blood_sugar_records/")
async def create_blood_sugar_record(record: BloodSugarRecord):
    blood_sugar_data.append(record)
    return {"message": "Blood sugar record created successfully"}

# 透過電話、姓名、line ID查詢一般民眾的血糖數值及測量時間


@app.get("/blood_sugar_records/", response_model=List[BloodSugarRecord])
async def get_blood_sugar_records(name: Optional[str] = None, phone: Optional[str] = None, line_id: Optional[str] = None):
    if name is not None:
        user = next((user for user in user_data if user.name == name), None)
    elif phone is not None:
        user = next((user for user in user_data if user.phone == phone), None)
    elif line_id is not None:
        user = next(
            (user for user in user_data if user.line_id == line_id), None)
    else:
        return []

    if user is None:
        return []
    return [record for record in blood_sugar_data if record.user_id == user.id]

# 顯示一般民眾的血糖數值及測量時間


@app.get("/blood_sugar_records/{user_id}/", response_model=List[BloodSugarRecord])
async def get_user_blood_sugar_records(user_id: str):
    return [record for record in blood_sugar_data if record.user_id == user_id]
