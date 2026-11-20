# Controller da API - as rotas daqui respondem DADOS em JSON.
#
#   Metodo   Endereco                 O que faz       Sucesso   Recusas
#   GET      /api/salas            lista todos     200       401
#   GET      /api/salas/<id>       devolve um      200       401 404   <- ITEM 7
#   DELETE   /api/salas/<id>       remove          204       401 404   <- ITEM 9
#
# Toda recusa tem o mesmo formato: {"erro": "mensagem"}.

from flask import Blueprint, request, session, jsonify
from models.sala import Sala
from dao.sala_dao import SalaDAO

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.before_request
def exigir_login():
    if not session.get("usuario_id"):
        return jsonify({"erro": "Autenticacao necessaria."}), 401


@api_bp.route("/salas", methods=["GET"])
def listar():
    lista = []

    for sala in SalaDAO.listar():
        lista.append(sala.para_dicionario())

    return jsonify(lista)


# ===== ITEM 7 ========================================================
# Escreva aqui a rota GET /api/salas/<id>, que devolve UM registro.
# Se o id nao existir, a resposta e 404 com {"erro": "Sala nao encontrada."}.
# =====================================================================
def buscar_sala(id):
    sala = SalaDAO.buscar_por_id(id)
    if sala is None:
        abort(404, "Evento não encontrado.")
    return sala


@api_bp.get("/sala/<int:id>")
def buscar(id):
    return jsonify(buscar_sala(id))


# ===== ITEM 9 ========================================================
# Escreva aqui a rota DELETE /api/salas/<id>, que remove UM registro.
# Sucesso: 204, sem corpo. Se o id nao existir: 404 com
# {"erro": "Sala nao encontrada."}.
# =====================================================================
