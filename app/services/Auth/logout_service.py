from flask import jsonify
from flask_login import current_user, logout_user


def User_logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "Logout realizado com sucesso"})
    return jsonify({"message": "Sessão já encerrada ou inexistente."}), 403
