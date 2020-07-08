from bni.collection import BniEnc

if __name__ == '__main__':
    cid = "123"
    secret = "11111222222223333333354545454545454545454"
    data = '{"nama_lengkap":"Dzun Nurroin","lembaga":"SMK Nurul Jadid"}'
    hashing = BniEnc.encrypt(data, cid, secret)
    decode = BniEnc.decrypt(hashing, cid, secret)

    print(hashing)
    print(decode)
