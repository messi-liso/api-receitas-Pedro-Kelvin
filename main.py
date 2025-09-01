from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

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
]
'''
class Receita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str
    
receitas: List[Receita] = []

@app.get("/")
def hello():
    return{"title": "livro de receitas"}

@app.get('/receitas/')
def get_todas_receitas():
    return receitas

@app.get("/receitas/{receita}")
def get_receita(receita: str):
    for i in receitas:
        if i['nome'] == receita:
            return i['ingredientes']
        
@app.post("/receitas", response_model=Receita, status_code=201)
def criar_receita(dados: Receita):
    
    nova_receita = dados
    receitas.append(nova_receita)
    
    return nova_receita