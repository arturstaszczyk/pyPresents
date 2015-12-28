class CannotFindReceiver(Exception):
    def __str__(self):
        return 'Cannot find receiver'