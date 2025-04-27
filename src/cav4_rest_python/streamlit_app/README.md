# Streamlit OIDC (OpenID Connect)

Esta aplicação é um exemplo de como incorporar autenticação OIDC (OpenID Connect) em uma aplicação Streamlit, usando o fluxo de autorização padrão e decodificando informações do ID Token.

## Instalação

Instruções a serem executadas na raiz do projeto

1. Criar e ativar ambiente virtual

```bash
python3 -m .venv venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -e .
```

Ou instale manualmente as bibliotecas necessárias:

```bash
pip install streamlit authlib requests python-dotenv PyJWT
```

## Configuração

### Arquivo `.env`

Crie um arquivo `.env` na raiz do projeto para configurar o certificado CA:

```
REQUESTS_CA_BUNDLE=certs/ca-root.pem
```

### Arquivo `.streamlit/secrets.toml`

Configure as credenciais OIDC, certifique-se que a `base_url` (incluindo a porta) está cadastrada como url de redirecionamento para o seu client id:

```toml
[oidc]
client_id = "<seu-client-id>"
client_secret = "<seu-client-secret>"
issuer = "https://server.addr/.well-known/openid-configuration"
base_url = "http://localhost:8501"
```

### Arquivo `.streamlit/config.toml`

Configure as opções do Streamlit:

```toml
[browser]
gatherUsageStats = false
```

### Certificado

O arquivo `ca-root.pem` deve estar presente no diretório `/certs` do projeto para permitir a comunicação HTTPS com o provedor OIDC. Podemos modificar a localização se for conveniente.

## Fluxo de Autenticação

1. Usuário acessa a aplicação e clica em "Entrar"
2. Redirecionamento para o provedor OIDC
3. Após autenticação bem-sucedida, o usuário é redirecionado de volta com um código
4. A aplicação troca o código por tokens
5. As informações do usuário são extraídas do ID Token
6. A página exibe as informações do usuário e os tokens (em modo debug)

## Funcionalidades

- Autenticação via OIDC
- Exibição de informações do usuário do ID Token
- Tempo restante da sessão
- Modo debug para visualização dos tokens
- Botão de logout
- Suporte a certificado CA personalizado

## Estrutura do Projeto

```
projeto/
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
├── ca-root.pem
├── .env
├── pyproject.toml
├── README.md
└── streamlit-ca-login.py
```

## Execução

Para iniciar a aplicação:

```bash
streamlit run streamlit-ca-login.py
```

A aplicação estará disponível em `http://localhost:8501`.

## Limitações

- A sessão não persiste entre refreshes da página
- Nova autenticação é necessária após refresh
- Não implementa refresh token
- Não verifica assinatura do ID Token

## Segurança

Este é um exemplo básico e algumas verificações de segurança foram omitidas para simplificação:

- Verificação de assinatura do ID Token
- Validação de audiência
- Validação de emissor
- Proteção contra CSRF

Para uso em produção, considere implementar estas validações adicionais.

## Dependências

- Python ≥ 3.8
- streamlit ≥ 1.32.0
- authlib ≥ 1.3.0
- requests ≥ 2.31.0
- python-dotenv ≥ 1.0.0
- PyJWT ≥ 2.8.0

## Possíveis problemas

### Erro de Certificado

- Verifique se o certificado está no local correto
- Confirme se REQUESTS_CA_BUNDLE está configurado
- Verifique a validade do certificado

### Erro de Autenticação

- Confirme as credenciais em `.streamlit/secrets.toml`
- Confirme se a URL configurada como base_url em `.streamlit/secrets.toml` está registrada como `redirect_uri` para as suas credenciais
- Confirme se a aplicação está rodando na mesma porta que consta como base_url em `.streamlit/secrets.toml`
- Verifique os logs para mensagens de erro
- Confirme se o servidor de autorização está acessível

## Contribuição

Contribuições são bem-vindas!
