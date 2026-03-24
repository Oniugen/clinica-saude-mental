from app import db
from datetime import datetime
from flask_login import UserMixin


class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    endereco = db.Column(db.String(300), nullable=True)
    historico_medico = db.Column(db.Text, nullable=True)
    estado_civil = db.Column(db.String(50), nullable=True)
    nome_contato_emergencia = db.Column(db.String(150), nullable=True)
    telefone_contato_emergencia = db.Column(db.String(20), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    consultas = db.relationship('Consulta', backref='paciente', lazy=True, cascade='all, delete-orphan')
    agendamentos = db.relationship('Agendamento', backref='paciente', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Paciente {self.nome}>'


class Profissional(db.Model):
    __tablename__ = 'profissionais'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    especialidade = db.Column(db.String(100), nullable=False)
    especialidade_customizada = db.Column(db.String(100), nullable=True)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    numero_registro = db.Column(db.String(50), nullable=True)
    estado_civil = db.Column(db.String(50), nullable=True)
    endereco = db.Column(db.String(300), nullable=True)
    nome_contato_emergencia = db.Column(db.String(150), nullable=True)
    telefone_contato_emergencia = db.Column(db.String(20), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    consultas = db.relationship('Consulta', backref='profissional', lazy=True, cascade='all, delete-orphan')
    agendamentos = db.relationship('Agendamento', backref='profissional', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Profissional {self.nome}>'


class Consultorio(db.Model):
    __tablename__ = 'consultorios'

    id = db.Column(db.Integer, primary_key=True)
    sala = db.Column(db.String(20), nullable=False, unique=True)
    descricao = db.Column(db.String(200), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Consultorio {self.sala}>'


class Consulta(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    consultorio_id = db.Column(db.Integer, db.ForeignKey('consultorios.id'), nullable=True)

    data_consulta = db.Column(db.DateTime, nullable=False)

    diagnostico = db.Column(db.Text, nullable=True)
    prescricao = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    data_registro = db.Column(db.DateTime, default=datetime.utcnow)
    consultorio_sala = db.Column(db.String(50), nullable=True)

    consultorio = db.relationship('Consultorio')

    def __repr__(self):
        return f'<Consulta {self.id}>'


class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=False)
    consultorio_id = db.Column(db.Integer, db.ForeignKey('consultorios.id'), nullable=True)

    data_agendamento = db.Column(db.DateTime, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=True)
    hora_fim = db.Column(db.Time, nullable=True)

    status = db.Column(db.String(50), default='Agendado')
    observacoes = db.Column(db.Text, nullable=True)

    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    consultorio_sala = db.Column(db.String(50), nullable=True)

    consultorio = db.relationship('Consultorio')

    def __repr__(self):
        return f'<Agendamento {self.id}>'


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    profissional_id = db.Column(db.Integer, db.ForeignKey('profissionais.id'), nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento
    profissional = db.relationship('Profissional', backref='usuarios')

    def __repr__(self):
        return f'<Usuario {self.email}>'