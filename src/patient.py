from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from utils.data_utils import BlockChain


class Patient(BlockChain):
    """
    Patient object.
    """

    def __init__(self, name, *args, **kw):
        super(BlockChain, self).__init__(*args, **kw)
        self.name = name
        self.player = "patient"
        self.blocks = [self.get_genesis_block()]
        self.private_key, self.public_key = self.get_keys()

    def get_keys(self):
        """
        Generate private and public keys of this specific patient and store them in the respective folders.
        """
        # Generate keys
        private_key = rsa.generate_private_key(
            public_exponent=2*(len(self.blocks))+3,
            key_size=512,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_key = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PrivateFormat.PKCS8,
                                                encryption_algorithm=serialization.NoEncryption())
        public_key = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PublicFormat.SubjectPublicKeyInfo)

        # Store keys
        with open(f'../private_keys/{self.name}_private.pem', 'wb') as f:
            f.write(private_key)
        with open(f'../public_keys/{self.name}_public.pen', 'wb') as f:
            f.write(public_key)

        return private_key, public_key
