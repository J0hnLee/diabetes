from typing import Union
from fastapi import FastAPI, HTTPException
import redis

from typing import Optional, List
from uuid import uuid4
from typing import List
from models import Citizen, BloodSugarRecord, BloodSugarSearch

app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379)


citizens = []
blood_sugar_records = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    redis_client.set(item_id, q)
    return {"item_id": item_id, "q": q}


@app.get("/allcitizens/")
async def all_citizens():
    return citizens


# 建立一般民眾的基本資料
@app.post("/citizens/", response_model=Citizen)
async def create_citizen(citizen: Citizen):
    # 檢查是否已經存在具有相同姓名和電話號碼的用戶
    existing_citizen = next((existing_citizen for existing_citizen in citizens if existing_citizen.name ==
                            citizen.name and existing_citizen.phone == citizen.phone), None)

    # 如果存在，返回錯誤消息
    if existing_citizen is not None:
        raise HTTPException(
            status_code=400, detail="Citizen with the same name and phone number already exists")

    # 如果不存在建立
    citizen.id = str(uuid4())  # 使用uuid生成唯一id
    citizens.append(citizen)

    return citizen


# 輸入一般民眾的血糖數值及測量時間

@app.post("/blood_sugar_records/", response_model=BloodSugarRecord)
async def create_blood_sugar_record(record: BloodSugarRecord):
    for citizen in citizens:
        if citizen.id == record.citizen_id:
            record.citizen = citizen
            blood_sugar_records.append(record)
            return record

    return {"error": "Citizen not found"}

# 根據姓名或電話號碼模糊搜索用戶資料
@app.post("/search_blood_sugar_records/", response_model=List[BloodSugarRecord])
async def search_blood_sugar_records(search: BloodSugarSearch):
    results = []

    for record in blood_sugar_records:
        if search.phone and search.phone in record.citizen.phone:
            results.append(record)
        elif search.name and search.name in record.citizen.name:
            results.append(record)
        elif search.birthdate and search.birthdate == record.citizen.birthdate:
            results.append(record)

    return results
