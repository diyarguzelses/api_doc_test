import requests


def test_endpoint(base_url, endpoint):
    """Gerçek API'yi test eder."""
    url = f"{base_url}{endpoint['path']}"
    method = endpoint['method']
    try:
        # Örnek değerleri koy
        if '{username}' in url:
            url = url.replace('{username}', 'octocat')  # Test için 'octocat' kullan

        response = requests.request(method, url)

        # Yanıtı JSON olarak ayrıştırmayı dene, değilse düz metin olarak kaydet
        try:
            response_body = response.json()
        except ValueError:
            response_body = response.text

        return {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "response_body": response_body
        }
    except Exception as e:
        return {"error": str(e)}


def compare_responses(expected, actual):
    """Beklenen ve gerçek yanıtları detaylı şekilde karşılaştırır."""
    differences = {}

    # 1. HTTP durum kodunu kontrol et
    if expected.get('status_code') != actual.get('status_code'):
        differences['status_code'] = {
            "expected": expected.get('status_code'),
            "actual": actual.get('status_code')
        }

    # 2. Yanıt gövdesini kontrol et
    expected_body = expected.get('response_body', {})
    actual_body = actual.get('response_body', {})

    # Eğer actual_body bir dict değilse veya eksikse
    if not isinstance(actual_body, dict):
        differences['response_body'] = {
            "expected": expected_body,
            "actual": f"Yanıt JSON formatında değil: {actual_body}"
        }
        return differences

    # 3. Beklenen ve gerçek değerleri kıyasla
    for key, expected_value in expected_body.items():
        actual_value = actual_body.get(key)

        # Beklenen anahtar mevcut mu?
        if key not in actual_body:
            differences[key] = {
                "expected": expected_value,
                "actual": None
            }
        # Değerler aynı mı?
        elif actual_value != expected_value:
            differences[key] = {
                "expected": expected_value,
                "actual": actual_value
            }

    # 4. Fazla anahtarları kontrol et (isteğe bağlı)
    extra_keys = set(actual_body.keys()) - set(expected_body.keys())
    if extra_keys:
        differences['extra_keys'] = list(extra_keys)

    return differences
