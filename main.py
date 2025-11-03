from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from schema import CreateReceita, Receita, Usuario, UsuarioPublic, BaseUsuario
from http import HTTPStatus

app = FastAPI(title='livro de receitas')

'''
receitas = [
    {
        'nome': 'batida de amendoim',
        'ingredientes': ['1 lata de leite condensado', '5 colheres (sopa) de pasta de amendoim', '2 latas de leite', '4 doses de cachaça', '2 doses de licor de cacau'],
        'modo de preparo': 'é uma bebida batida, adivinha como preparar...'
    },
    {
        'nome': 'torta',
        'ingredientes': ['200 g de macarrão espaguete (ou outra massa longa de grano duro)', ' ½ xícara (chá) de bacon em cubos (75 g)', '¼ de xícara (chá) de vinho branco', '2 ovos', '2 gemas', '½ xícara (chá) de queijo parmesão ralado', 'sal', 'pimenta-do-reino moída na hora a gosto', '½ xícara (chá) de queijo parmesão ralado fino'],
        'modo de preparo - macarrão': 'Leve uma panela média com cerca de 3 litros de água ao fogo alto. Quando ferver, adicione 1½ colher (sopa) de sal, junte o macarrão e deixe cozinhar pelo tempo indicado na embalagem, ou até ficar al dente, mexendo de vez em quando para que os fios não grudem um no outro. Enquanto o macarrão cozinha, separe os outros ingredientes. Numa tigela pequena, quebre um ovo de cada vez e transfira para outra tigela (lembre-se: são 2 ovos inteiros e 2 gemas; você pode reservar as claras na geladeira ou no congelador para outras receitas). Junte o queijo parmesão e misture bem com um garfo. Leve uma frigideira grande ao fogo médio para aquecer. Adicione o bacon e deixe dourar por cerca de 5 minutos, mexendo de vez em quando. Abaixe o fogo, regue com o vinho branco, com cuidado para não espirrar, misture bem e desligue. Assim que o macarrão estiver cozido, reserve 1 xícara (chá) da água do cozimento. Agora você vai precisar fazer tudo bem rapidinho: escorra a água, transfira o macarrão para a frigideira com o bacon quente, junte os ovos e misture bem — a ideia é que o calor da massa cozinhe os ovos, formando um creme. Caso necessário, volte a frigideira ao fogo baixo e vá adicionando aos poucos a água do cozimento reservada, mexendo com uma espátula por alguns minutinhos até formar um molho espesso. Cuidado para não cozinhar os ovos! Sirva a seguir com pimenta-do-reino a gosto e telha de parmesão (opcional, veja a receita abaixo).',
        'modo de preparo - telha de parmesão': 'Apoie uma colher de pau (ou de bambu) sobre uma tigela média — o cabo da colher vai servir de molde para as telhas. Leve uma frigideira média antiaderente ao fogo médio. Com a mão, polvilhe o parmesão na frigideira formando 3 discos pequenos, um ao lado do outro — eles não precisam ficar perfeitos; se for necessário, ajuste as bordas com uma espátula de silicone. Deixe o parmesão derreter, sem mexer, por cerca de 5 minutos, até a base começar a dourar – o queijo vai borbulhar formando 3 plaquinhas. Desligue o fogo. Com a espátula de silicone, retire um disco de parmesão de cada vez da frigideira e apoie ainda quente sobre o cabo da colher de pau — assim os discos ficam curvados, no formato de uma telha. Deixe a telha esfriar e endurecer antes de servir ou armazenar.'
    },
    {
        'nome': 'morango-do-amor',
        'ingredientes': ['1 lata de Leite Condensado MOÇA®', '100 g NESTLÉ® de Creme de Leite', '2 colheres (sopa) de Leite NINHO®', 'Forti+ Instantâneo em pó', '1 colher (sopa) de manteiga', '12 a 15 morangos higienizados e secos (1 bandejinha média)', '2 xícaras (chá) e meia de açúcar', '1 xícara (chá) e meia de água', '2 colheres (sopa) de vinagre', '10 gotas de corante alimentício em gel vermelho'],
        'modo de preparo': 'Brigadeiro Em uma panela, misture o Leite Condensado MOÇA, o NESTLÉ Creme de Leite, o Leite Forti+ Instantâneo em pó e a manteiga. Cozinhe em fogo baixo, mexendo sempre, até levantar fervura. Após ferver, cozinhe por mais 8 minutos ou até atingir ponto de brigadeiro mole. Transfira para um refratário e deixe descansar por pelo menos 4 horas até esfriar completamente. Montagem dos Morangos Lave e higienize os morangos. Seque bem com papel toalha. Envolva cada morango com uma camada de brigadeiro, moldando com as mãos limpas e levemente untadas. Espete cada morango em um palito e acomode em um prato untado ou com papel manteiga. Leve ao freezer por cerca de 30 minutos, até que fiquem firmes para receber a calda. Em uma panela, coloque o açúcar, a água, o vinagre e o corante vermelho. Misture apenas no início. Leve ao fogo baixo e não mexa mais. Ferva por cerca de 20 minutos ou até atingir o ponto de bala dura (faça o teste: pingue um pouco da calda em um copo com água gelada – se endurecer na hora, está pronto). Com cuidado, mergulhe os morangos congelados um a um na calda e acomode sobre um tapete de silicone ou forma bem untada. Deixe secar naturalmente até a calda firmar completamente e sirva.',
    }
    {
    'nome': 'Strogonoff-de-frango',
    'ingredientes': ['3 colheres de sopa de óleo'],['1 tablete de caldo de galinha'],['1 quilo de peito de frango em cubos'],['2 colheres de sopa de molho de tomate'],['2 colheres de sopa de mostarda'],['2 colheres de sopa de ketchup'],['Champignon a gosto'],['1 lata de creme de leite sem soro']
    'modo de preparo - ['Em uma panela, coloque 3 colheres de sopa de óleo e 1 tablete de caldo de galinha. Espere aquecer para dissolver o tablete.']['Em seguida, adicione 1 quilo de peito de frango em cubos e deixe dourar.']['Depois, acrescente 2 colheres de sopa de molho de tomate, 2 colheres de sopa de mostarda, 2 colheres de sopa de ketchup e champignon a gosto. Misture.']['Desligue o fogo e acrescente 1 lata de creme de leite. Misture novamente.']['Sirva em seguida.']
    }
]
'''

usuarios: List[Usuario]

receitas: List[Receita] = []

@app.get("/", status_code=HTTPStatus.OK)
def hello():
    return{"title": "livro de receitas"}

@app.get('/receitas', response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas

@app.get("/receitas/nome/{nome_receita}", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_receita(nome_receita: str):
    for receita in receitas:
        if receita.nome == nome_receita:
            return receita
        
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")


@app.get("/receitas/id/{id}", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_receita_por_id(id: int):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            return receitas[i]
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita por ID não encontrada")
        
        
@app.get("/usuarios/id/{id}", response_model=List[Usuario], status_code=HTTPStatus.OK)
def get_usuario_por_id(id_usuario: str):
    for usuario in usuarios:
        if usuario.id == id_usuario:
            return usuario
        
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuario Não Encontrado")
    
@app.get("/receitas/id/{id}", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_receita_por_id(id: int):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            return receitas[i]
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita por ID não encontrada")


@app.post("/usuarios", response_model=UsuarioPublic, status_code=HTTPStatus.CREATED)
def criar_usuario(dados: BaseUsuario):
    if len(usuarios) > 0:
        for usuario in usuarios:
            if usuario.nome == dados.nome:
                return {"Usuario já existente"}
    if len(usuarios) == 0:
        id = 1
        novo_id = id
        novo_usuario = Usuario(id = novo_id, nome = dados.nome, email = dados.email, senha = dados.senha)
        if len(dados.nome) < 2 or len(dados.nome) > 50:
            return {"mensagem": "o nome do usuario deve ter entre 2 e 50 caracteres"}

        if len(novo_usuario.email) <= 0 or len(novo_usuario) >= 50:
            return {"mensagem": "o email deve ter entre 1 e 50 caracteres"}
        else:
            usuarios.append(novo_usuario)
            
    elif len(usuarios) > 0:
        id = len(usuarios)+1
        novo_id = id
        novo_usuario = Usuario(id = novo_id, nome = dados.nome, email = dados.email, senha = dados.senha)
        if len(dados.nome) < 2 or len(dados.nome) > 50:
            return {"mensagem": "o nome do usuario deve ter entre 2 e 50 caracteres"}

        if len(novo_usuario.email) <= 0 or len(novo_usuario) >= 50:
            return {"mensagem": "o email deve ter entre 1 e 50 caracteres"}
        else:
            usuarios.append(novo_usuario)
    return novo_usuario

@app.post("/receitas", response_model=Receita, status_code=HTTPStatus.CREATED)
def criar_receita(dados: CreateReceita):
    if len(receitas) > 0:
        for receita in receitas:
            if receita.nome == dados.nome:
                raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Receita já existente")
    if len(receitas) == 0:
        id = 1
        novo_id = id
        nova_receita = Receita(id = novo_id, nome = dados.nome, ingredientes = dados.ingredientes, modo_de_preparo = dados.modo_de_preparo)
        if len(dados.nome) < 2 or len(dados.nome) > 50:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="o nome da receita deve ter entre 2 e 50 caracteres")
        if len(nova_receita.ingredientes) <= 0 or len(nova_receita.ingredientes) >= 21:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="a receita deve ter no minimo 1 ingrediente, e no maximo 20")
        else:
            receitas.append(nova_receita)
            
    elif len(receitas) > 0:
        id = len(receitas)+1
        novo_id = id
        nova_receita = Receita(id = novo_id, nome = dados.nome, ingredientes = dados.ingredientes, modo_de_preparo = dados.modo_de_preparo)
        if len(dados.nome) < 2 or len(dados.nome) > 50:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="o nome da receita deve ter entre 2 e 50 caracteres")
        if len(nova_receita.ingredientes) <= 0 or len(nova_receita.ingredientes) >= 21:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="a receita deve ter no minimo 1 ingrediente, e no maximo 20")
        else:
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
                receta_deletada = receitas[i].nome
                receitas.pop(i)
                return{"mensagem": f"Receita excluida: '{receta_deletada}'"}
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="receita não encontrada")
