# AES : 128비트 블록, 128비트 키
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# 키 생성 (16바이트)
key = get_random_bytes(16)
print(key)

# 평문 - 16바이트 단위
plaintext = 'Hello, World!!'

# 패딩
padded_text = pad(plaintext.encode('utf-8'), 16)

# 암호화 - 블록단위 암호화 지원
aes = AES.new(key, AES.MODE_ECB)
encrypted = aes.encrypt(padded_text)
print(encrypted)

# 암호화 강화
bytes_encrypted = base64.b64encode(encrypted)
print(bytes_encrypted)

# 복호화
bytes_decrypted = base64.b64decode(bytes_encrypted)

decrypted = aes.decrypt(bytes_decrypted)
unpad_decrypted = unpad(decrypted, 16)
print(unpad_decrypted)


