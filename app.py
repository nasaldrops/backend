from flask import Flask, jsonify, request
from flask_cors import CORS
import pyodbc
import os
from dotenv import load_dotenv

if os.getenv('ENVIRONMENT') != 'production':
    load_dotenv()

app = Flask(__name__)
CORS(app)



@app.route('/')
def hello():

    return 'Welcome to your Research Dashboard, created by CloudKubed'

#get all the projects
@app.route('/projects', methods=['GET'])
def get_projects():
    conn_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('DB_SERVER')};DATABASE={os.getenv('DB_DATABASE')};UID={os.getenv('DB_USERNAME')};PWD={os.getenv('DB_PASSWORD')}"
    
    try:
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Projects")
            projects = cursor.fetchall()
            projects_list = [{'project_id': row[0], 'title': row[1], 'description': row[2], 'status_id': row[3], 'researcher_id': row[4]} for row in projects]
            return jsonify(projects_list)
    except Exception as e:
        return jsonify({'error': str(e)})

from flask import request, jsonify


# add a new project to the db
@app.route('/projects', methods=['POST'])
def add_project():
    data = request.json 

    title = data.get('title')
    description = data.get('description')
    status_id = data.get('status_id')
    researcher_id = data.get('researcher_id')
    conn_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('DB_SERVER')};DATABASE={os.getenv('DB_DATABASE')};UID={os.getenv('DB_USERNAME')};PWD={os.getenv('DB_PASSWORD')}"
    try:
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            insert_query = "INSERT INTO Projects (title, description, status_id, researcher_id) VALUES (?, ?, ?, ?)"
            cursor.execute(insert_query, (title, description, status_id, researcher_id))
            conn.commit()
            return jsonify({'message': 'Project added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#delete a project here
@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    conn_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('DB_SERVER')};DATABASE={os.getenv('DB_DATABASE')};UID={os.getenv('DB_USERNAME')};PWD={os.getenv('DB_PASSWORD')}"

    try:
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            delete_query = "DELETE FROM Projects WHERE project_id = ?"
            cursor.execute(delete_query, (project_id,))
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({'message': 'No project found with the given ID'}), 404

            return jsonify({'message': 'Project deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#update the project info
@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    data = request.json 
    title = data.get('title')
    description = data.get('description')
    status_id = data.get('status_id')
    researcher_id = data.get('researcher_id')

    conn_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={os.getenv('DB_SERVER')};DATABASE={os.getenv('DB_DATABASE')};UID={os.getenv('DB_USERNAME')};PWD={os.getenv('DB_PASSWORD')}"

    try:
        with pyodbc.connect(conn_string) as conn:
            cursor = conn.cursor()
            update_query = "UPDATE Projects SET title = ?, description = ?, status_id = ?, researcher_id = ? WHERE project_id = ?"
            cursor.execute(update_query, (title, description, status_id, researcher_id, project_id))
            conn.commit()

            if cursor.rowcount == 0:
                return jsonify({'message': 'No project found with the given ID'}), 404

            return jsonify({'message': 'Project updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
