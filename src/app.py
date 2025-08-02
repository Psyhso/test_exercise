from flask import Flask, jsonify, request
from datetime import datetime
from parser.parser import parser

app = Flask(__name__)


@app.route('/tenders', methods=['GET'])
def get_tenders():
    """
    Парсинг и получение тендеров

    Параметры запроса:
    - count: количество тендеров для парсинга (по умолчанию 10, максимум 100)

    Пример: /tenders?count=20
    """
    try:
        count = request.args.get('count', default=10, type=int)

        if count <= 0:
            return jsonify({
                "success": False,
                "error": "Параметр count должен быть больше 0"
            }), 400

        if count > 100:
            count = 100

        tenders_data = parser(count)

        if isinstance(tenders_data, str) and tenders_data.startswith("Ошибка"):
            return jsonify({
                "success": False,
                "error": tenders_data,
                "data": []
            }), 500

        result = {
            "success": True,
            "data": tenders_data,
            "total_processed": len(tenders_data),
            "meta": {
                "requested_count": count,
                "timestamp": datetime.now().isoformat(),
                "source": "rostender.info"
            }
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Внутренняя ошибка сервера: {str(e)}",
            "data": []
        }), 500


@app.route('/', methods=['GET'])
def index():
    """Главная страница с инструкциями"""
    return jsonify({
        "message": "API для парсинга тендеров",
        "endpoints": {
            "/tenders": {
                "method": "GET",
                "description": "Парсинг тендеров с rostender.info",
                "parameters": {
                    "count": "количество тендеров (1-100, по умолчанию 10)"
                },
                "example": "/tenders?count=20"
            }
        },
        "usage_examples": [
            "curl http://localhost:5000/tenders",
            "curl http://localhost:5000/tenders?count=25"
        ]
    })


if __name__ == '__main__':
    print("Документация: http://localhost:5000")
    print("Парсинг тендеров: http://localhost:5000/tenders?count=10")

    app.run(debug=True, host='0.0.0.0', port=5000)
