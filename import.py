import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DB"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    filename = input('File Name: ')
    count = 0
    print("Counting rows...", end='')
    with open(filename, 'r') as file:
        for line in file:
            count += 1
    f = open(filename)
    reader = csv.reader(f)
    i = 0
    print(f" {count}")
    for provincia in reader:
        print('\r', end='')
        i += 1
        for asd in provincia:
            asd = asd.replace('{', '')
            asd = asd.replace('}', '')
            db.execute("INSERT INTO province (provincia) VALUES (:provincia)",
                    {"provincia": asd})
        print(f"Importing distring {i} of {count}", end='')


    db.commit()
    print("\nDone!")
if __name__ == "__main__":
    main()
