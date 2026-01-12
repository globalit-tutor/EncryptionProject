# 평문 : be careful for assassinator
# 변환 : be ca re fu lf or as sa sx si na to rx
# 키1 : assassinator
# 암호화 테이블 : asint orbcd efghj klmpz uvwxy
# 키2 : secret is beautiful
# 암호문 :

def prepare_text(text): # 암호화 전 평문을 2자씩 나눔
    ptext = []
    pos = 0       # 글자 위치

    # 공백 제거, 소문자 일괄변환
    text = text.replace(' ', '').lower()
    # print(text)

    # 2글자씩 그룹으로 묶음 (diagram)
    # while pos < len(text):
    #     first = text[pos]
    #     second = text[pos+1]
    #     ptext.append(first+second)
    #     pos += 2

    # 두 글자를 합치되 같은 문자 2개가 나오면 하나의 문자에 x 추가
    # while pos < len(text):
    #     first = text[pos]
    #     second = text[pos+1]
    #
    #     if first != second:
    #         ptext.append(first+second)
    #         pos += 2
    #     else:
    #         ptext.append(first+'x')
    #         pos += 1

    while pos < len(text):
        first = text[pos]
        # 마지막 문자 여부 체크
        if pos + 1 < len(text):
            second = text[pos+1]
        else:
            second = 'x'

        if first != second:
            ptext.append(first+second)
            pos += 2
        else:
            ptext.append(first+'x')
            pos += 1

    print(ptext)
    return ptext


def create_playfair_matrix(key): # 5x5 암호화 테이블 생성
    import string
    key_matrix = []    # [[],[],[],[],[]]
    keys = []
    # alphas = 'abcdefghijklmnopqrstuvwxy'
    alphas = string.ascii_lowercase.replace('z', 'q')

    # 먼저, 키를 테이블에 저장하고 (단, 중복은 제외)
    for ch in key:
        if ch not in keys:   # 중복제거
            keys.append(ch)

    # 나머지 테이블 공간에 알파벳을 채움 (단, 중복은 제외)
    while len(keys) < 25:
        for ch in alphas:
            if ch not in keys:   # 중복제거
                keys.append(ch)

    # print(keys, len(keys))

    # 5개씩 나눠 암호화 테이블에 저장
    # key_matrix.append(keys[0:5])
    # key_matrix.append(keys[5:10])
    # key_matrix.append(keys[10:15])
    # key_matrix.append(keys[15:20])
    # key_matrix.append(keys[20:25])
    for i in range(0, 25, 5):
        key_matrix.append(keys[i:i+5])

    print(key_matrix)
    return key_matrix


# 암호화 테이블에서 특정 문자의 위치를 알아냄
def find_pos(table, ch):
    for r in range(5):
        for c in range(5):
            if table[r][c] == ch:
                return r, c


# 플레이페어 암호화 함수
# def playfair_encrypt(pairs, table):
#     encrypted = []
#
#     for pair in pairs:
#         a, b = pair    # 변수 split
#         print(a, b)
#
#         # 암호화 테이블에서 해당 문자의 위치 검색
#         # print(table[0][0], table[0][1],
#         #       table[0][2], table[0][3], table[0][4])
#         # print(table[1][0], table[1][1],
#         #       table[1][2], table[1][3], table[1][4])
#         # print(table[2][0], table[2][1],
#         #       table[2][2], table[2][3], table[2][4])
#
#         # for r in range(5):
#         #     for c in range(5):
#         #         print(table[r][c], end=' ')
#         #     print()
#
#         # for r in range(5):
#         #     for c in range(5):
#         #         if table[r][c] == a: print(a, r, c)
#         #         if table[r][c] == b: print(b, r, c)
#
#         r1, c1 = find_pos(table, a)
#         r2, c2 = find_pos(table, b)
#         print(a, r1, c1)
#         print(b, r2, c2)
#
#         # 같은 행 : 오른쪽 다음 (열) 문자 선택
#         if r1 == r2:
#             code = table[r1][(c1 + 1) % 5] + table[r2][(c2 + 1) % 5]
#         # 같은 열 : 아래쪽 다음 (행) 문자 선택
#         elif c1 == c2:
#             code = table[(r1 + 1) % 5][c1] + table[(r2 + 1) % 5][c2]
#         # 다른 행/열 : 같은 행에서 상대쪽 열 문자 선택
#         else:
#             code = table[r1][c2] + table[r2][c1]
#
#         encrypted.append(code)
#
#     #print(encrypted)
#     return encrypted


def playfair_encrypt(pairs, table, encrypt=True):
    encrypted = []
    shift = 1 if encrypt else -1

    for pair in pairs:
        a, b = pair    # 변수 split
        print(a, b)

        r1, c1 = find_pos(table, a)
        r2, c2 = find_pos(table, b)
        print(a, r1, c1)
        print(b, r2, c2)

        # 같은 행 : 오른쪽 다음 (열) 문자 선택
        if r1 == r2:
            code = table[r1][(c1 + shift) % 5] + table[r2][(c2 + shift) % 5]
        # 같은 열 : 아래쪽 다음 (행) 문자 선택
        elif c1 == c2:
            code = table[(r1 + shift) % 5][c1] + table[(r2 + shift) % 5][c2]
        # 다른 행/열 : 같은 행에서 상대쪽 열 문자 선택
        else:
            code = table[r1][c2] + table[r2][c1]

        encrypted.append(code)

    return encrypted


if __name__ == '__main__':
    plain_text = 'be careful for assassinator'
    #plain_text = 'be#careful#for#assassinator'
    key = 'assassinator'

    pairs = prepare_text(plain_text)
    table = create_playfair_matrix(key)
    encrypted = playfair_encrypt(pairs, table)
    print(encrypted)

    decrypted = playfair_encrypt(encrypted, table, False)
    # 리스트의 개별문자를 모아서(join) 출력 (단, x는 제거)
    decrypted = "".join(decrypted).replace('x', '')
    print(decrypted)
