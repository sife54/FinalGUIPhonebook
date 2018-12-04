from Crypto.Cipher import AES

key = b'\xb0\xc3%\x02\x07"n\x83b;l\xafK4\x13\\\x19\x14\xb9\xa7\xe6\x14\x07+'
cipher = AES.new(key)

def pad(s):
    return s + ((16 - len(s) % 16) * '{')

def encrypt(plaintext):
    global cipher, key
    return cipher.encrypt(pad(plaintext))

def decrypt(ciphertext):
    global cipher
    dec = cipher.decrypt(ciphertext).decode('latin-1')
    l = dec.count('{')
    return dec[:len(dec)-l]

def main():
    message = "Hello World."
    print("Message:", message)
    encrypted = encrypt(message)
    decrypted = decrypt(encrypted)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)


if __name__ == "__main__":
    main()