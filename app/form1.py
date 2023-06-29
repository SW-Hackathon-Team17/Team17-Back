from flask import Blueprint, jsonify, request
from app.models import *
bp = Blueprint('form', __name__, url_prefix='/form')


@bp.route('/', methods=['GET', 'POST'])
def imgUrlSave():

    if request.method == "POST":
        forms = Form(check=1)
        db.session.add(forms)
        db.session.commit()
        ppt = Presentation(form=forms)
        db.session.add(ppt)
        db.session.commit()

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


@bp.route('/<int:Idx>/<int:pgNum>/script', methods=['GET,POST,PUT,DELETE'])
def form_list(Idx, pgNum):
    if request.method == "GET":
        form = Form.query.filter(Form.formIdx == Idx).first()
        form = form.form_set.first()
        print(form.__name__)
        if form.__name__ == 'ppt':
            form = form.ppt_set[pgNum-1]
            return jsonify({"script": form.script})
        else:
            return jsonify({"script": form.script})

    elif request.method == "POST":
        form = Form()
        db.session.add(form)
        db.session.commit()
        ppt = Presentation(formIdx=form)
        db.session.add(ppt)
        db.session.commit()
    return jsonify([{}])