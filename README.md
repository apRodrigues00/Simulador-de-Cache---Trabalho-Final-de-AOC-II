Trabalho de simulador de caches

Disciplina Arquitetura e Organização de Computadores II

Desenvolvido por: André Pereira e Douglas da Silva

Funcionamento:
    O simulador recebe como entrada este comando:
        cache_simulator nsets bsize assoc substituição flag_saida arquivo_de_entrada
    Exemplo:
        python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> <arquivo_de_entrada>

    nsets: número de índices
    bsize: tamanho do bloco
    assoc: número de associatividade
    substituição: política usada (R para RANDOM, L para LRU e F para FIFO)
    flag_saida: modo de exibição do resultado (0 para o formato de matriz e 1 para especificações)
    arquivo_de_entrada: nome do arquivo com binários usados para execução

Bibliotecas Usadas
    sys: para acessar os argumentos passados para o script na linha de comando
    math: para realizar cálculos de endereçamento
    random: para operações com a politíca de substituição RANDOM

    Exemplo de instalação de biblioteca em Python:
        pip install <nome_biblioteca>
