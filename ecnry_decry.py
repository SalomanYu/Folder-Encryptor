import os
import sys
import pyAesCrypt
from pyAesCrypt.crypto import decryptFile, encryptFile


def encryption(file, password):
    buffer_size = 512 * 1024
    pyAesCrypt.encryptFile(
        str(file),
        str(file) + ".crp",
        password,
        buffer_size
    )

    print("[Файл '" + str(os.path.splitext(file)[0]) + "' зашифрован]")

    os.remove(file)

def encrypt_dirs(dir, password):

    for name in os.listdir(dir):
        path = os.path.join(dir, name)

        if os.path.isfile(path):
            try:
                encryption(path, password)
            except Exception as ex:
                print(ex)
        else:
            encrypt_dirs(path, password)


def decryption(file, password):
    buffer_size = 512 * 1024
    pyAesCrypt.decryptFile(
        str(file),
        str(os.path.splitext(file)[0]),
        password,
        buffer_size
    )

    print("[Файл '" + str(os.path.splitext(file)[0]) + "' расшифрован]")

    os.remove(file)

def decrypt_dirs(dir, password):

    for name in os.listdir(dir):
        path = os.path.join(dir, name)

        if os.path.isfile(path):
            try:
                decryption(path, password)
            except Exception as ex:
                print(ex)
                return ex
        else:
            decrypt_dirs(path, password)

# decrypt_dirs('/home/saloman/Видео/helloworld/', '123')