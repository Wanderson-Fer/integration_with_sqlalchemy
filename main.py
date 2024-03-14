from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, inspect, select
from sqlalchemy.orm import DeclarativeBase, relationship, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    # Atributos
    id = Column(Integer, primary_key=True)
    name = Column(String, )
    fullname = Column(String, )

    address = relationship(  # One-to-many relationship
        "Address",  # Specifies the target model class
        back_populates="user",  # Stablishes a bi-relationship using this field on the target
        cascade="all, delete-orphan"  # Auto deleting references
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"


class Address(Base):
    __tablename__ = "address"

    # Atributos
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship(
        "User",
        back_populates="address"
    )

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"


def add_datas(eng):
    with Session(eng) as s:
        wand = User(
            name='Wanderson',
            fullname='Wanderson Fernandes',
            address=[
                Address(email_address='playerlocke@gmail.com')
            ]
        )

        juliana = User(
            name='Juliana',
            fullname='Juliana Mascarenhas',
            address=[
                Address(email_address='juliana@email.com'),
                Address(email_address='mascarenhasj@email.com'),
            ]
        )

        patrick = User(
            name='Patrick',
            fullname='Patrick Kauai'
        )

        # Enviando para o DB
        s.add_all([wand, juliana, patrick])
        s.commit()
        # s.close()


def print_stmt_with_scalars(stmt, eng):
    print('>>>')
    with Session(eng) as session:
        for record in session.scalars(stmt):
            print(record)
    print('-'*50)


def print_stmt_with_execute(stmt, eng):
    print('>>>')
    with Session(eng) as session:
        results = session.execute(stmt)
        print(results)
        for record in results:
            print(record)
    print('-'*50)

def print_stmt_with_fetch(stmt, eng):
    print('>>>')
    with Session(eng) as session:
        results = session.execute(stmt).fetchall()
        print(results)
        for record in results:
            print(record)
    print('-'*50)


if __name__ == '__main__':
    print(User.__tablename__)
    print(repr(User))

    # Conexão com o banco de dados
    engine = create_engine("sqlite://")

    # Criando as classes como tabelas no BD
    Base.metadata.create_all(engine)

    # Referência para inspecionar o BD
    inspector = inspect(engine)
    print(inspector.get_table_names())

    # Adicionando dados no BD
    add_datas(engine)

    # Criando instrução da consulta
    stmt_user = select(User).where(User.name.in_(['Juliana']))  # Select com Where
    # print(stmt)
    print('\nRecuperando usuários pelo nome')
    print_stmt_with_scalars(stmt_user, engine)

    print('\nRecuperando endereços de um usuário')
    stmt_address = select(Address).where(Address.user_id.in_([2]))  # Select com where
    print_stmt_with_scalars(stmt_address, engine)

    print('\nRecuperando todos os usuários de forma ordenada')
    stmt_ordered_users = select(User).order_by(User.fullname.desc())  # Select com Order
    print_stmt_with_scalars(stmt_ordered_users, engine)

    print('\nRecuperando info com join_from')
    stmt_join = select(User.fullname, Address.email_address).join_from(User, Address)
    print(stmt_join)
    print_stmt_with_scalars(stmt_join, engine)

    print('\nRecuperando info com join')
    stmt_join = select(User, Address).join(Address.user)
    print(stmt_join)
    print_stmt_with_execute(stmt_join, engine)

    print('\nRecuperando info com join & fetchall')
    stmt_join = select(User, Address).join(Address.user)
    print(stmt_join)
    print_stmt_with_fetch(stmt_join, engine)
