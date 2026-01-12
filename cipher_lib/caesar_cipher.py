# 단일 치환 암호 기법의 핵심
# 영문자에 대한 ASCII 코드값 변환 : chr, ord
# print(ord('a'), chr(97))

# 치환 규칙을 수학적으로 접근하는 방법
# a (97) -> x (120) (right shift 3)
# print( chr((ord('a') + 23)) )

# a (97) -> x (120) (left shift 3)
# print( chr((ord('a') + 3 )) )

# a (97) -> x (120) (x shift n)
# print( chr((ord('a') + 23) ) )

# hello world를 단일 치환으로 암호화
# plain_text = 'hello world'   # 평문
# direction = 'right'
# shift = 3
# cipher_text = ''             # 암호문

# for char in plain_text:
#     base = ord('a')   # 기준문자
#     if char == ' ':
#         cipher_text += ' '
#     elif direction == 'left':
#         false_cipher = ord(char) + shift
#         cipher_text += chr((ord(char) - base + shift) % 26 + base)
#     else:
#         false_cipher = ord(char) + (26 - shift)
#         cipher_text += chr((ord(char) - base - shift) % 26 + base)
#
#     print(char, ord(char), false_cipher)

# print('평문', plain_text)
# print(f'암호문 {cipher_text}')

def caesar_cipher1(text, dirc, shift):
    cipher_text = ''
    base = ord('a')   # 기준문자

    for char in text:
        if char == ' ':
            cipher_text += ' '
        elif dirc == 'left':
            cipher_text += chr((ord(char) - base + shift) % 26 + base)
        else:
            cipher_text += chr((ord(char) - base - shift) % 26 + base)

    return cipher_text


def caesar_cipher2(text, dirc, shift):
    cipher_text = ''
    base = ord('A')   # 기준문자

    for char in text:
        if char == ' ':
            cipher_text += ' '
        elif dirc == 'left':
            cipher_text += chr((ord(char) - base + shift) % 26 + base)
        else:
            cipher_text += chr((ord(char) - base - shift) % 26 + base)

    return cipher_text


if __name__ == '__main__':
    plain_text = input('암호화할 문장을 입력하세요 : ')
    direction =  input('이동 방향은? (right/left) : ')
    shift = int(input('이동 횟수는? : '))

    # encrypted_text = caesar_cipher1(plain_text, direction, shift)
    encrypted_text = caesar_cipher2(plain_text, direction, shift)

    print(plain_text, encrypted_text)



