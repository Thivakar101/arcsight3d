from flask import jsonify

def success_response(data=None, meta=None, status_code=200):
    return jsonify({
        "success": True,
        "data": data if data is not None else {},
        "error": None,
        "meta": meta if meta is not None else {}
    }), status_code

def error_response(code, message, details=None, status_code=400):
    return jsonify({
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details if details is not None else {}
        },
        "meta": {}
    }), status_code
