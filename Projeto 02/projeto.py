import requests
from datetime import datetime

def main():

  LIMITE_SAQUE_DIARIO = 3 # Limite de saques diários permitido
  LIMITE_OPERACAO_SAQUE = float(500) # Valor máximo permitido por operação saque
  saquesRealizados = 0 # Acumulado de saques já realizados
  saldo = float(0) # Saldo inicial
  transacoes = [] # Lista de operações realizadas
  usuarios = [] # Lista para armazenar usuários
  contas = [] # Lista para armazenar contas

  while True:
    # Receber a opção do usuário
    opcao = menu().upper()

    # Direcionar o programa de acordo com a opção escolhida
    if opcao == 'D':
      cabecalhoOperacao('Opção: Depositar')
      transacoes, saldo = depositar(transacoes, saldo)
    elif opcao == 'S':
      cabecalhoOperacao('Opção: Sacar')
      saquesRealizados, transacoes, saldo = sacar(transacoes=transacoes, saldo=saldo, saquesRealizados=saquesRealizados, limiteSaqueDiario=LIMITE_SAQUE_DIARIO, limiteOperacaoSaque=LIMITE_OPERACAO_SAQUE)
    elif opcao == 'E':
      cabecalhoOperacao('Opção: Extrato')
      extrato(transacoes, saldo=saldo)
    elif opcao == 'NU':
      cabecalhoOperacao('Opção: Cadastrar Novo Usuário')
      criarUsuario(usuarios)
    elif opcao == 'LU':
      cabecalhoOperacao('Opção: Listar Usuários')
      listarUsuarios(usuarios)
    elif opcao == 'NC':
      cabecalhoOperacao('Opção: Cadastrar Conta Corrente')
      criarContaCorrente(contas, usuarios)
    elif opcao == 'LC':
      cabecalhoOperacao('Opção: Listar Contas Corrente')
      listarContas(contas)
    elif opcao == 'Q':
      print('\nVolte Sempre!!!!')
      break


def menu():

  # Definição do menu de opções
  menu = f"""
  Escolha uma das opções abaixo:\n
  [D] - Depositar
  [S] - Sacar
  [E] - Extrato
  [NU] - Criar Novo Usuário
  [LU] - Listar Usuários
  [NC] - Criar Nova Conta Corrente
  [LC] - Listar Contas Corrente
  [Q] - Sair\n
  """

  # Retornar a opção informada pelo usuário
  cabecalhoOperacao('Menu Principal')
  return(input(menu))


# Função para imprimir o cabeçalho da operação
def cabecalhoOperacao(opcao):
  caracter = '='
  largura = 100
  linha = caracter * largura
  linhaSemTexto = caracter * (largura - len(opcao) - 2)

  linhaEsquerda = len(linhaSemTexto) // 2
  linhaDireita = linhaEsquerda if (len(linhaSemTexto) % 2 == 0) else (linhaEsquerda + 1)

  print('\n' + linha)
  print(f'{linhaEsquerda * caracter} {opcao} {linhaDireita * caracter}')
  print(linha)


# Função para validar valores de depósitos e saques informados pelo usuário
def checarValor(valor):
  try:
    valor = round(float(valor), 2)

    # Não são permitidos valores <= 0
    if valor <= 0:
      return 'NOK', '\t >>> E R R O: Informe um valor maior que 0 (zero)!'

    # Valor válido
    else:
      return 'OK', valor

  except:
    # Direcionar para a saída se se o valor informado for 's' ou 'S'
    if str(valor).upper() == 'Q':
      return 'Sair', valor

    # Sinalizar erro se o valor informado não for numérico
    else:
      return 'NOK', '\t >>> E R R O: Informe um valor numérico válido!'


def depositar(transacoes, saldo):

  while True:

    # Solicitar o valor do depósito
    retorno, valor = checarValor(input('\nInforme o valor que deseja depositar (Para sair, digite [Q]): '))

    # Realizar o depósito
    if retorno == 'OK':
      saldo += valor # Incrementa o saldo
      transacoes.append(['Depósito', valor]) # Armazena a transação
      print(f'\t >>> Depósito realizado com sucesso! Saldo disponível: R$ {saldo:.2f}')

    # Sinalizar erro
    elif retorno == 'NOK':
      print(valor)

    # Sair da operação
    elif retorno == 'Sair':
      return transacoes, saldo


def sacar(transacoes, saldo, saquesRealizados, limiteSaqueDiario, limiteOperacaoSaque):

  while True:

    # Chegar se o limite diário de saque já foi excedido
    limiteSaqueDiarioExcecido = True if saquesRealizados >= limiteSaqueDiario else False
    if limiteSaqueDiarioExcecido:
      print(f'\nVocê já atingiu a quantidade de {limiteSaqueDiario} saques diários permitidos!')
      return saquesRealizados, transacoes, saldo

    else:
      # Solicitar o valor do saque
      retorno, valor = checarValor(input('\nInforme o valor que deseja sacar (Para sair, digite [Q]): '))

      if retorno == 'OK':
        # Impedir saque se o valor for maior ao limite permitido por operação
        if valor > limiteOperacaoSaque:
          print(f'\t >>> E R R O: Seu limite de saque é de R$ {limiteOperacaoSaque:.2f} por operação!')

        # Impedir saque em caso de saldo insuficiente
        elif valor > saldo:
          print(f'\t >>> E R R O: Seu saldo disponível (R$ {saldo:.2f}) é insuficiente para esta operação!')

        # Realizar o saque
        else:
          saldo -= valor # Decrementa o saldo
          transacoes.append(['Saque', valor * -1]) # Armazena a transação
          saquesRealizados += 1 # Incrementa a quantidade de saques realizada
          print(f'\t >>> Saque realizado com sucesso! Saldo disponível: R$ {saldo:.2f}')

      # Sinalizar erro
      elif retorno == 'NOK':
        print(valor)

      # Sair da operação
      elif retorno == 'Sair':
        return saquesRealizados, transacoes, saldo


def extrato(transacoes, saldo):
  print('\nExtrato:')
  print('-' * 100)

  # Sinalizar se não houver transações
  if len(transacoes) == 0:
    print('\nNão foram realizadas movimentações!')

  # Detalha as transações
  else:
    for i in transacoes:
      print(f'{i[0]} {"." * (30 - len(i[0]))} R$ {i[1]:.2f}')
    print('-' * 100)
    print(f'Saldo disponível {"." * (30 - len("Saldo disponível"))} R$ {saldo:.2f}')


def buscar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    
    if response.status_code == 200:
        dados = response.json()
        if "erro" in dados:
            return "\t >>> E R R O: CEP não encontrado."
        else:
            return dados
    else:
        return "\t >>> E R R O: Erro ao acessar a API do ViaCEP."


def validar_nome(nome):
    partes = nome.strip().split()
    return len(partes) > 1


def validar_data(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except ValueError:
        return False


def criarUsuario(usuarios):

  while True:
    nome = input("\nInforme o nome do usuário (com pelo menos um sobrenome): ").title()
    if validar_nome(nome):
      break
    else:
      print("\t >>> E R R O: Nome inválido. Informe um nome com pelo menos um sobrenome.")


  while True:
    dataNascimento = input("\nInforme a data de nascimento do usuário (DD/MM/AAAA): ")
    if validar_data(dataNascimento):
      break
    else:
      print("\t >>> E R R O: Data de nascimento inválida. Informe uma data no formato DD/MM/AAAA.")


  while True:
    cpf = input("\nInforme o CPF do usuário (somente números): ")
    if cpf.isdigit() and len(cpf) == 11:
      if any(usuario["cpf"] == cpf for usuario in usuarios):
        print("\t >>> E R R O: CPF já cadastrado. Informe um CPF diferente.")
      else:
        break
    else:
      print("\t >>> E R R O: CPF inválido. Informe um CPF válido com 11 dígitos.")

  while True:
    cep = input("\nInforme o CEP do usuário (somente números): ")
    dadosCep = buscar_cep(cep)
    if isinstance(dadosCep, str):
      print(dadosCep)  # Mensagem de erro retornada pela função buscar_cep
    else:
      logradouro = dadosCep["logradouro"]
      bairro = dadosCep["bairro"]
      cidade = dadosCep["localidade"]
      estado = dadosCep["uf"]
      endereco = f"{logradouro}, {bairro} - {cidade} / {estado}"
      break

  while True:
    numero = input("\nInforme o número do endereço: ")
    if len(numero) > 0:
      break
    else:
      print("\t >>> E R R O: Número inválido. Informe um número válido.")
  
  endereco = f"{logradouro}, {numero} - {bairro} - {cidade} / {estado}"
  
  usuario = {
      "nome": nome,
      "dataNascimento": dataNascimento,
      "cpf": cpf,
      "endereco": endereco
  }

  usuarios.append(usuario)

  print('\nUsuário cadastrado com sucesso!!!')
  print(f'\n\t >>> Nome: {usuario["nome"]}')
  print(f'\t >>> Data de Nascimento: {usuario["dataNascimento"]}')
  print(f'\t >>> CPF: {usuario["cpf"]}')
  print(f'\t >>> Endereço: {usuario["endereco"]}')

  return usuarios


def listarUsuarios(usuarios):

  if usuarios:
    print('\nLista de Usuários:')
    print('-' * 100)

    for i in usuarios:
      print(f'Nome: {"." * (25 - len("Nome:"))} {i["nome"]}')
      print(f'CPF: {"." * (25 - len("CPF:"))} {i["cpf"]}')
      print(f'Data de Nascimento: {"." * (25 - len("Data de Nascimento:"))} {i["dataNascimento"]}')
      print(f'Endereço: {"." * (25 - len("Endereço:"))} {i["endereco"]}')
      print('-' * 100)
    
    print('Fim')
  else:
    print('\nNão existem usuários cadastrados!')


def criarContaCorrente(contas, usuarios):
    
  if not usuarios:
    print("\nNão existem usuários cadastrados!")
    print("\nCadastre pelo menos um usuário antes de cadastrar a conta corrente!")
    return
  
  agencia = "0001"
  numeroConta = len(contas) + 1

  while True:
    cpf = input("\nInforme o CPF do usuário para vincular à conta (somente números): ")
    usuario = next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)
    if usuario:
      break
    else:
      print("\t >>> Usuário não encontrado. Informe um CPF válido.")

  conta = {
      "agencia": agencia,
      "numeroConta": numeroConta,
      "usuario": usuario
  }
  
  contas.append(conta)
  
  print(f'\nConta corrente criada com sucesso!')
  print(f'\t >>> Agência: {conta["agencia"]}')
  print(f'\t >>> Número da Conta: {conta["numeroConta"]}')
  print(f'\t >>> Usuário: {conta["usuario"]["nome"]}')
  
  return contas


def listarContas(contas):

  if contas:
    print('\nLista de Contas:')
    print('-' * 100)

    for i in contas:
      print(f'Agência: {"." * (25 - len("Agência:"))} {i["agencia"]}')
      print(f'Número da Conta: {"." * (25 - len("Número da Conta:"))} {i["numeroConta"]}')
      print(f'Usuário: {"." * (25 - len("Usuário:"))} {i["usuario"]["nome"]}')
      print(f'CPF: {"." * (25 - len("CPF:"))} {i["usuario"]["cpf"]}')
      print('-' * 100)
    
    print('\nFim da relação de Contas!')
  else:
    print('\nNão existem contas cadastradas!')


if __name__ == '__main__':
  main()
