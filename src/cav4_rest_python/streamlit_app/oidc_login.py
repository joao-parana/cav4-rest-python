import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import requests
import secrets
import time
import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Login OIDC",
    page_icon="🔒",
    initial_sidebar_state="collapsed",
)

# Configurações do OIDC
OIDC_CONFIG = {
    'client_id': st.secrets['oidc']['client_id'],
    'client_secret': st.secrets['oidc']['client_secret'],
    'issuer': st.secrets['oidc']['issuer'],
    'redirect_uri': f"{st.secrets['oidc']['base_url']}",
    'scope': ['openid', 'profile']
}

@st.cache_resource
def get_oidc_config():
    """Obtém a configuração do provedor OIDC via discovery"""
    response = requests.get(OIDC_CONFIG['issuer'])
    if not response.ok:
        raise Exception(f"Erro ao obter configuração OIDC: {response.text}")
    return response.json()

def create_oauth_client():
    """Cria uma instância do cliente OAuth"""
    return OAuth2Session(
        client_id=OIDC_CONFIG['client_id'],
        client_secret=OIDC_CONFIG['client_secret'],
        scope=OIDC_CONFIG['scope'],
        redirect_uri=OIDC_CONFIG['redirect_uri']
    )

def get_auth_url():
    """Gera a URL de autorização"""
    config = get_oidc_config()
    client = create_oauth_client()
    
    params = {
        'nonce': secrets.token_urlsafe(32)
    }
    st.session_state.oauth_nonce = params['nonce']
    
    uri, _ = client.create_authorization_url(
        config['authorization_endpoint'],
        **params
    )
    return uri

def get_tokens(auth_code):
    """Troca o código de autorização por tokens"""
    config = get_oidc_config()
    client = create_oauth_client()
    
    tokens = client.fetch_token(
        config['token_endpoint'],
        code=auth_code,
        grant_type='authorization_code'
    )
    return tokens

def get_user_info():
    """Obtém informações do usuário do ID Token"""
    if 'id_token' not in st.session_state:
        return None
        
    try:
        user_info = jwt.decode(
            st.session_state.id_token,
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_iss": False
            }
        )
        return user_info
        
    except InvalidTokenError as e:
        st.error(f"Erro ao decodificar ID Token: {str(e)}")
        return None

def clear_session():
    """Limpa a sessão"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Callback do OAuth
if 'code' in st.query_params:
    try:
        tokens = get_tokens(st.query_params['code'])
        
        st.session_state.access_token = tokens['access_token']
        st.session_state.id_token = tokens['id_token']
        st.session_state.token_expiry = time.time() + tokens.get('expires_in', 3600)
            
        st.query_params.clear()
        st.rerun()
        
    except Exception as e:
        st.error(f"Erro durante autenticação: {str(e)}")
        clear_session()

# Fluxo principal
if 'access_token' not in st.session_state:
    st.markdown("""
        <h2>Bem-vindo ao Sistema</h2>
        <p>Por favor, faça login para continuar.</p>
        """, unsafe_allow_html=True)
    
    if st.button("Entrar"):
        auth_url = get_auth_url()
        st.markdown(f'<meta http-equiv="refresh" content="0;url={auth_url}">', unsafe_allow_html=True)
else:
    user_info = get_user_info()
    
    if user_info is None:
        clear_session()
    else:
        st.write(f"# Bem-vindo {user_info.get('name', 'Usuário')}! 👋")
        
        remaining_time = st.session_state.token_expiry - time.time()
        st.info(f"Tempo restante da sessão: {int(remaining_time)} segundos")
        
        if st.button("Sair"):
            clear_session()
        
        st.write("### Informações do usuário:")
        st.json(user_info)
        
        if st.checkbox("Mostrar tokens (Debug)"):
            st.write("ID Token (decodificado):", user_info)
            st.write("ID Token (raw):", st.session_state.id_token)
            if 'access_token' in st.session_state:
                st.write("Access Token:", st.session_state.access_token)
