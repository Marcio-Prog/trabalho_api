from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Dados em memória
livros = []
autores = []

# Modelos de dados
class Autor(BaseModel):
    id: int
    nome: str
    data_nascimento: Optional[str] = None
    nacionalidade: Optional[str] = None

class Livro(BaseModel):
    id: int
    titulo: str
    autor_id: int
    ano_publicacao: int
    genero: Optional[str] = None

# Página inicial 

@app.get('/')
def index():
    return 'Minha CRUD da Biblioteca'

# CRUD para Autores

@app.post("/autores", response_model=Autor)
def criar_autor(autor: Autor):
    autores.append(autor)
    return autor

@app.get("/autores", response_model=List[Autor])
def listar_autores():
    return autores

@app.get("/autores/{autor_id}", response_model=Autor)
def buscar_autor_por_id(autor_id: int):
    autor = next((a for a in autores if a.id == autor_id), None)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    return autor

@app.put("/autores/{autor_id}", response_model=Autor)
def atualizar_autor(autor_id: int, autor_atualizado: Autor):
    for index, autor in enumerate(autores):
        if autor.id == autor_id:
            autores[index] = autor_atualizado
            return autor_atualizado
    raise HTTPException(status_code=404, detail="Autor não encontrado")

@app.delete("/autores/{autor_id}")
def deletar_autor_por_id(autor_id: int):
    global autores
    autores = [autor for autor in autores if autor.id != autor_id]
    return {"message": "Autor deletado com sucesso"}

# CRUD para Livros

@app.post("/livros", response_model=Livro)
def criar_livro(livro: Livro):
    if not any(a.id == livro.autor_id for a in autores):
        raise HTTPException(status_code=404, detail="Autor não encontrado")
    livros.append(livro)
    return livro

@app.get("/livros", response_model=List[Livro])
def listar_livros():
    return livros

@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro_por_id(livro_id: int):
    livro = next((l for l in livros if l.id == livro_id), None)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro

@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    for index, livro in enumerate(livros):
        if livro.id == livro_id:
            livros[index] = livro_atualizado
            return livro_atualizado
    raise HTTPException(status_code=404, detail="Livro não encontrado")

@app.delete("/livros/{livro_id}")
def deletar_livro_por_id(livro_id: int):
    global livros
    livros = [livro for livro in livros if livro.id != livro_id]
    return {"message": "Livro deletado com sucesso"}

# Funcionalidade Extra: Pesquisa de Livros

@app.get("/livros/busca")
def buscar_livros(genero: Optional[str] = None, autor_id: Optional[int] = None):
    resultado = livros
    if genero:
        resultado = [livro for livro in resultado if livro.genero == genero]
    if autor_id:
        resultado = [livro for livro in resultado if livro.autor_id == autor_id]
    return resultado

