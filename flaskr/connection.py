import mysql.connector


db = mysql.connector.connect(
    host="localhost",          
    user="root",         
    password="admin",  
    database="text_prediction"  
)

cursor = db.cursor()

# Create
def create(id_ticket, category, title, description):
    query = "INSERT INTO text_store (id_ticket, category, title, description) VALUES (%s, %s, %s, %s)"
    values = (id_ticket, category, title, description)
    cursor.execute(query, values)
    db.commit()
    print(f"Registro creado con ID: {cursor.lastrowid}")

# Read
def read():
    query = "SELECT * FROM text_store"
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(row)

#Select 
def select_row(id):
    query = "SELECT * FROM text_store Where id_ticket = %s"
    values = (id,)
    cursor.execute(query,values)
    result = cursor.fetchall()
    return result

# Update
def update(id_ticket, category):
    query = "UPDATE text_store set category = %s WHERE id_ticket = %s"
    values = (category, id_ticket)
    cursor.execute(query, values)
    db.commit()

