
class Vectura:
    def __init__(self, model, datasource):
        self.model = model
        self.datasource = datasource
        self.BATCH_SIZE = 32
        self.current_index = 0