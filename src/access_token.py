def getPayload(pCode, pCode_verifier):
    return {
        'grant_type': 'authorization_code',
        'code': pCode,
        'redirect_uri': 'http://127.0.0.1:5000/verified',
        'client_id': '69fbd6dddb834660bcfc47c1b76ff6fd',
        'code_verifier': pCode_verifier
    }
