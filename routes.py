from flask import request, render_template, flash, redirect, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from auth import signup_user
from src.db import add_clientes_base, add_chamado_base, add_enderecos_base
from src.add_edit import edit_cliente, add_new_cliente, add_new_chamado, edit_chamado
from app import (app, db, User, Clientes, Chamados, Enderecos, cliente_schema, clientes_schema, chamado_schema,
                 chamados_schema)


# # # # # # # # # # # # # # # # !!!!Importante!!!! # # # # # # # # # # # # # # # #

# Gera os valores para as tabelas!!!
@app.route('/create', methods=['GET'])
def create_all():
    db.create_all()
    add_clientes_base()
    add_enderecos_base()
    add_chamado_base()
    return redirect('/')


# # # # # # # # # # # # # # # # Login # # # # # # # # # # # # # # # #

@app.route('/check', methods=['GET'])
def check_login():
    if current_user.is_authenticated:
        return redirect('/logout')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect('/profile')
            else:
                flash('Incorrect user or password')
                return redirect('/login')
        else:
            flash('Usuario não existe')
            return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        query = signup_user(request)
        if query:
            return redirect('/')
        else:
            return redirect('/signup')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')


# # # # # # # # # # # # # # # # Clientes # # # # # # # # # # # # # # # #

@app.route('/clientes', methods=['GET'])
@login_required
def show_cliente():
    content_type = request.headers.get('Content-Type')
    clientes = Clientes.query.all()
    result = clientes_schema.dump(clientes)
    if content_type == 'application/json':
        return jsonify(result=result)
    else:
        return render_template('clientes.html', data=result)


@app.route('/clientes/id=<int:cliente_id>', methods=['GET'])
@login_required
def show_cliente_by_id(cliente_id):
    content_type = request.headers.get('Content-Type')
    cliente = db.session.execute(db.select(Clientes).filter_by(id=cliente_id)).scalar_one()
    r = cliente_schema.dump(cliente)
    result = [r, ]
    if content_type == 'application/json':
        return jsonify(result=result)
    else:
        return render_template('clientes.html', data=result)


@app.route('/clientes/add', methods=['GET', 'POST'])
@login_required
def add_cliente():
    if request.method == 'GET':
        return render_template('add_cliente.html')
    else:
        add_new_cliente(request)
        return redirect('/clientes')


@app.route('/clientes/edit=<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def edit_clinete_id(cliente_id):
    cliente = db.session.execute(db.select(Clientes).filter_by(id=cliente_id)).scalar_one()
    if request.method == 'GET':
        return render_template('edit_cliente.html', cliente=cliente)
    else:
        edit_cliente(request, cliente)
        return redirect('/clientes')


@app.route('/clientes/delete=<int:cliente_id>', methods=['POST'])
@login_required
def delete_cliente(cliente_id):
    cliente = db.session.execute(db.select(Clientes).filter_by(id=cliente_id)).scalar_one()
    x = cliente_schema.dump(cliente)
    endereco_id = x['endereco']['id']
    db.session.delete(cliente)
    db.session.commit()
    endereco = db.session.execute(db.select(Enderecos).filter_by(id=endereco_id)).scalar_one()
    db.session.delete(endereco)
    db.session.commit()
    return redirect('/clientes')


# # # # # # # # # # # # # # # # Chamados # # # # # # # # # # # # # # # #

@app.route('/chamados/', methods=['GET'])
@login_required
def show_chamados():
    chamados = Chamados.query.all()
    content_type = request.headers.get('Content-Type')
    result = chamados_schema.dump(chamados)
    if content_type == 'application/json':
        return jsonify(result=result)
    else:
        return render_template('chamados.html', data=result)


@app.route('/chamados/id=<int:chamado_id>', methods=['GET', 'POST'])
@login_required
def show_chamado_by_id(chamado_id):
    content_type = request.headers.get('Content-Type')
    chamado = db.session.execute(db.select(Chamados).filter_by(id=chamado_id)).scalar_one()
    r = chamado_schema.dump(chamado)
    result = [r, ]
    if content_type == 'application/json':
        return jsonify(result=result)
    else:
        return render_template('chamados.html', data=result)


@app.route('/chamados/add', methods=['GET', 'POST'])
@login_required
def add_chamado():
    if request.method == 'GET':
        return render_template('add_chamado.html')
    else:
        add_new_chamado(request)
        return redirect('/chamados')


@app.route('/chamados/edit=<int:chamado_id>', methods=['GET', 'POST'])
@login_required
def edit_chamado_id(chamado_id):
    chamado = db.session.execute(db.select(Chamados).filter_by(id=chamado_id)).scalar_one()
    if request.method == 'GET':
        return render_template('edit_chamado.html', chamado=chamado)
    else:
        edit_chamado(request, chamado)
        return redirect('/chamados')


@app.route('/chamados/delete=<int:chamado_id>', methods=['POST'])
@login_required
def delete_chamado(chamado_id):
    chamado = db.session.execute(db.select(Chamados).filter_by(id=chamado_id)).scalar_one()
    db.session.delete(chamado)
    db.session.commit()
    return redirect('/chamados')


# # # # # # # # # # # # # # # # Gerais # # # # # # # # # # # # # # # #

@app.errorhandler(404)
def not_found(e):
    return redirect('/')


@app.route('/', methods=['GET'])
def home():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = None
    return render_template('home.html', user=user)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
