# OIDC e OAuth: Comparação e Implementação com Authlib em Python 3.12

## Visão Geral

### OAuth

**OAuth** é um **framework de autorização** que permite que aplicações de terceiros
obtenham acesso limitado e controlado a recursos HTTP de um serviço por um usuário.

**Versões:**

- **OAuth 1.0 (2007)**: Usava assinaturas complexas e falhava com aplicações nativas/móveis. **Ficou obsoleto**.
- **OAuth 2.0 (2012)**: Simplificado, usando tokens de acesso (geralmente JWT) e HTTPS para segurança

### OIDC (OpenID Connect)

**OIDC** é uma **camada de identidade** construída sobre OAuth 2.0 que adiciona autenticação, fornecendo informações sobre o usuário final.

## Principais Diferenças

| Característica | OAuth 2.0          | OIDC                                |
| -------------- | ------------------ | ----------------------------------- |
| Propósito      | Autorização        | Autenticação + Autorização          |
| Tokens         | Access Token       | ID Token (JWT) + Access Token       |
| User Info      | Não padrão         | Endpoint /userinfo padrão           |
| Fluxos         | Vários grant types | Extensão do Authorization Code Flow |

## Implementação com Authlib em Python 3.12

O [Authlib](https://authlib.org/) é uma biblioteca moderna para OAuth/OIDC em
Python, com suporte para:

- Clientes OAuth 1/2 e OIDC
- Servidores OAuth 2 e OIDC
- JWT (JSON Web Tokens)
- Integração com Flask, Starlette, FastAPI e Streamlit

### Vantagens do Authlib

1. **Suporte atualizado**: Compatível com Python 3.12 e padrões recentes
2. **Abordagem abrangente**: Oferece tanto client quanto server implementations
3. **Flexível**: Pode ser usado com vários frameworks web
4. **Seguro**: Implementa práticas recomendadas de segurança

### Desvantagens

1. **Curva de aprendizado**: Documentação pode ser desafiadora para iniciantes
2. **Menos exemplos**: Comparado a bibliotecas mais antigas como python-oauth2

## Exemplo de Servidor OAuth 2/OIDC com Authlib

```python
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from flask import Flask

app = Flask(__name__)
app.secret_key = 'segredo'

# Configuração mínima do servidor OAuth2
server = AuthorizationServer()
server.init_app(app)

# Implementação de um grant type (Authorization Code)
class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def authenticate_user(self, credentials):
        # Lógica de autenticação do usuário
        pass

# Registrar grant types
server.register_grant(AuthorizationCodeGrant)

# Para OIDC, adicionar:
from authlib.integrations.flask_oauth2 import OpenIDConnect
oidc = OpenIDConnect(app)
```

## Exemplo de Cliente OAuth 2/OIDC

```python
from authlib.integrations.requests_client import OAuth2Session

client = OAuth2Session(
    client_id='seu_client_id',
    client_secret='seu_secret',
    scope='openid email profile'
)

# Para OIDC
uri, state = client.create_authorization_url(
    'https://servidor/authorize',
    nonce='random_nonce'  # Necessário para OIDC
)

# Após redirecionamento
token = client.fetch_token(
    'https://servidor/token',
    authorization_response=request.url
)

# Obter informações do usuário (OIDC)
if 'id_token' in token:
    userinfo = client.parse_id_token(token)
else:
    userinfo = client.get('https://servidor/userinfo').json()
```

## Considerações de Segurança

1. **OAuth 2.0**: Sempre use HTTPS, valide escopos, proteja contra CSRF
2. **OIDC**: Valide nonce, iss (issuer), aud (audience) e exp (expiration)
3. **Authlib**: Oferece validadores embutidos para muitas dessas verificações

## Conclusão

Para Python 3.12, o Authlib é uma excelente escolha para implementar tanto servidores
quanto clientes OAuth 2.0 e OIDC. Ele oferece:

- Suporte moderno para os protocolos mais recentes
- Boa integração com ecossistema Python
- Implementações seguras por padrão

Para projetos que precisam apenas de OAuth 2.0 sem autenticação, a implementação será mais
simples. Para sistemas que requerem autenticação (login), OIDC é a escolha mais robusta.
