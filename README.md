# 🏦 Sistema Bancário com API

<p align="center">
  <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/andersondev96/bank-python-api?color=blue">
  <img alt="Repository size" src="https://img.shields.io/github/repo-size/andersondev96/bank-python-api">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-brightgreen">
   <a href="https://www.linkedin.com/in/anderson-fernandes96/">
      <img alt="Feito por Anderson" src="https://img.shields.io/badge/feito%20por-Anderson%20Fernandes-blue">
   </a>
</p>

<p align="center">
  <b>API REST robusta para gestão de contas de Pessoa Física e Jurídica, implementando regras de negócio bancárias, testes automatizados e persistência de dados.</b>
</p>

<p align="center">
  <a href="#-sobre-o-projeto">Sobre</a> •
  <a href="#-features">Features</a> •
  <a href="#-tecnologias">Tecnologias</a> •
  <a href="#-instalação-e-execução">Instalação</a> •
  <a href="#-documentação-da-api">Documentação</a> •
  <a href="#-autor">Autor</a>
</p>

---

## 📄 Sobre o projeto

O projeto consiste em uma **API para sistema bancário**, estruturada no padrão **MVC**. O objetivo principal é simular operações financeiras reais, garantindo a integridade dos dados e a aplicação de regras de negócio específicas para diferentes tipos de clientes.

Além das operações básicas, o projeto foca em qualidade de código através de **testes unitários** e integração com banco de dados **SQLite**, exercitando o ciclo completo de desenvolvimento de software backend.

## ✨ Features

- [x] 👥 **Gestão de Usuários:** Criação e listagem de clientes (PF e PJ).
- [x] 🏦 **Operações Bancárias:** Interface de cliente com métodos para Saque e Extrato.
- [x] 🛡️ **Regras de Negócio:** Limites de saque diferenciados por tipo de pessoa (Física/Jurídica).
- [x] 🗄️ **Persistência:** Conexão e manipulação de dados via SQLite.
- [x] 🧪 **Qualidade:** Controllers cobertos por testes unitários.

## 🚀 Tecnologias utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

[![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=for-the-badge)](https://docs.python.org/3)
[![Flask Badge](https://img.shields.io/badge/Flask-3BABC3?logo=flask&logoColor=fff&style=for-the-badge)](https://flask.palletsprojects.com/en/stable)
[![SQLAlchemy Badge](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=fff&style=for-the-badge)](https://www.sqlalchemy.org)
[![Pytest Badge](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=fff&style=for-the-badge)](https://docs.pytest.org/en/stable)
[![SQLite Badge](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=fff&style=for-the-badge)](https://sqlite.org/docs.html)

## ⚙️ Instalação e Execuação

### Pré-requisitos
Antes de começar, você vai precisar ter instalado em sua máquina o [Python 3.10+](https://www.python.org/downloads/).

### Passos para rodar localmente
```bash
# 1. Clone o repositório
$ git clone https://github.com/andersondev96/bank-python-api.py

# 2. Acesse a pasta do projeto no terminal/cmd
$ cd bank-python-api

# 3. Crie e ative o ambiente virtual
$ python -m venv venv
$ source venv/bin/activate  # Linux/macOS
$ venv\Scripts\activate     # Windows

# 4. Instale as dependências
$ pip install -r requirements.txt

# 5. Configure o Banco de Dados
# Execute o script 'schema.sql' no seu gerenciador de banco de dados preferido
# ou via linha de comando para criar as tabelas e popular os dados iniciais.

# 6. Execute a aplicação
python run.py
```

A API estará disponível na porta `3000`. Acesse: `http://localhost:3000`

## 📄 Documentação da API
### Endpoints principais
| Método | Endpoint | Descrição |
|:------:|-----------|-----------|
| `POST` | `/pessoa-fisica` | Cria uma nova pessoa física |
| `GET` | `/pessoa-fisica/<id>` | Retorna uma pessoa física específica |
| `POST` | `/pessoa-fisica/<id>/sacar` | Realiza um saque em uma pessoa física |
| `GET` | `/pessoa-fisica/<id>/extrato` | Retorna o extrato de uma pessoa física |
| `POST` | `/pessoa-juridica` | Cria uma nova pessoa jurídica
| `GET` | `/pessoa-juridica/<id>` | Retorna uma pessoa jurídica específica |
| `POST` | `/pessoa-juridica/<id>/sacar` | Realiza um saque em uma pessoa jurídica |
| `GET` | `/pessoa-juridica/<id>/extrato` | Retorna o extrato de uma pessoa jurídica |

### Exemplo de requisição (POST `/pessoa-fisica`)
```json
{
    "renda_mensal": 2000.0,
    "idade": 28,
    "nome_completo": "Maria da Silva",
    "celular": "9999-8888",
    "email": "joao@example.com",
    "categoria": "Categoria A",
    "saldo": 4000.0
}
```

### Exemplo de Resposta (201 Created)
```json
{
    "message": "Criação de Pessoa Física realizada com sucesso",
    "success": true
}
```

Teste as requisições utilizando o [**Insomnia**](https://insomnia.rest) ou  [**Postman**](https://www.postman.com).

[![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)](bank_postman_collection.json)

## 🧪 Testes
Execute a suíte de testes com pytest:
```
pytest -S -v
```

Os testes validam as regras de negócio de saque, criação de contas e integridade dos dados.

## 🤝 Como contribuir
1. Fork este repositório

2. Crie uma branch para sua funcionalidade:
    ```sh
    git checkout -b minha-feature
    ```

3. Realize suas alterações e comite:
    ```sh
    git commit -m "feature: Minha nova funcionalidade"
    ```

4. Envie para o repositório remoto:
    ```sh
    git push origin minha-feature
    ```

5. Abra um **Pull Request**!


## 📝 Licença
Este projeto está sob a licença [LICENSE](LICENSE).

## 👥 Autor

<div style="display:flex; flex-direction:column; align-items: center;">

<a href="https://www.linkedin.com/in/anderson-fernandes96/">
<img src="https://avatars.githubusercontent.com/u/49786548?v=4" width="64" style="border: 2px solid blue; border-radius: 50px" />
</a>

**Anderson Fernandes Ferreira**

[![Instagram](https://img.shields.io/badge/-Instagram-%23E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com/anderson_ff13)
[![Gmail](https://img.shields.io/badge/-Gmail-%23333?style=for-the-badge&logo=gmail&logoColor=white)](mailto:andersonfferreira96@gmail.com.br)
[![LinkedIn](https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/anderson-fernandes96/)


