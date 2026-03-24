# 🏥 Sistema de Gestão de Clínica de Saúde Mental

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)  
[![Flask](https://img.shields.io/badge/Flask-Framework-black)](https://flask.palletsprojects.com/)  
[![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)](https://www.sqlite.org/)  

Sistema desenvolvido em **Python** utilizando **Flask** e **SQLite**, com o objetivo de gerenciar pacientes, profissionais, consultas e agendamentos de uma clínica de saúde mental.

---

## 📚 Sobre o Projeto

Este sistema foi desenvolvido como **projeto académico** para a disciplina de **Programação para Dispositivos Móveis (Android)**.

O objetivo do projeto é aplicar conceitos de desenvolvimento de sistemas, organização de rotas, base de dados e interface web utilizando **Python, Flask e SQLite**.

O projeto foi desenvolvido em **grupo** como parte das atividades da faculdade.

---

## 👨‍💻 Integrantes do Projeto

```
Gabriel Alves
GitHub: https://github.com/Gb7Alves
LinkedIn: https://www.linkedin.com/in/gabriel-alves-adm?utm_source=share_via&utm_content=profile&utm_medium=member_ios

Breno Araujo
GitHub: https://github.com/Oniugen
LinkedIn: https://www.linkedin.com/in/breno-araújo-ferreira-ab6232367?utm_source=share_via&utm_content=profile&utm_medium=member_ios

Yann Gustavo
GitHub: LINK_GITHUB
LinkedIn: https://www.linkedin.com/in/yanngustavoap?utm_source=share_via&utm_content=profile&utm_medium=member_ios

Samuel Oliveira
GitHub: LINK_GITHUB
LinkedIn: LINK_LINKEDIN
```

---

## 🌟 Funcionalidades

### Gerenciamento de Dados
- 🧑‍⚕️ **Cadastro de Pacientes**: Registo completo com dados pessoais, contacto de emergência e histórico médico
- 👩‍⚕️ **Cadastro de Profissionais**: Registo de profissionais com especialidade, consultório responsável e dados de contacto
- 📋 **Registo de Consultas**: Documentação de consultas realizadas com diagnóstico e prescrição
- 📅 **Agendamento de Consultas**: Sistema avançado de agendamento com reserva de salas por horário
- 🏢 **Gerenciamento de Consultórios**: Cadastro e organização de salas/consultórios

### Sistema de Agendamento Avançado
- ⏰ **Reserva de Salas por Horário**: Agendamentos com faixa horária inicial e final
- 🚫 **Validação de Conflitos**: Impede dupla reserva da mesma sala no mesmo horário
- 🔗 **Preenchimento Automático**: Dados do agendamento são automaticamente preenchidos na consulta
- 📝 **Campos Bloqueados**: Informações do agendamento aparecem como somente leitura na consulta

### Gerenciamento de Acessos
- 👤 **Controlo de Utilizadores**: Sistema de login e autenticação
- 🔐 **Edição de Perfil**: Utilizadores podem alterar nome e palavra-passe
- ✅ **Aprovação de Utilizadores**: Administrador aprova novos utilizadores
- 🔑 **Vinculação a Profissionais**: Utilizadores podem ser vinculados a profissionais específicos
- 🗑️ **Remoção de Acessos**: Funcionalidade para remover utilizadores do sistema.

### Interface e UX
- 🎨 **Design Responsivo**: Interface adaptável para diferentes tamanhos de ecrã
- 🖼️ **Imagem de Fundo**: Ecrã de login com imagem profissional de clínica
- 📱 **Layout Horizontal**: Botões de ações exibidos lado a lado (responsivo)
- 🦶 **Rodapé Fixo**: Rodapé permanece no final da página mesmo com pouco conteúdo
- 🔍 **Busca em Tempo Real**: Filtro de profissionais e utilizadores

---

## 🛠 Tecnologias

- **Backend**: Python 3.x, Flask
- **Base de Dados**: SQLite com SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Autenticação**: Flask-Login com hash de palavra-passe
- **Responsividade**: CSS Grid e Flexbox

---

## 🚀 Como Executar o Sistema

### Pré-requisitos
- Python 3.x instalado
- pip (gestor de pacotes Python)

### Instalação e Execução

```bash
# Clone o projeto
git clone https://github.com/Gb7Alves/clinica-saude-mental.git

# Entre na pasta do projeto
cd clinica-saude-mental/clinica-projeto

# Instale as dependências
pip install -r requirements.txt

# Execute o sistema
python run.py

# Abra no navegador
http://127.0.0.1:5000

# Para parar o sistema pressione CTRL + C
```

---

## 📂 Estrutura do Projeto

```
clinica-projeto/
├── app/
│   ├── __init__.py              # Inicialização da aplicação Flask
│   ├── models.py                # Modelos de dados (ORM)
│   ├── routes.py                # Rotas e lógica de negócio
│   ├── static/
│   │   ├── img/                 # Imagens (logótipo, fundo de login)
│   │   └── js/
│   │       └── masks.js         # Máscaras de entrada (CPF, telefone)
│   └── templates/
│       ├── base.html            # Template base
│       ├── login.html           # Página de login
│       ├── register.html        # Página de registo
│       ├── index.html           # Dashboard principal
│       ├── pacientes/           # Templates de pacientes
│       ├── profissionais/       # Templates de profissionais
│       ├── consultas/           # Templates de consultas
│       ├── agendamentos/        # Templates de agendamentos
│       └── acessos/             # Templates de gerenciamento de acessos
├── clinica.db                   # Base de dados SQLite
├── migrate_db.py                # Script de migração de base de dados
├── requirements.txt             # Dependências do projeto
├── run.py                       # Ficheiro principal para executar
└── README.md                    # Este ficheiro
```

---

## 📋 Modelos de Dados

### Paciente
- ID, Nome, CPF, Data de Nascimento, Telefone, Email
- Endereço, Histórico Médico, Estado Civil
- Contacto de Emergência

### Profissional
- ID, Nome, CPF, Especialidade, Especialidade Customizada
- Consultório Responsável, Telefone, Email
- Número de Registo, Estado Civil, Endereço
- Contacto de Emergência

### Consultório
- ID, Sala (identificador único), Descrição

### Agendamento
- ID, Paciente, Profissional, Consultório
- Data do Agendamento, Hora de Início, Hora de Término
- Status (Agendado, Realizado, Cancelado, Reagendado, Não Compareceu)
- Observações

### Consulta
- ID, Paciente, Profissional, Consultório
- Data da Consulta, Diagnóstico, Prescrição
- Observações, Data de Registo

### Utilizador
- ID, Nome, Email, Palavra-passe (hash), Profissional Vinculado
- Status (Ativo/Inativo), Data de Criação

---

## 🔐 Segurança

- **Autenticação**: Sistema de login com verificação de credenciais
- **Hash de Palavra-passe**: Palavras-passe armazenadas com hash seguro (werkzeug.security)
- **Proteção de Rotas**: Rotas protegidas com `@login_required`
- **Validação de Dados**: Validação de CPF, email e outros campos

---

## 📞 Suporte

Para dúvidas ou problemas, entre em contacto com os integrantes do projeto através dos links do GitHub.

---

## 📄 Licença

Este projeto é de uso académico e pode ser modificado livremente para fins educacionais.

---

**Desenvolvido para a Clínica de Saúde Mental**
