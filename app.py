from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection (AWS RDS info you gave me)
db = mysql.connector.connect(
    host="cis3368spring.cd0tnym0yhpn.us-east-1.rds.amazonaws.com",  # Your AWS endpoint
    user="ZionBello",                                              # Your DB username
    password="Dabira01",                                           # Your DB password
    database="cis3368springdb"                                     # Your actual DB name (not 'cis3368spring')
)

cursor = db.cursor(dictionary=True)

# GET: Return all animals
@app.route('/api/zoo', methods=['GET'])
def get_animals():
    cursor.execute("SELECT * FROM zoo")
    animals = cursor.fetchall()
    return jsonify(animals), 200

# POST: Add a new animal
@app.route('/api/zoo', methods=['POST'])
def add_animal():
    data = request.json
    sql = """
        INSERT INTO zoo (domain, kingdom, class, species, age, animalname, alive)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data['domain'],
        data['kingdom'],
        data['class'],
        data['species'],
        data['age'],
        data['animalname'],
        data['alive']
    )
    cursor.execute(sql, values)
    db.commit()
    return jsonify({'message': 'Animal added successfully', 'id': cursor.lastrowid}), 201

# PUT: Update alive status
@app.route('/api/zoo', methods=['PUT'])
def update_animal():
    data = request.json
    sql = "UPDATE zoo SET alive = %s WHERE id = %s"
    values = (data['alive'], data['id'])
    cursor.execute(sql, values)
    db.commit()
    return jsonify({'message': 'Animal updated successfully'}), 200

# DELETE: Delete an animal
@app.route('/api/zoo', methods=['DELETE'])
def delete_animal():
    data = request.json
    sql = "DELETE FROM zoo WHERE id = %s"
    val = (data['id'],)
    cursor.execute(sql, val)
    db.commit()
    return jsonify({'message': 'Animal deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
