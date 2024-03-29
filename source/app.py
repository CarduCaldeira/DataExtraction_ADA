from flask import Flask, jsonify, request, Response


app = Flask(__name__) # intância o método Flask

# cria a página homepage
@app.route("/", methods=["GET"]) # define o endpoint da página
@app.route("/homepage", methods=["GET"]) # define o endpoint da página
def homepage():
    return jsonify("essa é a homepage")

# cria a página ada
@app.route("/ada", methods=["GET"]) # define o endpoint da página
def pagina_ada():
    return jsonify("essa é a página ada")


# (simulando um banco de dados)
# leitura do arquivo ou banco de dados
dados_alunos = [
    {"id": 1, "nome": "Renan", "idade": 34, "comida_favorita": "Nhoque"},
    {"id": 2, "nome": "Erick", "idade": 29, "comida_favorita": "Xis"},
]

# endpoint para retornar todos os dados
@app.route("/alunos", methods=["GET"])
def retorna_alunos():
    return jsonify(dados_alunos)

## outro endpoint para retornar todos os dados
# @app.route("/aluno", methods=["GET"])
# def retorna_alunos2():
#     return jsonify(dados_alunos)

# endpoint para retornar tanto todos os dados quanto filtrar pelo id
@app.route("/aluno", methods=["GET"], defaults={"id": None})
@app.route("/aluno/<int:id>", methods=["GET"])
def retorna_aluno(id):
    if id is None:
        return jsonify(dados_alunos)
    else:
        for aluno in dados_alunos:
            if aluno.get("id") == id:
                print(f"Encontrei o aluno do id {id}: {aluno}")
                return jsonify(aluno)
        return jsonify({"message": "Aluno/a não encontrado"})
        
## endpoint para filtrar um aluno não informando que o id é um inteiro
## para isso precisamos tratar o id no código
# @app.route("/aluno/<id>", methods=["GET"])
# def retorna_aluno(id):
#     ### codigo
#     print(type(id), id)
#     for aluno in dados_alunos:
#         print("id da base de dados", type(aluno.get("id")))
#         if str(aluno.get("id")) == id:
#             print(f"Encontrei o aluno do id {id}: {aluno}")
#             return jsonify(aluno)

# Adicionar aluno no nosso banco de dados
@app.route("/aluno", methods=["POST"])
def incluir_novo_aluno():
    novo_aluno = request.get_json()
    # antes do append deveríamos verificar se estão presentes todos os campos e nos formatos específicos
    dados_alunos.append(novo_aluno)
    # neste ponto salvar os dados em um arquivo/banco de dados
    return jsonify(dados_alunos)

# Alterar aluno no banco de dados
@app.route("/aluno/<int:id>", methods=["PUT"])
def alterar_aluno(id):
    aluno_alterado = request.get_json()
    for aluno in dados_alunos:
        if aluno.get("id") == id:
            aluno.update(aluno_alterado)
            print(f"\n\nDEBUG: {aluno}")
            return jsonify(aluno)


# Deleta aluno no banco de dados
@app.route("/aluno/<int:id>", methods=["DELETE"])
def deleta_aluno(id):
    for aluno in dados_alunos:
        if aluno.get("id") == id:
            dados_alunos.remove(aluno)
            print(f"\n\nDEBUG: {dados_alunos}")
            return jsonify(dados_alunos)

@app.route('/csv')
def csv():
    data = u'1,2,3\n4,5,6\n'
    bom = u'\ufeff'
    response = Response(bom + data, content_type='text/csv; charset=utf-16')
    return response

if __name__ == "__main__":
    # define a porta da aplicação
    port = 5000
    # Inicia a execução da aplicação
    try:
        app.run(port=port)
    except KeyboardInterrupt:
        print('Detected keyboard interrupt, stopping ngrok and Flask...')
    