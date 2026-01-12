# 비즈네르 암호 : 시저 암호를 26가지 다른 버젼으로 만든 것
# 시저 암호 : 알파벳을 몇 칸 옆으로 밀어서 바꿈
# 키 : 얼마나 밀지 알려주는 중요한 비밀단어

def vigenere_cipher(text, key, encrypt=True):
    cipher_text = ''
    key_index = 0          # 키의 위치
    key = key.upper()      # 계산을 쉽게 하기 위해 대문자(또는 소문자)로 통일

    for char in text:
        if char.isalpha():       # 문자가 알파벳인지 체크
            # 비밀키에 의해 얼마나 밀건지 계산
            if (key[key_index % len(key)]) == ' ': key_index += 1  # 공백은 건너뜀
            shift = ord(key[key_index % len(key)]) - 65

            if not encrypt:          # 복호화중이라면 반대로 당김
                shift = -shift

            if char.islower():
                cipher_text += chr((ord(char) - 97 + shift) % 26 + 97)
            elif char.isupper():
                cipher_text += chr((ord(char) - 65 + shift) % 26 + 65)

            key_index += 1    # 다음 암호화에 쓸 키를 위해 키 인덱스 증가
        else:
            cipher_text += char

    return cipher_text



if __name__ == '__main__':
    plain_text = 'wish to be free from myself'
    secret_key = 'Secret Is bEautIfuL'

    encrypted = vigenere_cipher(plain_text, secret_key)
    print(encrypted)

    decrypted = vigenere_cipher(encrypted, secret_key, False)
    print(decrypted)



