import datetime
import shutil
from functools import partial
from tempfile import TemporaryDirectory

import cryptography.fernet as fernet


class CryptMod:
    def __init__(self, faster=True):
        self.faster = faster
        pass

    def encrypt(self, file):
        """
        Encrypts a file using Fernet encryption.
        """
        key = fernet.Fernet.generate_key()
        temp_dir = TemporaryDirectory()
        start_time = datetime.datetime.now()

        with open(file, "rb") as input_file, open(temp_dir.name + file, "ab+") as output_file:
            # Write the key length and key to the output file
            output_file.write(len(key).to_bytes(2, 'big'))
            output_file.write(key)
            # Encrypt and write the file contents
            for chunk in chunked_file_reader(input_file):
                if self.faster:
                    output_file.write(fernet.Fernet(key).encrypt(chunk))
                    self.faster = False
                else:
                    output_file.write(chunk)

        # Replace the original file with the encrypted file
        shutil.move(temp_dir.name + file, file)

        use_time = datetime.datetime.now() - start_time
        print("Encryption completed in: " + str(use_time))

    def decrypt(self, file):
        """
        Decrypts a file using Fernet decryption.
        """
        try:
            temp_dir = TemporaryDirectory()
            start_time = datetime.datetime.now()

            with open(file, "rb") as input_file, open(temp_dir.name + file, "ab+") as output_file:
                # Read the key length and key from the input file
                key_len = int.from_bytes(input_file.read(2), 'big')
                right_key = input_file.read(key_len)

                # Decrypt and write the file contents
                for chunk in chunked_file_reader(input_file, block_size=1398200):
                    if self.faster:
                        output_file.write(fernet.Fernet(right_key).decrypt(chunk))
                        self.faster = False
                    else:
                        output_file.write(chunk)

            # Replace the original file with the decrypted file
            shutil.move(temp_dir.name + file, file)

            use_time = datetime.datetime.now() - start_time
            print("Decryption completed in: " + str(use_time))
        except IOError:
            pass


def chunked_file_reader(file, block_size=1024 * 1024 * 1):
    """
    Generator function to read a file in chunks.
    1 1398200
    4 5592504
    16 22369720
    64 89478584
    """
    for chunk in iter(partial(file.read, block_size), b''):
        yield chunk
