from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():

    app = Flask(__name__)

    # Chave secreta
    app.config['SECRET_KEY'] = 'clinica-secreta'

    # Configuração do banco
    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'clinica.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Login
    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    login_manager.login_message = "Faça login para acessar o sistema."

    # Filtro customizado para formatação de CPF
    @app.template_filter('format_cpf')
    def format_cpf(cpf):
        if not cpf:
            return '-'
        # Remove caracteres não numéricos
        cpf_limpo = ''.join(filter(str.isdigit, str(cpf)))
        # Formata como 000.000.000-00
        if len(cpf_limpo) == 11:
            return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"
        return cpf

    # Importar rotas
    from app.routes import (
        main_bp,
        pacientes_bp,
        profissionais_bp,
        consultas_bp,
        agendamentos_bp,
        acessos_bp
    )

    # Registrar rotas
    app.register_blueprint(main_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(profissionais_bp)
    app.register_blueprint(consultas_bp)
    app.register_blueprint(agendamentos_bp)
    app.register_blueprint(acessos_bp)

    # Importar modelo
    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Criar banco e rodar migrações
    with app.app_context():
        db.create_all()
        
        # Executar script de migração para garantir colunas novas
        try:
            from migrate_db import migrate
            migrate()
        except Exception as e:
            print(f"Erro ao rodar migração: {e}")

    return app