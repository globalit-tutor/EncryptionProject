# pip install pycryptodome

import hashlib

def get_filehash(file):
    # 해시알고리즘 초기화
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    # 해시알고리즘 적용전 파일내용을 바이너리로 한번에 읽음 - 저용량 파일
    binary_readed = open(file, 'rb').read()
    md5.update(binary_readed)
    sha1.update(binary_readed)
    sha256.update(binary_readed)

    # 해시알고리즘 적용전 파일내용을 청크chunk단위로 읽음 - 대용량 파일
    # 청크chunk: 큰 데이터를 처리하기 편하게 일정 크기로 잘라놓은 데이터 조각
    # 청크chunk의 장점 - 메모리 절약, 스트리밍 처리, 입출력 효율
    # lambda: f.read(8192), b"" -> [청크][청크][청크][청크][청크][청크]
    with open(file, 'rb') as f:
        #for chunk in iter(lambda: f.read(8192), b""):   # 8KB
        for chunk in iter(lambda: f.read(65536), b""):   # 64KB
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)

    # 디지털지문 생성
    md5digest = md5.hexdigest()
    sha1digest = sha1.hexdigest()
    sha256digest = sha256.hexdigest()

    return md5digest, sha1digest, sha256digest


if __name__ == '__main__':
    file_path = 'c:/Java/BIND9.16.50.x64.zip'

    md5hashed, sha1hased, sha256hashed = get_filehash(file_path)
    print(md5hashed)
    print(sha1hased)
    print(sha256hashed)



