from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
import numpy as np

from ml.feature_extractor import extract_features
from ml.model_loader import model, FEATURE_COLUMNS

from models.scan import Scan
from extensions import db
from flask import redirect

user_bp = Blueprint("user", __name__)


@user_bp.route("/user/dashboard")
@login_required
def dashboard():
    if current_user.role != "user":
        return "Access denied", 403

    scans = Scan.query.filter_by(user_id=current_user.id)\
                      .order_by(Scan.timestamp.desc())\
                      .limit(5)\
                      .all()

    total = Scan.query.filter_by(user_id=current_user.id).count()
    phishing = Scan.query.filter_by(user_id=current_user.id, prediction="Phishing").count()
    legitimate = Scan.query.filter_by(user_id=current_user.id, prediction="Legitimate").count()

    return render_template(
        "user/dashboard.html",
        scans=scans,
        total=total,
        phishing=phishing,
        legitimate=legitimate
    )


@user_bp.route("/user/predict", methods=["POST"])
@login_required
def predict():
    if current_user.role != "user":
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json(force=True)
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    feature_dict = extract_features(url, FEATURE_COLUMNS)
    feature_vector = [feature_dict[col] for col in FEATURE_COLUMNS]
    feature_vector = np.array(feature_vector).reshape(1, -1)

    probability = model.predict_proba(feature_vector)[0]

    phishing_prob = probability[1]
    confidence = round(phishing_prob * 100, 2)

    if confidence >= 85:
        final_result = "Phishing"
    elif confidence >= 60:
        final_result = "Suspicious"
    else:
        final_result = "Legitimate"

    new_scan = Scan(
    url=url,
    prediction=final_result,
    confidence=confidence,
    user_id=current_user.id
)

    db.session.add(new_scan)
    db.session.commit()

    
    return jsonify({
        "url": url,
        "prediction": final_result,
        "confidence": confidence
    })
    
@user_bp.route("/user/history")
@login_required
def history():
    if current_user.role != "user":
        return "Access denied", 403

    scans = Scan.query.filter_by(user_id=current_user.id)\
                      .order_by(Scan.timestamp.desc())\
                      .all()

    return render_template("user/history.html", scans=scans)


@user_bp.route("/user/delete/<int:scan_id>", methods=["POST"])
@login_required
def delete_scan(scan_id):

    scan = Scan.query.filter_by(id=scan_id, user_id=current_user.id).first()

    if scan:
        db.session.delete(scan)
        db.session.commit()

    return redirect("/user/history")

@user_bp.route("/user/delete-selected", methods=["POST"])
@login_required
def delete_selected():

    ids = request.form.getlist("scan_ids")

    if ids:
        Scan.query.filter(
            Scan.id.in_(ids),
            Scan.user_id == current_user.id
        ).delete(synchronize_session=False)

        db.session.commit()

    return redirect("/user/history")