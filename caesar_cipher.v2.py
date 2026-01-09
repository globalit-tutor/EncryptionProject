
# a b c d e f ... x y z
# d e f g h i ... a b c

def caesar_cipher(text, shift, left=True):
    cipher_text = ''

    if not left:
        shift = -shift

    for char in text:
        if char.islower():
            cipher_text += chr((ord(char) - 97 + shift) % 26 + 97)
        elif char.isupper():
            cipher_text += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            cipher_text += char

    return cipher_text


if __name__ == '__main__':
    text = 'hello, world'

    #encrypted = caesar_cipher(text, 3, True)
    encrypted = caesar_cipher(text, 3)                  # 암호화
    print(encrypted)
    decrypted = caesar_cipher(encrypted, 3, False)  # 복호화
    print(decrypted)

    encrypted = caesar_cipher(text, 3, False)       # 암호화
    print(encrypted)
    decrypted = caesar_cipher(encrypted, 3)             # 복호화
    print(decrypted)


    # ---------
    text = 'HELLO, WORLD'

    encrypted = caesar_cipher(text, 3)
    print(encrypted)

    decrypted = caesar_cipher(encrypted, 3, False)
    print(decrypted)


    # ---------
    text = 'Hello, World'
    encrypted = caesar_cipher(text, 3)
    print(encrypted)

    decrypted = caesar_cipher(encrypted, 3, False)
    print(decrypted)


