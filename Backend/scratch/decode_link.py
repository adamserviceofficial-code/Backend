import zlib
import base64
import json

def base62_decode(data):
    BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    num = 0
    for char in data:
        num = num * 62 + BASE62_ALPHABET.index(char)
    return num.to_bytes((num.bit_length() + 7) // 8, 'big') or b'\0'

def decompress_data(data):
    return zlib.decompress(data).decode()

encoded_data = "lLuGQMdHL8b8VtlqoRigPmtW1qOyxReq320X4j5dbhtI7waPQu4Fs9aDQhdTabwyZRdmxXo65b0eaR"
try:
    compressed = base62_decode(encoded_data)
    decompressed = decompress_data(compressed)
    print(f"Decoded data: {decompressed}")
except Exception as e:
    print(f"Error: {e}")
