from flask import Blueprint, jsonify, request
from app.models import *
import numpy as np
from konlpy.tag import Okt
from .chat import ChatGPT_JSON
bp = Blueprint('ai', __name__, url_prefix='/ai')


@bp.route('/keyword', methods=['POST'])
def hello():
    dic = {}
    okt = Okt()
    nouns = okt.nouns(request.json["string"])
    for word in nouns:
        dic[word] = dic.get(word, 0) + 1
    dic = dic.keys()
    return jsonify(dic)


@bp.route('/chatgpt', methods=['POST'])
def chatgpt():
    list = ChatGPT_JSON(request.json["field"], request.json["script"])
    return jsonify({list})
