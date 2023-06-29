from flask import Blueprint, jsonify, request
from app.models import *
bp = Blueprint('form', __name__, url_prefix='/form')


@bp.route('/', methods=['GET', 'POST'])
def form_list():
    if request.method == "GET":
        list = Form.query.all()
        reslist = []
        for form in list:
            if form.presentation:
                ppt = form.presentation[0]
                image = ppt.image[0]
                reslist.append(
                    {"formIdx": form.formIdx, "imageUrl": image.imgUrl})
            else:
                reslist.append(
                    {"formIdx": form.formIdx, "imageUrl": None})
        return jsonify(reslist)
    elif request.method == "POST":
        form = Form()
        db.session.add(form)
        ppt = Presentation(form=form)
        db.session.add(ppt)
        # "imgUrls" : ["http~~","http~~","http~~"],
        imgUrls = request.json.get('imgUrls')

        # 파싱 ->
        for pgNum, imgUrl in enumerate(imgUrls):
            if not imgUrl:
                errMsg = 'Validation Error'
                return jsonify({'status': 'error', 'message': errMsg}), 422
            else:
                image = Image(presentation=ppt, pgNum=pgNum+1,
                              imgUrl=imgUrl, script=None, topic=None)
                db.session.add(image)
                db.session.commit()

        return jsonify({'status': 'success', 'message': 'Image saved successfully'}), 200


@bp.route('/<int:Idx>/<int:pgNum>/script', methods=['GET', 'POST', 'PUT', 'DELETE'])
def form_script(Idx, pgNum):
    if request.method == "GET":
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image[pgNum-1]
            return jsonify({"script": image.script})
        else:
            scriptonly = form.scriptonly
            return jsonify({"script": scriptonly.script})

    elif request.method == "POST":
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image
            image[pgNum-1].script = request.json['script']
            db.session.commit()
        else:
            scriptonly = form.scriptonly[0]
            scriptonly.script = request.json['script']
            db.session.commit()
        return jsonify({'status': 'success', 'message': 'Script saved successfully'}), 200

    elif request.method == "PUT":
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image
            image[pgNum-1].script = request.json['script']
            db.session.commit()
        else:
            scriptonly = form.scriptonly[0]
            scriptonly.script = request.json['script']
            db.session.commit()
        return jsonify({'status': 'success', 'message': 'Script revised successfully'}), 200

    elif request.method == "DELETE":
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image
            image[pgNum-1].script = None
            keywordlist = image[pgNum-1].keyword
            for keyword in keywordlist:
                db.session.delete(keyword)
            db.session.commit()
        else:
            scriptonly = form.scriptonly[0]
            db.session.delete(scriptonly)
            db.session.commit()
        return jsonify({'status': 'success', 'message': 'Script deleted successfully'}), 200


@bp.route('/<int:Idx>/<int:pgNum>/keyword', methods=['GET', 'POST', 'PUT'])
def form_keyword(Idx, pgNum):
    
    if request.method == "GET":
        form = Form.query.filter(Form.formIdx == Idx).first()
        keylist = []
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image[pgNum-1]
            for i in image.keyword:
                keylist.append({
                    "key":i.keyword, "level":i.level
                })
            return jsonify(keylist)
        else:
            scriptonly = form.scriptonly
            for i in scriptonly.keyword:
                keylist.append({
                    "key":scriptonly.keyword, "level":scriptonly.level
                })
            return jsonify(keylist)
            

    elif request.method == "POST":
        # key를 저장해야할 form을 idx로 가져옴
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image[pgNum-1]
            for i in request.json:
                new_keyword = Keyword(
                    imgIdx=image.imgIdx, keyword=i['keyword'], level=i['level'], topic=None)
                db.session.add(new_keyword)
            db.session.commit()
        else:  # scriptOnly인 경우
            image = form.scriptonly[0]
            for i in request.json:
                new_keyword = Keyword(
                    imgIdx=image.imgIdx, keyword=i['keyword'], level=i['level'], topic=None)
                db.session.add(new_keyword)
            db.session.commit()
        return jsonify({'status': 'success', 'message': 'Keyword saved successfully'}), 200


    elif request.method == "PUT":
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image[pgNum-1]
            for i in image.keyword:
                db.session.delete(i)
            for i in request.json:
                new_keyword = Keyword(
                    imgIdx=image.imgIdx, keyword=i['keyword'], level=i['level'], topic=None)
                db.session.add(new_keyword)
            db.session.commit()
            return  jsonify({'status': 'success', 'message': 'Keyword updated successfully'}), 200
        else:
            scriptonly = form.scriptonly
            for i in scriptonly.keyword:
                db.session.delete(i)
            for i in request.json:
                new_keyword = Keyword(
                    imgIdx=image.imgIdx, keyword=i['keyword'], level=i['level'], topic=None)
                db.session.add(new_keyword)
            db.session.commit()
            
            return  jsonify({'status': 'success', 'message': 'Keyword updated successfully'}), 200
        



@bp.route('/query', methods=['GET', 'POST', 'PUT', 'DELETE'])
def query():
    form = Form.query.filter(Form.formIdx == 3).first()
    keyword = Scriptonly(form=form, script="fsfsf")
    db.session.add(keyword)
    db.session.commit()
    return "clear"
