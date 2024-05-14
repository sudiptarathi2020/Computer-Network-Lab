import math
import random
from PIL import Image

# Function to generate prime numbers
def generate_primes(n):
    primes = []
    for num in range(2, n):
        prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if (num % i) == 0:
                prime = False
                break
        if prime:
            primes.append(num)
    return primes

# Function to generate public and private keys
def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    g = math.gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = math.gcd(e, phi)

    # Compute d, the modular inverse of e
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

# Function to compute modular inverse
def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Function to encrypt the image
def encrypt_image(image_path, public_key):
    image = Image.open(image_path)
    width, height = image.size
    pixels = list(image.getdata())

    e, n = public_key
    encrypted_pixels = []
    for pixel in pixels:
        encrypted_pixel = tuple(pow(component, e, n) for component in pixel)
        encrypted_pixels.append(encrypted_pixel)

    return encrypted_pixels, width, height

# Function to save the encrypted image
def save_encrypted_image(encrypted_pixels, width, height, output_path):
    encrypted_image = Image.new('RGB', (width, height))
    encrypted_image.putdata(encrypted_pixels)
    encrypted_image.save(output_path)

# Function to decrypt the image
def decrypt_image(encrypted_pixels, private_key):
    d, n = private_key
    decrypted_pixels = []
    for pixel in encrypted_pixels:
        decrypted_pixel = tuple(pow(component, d, n) for component in pixel)
        decrypted_pixels.append(decrypted_pixel)

    return decrypted_pixels

# Function to save the decrypted image
def save_decrypted_image(decrypted_pixels, width, height, output_path):
    decrypted_image = Image.new('RGB', (width, height))
    decrypted_image.putdata(decrypted_pixels)
    decrypted_image.save(output_path)

# Main function
def main():
    image_path = 'image.jpg'  # Path to your image file
    output_path_encrypted = 'encrypted_image.png'  # Output path for encrypted image
    output_path_decrypted = 'decrypted.jpg'  # Output path for decrypted image

    # Generate prime numbers
    primes = generate_primes(100)
    p, q = random.choice(primes), random.choice(primes)

    # Generate keys
    public_key, private_key = generate_keys(p, q)

    # Encrypt image
    encrypted_pixels, width, height = encrypt_image(image_path, public_key)

    # Save encrypted image
    save_encrypted_image(encrypted_pixels, width, height, output_path_encrypted)

    # Decrypt image
    decrypted_pixels = decrypt_image(encrypted_pixels, private_key)

    # Save decrypted image
    save_decrypted_image(decrypted_pixels, width, height, output_path_decrypted)

if __name__ == "__main__":
    main()

