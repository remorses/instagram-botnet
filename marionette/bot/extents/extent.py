class Extent:
    def __init__(self, bot):
        self.__bot = bot

        self._accumulate = bot.accumulate
        self._reset = bot.reset
        self._api = bot.api
        self._logger = bot.api.logger

    @property
    def _acc(self):
        return self.__bot.acc

    def __getitem__(self, method):
        func = getattr(self, method, False)
        if not func:
            print('not found {}'.format(method))
        return func
