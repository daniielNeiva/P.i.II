import json
from sqlmodel import SQLModel, create_engine
from models import Montadora

def get_engine():
    engine = create_engine('sqlite:///montadoras.db')
    return engine

def recreate_database():
    engine = get_engine()
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)



def save_to_file(montadoras, filename='montadoras.json'):
    with open(filename, 'w') as file:
        json.dump([montadora.dict() for montadora in montadoras], file)

def load_from_file(filename='montadoras.json'):
    try:
        with open(filename, 'r') as file:
            montadoras_data = json.load(file)
            return [Montadora(**data) for data in montadoras_data]
    except FileNotFoundError:
        return []
from sqlmodel import SQLModel, create_engine
from models import Montadora

