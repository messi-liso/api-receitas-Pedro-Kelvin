from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from schema import CreateReceita, Receita, Usuario, UsuarioPublic, BaseUsuario
from config import settings
from http import HTTPStatus
import re # Importando re para o desafio de validação de senha
from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_session


app = FastAPI(title='livro de receitas')

# --- BANCO DE DADOS EM MEMÓRIA ---
# Movendo as listas para o topo e inicializando-as
usuarios: List[Usuario] = []
receitas: List[Receita] = []

# --- FUNÇÃO HELPER PARA VALIDAÇÃO DE SENHA (DESAFIO EXTRA) ---
def validar_senha(senha: str):
    """
    Valida se a senha contém letras e números.
    Retorna True se válida, False caso contrário.
    """
    if re.search(r"[a-zA-Z]", senha) and re.search(r"\d", senha):
        return True
    return False

# --- ROTAS GERAIS ---

@app.get("/", status_code=HTTPStatus.OK)
def hello():
    return{"title": "livro de receitas"}

# --- ROTAS DE USUÁRIOS (Conforme PDF) ---

@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados: BaseUsuario, session: Session = Depends(get_session)):
    """
    Cria um novo usuário.
    Valida se o email já existe.
    Valida a senha (desafio extra).
    """
    db_user = session.scalar(
        select(User).where(
            (User.nome_usuario == dados.nome_usuario) | (User.email == dados.email)
        )
    )
   
    if db_user:
       if db_user.nome_usuario == dados.nome_usuario:
            raise HTTPException(
               status_code=HTTPStatus.CONFLICT,
               detail='Nome de usuário já existe',
           )
       elif db_user.email == dados.email:
           raise HTTPException(
               status_code=HTTPStatus.CONFLICT,
               detail='Email já existe',
           )
           
    db_user = User(
        nome_usuario=dados.nome_usuario, senha=dados.senha, email=dados.email
    )

    if not validar_senha(dados.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter letras e números."
        )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def get_todos_usuarios(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users

@app.get("/usuarios/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.nome_usuario == nome_usuario))
    )
    if db_user:
        return db_user
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

@app.get("/usuarios/id/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_id(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.id == id))
    )
    if db_user:
        return db_user
        
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    
@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario, session: Session = Depends(get_session)):
    
    db_user = session.scalar(select(User).where(User.id == id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
        
    db_user.nome_usuario = dados.nome_usuario
    db_user.senha = dados.senha
    db_user.email = dados.email
    session.commit()
    session.refresh(db_user)
    # Desafio Extra: Validar senha
    if not validar_senha(dados.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="A senha deve conter letras e números."
        )
    return db_user

@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def delete_usuario(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )
        
    session.delete(db_user)
    session.commit()
    
    return db_user
@app.get('/receitas', response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas

@app.get("/receitas/nome/{nome_receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita(nome_receita: str):
    # Corrigido: deve retornar um objeto Receita, não uma Lista
    for receita in receitas:
        if receita.nome == nome_receita:
            return receita
        
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.get("/receitas/id/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita_por_id(id: int):
    # Removida a duplicata, corrigido response_model para Receita
    for i in range(len(receitas)):
        if receitas[i].id == id:
            return receitas[i]
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita por ID não encontrada")
        

@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
def criar_receita(dados: CreateReceita):
    if len(receitas) > 0:
        for receita in receitas:
            if receita.nome == dados.nome:
                raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Receita já existente")
    
    # Simplificando a lógica de criação de ID
    novo_id = len(receitas) + 1
    nova_receita = Receita(
        id = novo_id, 
        nome = dados.nome, 
        ingredientes = dados.ingredientes, 
        modo_de_preparo = dados.modo_de_preparo
    )
    
    # Validações
    if len(dados.nome) < 2 or len(dados.nome) > 50:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="o nome da receita deve ter entre 2 e 50 caracteres")
    if len(nova_receita.ingredientes) <= 0 or len(nova_receita.ingredientes) >= 21:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="a receita deve ter no minimo 1 ingrediente, e no maximo 20")
    
    receitas.append(nova_receita)
    return nova_receita
    

@app.put("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: CreateReceita):
    if len(dados.nome) < 2 or len(dados.nome) > 50:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="o nome da receita deve ter entre 2 e 50 caracteres")
    if len(dados.ingredientes) < 1 or len(dados.ingredientes) > 20:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="a receita deve ter no minimo 1 ingrediente e no maximo 20")
    for receita in receitas:
        if receita.id != id and receita.nome == dados.nome:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="receita com esse nome já existe")
        
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_atualizada = Receita(
                id = id,
                nome = dados.nome,
                ingredientes = dados.ingredientes,
                modo_de_preparo = dados.modo_de_preparo
            )
            receitas[i] = receita_atualizada
            return receita_atualizada
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="receita não encontrada")

@app.delete("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    if len(receitas) == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="não há receitas para excluir")
    if len(receitas) > 0:
        for i in range(len(receitas)):
            if receitas[i].id == id:
                receita_deletada = receitas.pop(i) # .pop() já retorna o item removido
                return receita_deletada # Retorna o objeto da receita deletada
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="receita não encontrada")
