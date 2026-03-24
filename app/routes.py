from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager
from app.models import Usuario, Paciente, Profissional, Consultorio, Agendamento, Consulta
from datetime import datetime, date, time, timedelta
import os

# ==================== BLUEPRINTS ====================

from flask import Blueprint

main_bp = Blueprint('main', __name__)
pacientes_bp = Blueprint('pacientes', __name__, url_prefix='/pacientes')
profissionais_bp = Blueprint('profissionais', __name__, url_prefix='/profissionais')
consultas_bp = Blueprint('consultas', __name__, url_prefix='/consultas')
agendamentos_bp = Blueprint('agendamentos', __name__, url_prefix='/agendamentos')
acessos_bp = Blueprint('acessos', __name__, url_prefix='/acessos')

# ==================== AUTENTICACAO ====================

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('main.index'))
        else:
            flash('Email ou senha incorretos!', 'danger')

    return render_template('login.html')


@main_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        profissional_id = request.form.get('profissional_id')

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Email já cadastrado!', 'danger')
        else:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha=generate_password_hash(senha),
                profissional_id=profissional_id or None
            )
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('main.login'))

    profissionais = Profissional.query.all()
    return render_template('register.html', profissionais=profissionais)


@main_bp.route('/logout')
@login_required
def logout():

    logout_user()
    return redirect(url_for('main.login'))


# ==================== TELA INICIAL ====================

@main_bp.route('/')
@login_required
def index():

    total_pacientes = Paciente.query.count()
    total_profissionais = Profissional.query.count()
    total_consultas = Consulta.query.count()

    try:
        agendamentos_proximos = Agendamento.query.filter(
            Agendamento.status == 'Agendado',
            Agendamento.data_agendamento >= datetime.now()
        ).count()
    except:
        # Fallback caso as novas colunas nao existam no banco do usuario
        agendamentos_proximos = 0

    # Verificar se uma data foi selecionada via GET
    data_selecionada_str = request.args.get('data')
    hoje = date.today()
    
    if data_selecionada_str:
        try:
            data_selecionada = datetime.strptime(data_selecionada_str, '%Y-%m-%d').date()
        except:
            data_selecionada = hoje
    else:
        data_selecionada = hoje
    
    # Agendamentos do dia selecionado
    inicio_dia = datetime.combine(data_selecionada, time.min)
    fim_dia = datetime.combine(data_selecionada, time.max)

    agendamentos_dia = Agendamento.query.filter(
        Agendamento.data_agendamento >= inicio_dia,
        Agendamento.data_agendamento <= fim_dia
    ).order_by(Agendamento.data_agendamento).all()

    return render_template(
        'index.html',
        total_pacientes=total_pacientes,
        total_profissionais=total_profissionais,
        total_consultas=total_consultas,
        agendamentos_proximos=agendamentos_proximos,
        agendamentos_dia=agendamentos_dia,
        data_selecionada=data_selecionada.strftime('%Y-%m-%d'),
        data_hoje=hoje.strftime('%Y-%m-%d')
    )


# ==================== PACIENTES ====================

@pacientes_bp.route('/')
@login_required
def listar_pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes/listar.html', pacientes=pacientes)


@pacientes_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_paciente():

    if request.method == 'POST':

        try:

            novo_paciente = Paciente(
                nome=request.form['nome'],
                cpf=request.form['cpf'],
                data_nascimento=datetime.strptime(
                    request.form['data_nascimento'], '%Y-%m-%d'
                ),
                estado_civil=request.form.get('estado_civil'),
                telefone=request.form['telefone'],
                email=request.form.get('email'),
                endereco=request.form.get('endereco'),
                nome_contato_emergencia=request.form.get('nome_contato_emergencia'),
                telefone_contato_emergencia=request.form.get('telefone_contato_emergencia'),
                historico_medico=request.form.get('historico_medico')
            )

            db.session.add(novo_paciente)
            db.session.commit()

            flash('Paciente criado!', 'success')

            return redirect(url_for('pacientes.listar_pacientes'))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('pacientes/novo.html')


@pacientes_bp.route('/<int:id>')
@login_required
def ver_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    consultas = Consulta.query.filter_by(paciente_id=id).all()
    agendamentos = Agendamento.query.filter_by(paciente_id=id).all()

    return render_template(
        'pacientes/ver.html',
        paciente=paciente,
        consultas=consultas,
        agendamentos=agendamentos
    )


@pacientes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    if request.method == 'POST':

        try:

            paciente.nome = request.form['nome']
            paciente.cpf = request.form['cpf']
            paciente.data_nascimento = datetime.strptime(
                request.form['data_nascimento'], '%Y-%m-%d'
            )
            paciente.estado_civil = request.form.get('estado_civil')
            paciente.telefone = request.form['telefone']
            paciente.email = request.form.get('email')
            paciente.endereco = request.form.get('endereco')
            paciente.nome_contato_emergencia = request.form.get('nome_contato_emergencia')
            paciente.telefone_contato_emergencia = request.form.get('telefone_contato_emergencia')
            paciente.historico_medico = request.form.get('historico_medico')

            db.session.commit()

            flash('Paciente atualizado!', 'success')

            return redirect(url_for('pacientes.ver_paciente', id=id))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('pacientes/editar.html', paciente=paciente)


@pacientes_bp.route('/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_paciente(id):

    paciente = Paciente.query.get_or_404(id)

    try:

        db.session.delete(paciente)
        db.session.commit()

        flash('Paciente deletado!', 'success')

    except Exception as e:

        db.session.rollback()
        flash(f'Erro: {str(e)}', 'danger')

    return redirect(url_for('pacientes.listar_pacientes'))


# ==================== PROFISSIONAIS ====================

@profissionais_bp.route('/')
@login_required
def listar_profissionais():
    profissionais = Profissional.query.all()
    return render_template('profissionais/listar.html', profissionais=profissionais)


@profissionais_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_profissional():

    if request.method == 'POST':

        try:

            novo_profissional = Profissional(
                nome=request.form['nome'],
                cpf=request.form['cpf'],
                especialidade=request.form['especialidade'],
                especialidade_customizada=request.form.get('especialidade_customizada'),
                estado_civil=request.form.get('estado_civil'),
                telefone=request.form['telefone'],
                email=request.form.get('email'),
                numero_registro=request.form.get('numero_registro'),
                endereco=request.form.get('endereco'),
                nome_contato_emergencia=request.form.get('nome_contato_emergencia'),
                telefone_contato_emergencia=request.form.get('telefone_contato_emergencia')
            )

            db.session.add(novo_profissional)
            db.session.commit()

            flash('Profissional criado!', 'success')

            return redirect(url_for('profissionais.listar_profissionais'))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('profissionais/novo.html')


@profissionais_bp.route('/<int:id>')
@login_required
def ver_profissional(id):

    profissional = Profissional.query.get_or_404(id)

    consultas = Consulta.query.filter_by(profissional_id=id).all()
    agendamentos = Agendamento.query.filter_by(profissional_id=id).all()

    return render_template(
        'profissionais/ver.html',
        profissional=profissional,
        consultas=consultas,
        agendamentos=agendamentos
    )


@profissionais_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_profissional(id):

    profissional = Profissional.query.get_or_404(id)

    if request.method == 'POST':

        try:

            profissional.nome = request.form['nome']
            profissional.cpf = request.form['cpf']
            profissional.especialidade = request.form['especialidade']
            profissional.especialidade_customizada = request.form.get('especialidade_customizada')
            profissional.estado_civil = request.form.get('estado_civil')
            profissional.telefone = request.form['telefone']
            profissional.email = request.form.get('email')
            profissional.numero_registro = request.form.get('numero_registro')
            profissional.endereco = request.form.get('endereco')
            profissional.nome_contato_emergencia = request.form.get('nome_contato_emergencia')
            profissional.telefone_contato_emergencia = request.form.get('telefone_contato_emergencia')

            db.session.commit()

            flash('Profissional atualizado!', 'success')

            return redirect(url_for('profissionais.ver_profissional', id=id))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('profissionais/editar.html', profissional=profissional)


@profissionais_bp.route('/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_profissional(id):

    profissional = Profissional.query.get_or_404(id)

    try:

        db.session.delete(profissional)
        db.session.commit()

        flash('Profissional deletado!', 'success')

    except Exception as e:

        db.session.rollback()
        flash(f'Erro: {str(e)}', 'danger')

    return redirect(url_for('profissionais.listar_profissionais'))


# ==================== CONSULTAS ====================

@consultas_bp.route('/')
@login_required
def listar_consultas():
    consultas = Consulta.query.all()
    return render_template('consultas/listar.html', consultas=consultas)


@consultas_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def nova_consulta():

    if request.method == 'POST':

        try:

            consulta = Consulta(
                paciente_id=request.form['paciente_id'],
                profissional_id=request.form['profissional_id'],
                consultorio_id=request.form.get('consultorio_id') or None,
                consultorio_sala=request.form.get('consultorio_sala'),
                data_consulta=datetime.strptime(
                    request.form['data_consulta'], '%Y-%m-%dT%H:%M'
                ),
                diagnostico=request.form.get('diagnostico'),
                prescricao=request.form.get('prescricao'),
                observacoes=request.form.get('observacoes')
            )

            db.session.add(consulta)
            db.session.commit()

            flash('Consulta registrada!', 'success')

            return redirect(url_for('consultas.listar_consultas'))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    pacientes = Paciente.query.all()
    profissionais = Profissional.query.all()
    consultorios = Consultorio.query.all()

    # Parâmetros de preenchimento automático a partir do dashboard
    paciente_id_pre = request.args.get('paciente_id')
    profissional_id_pre = request.args.get('profissional_id')
    consultorio_sala_pre = request.args.get('consultorio_sala')
    data_agendamento_pre = request.args.get('data_agendamento')
    
    # Buscar nomes dos registros pré-preenchidos
    paciente_nome = None
    profissional_nome = None
    
    if paciente_id_pre:
        try:
            paciente = Paciente.query.get(paciente_id_pre)
            paciente_nome = paciente.nome if paciente else "Paciente não encontrado"
        except:
            paciente_nome = "Erro ao buscar paciente"
    
    if profissional_id_pre:
        try:
            profissional = Profissional.query.get(profissional_id_pre)
            profissional_nome = profissional.nome if profissional else "Profissional não encontrado"
        except:
            profissional_nome = "Erro ao buscar profissional"

    return render_template(
        'consultas/nova.html',
        pacientes=pacientes,
        profissionais=profissionais,
        consultorios=consultorios,
        paciente_id_pre=paciente_id_pre,
        profissional_id_pre=profissional_id_pre,
        consultorio_sala_pre=consultorio_sala_pre,
        data_agendamento_pre=data_agendamento_pre,
        paciente_nome=paciente_nome,
        profissional_nome=profissional_nome
    )


@consultas_bp.route('/<int:id>')
@login_required
def ver_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    return render_template('consultas/ver.html', consulta=consulta)


@consultas_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    if request.method == 'POST':

        try:

            consulta.paciente_id = request.form['paciente_id']
            consulta.profissional_id = request.form['profissional_id']
            consulta.consultorio_id = request.form.get('consultorio_id') or None
            consulta.consultorio_sala = request.form.get('consultorio_sala')
            consulta.data_consulta = datetime.strptime(
                request.form['data_consulta'], '%Y-%m-%dT%H:%M'
            )
            consulta.diagnostico = request.form.get('diagnostico')
            consulta.prescricao = request.form.get('prescricao')
            consulta.observacoes = request.form.get('observacoes')

            db.session.commit()

            flash('Consulta atualizada!', 'success')

            return redirect(url_for('consultas.ver_consulta', id=id))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    pacientes = Paciente.query.all()
    profissionais = Profissional.query.all()
    consultorios = Consultorio.query.all()

    return render_template(
        'consultas/editar.html',
        consulta=consulta,
        pacientes=pacientes,
        profissionais=profissionais,
        consultorios=consultorios
    )


@consultas_bp.route('/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_consulta(id):

    consulta = Consulta.query.get_or_404(id)

    try:

        db.session.delete(consulta)
        db.session.commit()

        flash('Consulta deletada!', 'success')

    except Exception as e:

        db.session.rollback()
        flash(f'Erro: {str(e)}', 'danger')

    return redirect(url_for('consultas.listar_consultas'))


# ==================== AGENDAMENTOS ====================

@agendamentos_bp.route('/')
@login_required
def listar_agendamentos():
    agendamentos = Agendamento.query.all()
    return render_template('agendamentos/listar.html', agendamentos=agendamentos)


@agendamentos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_agendamento():

    if request.method == 'POST':

        try:

            data_agendamento = datetime.strptime(
                request.form['data_agendamento'], '%Y-%m-%d'
            )

            hora_inicio = datetime.strptime(
                request.form['hora_inicio'], '%H:%M'
            ).time()

            hora_fim = datetime.strptime(
                request.form['hora_fim'], '%H:%M'
            ).time()

            consultorio_id = request.form.get('consultorio_id')
            consultorio_sala = request.form.get('consultorio_sala')

            # Validar se hora_fim eh posterior a hora_inicio
            if hora_fim <= hora_inicio:
                flash('A hora de termino deve ser posterior a hora de inicio!', 'danger')
                pacientes = Paciente.query.all()
                profissionais = Profissional.query.all()
                consultorios = Consultorio.query.all()
                return render_template(
                    'agendamentos/novo.html',
                    pacientes=pacientes,
                    profissionais=profissionais,
                    consultorios=consultorios
                )
            
            # Verificar conflitos de agendamento na mesma sala
            consultorio_id_num = request.form.get('consultorio_id')
            if consultorio_id_num:
                conflitos = Agendamento.query.filter(
                    Agendamento.consultorio_id == consultorio_id_num,
                    Agendamento.data_agendamento.cast(db.Date) == data_agendamento.date(),
                    Agendamento.status.in_(['Agendado', 'Realizado'])
                ).all()
                
                for agend in conflitos:
                    if agend.hora_inicio and agend.hora_fim:
                        # Verificar se ha sobreposicao de horarios
                        if not (hora_fim <= agend.hora_inicio or hora_inicio >= agend.hora_fim):
                            flash('Ja existe um agendamento nesta sala no horario selecionado!', 'danger')
                            pacientes = Paciente.query.all()
                            profissionais = Profissional.query.all()
                            consultorios = Consultorio.query.all()
                            return render_template(
                                'agendamentos/novo.html',
                                pacientes=pacientes,
                                profissionais=profissionais,
                                consultorios=consultorios
                            )

            agendamento = Agendamento(
                paciente_id=request.form['paciente_id'],
                profissional_id=request.form['profissional_id'],
                consultorio_id=consultorio_id,
                consultorio_sala=consultorio_sala,
                data_agendamento=data_agendamento,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                status=request.form.get('status', 'Agendado'),
                observacoes=request.form.get('observacoes')
            )

            db.session.add(agendamento)
            db.session.commit()

            flash('Agendamento criado!', 'success')

            return redirect(url_for('agendamentos.listar_agendamentos'))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    pacientes = Paciente.query.all()
    profissionais = Profissional.query.all()
    consultorios = Consultorio.query.all()

    return render_template(
        'agendamentos/novo.html',
        pacientes=pacientes,
        profissionais=profissionais,
        consultorios=consultorios
    )


@agendamentos_bp.route('/<int:id>')
@login_required
def ver_agendamento(id):

    agendamento = Agendamento.query.get_or_404(id)

    return render_template('agendamentos/ver.html', agendamento=agendamento)


@agendamentos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_agendamento(id):

    agendamento = Agendamento.query.get_or_404(id)

    if request.method == 'POST':

        try:

            data_agendamento = datetime.strptime(
                request.form['data_agendamento'], '%Y-%m-%d'
            )

            hora_inicio = datetime.strptime(
                request.form['hora_inicio'], '%H:%M'
            ).time()

            hora_fim = datetime.strptime(
                request.form['hora_fim'], '%H:%M'
            ).time()

            consultorio_id = request.form.get('consultorio_id')

            # Validar se hora_fim eh posterior a hora_inicio
            if hora_fim <= hora_inicio:
                flash('A hora de termino deve ser posterior a hora de inicio!', 'danger')
                pacientes = Paciente.query.all()
                profissionais = Profissional.query.all()
                consultorios = Consultorio.query.all()
                return render_template(
                    'agendamentos/editar.html',
                    agendamento=agendamento,
                    pacientes=pacientes,
                    profissionais=profissionais,
                    consultorios=consultorios
                )

            agendamento.paciente_id = request.form['paciente_id']
            agendamento.profissional_id = request.form['profissional_id']
            agendamento.consultorio_id = consultorio_id
            agendamento.consultorio_sala = request.form.get('consultorio_sala')
            agendamento.data_agendamento = data_agendamento
            agendamento.hora_inicio = hora_inicio
            agendamento.hora_fim = hora_fim
            agendamento.status = request.form.get('status')
            agendamento.observacoes = request.form.get('observacoes')

            db.session.commit()

            flash('Agendamento atualizado!', 'success')

            return redirect(url_for('agendamentos.ver_agendamento', id=id))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    pacientes = Paciente.query.all()
    profissionais = Profissional.query.all()
    consultorios = Consultorio.query.all()

    return render_template(
        'agendamentos/editar.html',
        agendamento=agendamento,
        pacientes=pacientes,
        profissionais=profissionais,
        consultorios=consultorios
    )


@agendamentos_bp.route('/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_agendamento(id):

    agendamento = Agendamento.query.get_or_404(id)

    try:

        db.session.delete(agendamento)
        db.session.commit()

        flash('Agendamento deletado!', 'success')

    except Exception as e:

        db.session.rollback()
        flash(f'Erro: {str(e)}', 'danger')

    return redirect(url_for('agendamentos.listar_agendamentos'))


# ==================== ACESSOS ====================

@acessos_bp.route('/')
@login_required
def listar_acessos():
    usuarios = Usuario.query.all()
    return render_template('acessos/listar.html', usuarios=usuarios)


@acessos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_acesso(id):

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':

        try:

            usuario.nome = request.form['nome']
            usuario.email = request.form['email']
            usuario.profissional_id = request.form.get('profissional_id') or None

            db.session.commit()

            flash('Acesso atualizado!', 'success')

            return redirect(url_for('acessos.listar_acessos'))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    profissionais = Profissional.query.all()

    return render_template('acessos/editar.html', usuario=usuario, profissionais=profissionais)


@acessos_bp.route('/<int:id>/deletar', methods=['POST'])
@login_required
def deletar_acesso(id):

    usuario = Usuario.query.get_or_404(id)

    try:

        db.session.delete(usuario)
        db.session.commit()

        flash('Acesso removido!', 'success')

    except Exception as e:

        db.session.rollback()
        flash(f'Erro: {str(e)}', 'danger')

    return redirect(url_for('acessos.listar_acessos'))


@acessos_bp.route('/<int:id>/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha(id):

    usuario = Usuario.query.get_or_404(id)

    if request.method == 'POST':

        try:

            senha_atual = request.form['senha_atual']
            nova_senha = request.form['nova_senha']
            confirmar_senha = request.form['confirmar_senha']

            if not check_password_hash(usuario.senha, senha_atual):
                flash('Senha atual incorreta!', 'danger')
            elif nova_senha != confirmar_senha:
                flash('Novas senhas não conferem!', 'danger')
            else:
                usuario.senha = generate_password_hash(nova_senha)
                db.session.commit()
                flash('Senha alterada com sucesso!', 'success')
                return redirect(url_for('acessos.listar_acessos'))

        except Exception as e:

            db.session.rollback()
            flash(f'Erro: {str(e)}', 'danger')

    return render_template('acessos/alterar_senha.html', usuario=usuario)
