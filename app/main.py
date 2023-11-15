import json
import os
import re

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pymongo import MongoClient


app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["form_templates"]
collection = db["templates"]

FIELD_TYPES_PATTERNS = {
    "date": r"^(?:\d{2}\.\d{2}\.\d{4}|\d{4}-\d{2}-\d{2})$",
    "phone": r"\+7 \d{3} \d{3} \d{2} \d{2}$",
    "email": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
}


def load_sample_data():
    collection.delete_many({})

    with open("sample_data.json", "r") as file:
        sample_data = json.load(file)
    collection.insert_many(sample_data)


@app.on_event("startup")
def startup_event():
    load_sample_data()


def validate_and_type_fields(value):
    for field_type, pattern in FIELD_TYPES_PATTERNS.items():
        if re.match(pattern, value):
            return field_type
    return "text"


@app.post("/get_form")
async def get_form(fields: dict) -> JSONResponse:
    field_names = set(fields.keys())

    query = {"$and": [{"$and": [{field: {"$exists": True}} for field in field_names]}]}
    template = collection.find_one(query)

    if template:
        if all(validate_and_type_fields(fields[field]) == template[field] for field in field_names):
            return JSONResponse(content={"name": template["name"]}, status_code=200)

    typed_fields = {field: validate_and_type_fields(value) for field, value in fields.items()}
    return JSONResponse(content=typed_fields, status_code=200)
