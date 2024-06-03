# API de Receitas e Despesas

Este projeto consiste em uma API desenvolvida em Python utilizando Flask, SQLAlchemy e MySQL, destinada a gerenciar receitas e despesas pessoais. A API permite aos usuários cadastrar, atualizar, remover e consultar suas transações financeiras de forma segura e eficiente.

## Funcionalidades

- **Cadastro de Receitas e Despesas**: Os usuários podem adicionar, editar e excluir informações de receitas e despesas.
- **Consulta de Transações**: Possibilidade de filtrar transações por data, tipo (receita ou despesa) e categoria.
- **Relatórios Financeiros**: Geração de relatórios de fluxo de caixa e resumo financeiro.
- **Autenticação e Controle de Acesso**: Acesso restrito a informações pessoais com autenticação de usuário.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **MySQL**: Sistema de gerenciamento de banco de dados.

## Requisitos e Observações

Para executar este projeto, você precisará ter Python e MySQL instalados em sua máquina.
Também será necessário cadastrar as roles de usuários.
Antes dos comandos abaixo crie no diretório raiz o arquivo '.env'
Execute primeiro: python -m venv env
Em seguida: pip install -r requirements.txt
Em seguida: Flask db migrate
Em seguida: Flask db upgrade
Roda esses comandos no banco: 
INSERT INTO role (id,name) VALUES (1,'admin');
INSERT INTO role (id,name) VALUES (2,'default');
Execute um POST nesse endpoint: http://127.0.0.1:5000/register
Com o body abaixo:
{
    "username": "admin",
    "password": "123"
}
Em seguida no Banco de dados execute: SELECT * FROM USER; 
Com isso altere o role_id do admin para 1.
Para usar os outros endpoints precisa-se estar logado inicialmente.

## Configuração Inicial

Antes de iniciar o servidor, é necessário configurar o banco de dados. As instruções para criação do banco de dados e tabelas estão disponíveis no script SQL anexo ao projeto.

## Autores

- João Pedro Rodrigues Tenório
- Parjasnelly Araújo Marques