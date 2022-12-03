from app.__init__ import db, login_manager, ma

from marshmallow import fields
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(192), unique=True)
    password = db.Column(db.String())
    email = db.Column(db.String(192), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Clientes(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String())
    sobrenome = db.Column(db.String())
    cpf = db.Column(db.String(96), unique=True)
    telefone = db.Column(db.String())
    endereco = db.relationship('Enderecos', uselist=False, backref='clientes', lazy=True)


class Enderecos(db.Model):
    __tablename__ = 'enderecos'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    cidade = db.Column(db.String())
    rua = db.Column(db.String())
    numero = db.Column(db.Integer())


class Chamados(db.Model):
    __tablename__ = 'chamados'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = db.relationship('Clientes')
    assunto = db.Column(db.String())
    estado = db.Column(db.String())
    pedido = db.Column(db.Text())


class EnderecosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Enderecos
        include_fk = True
        load_instance = True


class ClientesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Clientes
        include_relationships = True
        load_instance = True

    endereco = fields.Nested(EnderecosSchema)  # type: ignore


cliente_schema = ClientesSchema()
clientes_schema = ClientesSchema(many=True)


class ChamadosSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Chamados
        include_relationships = True
        load_instance = True

    cliente = fields.Nested(ClientesSchema)  # type: ignore


chamado_schema = ChamadosSchema()
chamados_schema = ChamadosSchema(many=True)
