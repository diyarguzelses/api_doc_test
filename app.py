from flask import Flask, request, jsonify, render_template, redirect, url_for
import json
import requests
from utils.documentation import extract_endpoints
from utils.comparison import test_endpoint, compare_responses

app = Flask(__name__)

# Global değişken: Dokümantasyon
doc_data = None


@app.route('/')
@app.route('/')
def home():
    """Ana sayfa: İşlem butonlarını görüntüler."""
    message = request.args.get('message', '')  # Sorgu parametresinden "message" al
    return render_template("home.html", message=message)


@app.route('/upload-doc', methods=['POST'])
def upload_doc():
    """Dokümantasyon JSON dosyasını yükler."""
    global doc_data
    file = request.files.get('doc_file')
    if not file:
        return jsonify({"error": "Dokümantasyon dosyası yüklenmedi!"}), 400

    try:
        doc_data = json.loads(file.read())
        return redirect(url_for('home', message="Dokümantasyon başarıyla yüklendi!"))
    except Exception as e:
        return redirect(url_for('home', message=f"Hata: {str(e)}"))


@app.route('/test-doc', methods=['POST'])
def test_doc():
    """Dokümantasyon ve gerçek API'yi karşılaştırır."""
    global doc_data
    if not doc_data:
        return jsonify({"error": "Önce bir dokümantasyon yüklenmeli!"}), 400

    base_url = request.form.get('base_url')
    if not base_url:
        return jsonify({"error": "Base URL gerekli!"}), 400

    # Endpoint'leri dokümantasyondan çıkar
    endpoints = extract_endpoints(doc_data)

    # Beklenen değerleri dokümantasyondan al
    expected_responses = {}
    for path, methods in doc_data.get("paths", {}).items():
        for method, details in methods.items():
            if method.lower() == "get":
                example_response = details.get("responses", {}).get("200", {}).get("content", {}).get(
                    "application/json", {}).get("example", {})
                expected_responses[path] = {
                    "status_code": 200,
                    "response_body": example_response
                }

    # Her endpoint'i test et
    report = []
    for endpoint in endpoints:
        actual = test_endpoint(base_url, endpoint)
        expected = expected_responses.get(endpoint['path'], {})
        differences = compare_responses(expected, actual)

        report.append({
            "endpoint": endpoint['path'],
            "method": endpoint['method'],
            "status": "Success" if not differences else "Failed",
            "expected_response": expected.get("response_body", {}),
            "actual_response": actual.get("response_body", {}),
            "differences": differences
        })

    return render_template("report.html", report=report, doc_data=doc_data)







if __name__ == "__main__":
    app.run(debug=True)

