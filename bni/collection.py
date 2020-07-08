import base64
import math
import time


class BniEnc:
    TIME_DIFF_LIMIT = 400

    @staticmethod
    def ts_diff(ts):
        return math.fabs(ts - time.time()) <= BniEnc.TIME_DIFF_LIMIT

    @staticmethod
    def enc(string, key):
        result = ""
        strls = len(string)
        strlk = len(key)
        for i in range(0, strls):
            char = string[i:i + 1]
            st = (i % strlk) - 1
            xlen = None if st < 0 else st + 1
            keychar = key[st:xlen]
            char = chr((ord(char) + ord(keychar)) % 128)
            result += char
        return result

    @staticmethod
    def double_encrypt(string_obj, cid, secret):
        result = BniEnc.enc(string_obj, cid)
        result = BniEnc.enc(result, secret)
        result = result.encode('ascii')
        result = base64.b64encode(result)
        result = result.decode('ascii').rstrip('=')
        result = result.translate(str.maketrans('+/', '-_'))
        return result

    @staticmethod
    def dec(string, key):
        result = ''
        strls = len(string)
        strlk = len(key)
        for i in range(0, strls):
            char = string[i:i + 1]
            st = (i % strlk) - 1
            xlen = None if st < 0 else st + 1
            keychar = key[st:xlen]
            char = chr((ord(char) - ord(keychar) + 256) % 128)
            result += char
        return result

    @staticmethod
    def double_decrypt(string, cid, secret):
        ceils = math.ceil(len(string) / 4.0) * 4
        while len(string) < ceils:
            string += "="
        string = string.replace('-', '+').replace('_', '/')
        result = string.encode('ascii')
        result = base64.b64decode(result)
        result = result.decode('ascii')
        result = BniEnc.dec(result, cid)
        result = BniEnc.dec(result, secret)
        return result

    @staticmethod
    def encrypt(json_data, cid, secret):
        t = str(int(time.time()))[::-1]
        return BniEnc.double_encrypt(t + "." + json_data, cid, secret)

    @staticmethod
    def decrypt(hased_string, cid, secret):
        parse_str = BniEnc.double_decrypt(hased_string, cid, secret)
        data = parse_str.split(".", 1)
        if len(data) == 2:
            strrevtime = data[0][::-1]
            if BniEnc.ts_diff(int(strrevtime)):
                return data[1]
        return None
