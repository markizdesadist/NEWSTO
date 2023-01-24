from database.database import Data

xml_base = list()

if __name__ == '__main__':
    new = Data()
    for elem in xml_base:
        new.create_base(elem)
