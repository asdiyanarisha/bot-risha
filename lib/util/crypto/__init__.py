import hashlib

import bcrypt


def md5_text(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()


def bcrypt_password(plain_password):
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt(prefix=b"2a")).decode('utf-8')


def get_passhash(plain_password):
    return bcrypt_password(plain_password)

