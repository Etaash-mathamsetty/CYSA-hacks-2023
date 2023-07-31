from simplejsondb import Database

# If database named 'db' doesn't exist yet, creates a new empty dict database
database = Database('db.json', default=dict())

# Now, we can treat the database instance as a dictionary!
# database.data['Hello'] = 'Hola'
# database.data['Goodbye'] = 'Adios'
# print(database.data.values())   # dict_values(['Hola', 'Adios'])

# put a dictionary as the value
def write(key, value):
    database.data[key] = value
    database.save()

def read_all():
    return database.data

def read(key):
    return database.data[key]

# if __name__ == "__main__":