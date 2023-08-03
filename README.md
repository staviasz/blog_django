# Documentação da Aplicação Full-Stack de Blog em Django

Esta documentação descreve uma aplicação full-stack de blog desenvolvida em Django. O projeto inclui recursos para criar, visualizar e gerenciar postagens de blog, juntamente com recursos de segurança e formatação de texto. A aplicação é composta por uma parte backend (servidor Django) e uma parte frontend (interface do usuário).

## Requisitos

- Django
- psycopg2-binary
- Pillow
- django-summernote
- python-dotenv
- django-axes

## Funcionalidades

1. Criação e gerenciamento de postagens de blog.
2. Formatação de texto avançada usando o editor WYSIWYG django-summernote.
3. Segurança aprimorada usando django-axes para proteção contra ataques de força bruta.

## Configuração

1. Clone este repositório para o seu ambiente local.
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate
   
### Instalação das Dependências

Para instalar as dependências do projeto, utilize o seguinte comando:
    ```bash
    pip install -r requirements.tx
    ```
### Configuração do Ambiente

Crie um arquivo .env na pasta raiz do projeto.
  Configure as variáveis de ambiente necessárias, como as configurações do banco de dados e as chaves secretas.

### Uso

  Execute as migrações do banco de dados:
    ```bash
      python manage.py migrate
      ```
      
  Inicie o servidor de desenvolvimento:
    ```bash
    python manage.py runserver
    ```

  Acesse a aplicação em seu navegador através do seguinte link: http://localhost:8000.


### Licença
  Desenvolvido por Erick Staviasz no curso de Django ministrado por Otávio Miranda.


### Recursos Adicionais
- Django Documentação Oficial
- django-summernote Documentação
- django-axes Documentação


    
    
