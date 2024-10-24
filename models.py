import uuid
from sqlmodel import SQLModel, Field

class Montadora(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    nome: str
    pais: str
    ano_fundacao: int
