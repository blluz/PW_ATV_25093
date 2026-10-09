# -*- coding: utf-8 -*-
"""
SISTEMA DE GERENCIAMENTO DE AULAS ESCOLARES - Versão 1
Dados armazenados em listas durante a execução do programa.
"""

from datetime import datetime

# ---------------------------------------------------------------
# "Banco de dados" em memória
# ---------------------------------------------------------------
professores = []   # {"nome", "disciplina", "aulas_semanais"}
turmas = []        # {"nome", "serie", "periodo"}
disciplinas = []   # {"nome", "carga_horaria"}
aulas = []         # {"id", "professor", "turma", "disciplina", "data",
                   #  "previstas", "status", "reposicao"}

# status possíveis de uma aula (só um por vez, nunca dois ao mesmo tempo)
AGENDADA = "Agendada"
MINISTRADA = "Ministrada"
NAO_MINISTRADA = "Não ministrada"

PERIODOS_VALIDOS = ["manhã", "tarde", "noite"]


# ---------------------------------------------------------------
# Funções auxiliares de entrada
# ---------------------------------------------------------------
def ler_texto(mensagem):
    """Lê um texto e repete até que não seja vazio."""
    while True:
        valor = input(mensagem).strip()
        if valor != "":
            return valor
        print("Erro: este campo não pode ficar vazio.")


def ler_inteiro_positivo(mensagem):
    """Lê um número inteiro maior que zero."""
    while True:
        valor = input(mensagem).strip()
        if not valor.isdigit():
            print("Erro: digite apenas números inteiros.")
        elif int(valor) <= 0:
            print("Erro: o valor deve ser maior que zero.")
        else:
            return int(valor)


def ler_data(mensagem):
    """Lê uma data no formato DD/MM/AAAA e valida."""
    while True:
        valor = input(mensagem).strip()
        try:
            datetime.strptime(valor, "%d/%m/%Y")
            return valor
        except ValueError:
            print("Erro: data inválida. Use o formato DD/MM/AAAA.")


def buscar_por_nome(lista, nome):
    """Procura um item pelo nome (ignorando maiúsculas/minúsculas)."""
    for item in lista:
        if item["nome"].lower() == nome.lower():
            return item
    return None


def normalizar_periodo(texto):
    """Aceita 'manha' ou 'manhã', etc. Retorna o período ou None."""
    texto = texto.strip().lower()
    if texto == "manha":
        texto = "manhã"
    if texto in PERIODOS_VALIDOS:
        return texto
    return None


# ---------------------------------------------------------------
# Etapa 2 - Cadastro de professores
# ---------------------------------------------------------------
def cadastrar_professor():
    print("\n--- CADASTRAR PROFESSOR ---")
    nome = ler_texto("Nome: ")
    if buscar_por_nome(professores, nome) is not None:
        print("Erro: já existe um professor cadastrado com esse nome.")
        return
    disciplina = ler_texto("Disciplina: ")
    aulas_semanais = ler_inteiro_positivo("Aulas semanais: ")

    professores.append({
        "nome": nome,
        "disciplina": disciplina,
        "aulas_semanais": aulas_semanais,
    })
    print("Professor cadastrado com sucesso!")


# ---------------------------------------------------------------
# Etapa 3 - Cadastro de turmas
# ---------------------------------------------------------------
def cadastrar_turma():
    print("\n--- CADASTRAR TURMA ---")
    nome = ler_texto("Nome da turma (ex.: 2º DS A): ")
    if buscar_por_nome(turmas, nome) is not None:
        print("Erro: já existe uma turma cadastrada com esse nome.")
        return
    serie = ler_texto("Série (ex.: 2ª Série): ")

    while True:
        periodo = normalizar_periodo(input("Período (manhã, tarde ou noite): "))
        if periodo is not None:
            break
        print("Erro: período inválido. Digite manhã, tarde ou noite.")

    turmas.append({"nome": nome, "serie": serie, "periodo": periodo})
    print("Turma cadastrada com sucesso!")
    print(f"{nome} – {serie} – {periodo.capitalize()}")


# ---------------------------------------------------------------
# Etapa 4 - Cadastro de disciplinas
# ---------------------------------------------------------------
def cadastrar_disciplina():
    print("\n--- CADASTRAR DISCIPLINA ---")
    nome = ler_texto("Nome da disciplina: ")
    if buscar_por_nome(disciplinas, nome) is not None:
        print("Erro: já existe uma disciplina cadastrada com esse nome.")
        return
    carga = ler_inteiro_positivo("Carga horária semanal (aulas): ")

    disciplinas.append({"nome": nome, "carga_horaria": carga})
    print("Disciplina cadastrada com sucesso!")
    print(f"{nome} – {carga} aulas semanais")


# ---------------------------------------------------------------
# Etapa 6 - Controle de faltas (usado após o registro e pela opção 6)
# ---------------------------------------------------------------
def registrar_ocorrencia(aula):
    """Pergunta se o professor compareceu e atualiza a aula."""
    if aula["status"] != AGENDADA:
        print("Esta aula já teve sua ocorrência registrada.")
        return

    while True:
        resposta = input("Professor compareceu? (SIM/NAO): ").strip().lower()
        if resposta in ("sim", "s"):
            compareceu = True
            break
        elif resposta in ("nao", "não", "n"):
            compareceu = False
            break
        print("Erro: responda SIM ou NÃO.")

    # A aula recebe apenas UM status: ministrada OU não ministrada
    if compareceu:
        aula["status"] = MINISTRADA
        aula["reposicao"] = 0
        situacao = "Aula ministrada"
    else:
        aula["status"] = NAO_MINISTRADA
        aula["reposicao"] = aula["previstas"]
        situacao = "Aulas pendentes de reposição"

    print("\nREGISTRO DE OCORRÊNCIA")
    print(f"Professor: {aula['professor']}")
    print(f"Turma: {aula['turma']}")
    print(f"Disciplina: {aula['disciplina']}")
    print(f"Aulas previstas: {aula['previstas']}")
    print(f"Professor compareceu? {'SIM' if compareceu else 'NÃO'}")
    print(f"Situação: {situacao}")
    if not compareceu:
        print(f"Quantidade: {aula['reposicao']} aulas")


def registrar_falta_professor():
    print("\n--- REGISTRAR FALTA / PRESENÇA DO PROFESSOR ---")
    pendentes = []
    for aula in aulas:
        if aula["status"] == AGENDADA:
            pendentes.append(aula)

    if len(pendentes) == 0:
        print("Não há aulas aguardando registro de presença.")
        return

    print("Aulas aguardando registro:")
    for aula in pendentes:
        print(f"  [{aula['id']}] {aula['data']} | {aula['professor']} | "
              f"{aula['turma']} | {aula['disciplina']} | "
              f"{aula['previstas']} aula(s)")

    while True:
        numero = ler_inteiro_positivo("Digite o número (ID) da aula: ")
        escolhida = None
        for aula in pendentes:
            if aula["id"] == numero:
                escolhida = aula
        if escolhida is not None:
            break
        print("Erro: ID inválido ou aula já registrada.")

    registrar_ocorrencia(escolhida)


# ---------------------------------------------------------------
# Etapa 5 - Registro de aulas
# ---------------------------------------------------------------
def registrar_aula():
    print("\n--- REGISTRAR AULA ---")

    if len(professores) == 0 or len(turmas) == 0 or len(disciplinas) == 0:
        print("Antes de registrar uma aula, cadastre ao menos um professor, "
              "uma turma e uma disciplina.")
        return

    # Professor
    while True:
        nome_prof = ler_texto("Nome do professor: ")
        professor = buscar_por_nome(professores, nome_prof)
        if professor is not None:
            break
        print("Erro: professor não encontrado. Cadastrados: "
              + ", ".join(p["nome"] for p in professores))

    # Turma
    while True:
        nome_turma = ler_texto("Turma: ")
        turma = buscar_por_nome(turmas, nome_turma)
        if turma is not None:
            break
        print("Erro: turma não encontrada. Cadastradas: "
              + ", ".join(t["nome"] for t in turmas))

    # Disciplina
    while True:
        nome_disc = ler_texto("Disciplina: ")
        disciplina = buscar_por_nome(disciplinas, nome_disc)
        if disciplina is not None:
            break
        print("Erro: disciplina não encontrada. Cadastradas: "
              + ", ".join(d["nome"] for d in disciplinas))

    data = ler_data("Data da aula (DD/MM/AAAA): ")
    previstas = ler_inteiro_positivo("Número de aulas previstas para o dia: ")

    nova_aula = {
        "id": len(aulas) + 1,
        "professor": professor["nome"],
        "turma": turma["nome"],
        "disciplina": disciplina["nome"],
        "data": data,
        "previstas": previstas,
        "status": AGENDADA,
        "reposicao": 0,
    }
    aulas.append(nova_aula)
    print("Aula cadastrada com sucesso!")

    # Já aproveita para perguntar sobre a presença do professor
    while True:
        agora = input("Deseja registrar a presença do professor agora? (S/N): ").strip().lower()
        if agora in ("s", "sim"):
            registrar_ocorrencia(nova_aula)
            break
        elif agora in ("n", "nao", "não"):
            print("Você poderá registrar depois pela opção 6 do menu.")
            break
        print("Erro: responda S ou N.")


# ---------------------------------------------------------------
# Etapa 7 - Consulta e relatório
# ---------------------------------------------------------------
def imprimir_aula(aula):
    linha = (f"[{aula['id']}] {aula['data']} | {aula['professor']} | "
             f"{aula['turma']} | {aula['disciplina']} | "
             f"Previstas: {aula['previstas']} | {aula['status']}")
    if aula["reposicao"] > 0:
        linha += f" | Reposição pendente: {aula['reposicao']}"
    print(linha)


def consultar_aulas():
    print("\n--- CONSULTAR AULAS ---")
    if len(aulas) == 0:
        print("Nenhuma aula registrada ainda.")
        return

    print("1 - Todas as aulas")
    print("2 - Somente aulas pendentes de reposição")
    while True:
        filtro = input("Escolha: ").strip()
        if filtro in ("1", "2"):
            break
        print("Erro: opção inválida.")

    encontrou = False
    for aula in aulas:
        if filtro == "1" or aula["reposicao"] > 0:
            imprimir_aula(aula)
            encontrou = True
    if not encontrou:
        print("Nenhuma aula pendente de reposição.")


def relatorio_aulas():
    print("\n--- RELATÓRIO DE AULAS ---")
    total_previstas = 0
    ministradas = 0
    nao_ministradas = 0
    reposicao = 0
    aguardando = 0

    # Valores calculados a partir dos registros
    for aula in aulas:
        total_previstas += aula["previstas"]
        if aula["status"] == MINISTRADA:
            ministradas += aula["previstas"]
        elif aula["status"] == NAO_MINISTRADA:
            nao_ministradas += aula["previstas"]
            reposicao += aula["reposicao"]
        else:
            aguardando += aula["previstas"]

    print(f"Total de aulas previstas:        {total_previstas}")
    print(f"Aulas ministradas:               {ministradas}")
    print(f"Aulas não ministradas:           {nao_ministradas}")
    print(f"Aulas pendentes de reposição:    {reposicao}")
    if aguardando > 0:
        print(f"Aulas aguardando confirmação:    {aguardando}")


# ---------------------------------------------------------------
# Etapa 1 - Menu principal
# ---------------------------------------------------------------
def mostrar_menu():
    print("\n==============================")
    print("   SISTEMA DE CONTROLE ESCOLAR")
    print("==============================")
    print("1 - Cadastrar professor")
    print("2 - Cadastrar turma")
    print("3 - Cadastrar disciplina")
    print("4 - Registrar aula")
    print("5 - Consultar aulas")
    print("6 - Registrar falta do professor")
    print("7 - Relatório de aulas")
    print("8 - Sair do sistema")


def main():
    opcao = ""
    while opcao != "8":
        mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_professor()
        elif opcao == "2":
            cadastrar_turma()
        elif opcao == "3":
            cadastrar_disciplina()
        elif opcao == "4":
            registrar_aula()
        elif opcao == "5":
            consultar_aulas()
        elif opcao == "6":
            registrar_falta_professor()
        elif opcao == "7":
            relatorio_aulas()
        elif opcao == "8":
            print("Encerrando o sistema. Até logo!")
        else:
            print("Opção inválida! Digite um número de 1 a 8.")


main()
