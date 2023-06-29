from flask import Blueprint, jsonify, request
from app.models import *
from .image import upload_file
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
        li = upload_file()
        form = Form()
        db.session.add(form)
        ppt = Presentation(formIdx=form.formIdx)
        db.session.add(ppt)
        # "imgUrls" : ["http~~","http~~","http~~"],

        # 파싱 ->
        for pgNum, imgUrl in enumerate(li):
            if not imgUrl:
                errMsg = 'Validation Error'
                return jsonify({'status': 'error', 'message': errMsg}), 422
            else:
                image = Image(pptIdx=ppt.pptIdx, pgNum=pgNum+1,
                              imgUrl=imgUrl, script=None, topic=None)
                db.session.add(image)
                db.session.commit()

        return jsonify(li)


@bp.route('/<int:Idx>', methods=['GET'])
def img_url(Idx):
    list = []
    form = Form.query.filter(Form.formIdx == Idx).first()
    ppt = form.presentation[0]
    image = ppt.image
    for i in image:
        list.append({"pgNum": i.pgNum, "imgUrl": i.imgUrl})
    return jsonify(list)


@bp.route('/<int:Idx>/<int:pgNum>/data', methods=['GET', 'POST', 'PUT'])
def form_script(Idx, pgNum):
    if request.method == "GET":
        reslist = []
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image[pgNum-1]
            reslist.append({"script": image.script})
        else:
            scriptonly = form.scriptonly[0]
            reslist.append({"script": scriptonly.script})
        # keyword 저장
        keylist = []
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image[pgNum-1]
            for i in image.keyword:
                keylist.append({
                    "key": i.keyword, "level": i.level
                })
            reslist.append(keylist)
        else:
            scriptonly = form.scriptonly[0]
            for i in scriptonly.keyword:
                keylist.append({
                    "key": scriptonly.keyword, "level": scriptonly.level
                })
            reslist.append(keylist)
        return jsonify(reslist)

    elif request.method == "POST":
        fIdx = Idx
        if fIdx != 0:
            form = Form.query.filter(Form.formIdx == Idx).first()
            if form.presentation:
                ppt = form.presentation[0]
                image = ppt.image
                image[pgNum-1].script = request.json[0]['script']
                db.session.commit()
            else:
                scriptonly = form.scriptonly[0]
                scriptonly.script = request.json[0]['script']
                db.session.commit()

        else:
            form = Form()
            db.session.add(form)
            scriptonly = Scriptonly(
                formIdx=form.formIdx, script=request.json[0]['script'])
            db.session.add(scriptonly)
            db.session.commit()
            fIdx = form.formIdx

        # keword 저장
        # key를 저장해야할 form을 idx로 가져옴
        # keyword
        form = Form.query.filter(Form.formIdx == fIdx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image[pgNum-1]
            if image.keyword:
                for i in image.keyword:
                    db.session.delete(i)
            for i in request.json[1]:
                new_keyword = Keyword(
                    imgIdx=image.imgIdx, keyword=i['keyword'], level=i['level'], topic=None)
                db.session.add(new_keyword)
            db.session.commit()
        else:
            scriptonly = form.scriptonly[0]
            if scriptonly.keyword:
                for i in scriptonly.keyword:
                    db.session.delete(i)
            for i in request.json[1]:
                new_keyword = Keyword(
                    scriptOnlyIdx=scriptonly.scriptOnlyIdx, keyword=i['keyword'], level=i['level'], topic=None)
                db.session.add(new_keyword)
            db.session.commit()
        return jsonify({"formIdx": fIdx})

    elif request.method == "PUT":
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image
            image[pgNum-1].script = request.json[0]['script']
            db.session.commit()
        else:
            scriptonly = form.scriptonly[0]
            scriptonly.script = request.json[0]['script']
            db.session.commit()

        # keyword
        form = Form.query.filter(Form.formIdx == Idx).first()
        if form.presentation:
            ppt = form.presentation[0]
            image = ppt.image[pgNum-1]
            if image.keyword:
                for i in image.keyword:
                    db.session.delete(i)
            for i in request.json[1]:
                new_keyword = Keyword(
                    imgIdx=image.imgIdx, keyword=i['keyword'], level=i['level'], topic=None)
                db.session.add(new_keyword)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Keyword updated successfully'}), 200
        else:
            scriptonly = form.scriptonly[0]
            if scriptonly.keyword:
                for i in scriptonly.keyword:
                    db.session.delete(i)
            for i in request.json[1]:
                new_keyword = Keyword(
                    imgIdx=image.imgIdx, keyword=i['keyword'], level=i['level'], topic=None)
                db.session.add(new_keyword)
            db.session.commit()

            return jsonify({'status': 'success', 'message': 'Keyword updated successfully'}), 200


@bp.route('/query', methods=['GET', 'POST', 'PUT', 'DELETE'])
def query():
    image = Image.query.filter(Image.imgIdx == 1).first()
    print(image.keyword)
    return "clear"
