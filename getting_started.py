from sqlalchemy import create_engine, text

if __name__ == '__main__':
    engine = create_engine('sqlite+pysqlite:///:memory:', echo='debug')

    # with engine.connect() as conn:
    #     result = conn.execute(text("select 'Hello world'"))
    #     print(result.all())

    with engine.begin() as conn:  # Begin once
        conn.execute(text("CREATE TABLE some_table(x int, y int)"))

        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [
                {'x': 1, 'y': 2},  # The statement goes be executed for each dict
                {'x': 3, 'y': 4},
            ]
        )
        # conn.commit()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM some_table"))
        print(result.all())
