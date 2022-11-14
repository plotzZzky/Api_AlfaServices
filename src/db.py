from app import db, Chamados, Clientes, Enderecos

clientes = [
    {'nome': 'ze', 'sobrenome': 'da silva', 'cpf': '000.000.000-00', 'telefone': '(51)0000-0000', },
    {'nome': 'julio', 'sobrenome': 'cesar', 'cpf': '000.000.000-11', 'telefone': '(51)0000-0012', },
    {'nome': 'Elvis', 'sobrenome': 'Presley', 'cpf': '999.999.999-99', 'telefone': '(51)0000-0012', },
]

enderecos = [
    {'cliente_id': 1, 'cidade': 'esteio', 'rua': 'Pequim', 'numero': 90},
    {'cliente_id': 2, 'cidade': 'esteio', 'rua': 'brasil', 'numero': 120},
    {'cliente_id': 3, 'cidade': 'esteio', 'rua': 'las vegas', 'numero': 318}
]

chamdos = [
    {'cliente_id': 1, 'assunto': 'troca de modem', 'estado': 'Em aberto',
     'pedido': 'Cliente soclita a troca de modem com defeito'},
    {'cliente_id': 2, 'assunto': 'instalacao de tv', 'estado': 'Em aberto',
     'pedido': 'Cliente soclita a tinstalacao de tv com 300 canais'},
    {'cliente_id': 3, 'assunto': 'Troca de plano', 'estado': 'Em aberto',
     'pedido': 'Cliente soclita a troca dos planos de internet e tv junto com seus aparelhos'},
]


def add_clientes_base():
    for item in clientes:
        cliente = Clientes(nome=item['nome'], sobrenome=item['sobrenome'], cpf=item['cpf'], telefone=item['telefone'])
        db.session.add(cliente)
        db.session.commit()


def add_enderecos_base():
    for item in enderecos:
        endereco = Enderecos(cliente_id=item['cliente_id'], cidade=item['cidade'], rua=item['rua'],
                             numero=item['numero'])
        db.session.add(endereco)
        db.session.commit()


def add_chamado_base():
    for item in chamdos:
        chamdo = Chamados(cliente_id=item['cliente_id'], assunto=item['assunto'],
                          estado=item['estado'], pedido=item['pedido'])
        db.session.add(chamdo)
        db.session.commit()
