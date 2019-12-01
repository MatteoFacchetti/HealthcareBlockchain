import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from utils.data_utils import BlockChain, Block


class Patient(BlockChain):
    """
    Patient object.
    """
    def __init__(self, name, *args, **kw):
        super(BlockChain, self).__init__(*args, **kw)
        self.name = name
        self.player = "patient"
        self.blocks = [self.get_genesis_block()]
        self.get_keys()

    def add_block(self, kind, data):
        """
        Add a new block to the chain.
        """
        self.blocks.append(Block(len(self.blocks), player=self.player, name=self.name,
                                 timestamp=datetime.datetime.utcnow(), kind=kind, data=data,
                                 previous_hash=self.blocks[len(self.blocks) - 1].hash))
        # Encrypt blockchain
        with open(f"../public_keys/{self.name}_public.txt", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        prova = public_key.encrypt(
            b"prova",
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        # TODO: Prevent from adding prescriptions that are not compatible with previous diseases
        if kind == "prescription":
            pass

    def get_keys(self):
        """
        Generate private and public keys of this specific patient and store them in the respective folders.
        """
        # Generate keys
        private_key = rsa.generate_private_key(
            public_exponent=2*(len(self.blocks))+3,
            key_size=2048,
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
        with open(f'../public_keys/{self.name}_public.pem', 'wb') as f:
            f.write(public_key)
