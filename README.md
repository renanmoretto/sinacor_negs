# sinacor_negs
'sinacor_negs' é uma lib feita para facilitar a leitura de arquivos negs.txt da bolsa (B3/Sinacor). A lib foi feita utilizando pandas e retorna os dados em forma de DataFrames.

Para mais informações sobre o formato do arquivo:
https://clientes.b3.com.br/data/files/95/D2/6D/BC/0556F71034D833F7BFC9F9C2/Leiautes%20de%20Arquivos%20SINACOR%20-%20Ampliacao%20Codigo%20do%20Investidor_v2.pdf

## Instalação
`pip install sinacor_negs`

## Como usar
```python
import sinacor_negs as snegs

negs_txt_path = 'sample/negs.txt'

negs = snegs.read_negs_txt(negs_txt_path)

# negs.header -> header do negs
# negs.trades -> trades do negs (todos os negócios).
# negs.trailer -> trailer do negs.
```

