from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/pets', methods=['GET'])
def get_pets():
    return jsonify([
        {"id": 1, "name": "Dog"},
        {"id": 2, "name": "Cat"}
    ])

@app.route('/pets/<int:pet_id>', methods=['GET'])
def get_pet(pet_id):
    if pet_id == 1:
        return jsonify({"id": 1, "name": "Dog"})
    elif pet_id == 2:
        return jsonify({"id": 2, "name": "Cat"})
    else:
        return jsonify({"error": "Not Found"}), 404

if __name__ == "__main__":
    app.run(port=5001)
