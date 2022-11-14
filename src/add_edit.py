from app import db, Clientes, Enderecos, Chamados


def add_new_cliente(request):
    nome = request.form['nome'].capitalize()
    sobrenome = request.form['sobrenome'].capitalize()
    telefone = request.form['telefone']
    cpf = request.form['cpf']
    cliente = Clientes(nome=nome, cpf=cpf, sobrenome=sobrenome, telefone=telefone)
    db.session.add(cliente)
    db.session.commit()
    new_cliente_id = cliente.id
    cidade = request.form['cidade']
    rua = request.form['rua']
    numero = request.form['numero']
    endereco = Enderecos(cliente_id=new_cliente_id, cidade=cidade, rua=rua, numero=numero)
    db.session.add(endereco)
    db.session.commit()


def edit_cliente(request, cliente):
    cliente.nome = request.form['nome'].capitalize()
    cliente.sobrenome = request.form['sobrenome'].capitalize()
    cliente.telefone = request.form['telefone']
    cliente.cpf = request.form['cpf']
    db.session.commit()
    endereco = db.session.execute(db.select(Enderecos).filter_by(cliente_id=cliente.id)).scalar_one()
    endereco.cidade = request.form['cidade'].capitalize()
    endereco.rua = request.form['rua'].capitalize()
    endereco.numero = request.form['numero']
    db.session.commit()


def add_new_chamado(request):
    cpf = request.form['cpf']
    query = db.session.execute(db.select(Clientes).filter_by(cpf=cpf)).one()
    cliente = [x.serialize() for x in query]
    assunto = request.form['assunto'].capitalize()
    pedido = request.form['pedido'].capitalize()
    estado = request.form['estado'].capitalize()
    endereco_id = cliente[0]['endereco'][0]['id']
    chamado = Chamados(cliente_id=cliente[0]['id'], assunto=assunto, pedido=pedido, estado=estado,
                       endereco_id=endereco_id)
    db.session.add(chamado)
    db.session.commit()


def edit_chamado(request, chamado):
    chamado.assunto = request.form['assunto'].capitalize()
    chamado.pedido = request.form['pedido'].capitalize()
    chamado.estado = request.form['estado'].capitalize()
    db.session.commit()
