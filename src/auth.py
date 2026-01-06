import secrets
import string
import hashlib
import base64

def generate_random_string(pLength: int) -> str:
    allowed_chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(allowed_chars) for _ in range(pLength))

def getCodeVerifier():
    return generate_random_string(64)

def generateCodeChallenge(pCode_verifier: str) -> str:
    hashed = hashlib.sha256(pCode_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')

def getParams(pCode_verifier: str):
    code_challenge = generateCodeChallenge(pCode_verifier)

    return {
        'response_type': 'code',
        'client_id' : '69fbd6dddb834660bcfc47c1b76ff6fd',
        'scope': 'playlist-read-private playlist-read-collaborative user-read-private user-read-email',
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge,
        'redirect_uri' : 'http://127.0.0.1:5000/verified'
    }
