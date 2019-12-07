import datetime

from blockchain import BlockChain, Block


class Event(BlockChain):
    """
    Event object. It could be a disease, a prescription, a surgery, etc.
    """
    def __init__(self, event, name, incompatibilities=None, *args, **kw):
        super(BlockChain, self).__init__(*args, **kw)
        self.player = "event"
        self.name = name
        self.event = event
        self.blocks = [self.get_genesis_block()]
        self.incompatibilities = incompatibilities

        if not isinstance(incompatibilities, (list, type(None))):
            raise Exception("`incompatibilities` should be either `list` or `None`")

    def add_block(self, patient, doctor):
        """
        Add a new block to the chain.

        Parameters
        ----------
        patient : :obj:`Patient`
            The BlockChain relative to the patient that faced this event.
        """
        self.blocks.append(Block(len(self.blocks), event=self.event, name=self.name, player=self.player, doctor=doctor,
                                 timestamp=datetime.datetime.utcnow(), patient=patient.name,
                                 previous_hash=self.blocks[len(self.blocks) - 1].hash))
