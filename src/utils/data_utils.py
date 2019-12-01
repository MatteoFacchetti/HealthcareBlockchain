import hashlib


class Block:
    """
    Minimal block containing an index, a timestamp, the data to store and the previous hash.

    """
    def __init__(self, index, timestamp, data, previous_hash):
        """

        Parameters
        ----------
        index
        timestamp
        data
        previous_hash
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hashing()

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        return key.hexdigest()


class BlockChain:

