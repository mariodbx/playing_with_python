from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def triple_des_encrypt(message, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_message = pad(message, DES3.block_size)
    ciphertext = cipher.encrypt(padded_message)
    return ciphertext

def triple_des_decrypt(ciphertext, key):
    cipher = DES3.new(key, DES3.MODE_ECB)
    decrypted_message = cipher.decrypt(ciphertext)
    unpadded_message = unpad(decrypted_message, DES3.block_size)
    return unpadded_message

# Example usage:
message = b"Testing how triple des works"
key = get_random_bytes(24)  # Generate a random 24-byte (192-bit) key

# Encryption
encrypted_message = triple_des_encrypt(message, key)
print("Encrypted:", encrypted_message)

# Decryption
decrypted_message = triple_des_decrypt(encrypted_message, key)
print("Decrypted:", decrypted_message.decode('utf-8'))
