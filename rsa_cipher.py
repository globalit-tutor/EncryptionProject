from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# 암호화 (송신자: 공개키 사용)
def rsa_encrypt(text, key):
    # 키 문자열을 RSA 공개키 객체로 변환
    recipient_key = RSA.import_key(key)
    # RSA-OAEP 방식으로 패딩 처리 - 무작위성 기반
    # PKCS : 공개키 암호 표준
    # OAEP : 암호화전 평문을 무작위화 + 섞고 패딩하는 방법
    # -> 같은 메세지라도 암호화시 매번 다른 암호문 생성
    rsa_cipher = PKCS1_OAEP.new(recipient_key)
    # 메세지를 utf-8인코딩 후 암호화 수행
    encrypted = rsa_cipher.encrypt(text.encode('utf-8'))

    return encrypted


# 복호화 (수신자: 개인키 사용)
def rsa_decrypt(text, key):
    # 키 문자열을 RSA 개인키 객체로 변환
    my_key = RSA.import_key(key)
    rsa_cipher = PKCS1_OAEP.new(my_key)
    decrypted = rsa_cipher.decrypt(text)

    return decrypted.decode('utf-8')


# 1. 키 생성 - 2048 비트
key = RSA.generate(2048)
private_key = key.exportKey()
public_key = key.publickey().exportKey()

print('사설키', private_key)
print('공개키', public_key)

# 2. 암호화
plaintext = 'Hello, World!!'
encrypted = rsa_encrypt(plaintext, public_key)
print(encrypted)
print(len(encrypted))
print('Base64인코딩', base64.b64encode(encrypted))


# 3. 복호화
decrypted = rsa_decrypt(encrypted, private_key)
print(decrypted)
print(len(decrypted))

