import datetime

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from blockchain import BlockChain, Block


class Patient(BlockChain):
    """
    Patient object.
    """
    def __init__(self, name, *args, **kw):
        super(BlockChain, self).__init__(*args, **kw)
        self.name = name
        self.player = "patient"
        self.blocks = [self.get_genesis_block()]
        self.get_keys(genesis=True)

    def add_block(self, event, doctor):
        """
        Add a new block to the chain.

        Parameters
        ----------
        event : :obj:`Event`
            BlockChain relative to the event that the patient faced.
        doctor : :obj:`Doctor`
            BlockChain relative to the doctor that adds the event to the chain of the patient.

        Returns
        -------

        """
        self.blocks.append(Block(len(self.blocks), player=self.player, name=self.name, doctor=doctor.name,
                                 timestamp=datetime.datetime.utcnow(), kind=event.event, data=event.name,
                                 previous_hash=self.blocks[len(self.blocks) - 1].hash))

        # TODO: Prevent from adding prescriptions that are not compatible with previous diseases
        if event.event == "prescription":
            pass

    def get_keys(self, genesis=False):
        """
        Generate private and public keys of this specific patient and store them in the respective folders.

        Parameters
        ----------
        genesis : bool
            If True, the keys are stored as genesis keys, meaning that they will not be overwritten in future.
            Genesis keys should be always kept secret and only used by the patient.
            Doctors should not have access to the genesis keys of the patients.
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
        if genesis:
            with open(f'../private_keys/{self.name}_private_gen.pem', 'wb') as f:
                f.write(private_key)
            with open(f'../public_keys/{self.name}_public_gen.pem', 'wb') as f:
                f.write(public_key)
