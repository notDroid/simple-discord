from harmony.app.db.writers import DirectWriter
from harmony.app.core import active_writer_var


class BaseRepository:
    def __init__(self, client):
        self.client = client
        self._direct_writer = DirectWriter(client)

    @property
    def writer(self):
        current_tx_writer = active_writer_var.get() # Check if there's an active transaction writer in the context
        return current_tx_writer or self._direct_writer