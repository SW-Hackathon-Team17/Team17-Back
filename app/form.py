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
