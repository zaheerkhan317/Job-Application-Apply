# encode_token.py
import base64
print(base64.b64encode(open("token.pickle","rb").read()).decode())
