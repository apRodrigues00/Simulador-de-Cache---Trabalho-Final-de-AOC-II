import sys
import math
import random

def main():
    if len(sys.argv) != 7:
        print("Número de argumentos incorreto. Utilize:")
        print("python cache_simulator.py <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
        exit(1)
    
    nsets = int(sys.argv[1])
    bsize = int(sys.argv[2])
    assoc = int(sys.argv[3])
    subst = sys.argv[4]
    flagOut = int(sys.argv[5])
    inputFile = sys.argv[6]

    # Inicialização das variáveis para estatísticas
    number_access = 0
    hit = 0
    miss = 0
    miss_compulsory = 0
    miss_capacity = 0
    miss_conflict = 0

    # Inicialização das estruturas de cache
    cache_val = [0] * (nsets * assoc)
    cache_tag = [-1] * (nsets * assoc)

    # Cálculo do número de bits para offset, índice e tag
    n_bits_offset = int(math.log2(bsize))
    n_bits_index = int(math.log2(nsets))
    n_bits_tag = 32 - n_bits_offset - n_bits_index

    with open(inputFile, 'rb') as file:
        while True:
            address = file.read(4)
            if not address:
                break
            address = int.from_bytes(address, byteorder='big')

            number_access += 1 
            tag = address >> (n_bits_offset + n_bits_index)
            index = (address >> n_bits_offset) & ((2 ** n_bits_index) - 1)

            found = False

            # Mapeamento direto
            if assoc == 1:  
                cache_index = index
                if cache_val[cache_index] == 1 and cache_tag[cache_index] == tag:
                    hit += 1
                    found = True
                else:
                    miss += 1
                    if cache_val[cache_index] == 0:
                        miss_compulsory += 1
                        cache_val[cache_index] = 1
                        cache_tag[cache_index] = tag
                    else:
                        # Não há política de substituição no mapeamento direto
                        pass

            # Mapeamento associativo        
            else:  
                start_index = index * assoc
                end_index = start_index + assoc
                for i in range(start_index, end_index):
                    if cache_val[i] == 1 and cache_tag[i] == tag:
                        hit += 1
                        found = True
                        break

                if not found:
                    miss += 1
                    if 0 in cache_val[start_index:end_index]:
                        miss_compulsory += 1
                        for i in range(start_index, end_index):
                            if cache_val[i] == 0:
                                cache_val[i] = 1
                                cache_tag[i] = tag
                                break
                    elif 0 in cache_val:
                        miss_conflict += 1
                        # Escolha aleatória do bloco a ser substituído
                        cache_index = random.randint(start_index, end_index - 1)
                        cache_tag[cache_index] = tag
                        
                    else: 
                        miss_capacity += 1
                        # Escolha aleatória do bloco a ser substituído
                        cache_index = random.randint(start_index, end_index - 1)
                        cache_tag[cache_index] = tag


    hit_rate = round(hit / number_access, 4)
    miss_rate = round(miss / number_access, 4)
    compulsory_miss_rate = round(miss_compulsory / miss if miss != 0 else 0, 4)
    capacity_miss_rate = round(miss_capacity / miss if miss != 0 else 0, 4)
    conflict_miss_rate = round(miss_conflict / miss if miss != 0 else 0, 4)

    if flagOut == 0:
        print("Número de acessos: ", number_access)
        print(f"Taxa de hits: {hit_rate} \tNúmero de hits: {hit}")
        print(f"Taxa de misses: {miss_rate} \tNúmero de misses: {miss}")
        print(f"Taxa de misses compulsório: {compulsory_miss_rate} \tNúmero de misses compulsório: {miss_compulsory}")
        print(f"Taxa de misses de capacidade: {capacity_miss_rate} \tNúmero de misses de capacidade: {miss_capacity}")
        print(f"Taxa de misses de conflito: {conflict_miss_rate} \tNúmero de misses de conflito: {miss_conflict}")
    
    elif flagOut == 1:
        print(number_access, hit_rate, miss_rate, compulsory_miss_rate, capacity_miss_rate, conflict_miss_rate)
    
    else:
        print("Flag de saída inválida!")

if __name__ == '__main__':
    main()
