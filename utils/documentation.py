import json

def extract_endpoints(doc_data):
    """Dokümantasyondan endpoint bilgilerini çıkarır."""
    endpoints = []
    for path, methods in doc_data.get('paths', {}).items():
        for method, details in methods.items():
            endpoints.append({
                "path": path,
                "method": method.upper(),
                "parameters": details.get('parameters', []),
                "responses": details.get('responses', {})
            })
    return endpoints
