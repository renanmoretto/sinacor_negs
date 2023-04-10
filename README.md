# sinacor_negs
'sinacor_negs' é uma lib feita para facilitar a leitura de arquivos negs.txt da bolsa (B3/Sinacor). A lib foi feita utilizando pandas e retorna os dados em forma de DataFrames.

## Instalação
`pip install sinacor_negs`

## Como usar
```python
import sinacor_negs as snegs

negs_txt_path = 'sample//negs.txt'

negs = snegs.read_negs_txt(negs_txt_path)

# negs.header -> dataframe do header.
# negs.negs -> dataframe do negs (todos os negócios).
# negs.trailer -> dataframe do trailer.
```

