"""
Negs
---------

Objeto Negs contendo as informações do arquivo negs da B3 (Sinacor)

"""

from pandas import DataFrame


class Negs:
    """
    Attributes
    ----------
    header: pd.DataFrame
        dataframe do header do negs

    trades: pd.DataFrame
        dataframe do negs (todos os negócios)

    trailer: pd.DataFrame
        dataframe do trailer do negs
    """

    def __init__(
        self,
        header: DataFrame = DataFrame(),
        trades: DataFrame = DataFrame(),
        trailer: DataFrame = DataFrame(),
    ) -> None:
        self.header = header
        self.trades = trades
        self.trailer = trailer
