import secrets

def generate_secret_key():
    # Generate a 32-byte random key
    key = secrets.token_hex(32)
    print("Generated Secret Key:", key)
    return key

if __name__ == "__main__":
    generate_secret_key() 