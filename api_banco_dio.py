from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import bindparam
from sqlalchemy import Numeric
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete

Base = declarative_base()


class Clients(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String(9))
    endereco = Column(String(40))

    contas = relationship(
        "Contas", back_populates="clientes", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente = " \
               f"conta: '{self.contas}', " \
               f"nome: '{self.nome}', " \
               f"cpf: '{self.cpf}', " \
               f"endereço: '{self.endereco}'"


class Contas(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"))
    saldo = Column(Numeric(precision=10, scale=2))

    clientes = relationship("Clients", back_populates="contas")

    def __repr__(self):
        return f"{self.clientes}, {self.tipo}, {self.agencia}, {self.num}, {self.saldo}"


# Criando a engine de conexão com o DB
engine = create_engine('sqlite://', echo=False)

Base.metadata.create_all(engine)

with Session(engine) as session:
    pedro = Clients(
        nome='pedro souza',
        cpf='67854320638',
        endereco='são paulo-sp brasil',
        contas=[
            Contas(tipo='poupança', agencia='1213', num=54789, saldo=125897.43)
        ]
    )

    ana = Clients(
        nome='ana souza',
        cpf='02362423478',
        endereco='são paulo-sp brasil',
        contas=[
            Contas(tipo='corrente', agencia='1213', num=54793, saldo=34200.00)
        ]
    )

    fabio = Clients(
        nome='fabio martins',
        cpf='04836283983',
        endereco='florianópolis-sc brasil',
        contas=[
            Contas(tipo='corrente', agencia='7222', num=100345, saldo=12567.32)
        ]
    )

    rita = Clients(
        nome='rita von hunt',
        cpf='03483912789',
        endereco='curitiba-pr brasil',
        contas=[
            Contas(tipo='poupança', agencia='7844', num=23445, saldo=2345.78)
        ]
    )

    dexter = Clients(
        nome='dexter araujo',
        cpf='73490235673',
        endereco='curitiba-pr brasil',
        contas=[
            Contas(tipo='poupança', agencia='7844', num=23789, saldo=879.54)
        ]
    )
session.add_all([pedro, ana, rita, fabio, dexter])
session.commit()



session = Session(engine)
'''
# Selecionar todos os clientes da tabela
statement = select(Clients)
for user in session.scalars(statement):
    print(user)

# selecionar um cliente especifico pelo campo nome
stmt = select(Clients).where(Clients.nome.in_(['ana souza']))
for user in session.scalars(stmt):
    print(user)'''

# criando um join com as tabelas clientes e contas

stmt_join = (
    select(Contas.saldo, Clients.nome)
    .join(Contas.clientes)
    .where(Clients.endereco == 'curitiba-pr brasil')
    .where(Contas.saldo >= 500.00)
)

# session.execute retorna todos os campos da tabela que eu queira
clientes_curitiba = session.execute(stmt_join)
for cliente in clientes_curitiba:
    nome, saldo = cliente[1], cliente[0]
    print(f"Nome: {nome.title()}, Saldo: R${saldo}")

# session.scalars retorna apenas um campo específico, neste caso o primeiro selecionado no join
for cliente in session.scalars(stmt_join):
    print(f'Saldo {cliente}')

stmt = select(Clients).where(Clients.nome == 'dexter araujo franco')
for user in session.scalars(stmt):
    print(user)

stmt = session.execute(select(Clients.nome, Clients.cpf).order_by(Clients.nome))
for row in stmt:
    print(f'Nome: {row[0].title()}, CPF: {row[1]}')

stmt = session.execute(
    select(Clients.nome, Contas)
    .join(Clients)
    )
for row in stmt:
    print(row)

# alterando dados
stmt_update = session.execute(
    update(Clients)
    .where(Clients.nome == 'dexter araujo').values(cpf='12345678998')
    )
stmt = select(Clients).where(Clients.nome == 'dexter araujo')
dexter_update = session.execute(stmt)
for row in dexter_update:
    print(row)

# deletando

#session.delete(pedro)
stmt = session.execute(
    delete(Clients).where(Clients.nome == 'fabio martins')
)
stmt_delete = session.execute(select(Clients.nome))
for row in stmt_delete:
    print(row)


