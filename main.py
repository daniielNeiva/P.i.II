from typing import Annotated
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from sqlmodel import SQLModel
from models import Montadora
from persistence.Montadoras_repository import MontadoraRepository
from persistence.Utils import get_engine, load_from_file, recreate_database
from view_models import InputMontadora
from contextlib import asynccontextmanager

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

repository = MontadoraRepository()

@asynccontextmanager
async def lifespan(app: FastAPI):
    repository.montadoras = load_from_file()
    yield

app = FastAPI(lifespan=lifespan)

recreate_database()

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "name": "João"})

@app.get('/montadoras_list')
def montadora_list(request: Request, query: str = None, order: str = None, attribute: str = None):
    if query:
        montadoras = repository.filter_by_name_or_country(query)
    elif attribute and order:
        montadoras = repository.order_by_attribute(attribute, order)
    else:
        montadoras = repository.get_all()
    return templates.TemplateResponse(
        request=request,
        name='montadora_list.html',
        context={'montadoras': montadoras}
    )

@app.get('/montadoras_form')
def montadora_form(request: Request):
    return templates.TemplateResponse(request, 'montadora_form.html')

@app.post('/montadora_save')
def montadora_save(request: Request, nome: Annotated[str, Form(...)], pais: Annotated[str, Form(...)], ano: Annotated[int, Form(...)]):
    montadora = Montadora(nome=nome, pais=pais, ano_fundacao=ano)
    repository.save(montadora)
    return RedirectResponse('/montadoras_list', status_code=303)

@app.get('/montadora_details/{montadora_id}')
def montadora_details(request: Request, montadora_id: str):
    montadora = repository.get(montadora_id)
    return templates.TemplateResponse(
        request=request,
        name='montadora_details.html',
        context={'montadora': montadora}
    )

@app.post('/montadora_delete/{montadora_id}')
def montadora_delete(request: Request, montadora_id: str):
    repository.delete(montadora_id)
    return RedirectResponse('/montadoras_list', status_code=303)

@app.get('/montadora_edit/{montadora_id}')
def montadora_edit(request: Request, montadora_id: str):
    montadora = repository.get(montadora_id)
    return templates.TemplateResponse(
        request=request,
        name='montadora_edit.html',
        context={'montadora': montadora}
    )

@app.post('/montadora_update/{montadora_id}')
def montadora_update(request: Request, montadora_id: str, nome: Annotated[str, Form(...)], pais: Annotated[str, Form(...)], ano: Annotated[int, Form(...)]):
    montadora_data = Montadora(nome=nome, pais=pais, ano_fundacao=ano)
    repository.update(montadora_id, montadora_data)
    return Redirect