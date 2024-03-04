import sys
import math
import random


def replacement_policy(subst, start_index, end_index, cache_order, access_order, cache_tag, tag):
    
    cache_index = 0
    if subst == "R":
        cache_index = random.randint(start_index, end_index - 1)  # Escolha aleatória do bloco a ser substituído
    elif subst == "L":
        cache_index = start_index + cache_order[start_index:end_index].index(min(cache_order[start_index:end_index]))
        cache_order[cache_index] = access_order  # Atualiza a ordem de acesso do conjunto
    cache_tag[cache_index] = tag
    return cache_order, cache_tag


def print_cache_data(hit, number_access, miss, miss_compulsory, miss_capacity, miss_conflict, flagOut):
    
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


def direct_mapping(cache_index, cache_val, cache_tag, tag, hit, miss, miss_compulsory):

    if cache_val[cache_index] == 1 and cache_tag[cache_index] == tag:
        hit += 1
    else:
        miss += 1
        if cache_val[cache_index] == 0:
            miss_compulsory += 1
            cache_val[cache_index] = 1
            cache_tag[cache_index] = tag
    return cache_val, cache_tag, hit, miss, miss_compulsory


def associative_mapping(start_index, end_index, cache_val, cache_tag, tag, cache_order, access_order, subst, found, hit, miss, miss_compulsory, miss_conflict, miss_capacity):
    for i in range(start_index, end_index):
        if cache_val[i] == 1 and cache_tag[i] == tag:
            hit += 1
            found = True
            cache_order[i] = access_order  # Atualiza a ordem de acesso do conjunto
            break

    if not found:
        miss += 1
        if 0 in cache_val[start_index:end_index]:
            miss_compulsory += 1
            for i in range(start_index, end_index):
                if cache_val[i] == 0:
                    cache_val[i] = 1
                    cache_tag[i] = tag
                    cache_order[i] = access_order  # Atualiza a ordem de acesso do conjunto
                    break
        elif 0 in cache_val:
            miss_conflict += 1
            cache_order, cache_tag = replacement_policy(subst, start_index, end_index, cache_order, access_order, cache_tag, tag)
        else:
            miss_capacity += 1
            cache_order, cache_tag = replacement_policy(subst, start_index, end_index, cache_order, access_order, cache_tag, tag)

    return hit, miss, miss_compulsory, miss_conflict, miss_capacity


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

    # Inicialização das estruturas da cache
    cache_val = [0] * (nsets * assoc)
    cache_tag = [-1] * (nsets * assoc)
    cache_order = [0] * (nsets * assoc)

    # Cálculo do número de bits pro offset, índice e tag
    n_bits_offset = int(math.log2(bsize))
    n_bits_index = int(math.log2(nsets))
    n_bits_tag = 32 - n_bits_offset - n_bits_index

    # Debugg
    count_print = 0

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
                cache_val, cache_tag, hit, miss, miss_compulsory = direct_mapping(index, cache_val, cache_tag, tag,
                                                                                   hit, miss, miss_compulsory)
            # Mapeamento associativo
            else:
                start_index = index * assoc
                end_index = start_index + assoc
                access_order = number_access

                hit, miss, miss_compulsory, miss_conflict, miss_capacity = associative_mapping(start_index, end_index,
                                                                                               cache_val, cache_tag, tag,
                                                                                               cache_order,
                                                                                               access_order, subst, found,
                                                                                               hit, miss,
                                                                                               miss_compulsory,
                                                                                               miss_conflict,
                                                                                               miss_capacity)

    print_cache_data(hit, number_access, miss, miss_compulsory, miss_capacity, miss_conflict, flagOut)


if __name__ == '__main__':
    main()
