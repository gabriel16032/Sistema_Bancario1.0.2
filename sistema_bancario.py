from datetime import datetime

transacoes = []
contador_saq = 0
maximo_saques_dia = 10



class ContasUsuarios:
    def __init__(self):
        self.cadastros = {}

    def cria_usuario(self):
        while True:
            cpf = input("CPF a cadastrar: ")

            if cpf in self.cadastros:
                print("CPF já cadastrado!")
            else:
                break

        nome = input("Nome: ")
        data_nascimento_str = input("Data de nascimento: ")
        data_nascimento = self.converte_data(data_nascimento_str)


        rua = input("Rua, nro: ")
        bairro = input("Bairro: ")
        cidade_est = input("Cidade/estado: ")
        endereco = {"Rua": rua, "Bairro": bairro, "Cidade/Estado": cidade_est}

        dados = {"Nome": nome, "Data de Nascimento": data_nascimento, "Endereço": endereco}

        self.cadastros[cpf] = dados

        print(f"USUÁRIO CRIADO: {dados}")

    def converte_data(self, data_nascimento_str):
            if len(data_nascimento_str) == 8:
                data_nascimento_str = f"{data_nascimento_str[:2]}/{data_nascimento_str[2:4]}/{data_nascimento_str[4:]}"

                try:
                    data_nascimento = datetime.strptime(data_nascimento_str, "%d/%m/%Y")

                    return data_nascimento_str


                except ValueError:
                    print("Data inválida!")
                    return None
            else:
                print("Data inválida!")
                return None

    def exibe_usuario(self, ):
        cpf = input("CPF do usuário a consultar: ")

        if cpf in self.cadastros:
            dados = self.cadastros[cpf]
            print("USUÁRIO".center(20, "="))
            print(f"""Nome: {dados['Nome']}
Data de nascimento: {dados['Data de Nascimento']}
Endereço: {dados['Endereço']['Rua']}
Bairro: {dados['Endereço']['Bairro']}
Cidade: {dados['Endereço']['Cidade/Estado']}
Agência: {dados.get('Conta', {}).get('Agência', {})}
Número da Conta: {dados.get('Conta', {}).get('Nro da Conta', {})}
====================""") #caso não haja conta associada ao usuário, nenhuma conta é mostrada.

clientes = ContasUsuarios()

class ContasBanc:
    def __init__(self, clientes):
        self.clientes = clientes
    
    def cria_cc(self): #CRIA CONTA CORRENTE E ENVIA OS DADOS DA CONTA PARA O DICIONÁRIO CPF
        agencia = input("Insira a agencia: ")
        nro_conta = input("Insira o número da conta: ")
        conta = {"Agência": agencia, "Nro Conta": nro_conta}

        atribuicao = input("Insira o CPF do usuário da conta: ")

        if atribuicao in clientes.cadastros:
            self.clientes.cadastros[atribuicao]['Conta'] = conta
        else:
            print("É necessário criar o usuário antes de criar uma nova conta!")

        print(self.clientes.cadastros)

conta_corrente = ContasBanc(clientes)

def saque(saldo, valor):

     while True:
         valor = float(input("SACAR: "))

         global contador_saq, maximo_saques_dia

         if contador_saq >= maximo_saques_dia:
             print("Você atingiu o limite de saques no dia, volte amanhã.")
             break

         if valor <= 500:
             if saldo >= valor:
                 saldo -= valor
                 contador_saq += 1
                 print(f"SAQUE REALIZADO: R${saldo:.2f}")
                 registrar_trans("Saque", valor)
                 break
             else:
                 print(f"SALDO INSUFICIENTE, seu saldo é R${saldo:.2f}")
         else:
             print("EXCEDEU LIMITE DE VALOR DE SAQUE! Deve ser menor que R$500,00.")  

     return saldo

def deposito(saldo, valor):
     while True:
         valor = float(input("DEPOSITAR: "))

         if valor > 0:
             saldo += valor
             print(f"DEPOSITO REALIZADO: R${saldo:.2f}")
             registrar_trans("Depósito", valor)
             break

         else:
             print("ERRO! Insira um valor positivo.")

     return saldo

def registrar_trans(tipo, valor):
     data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

     transacao = {"tipo": tipo, "valor": valor, "data_hora": data_hora}

     transacoes.append(transacao)

def mostrar_extrato():
     print("EXTRATO".center(50, "="))
     if transacoes: 

         for transacao in transacoes:
             print(f"{transacao ['data_hora']} {transacao['tipo']}: R${transacao['valor']}")
            
     else:
         print("Nenhuma transação registrada.")

def iniciar():
     saldo = 0
     valor = 0
     
     while True:
        print(" BANCO NSCRED ".center (30, "="))
        menu = input("[U] Usuários\n[O] Operações:\n").upper()

        if menu == "U":
            while True:
                menu_usr = input("[C] Criar conta corrente\n[U] Criar usuário\n[EU] Exibir Usuário\n[0] Voltar\n").upper()

                if menu_usr == "U":
                    clientes.cria_usuario()
                elif menu_usr == "EU":
                    clientes.exibe_usuario()
                elif menu_usr == "C":
                    conta_corrente.cria_cc()
                elif menu_usr == "0":
                    break

        if menu == "O":
            menu_opr = input("[D] Depósito\n[S] Sacar\n[E] Extrato\n[0] Sair:\n").upper()

            if menu_opr == "D":
                saldo = deposito(saldo, valor)


            elif menu_opr == "S":
                saldo = saque(saldo, valor)
            
            elif menu_opr == "E":
                mostrar_extrato()
            
            elif menu_opr == "0":
                print("Saindo...")
                break

            else:
                print("Solicitação inválida.")
                break



iniciar()







