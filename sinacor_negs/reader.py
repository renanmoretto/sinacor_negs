"""
Leitor do arquivo .txt do negs e que retorna um objeto Negs
"""

import pandas as pd
import numpy as np
from pandas import DataFrame

from .utils import drop_left_zeros_df
from .negs import Negs


def check_first_layout(negs_txt: DataFrame) -> bool:
    """Checa o layout do arquivo
    first_layout == True > Layout atual, contas com até 7 dígitos
    first_layout == False > Layout novo, contas com mais de 7 dígitos
    """
    if negs_txt.columns[0][39:40] == "S":
        return False
    return True


def get_header(negs_txt: DataFrame, first_layout: bool) -> DataFrame:
    """Função para ler o header do negs

    Returns:
        header: DataFrame
    """
    header_txt = negs_txt.columns[0]
    header = pd.DataFrame(index=[0])
    header["tipo_registro"] = header_txt[0:2]
    header["nome_arquivo"] = header_txt[2:10]
    header["codigo_arquivo"] = header_txt[2:6]
    header["codigo_usuario"] = header_txt[6:10]
    header["codigo_origem"] = header_txt[10:18]
    header["codigo_destino"] = header_txt[18:22]
    header["data_geracao"] = header_txt[22:30]
    header["data_pregao"] = header_txt[30:38]

    if first_layout:
        header["reserva"] = header_txt[38:200]
    else:
        header["reserva"] = header_txt[39:200]

    header = drop_left_zeros_df(header)

    return header


def get_trades(negs_txt: DataFrame, first_layout: bool) -> DataFrame:
    """Função para ler as operações do negs

    Returns:
        trades: DataFrame
    """
    trades_txt = pd.Series(negs_txt.iloc[:-1, 0])
    negs = pd.DataFrame(index=np.arange(len(trades_txt)))

    negs["tipo_registro"] = trades_txt.str[0:2]
    negs["numero_negocio_por_codigo_negociacao"] = trades_txt.str[2:9]
    negs["natureza_operacao"] = trades_txt.str[9:10]
    negs["codigo_negociacao"] = trades_txt.str[10:22]
    negs["tipo_mercado"] = trades_txt.str[22:25]
    negs["tipo_transacao"] = trades_txt.str[25:28]
    negs["nome_sociedade_emissora"] = trades_txt.str[28:40]
    negs["especificacao"] = trades_txt.str[40:50]
    negs["quantidade_negocio"] = trades_txt.str[50:61].str.lstrip("0").astype(int)
    negs["preco_negocio"] = trades_txt.str[61:72].str.lstrip("0").astype(float).div(100)
    negs["codigo_usuario_contraparte"] = trades_txt.str[72:77]
    negs["prazo_vencimento"] = trades_txt.str[77:80]
    negs["tipo_liquidacao"] = trades_txt.str[80:81]
    negs["hora_minuto_negocio"] = trades_txt.str[81:86]
    negs["situacao_negocio"] = trades_txt.str[86:87]
    negs["codigo_objeto_papel"] = trades_txt.str[87:99]
    negs["codigo_cliente"] = trades_txt.str[99:106]
    negs["digito_cliente"] = trades_txt.str[106:107]
    negs["codigo_isin"] = trades_txt.str[107:119]
    negs["distribuicao_isin"] = trades_txt.str[119:122]
    negs["fator_cotacao_negocio"] = trades_txt.str[122:129]
    negs["preco_exercicio_serie"] = trades_txt.str[129:140]
    negs["indicador_after_market"] = trades_txt.str[140:141]
    negs["reserva1"] = trades_txt.str[141:149]
    negs["prazo_vencimento_termo"] = trades_txt.str[149:154]
    negs["reserva2"] = trades_txt.str[154:167]
    negs["bolsa_movimento"] = trades_txt.str[167:168]
    negs["tipo_liquidacao"] = trades_txt.str[168:169]
    negs["prazo_liquidacao"] = trades_txt.str[169:172].str.lstrip("0").astype(int)
    negs["reserva3"] = trades_txt.str[172:198]
    negs["tipo_operacao_recompra"] = trades_txt.str[200:201]

    if not first_layout:
        negs["fase_grupo_instrumento"] = trades_txt.str[172:175]
        negs["fase_sessao_negociacao"] = trades_txt.str[175:176]
        negs["estado_instrumento"] = trades_txt.str[176:180]
        negs["codigo_bdi"] = trades_txt.str[180:184]
        negs["codigo_cliente"] = trades_txt.str[184:193]
        negs["reserva3"] = trades_txt.str[193:200]

    negs = drop_left_zeros_df(negs)

    return negs


def get_trailer(negs_txt: DataFrame) -> DataFrame:
    """Função para ler o trailer ("rodapé") do negs

    Returns:
        trailer: DataFrame
    """
    trailer_txt = negs_txt.iloc[-1].values[0]
    trailer = pd.DataFrame(index=[0])

    trailer["tipo_registro"] = trailer_txt[0:2]
    trailer["nome_arquivo"] = trailer_txt[2:10]
    trailer["codigo_arquivo"] = trailer_txt[2:6]
    trailer["codigo_usuario"] = trailer_txt[6:10]
    trailer["codigo_origem"] = trailer_txt[10:18]
    trailer["codigo_destino"] = trailer_txt[18:22]
    trailer["data_geracao_arquivo"] = trailer_txt[22:30]
    trailer["total_registros_gerados"] = trailer_txt[30:39]
    trailer["reserva"] = trailer_txt[39:200]

    trailer = drop_left_zeros_df(trailer)

    return trailer


def read_negs_txt(negs_path: str) -> Negs:
    """Função principal para ler o NEGS enviado pela B3/Sinacor em .txt

    Args:
        path: str
            diretorio do NEGS.txt

    Returns:
        negs: Negs
            variável negs contendo os 4 atributos do tipo Negs
    """

    if negs_path[-4:] != ".txt":
        raise ValueError(
            "'negs_path' não é um arquivo .txt. Por favor, informe um path válido"
        )

    negs_txt = pd.read_csv(negs_path)

    first_layout = check_first_layout(negs_txt)
    header = get_header(negs_txt, first_layout)
    trades = get_trades(negs_txt, first_layout)
    trailer = get_trailer(negs_txt)

    return Negs(header=header, trades=trades, trailer=trailer)
