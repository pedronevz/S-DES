# ======> ENCRYPT <====== #
def PermutacaoP10(chave):
    p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    permuted_key = []

    for i in p10:
        permuted_key.append(chave[i - 1]) 
    
    result = ''.join(permuted_key)
    return result

#  Deslocamento Circular
def CLS(key, shift):
    left_half = key[:5]  # Primeiros 5 bits
    right_half = key[5:]  # Últimos 5 bits
    
    shifted_left = []
    shifted_right = []
    
    # Deslocamento na primeira metade
    for i in range(len(left_half)):
        shifted_left.append(left_half[(i + shift) % len(left_half)])
        
    # Deslocamento na segunda metade
    for i in range(len(right_half)):
        shifted_right.append(right_half[(i + shift) % len(right_half)])
    
    shifted_key = ''.join(shifted_left) + ''.join(shifted_right)
    return shifted_key


def PermutacaoP8(chave):
    p8 = [6, 3, 7, 4, 8, 5, 10, 9]
    permuted_key = []

    for i in p8:
        permuted_key.append(chave[i - 1]) 
    
    result = ''.join(permuted_key)
    return result

# (IP)
def PermutacaoInicial(bloco):
    ip = [2, 6, 3, 1, 4, 8, 5, 7]
    permuted_block = []

    for i in ip:
        permuted_block.append(bloco[i - 1]) 
    
    result = ''.join(permuted_block)

    print(f'Bloco pós IP: {result}')
    return result

# (E/P)
def ExpansaoPermutacao(bits):
    ep = [4, 1, 2, 3, 
          2, 3, 4, 1]
    permuted_bits = []

    for i in ep:
        permuted_bits.append(bits[i - 1]) 
    
    result = ''.join(permuted_bits)
    return result

# XOR entre bits a e b
def XOR(a, b):
    xor_result_list = []  

    tamanho = len(a)

    for i in range(tamanho):  
        bit1 = int(a[i])  
        bit2 = int(b[i])  
        xor_bit = bit1 ^ bit2
        xor_result_list.append(str(xor_bit))

    xor_result = ''.join(xor_result_list)
    return (xor_result)

# S-Boxes
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]


def SBoxes(bits):
    left, right = bits[:4], bits[4:]

    def CalcularSBox(bloco, sbox):
        linha = int(bloco[0] + bloco[3], 2)  # Bits 1 e 4 para linha
        coluna = int(bloco[1] + bloco[2], 2)  # Bits 2 e 3 para coluna
        return format(sbox[linha][coluna], '02b')  # Saída de 2 bits

    s0_output = CalcularSBox(left, S0)
    s1_output = CalcularSBox(right, S1)

    return s0_output + s1_output    # Saída com 4 bits


def PermutacaoP4(bits):
    p4 = [2, 4, 3, 1]
    permuted_bits = []

    for i in p4:
        permuted_bits.append(bits[i - 1]) 
    
    result = ''.join(permuted_bits)
    return result


def SwitchFunction(bits):
    return bits[4:] + bits[:4] 

# Divisão das metades do bloco de dados + Função Fk
def Fk(bits, subchave, rodada):
    left, right = bits[:4], bits[4:] 
    
    # E/P nos bits da direita
    ep_bits = ExpansaoPermutacao(right)
    
    # XOR do resultado da E/P com a subchave
    xor_result = XOR(ep_bits, subchave)
    
    # Passar pela S-Boxes
    sbox_output = SBoxes(xor_result)
    
    # Permutação P4
    p4_output = PermutacaoP4(sbox_output)
    
    # XOR com os bits da esquerda
    fk_output = XOR(left, p4_output)
    
    bloco = fk_output + right

    print(f'Bloco pós rodada {rodada} de Feistel: {bloco}')
    return bloco


def RodadasFeistelEncrypt(bloco, K1, K2):
    # Primeira rodada com K1
    bloco_1 = Fk(bloco, K1, 1)
    
    bloco_trocado = SwitchFunction(bloco_1)
    
    # Segunda rodada com K2
    bloco_2 = Fk(bloco_trocado, K2, 2)
    
    return bloco_2

# (IP⁻¹)
def PermutacaoFinal(bloco):
    ip_inv = [4, 1, 3, 5, 7, 2, 8, 6]
    permuted_block = []

    for i in ip_inv:
        permuted_block.append(bloco[i - 1]) 
    
    result = ''.join(permuted_block)
    return result

def GerarSubchaves(chaveInicial):
    chave_gerada = PermutacaoP10(chaveInicial)
    chave_gerada = CLS(chave_gerada, 1)
    k1 = PermutacaoP8(chave_gerada) # K1 gerada

    print(f'Chave K1 gerada: {k1}')
    
    chave_gerada = CLS(chave_gerada, 2) # Novo CLS é aplicado no antigo CLS, agora deslocando 2 bits
    k2 = PermutacaoP8(chave_gerada) # K2 gerada

    print(f'Chave K2 gerada: {k2}')

    return k1, k2


def Encrypt(chave10, bloco8):
    # 1. Geração de Chaves Subjacentes
    k1, k2 = GerarSubchaves(chave10)
    print('.....')

    # 2. Permutação Inicial (IP): 
    ip = PermutacaoInicial(bloco8)
    print('.....')

    # 3. Divisão em Metades + #4. Rodadas de Feistel: 
    bloco_feistel = RodadasFeistelEncrypt(ip, k1, k2)
    print('.....')

    # 5. Permutação Final (IP⁻¹):
    bloco_cifrado = PermutacaoFinal(bloco_feistel)
    
    return bloco_cifrado

# ======> DECRYPT <====== #
def RodadasFeistelDecrypt(bloco, K1, K2):
    # Primeira rodada com K1
    bloco_1 = Fk(bloco, K2, 1)      # No decrypt, utiliza-se K2 primeiro e K1 depois
    
    bloco_trocado = SwitchFunction(bloco_1)
    
    # Segunda rodada com K2
    bloco_2 = Fk(bloco_trocado, K1, 2)
    
    return bloco_2

def Decrypt(chave10, cypher8):
    # 1. Geração de Chaves Subjacentes
    k1, k2 = GerarSubchaves(chave10)
    print('.....')

    # 2. Permutação Inicial (IP): 
    ip = PermutacaoInicial(cypher8)
    print('.....')

    # 3. Divisão em Metades + # 4. Rodadas de Feistel: 
    bloco_feistel = RodadasFeistelDecrypt(ip, k1, k2)
    print('.....')

    # 5. Permutação Final (IP⁻¹):
    bloco_cifrado = PermutacaoFinal(bloco_feistel)
    
    return bloco_cifrado


if __name__ == '__main__':
    while True:
        print("\nEscolha uma opção:")
        print("1 - Encriptar")
        print("2 - Decriptar")
        print("3 - Fechar o programa")
        
        opcao = int(input("\nDigite sua opção: "))
        
        if opcao == 3:
            print("Fechando o programa...")
            break
                    
        if opcao == 1:
            # Testando o algoritmo
            chave_10 = "1010000010"
            bloco_8 = "11010111"
            print('\n.....')
            print(f'Execução do algoritmo com a chave inicial {chave_10} e com o bloco de dados {bloco_8}')
            print('.....')
            # Encriptação
            bloco_cifrado = Encrypt(chave_10, bloco_8)
            print("Bloco Cifrado:", bloco_cifrado)

        elif opcao == 2:
            # Testando o algoritmo
            chave_10 = "1010000010"
            cypher_8 = "10101000"
            print('\n.....')
            print(f'Execução do algoritmo com a chave inicial {chave_10} e com o bloco cifrado {cypher_8}')
            print('.....')
            # Encriptação
            bloco_decifrado = Decrypt(chave_10, cypher_8 )
            print("Bloco Decifrado:", bloco_decifrado)

        else:
            print("Opção inválida. Tente novamente.")