from sqlalchemy import create_engine, text

engine = create_engine('mysql+mysqlconnector://root:6172@localhost:3306/av3', echo=True)

with engine.connect() as connection:
    result = connection.execute(text("show tables;"))
    for row in result.mappings():
        print(row)