from datetime import date
from typing import List


# Classe base para transações
class Transacao:
  def __init__(self, valor: float):
    self.valor = valor
  
  def registrar(self, conta: 'Conta'):
    raise NotImplementedError("Método deve ser implementado nas subclasses")


# Classe para depósitos, herda de Transacao
class Deposito(Transacao):
  def registrar(self, conta: 'Conta'):
    conta.saldo += self.valor
    conta.historico.adicionarTransacao(self)


# Classe para saques, herda de Transacao
class Saque(Transacao):
  def registrar(self, conta: 'Conta'):
    if conta.saldo >= self.valor:
      conta.saldo -= self.valor
      conta.historico.adicionarTransacao(self)
      return True
    return False


# Classe para histórico de transações
class Historico:
  def __init__(self):
    self.transacoes: List[Transacao] = []
  
  def adicionarTransacao(self, transacao: Transacao):
    self.transacoes.append(transacao)


# Classe para contas bancárias
class Conta:
  def __init__(self, numero: int, agencia: str, cliente: 'Cliente'):
    self.saldo = 0.0
    self.numero = numero
    self.agencia = agencia
    self.cliente = cliente
    self.historico = Historico()
  
  def saldo(self) -> float:
    return self.saldo
  
  @classmethod
  def novaConta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
    return cls(numero, "0001", cliente)
  
  def sacar(self, valor: float) -> bool:
    saque = Saque(valor)
    return saque.registrar(self)
  
  def depositar(self, valor: float) -> bool:
    deposito = Deposito(valor)
    deposito.registrar(self)
    return True


# Classe para clientes
class Cliente:
  def __init__(self, endereco: str):
    self.endereco = endereco
    self.contas: List[Conta] = []
  
  def realizar_transacao(self, conta: Conta, transacao: Transacao):
    transacao.registrar(conta)
  
  def adicionar_conta(self, conta: Conta):
    self.contas.append(conta)


# Classe para conta corrente, herda de Conta
class ContaCorrente(Conta):
  def __init__(self, numero: int, agencia: str, cliente: Cliente, limite: float, limiteSaques: int):
    super().__init__(numero, agencia, cliente)
    self.limite = limite
    self.limiteSaques = limiteSaques


# Classe para pessoas físicas, herda de Cliente
class PessoaFisica(Cliente):
  def __init__(self, cpf: str, nome: str, dataNascimento: date, endereco: str):
    super().__init__(endereco)
    self.cpf = cpf
    self.nome = nome
    self.dataNascimento = dataNascimento


# Exemplo de uso
cliente = PessoaFisica("123.456.789-00", "Rodolfo Martins", date(1990, 1, 1), "Rua Exemplo, 123")
conta = Conta.novaConta(cliente, 1001)
cliente.adicionar_conta(conta)


# Realiza um depósito
conta.depositar(200.0)


# Realiza um saque
conta.sacar(50.0)


# Imprime saldo e histórico de transações
print(f"\nSaldo atual: R${conta.saldo}")

print('\nTransações:')

for transacao in conta.historico.transacoes:
  print(f"\t{'Depósito' if isinstance(transacao, Deposito) else 'Saque'} de R${transacao.valor:.2f}")
