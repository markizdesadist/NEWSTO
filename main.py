from database.database import DataBase

xml_base = list()

if __name__ == '__main__':
    db = DataBase()
    db.database_initialization()
    # db.insert_owner_value(elem_xml)
    db.display()

