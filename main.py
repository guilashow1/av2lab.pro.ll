
usuarios = {}  
estudantes = {}  
cursos = {}  
notas = {}  
professores = {} 

def cadastrar_usuario(tipo_usuario="administrador"):
    while True:
        usuario = input(f"Digite o nome do {tipo_usuario}: ")
        if usuario in usuarios:
            print(f"Este {tipo_usuario} já existe! Tente outro nome.")
        else:
            break
    senha = input(f"Digite a senha do {tipo_usuario}: ")
    usuarios[usuario] = {"senha": senha, "tipo": tipo_usuario}
    print(f"{tipo_usuario.capitalize()} {usuario} cadastrado com sucesso!")


def login():
    usuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")
    if usuario in usuarios and usuarios[usuario]["senha"] == senha:
        print(f"Bem-vindo, {usuario}!")
        return usuario
    else:
        print("Login inválido! Usuário ou senha incorretos.")
        return None


def cadastrar_estudante():
    matricula = input("Digite o número de matrícula do estudante: ")
    if matricula in estudantes:
        print("Este estudante já está cadastrado.")
        return
    nome = input("Digite o nome do estudante: ")
    email = input("Digite o e-mail do estudante: ")
    curso = input("Digite o curso do estudante: ")
    estudantes[matricula] = {"nome": nome, "email": email, "curso": curso}
    print(f"Estudante {nome} cadastrado com sucesso!")


def cadastrar_professor():
    email = input("Digite o e-mail do professor: ")
    if email in professores:
        print("Este professor já está cadastrado.")
        return
    nome = input("Digite o nome do professor: ")
    professores[email] = {"nome": nome}
    print(f"Professor {nome} cadastrado com sucesso!")


def cadastrar_curso():
    codigo_curso = input("Digite o código do curso: ")
    if codigo_curso in cursos:
        print("Este curso já está cadastrado.")
        return
    nome_curso = input("Digite o nome do curso: ")
    creditos = int(input("Digite o número de créditos do curso: "))

    
    print("Professores disponíveis:")
    for email, dados in professores.items():
        print(f"{dados['nome']} (E-mail: {email})")

    professor_email = input("Digite o e-mail do professor responsável pelo curso: ")
    if professor_email not in professores:
        print("Professor não encontrado! Cadastre o professor primeiro.")
        return

    cursos[codigo_curso] = {"nome": nome_curso, "creditos": creditos, "professor": professor_email}
    print(f"Curso {nome_curso} cadastrado com sucesso, sob responsabilidade do professor {professores[professor_email]['nome']}.")


def registrar_nota(usuario_logado):
    if usuarios[usuario_logado]["tipo"] == "professor":
        professor_email = usuario_logado
        cursos_do_professor = [codigo for codigo, dados in cursos.items() if dados["professor"] == professor_email]
        print(f"Cursos que você leciona: {cursos_do_professor}")
    else:
        cursos_do_professor = cursos.keys()

    matricula = input("Digite a matrícula do estudante: ")
    if matricula in estudantes:
        codigo_curso = input("Digite o código do curso: ")
        if codigo_curso in cursos_do_professor:
            nota = float(input("Digite a nota do estudante: "))
            if matricula not in notas:
                notas[matricula] = {}
            notas[matricula][codigo_curso] = nota
            print(f"Nota {nota} registrada para o estudante {estudantes[matricula]['nome']} no curso {cursos[codigo_curso]['nome']}")
        else:
            print("Você não tem permissão para registrar notas nesse curso!")
    else:
        print("Estudante não encontrado!")


def exibir_estudantes():
    if estudantes:
        print("\nLista de Estudantes:")
        for matricula, dados in estudantes.items():
            print(f"Matrícula: {matricula}, Nome: {dados['nome']}, E-mail: {dados['email']}, Curso: {dados['curso']}")
    else:
        print("Nenhum estudante cadastrado.")


def exibir_professores():
    if professores:
        print("\nLista de Professores:")
        for email, dados in professores.items():
            print(f"Nome: {dados['nome']}, E-mail: {email}")
    else:
        print("Nenhum professor cadastrado.")


def exibir_cursos():
    if cursos:
        print("\nLista de Cursos:")
        for codigo, dados in cursos.items():
            professor_email = dados['professor']
            professor_nome = professores[professor_email]['nome']
            print(f"Código: {codigo}, Nome: {dados['nome']}, Créditos: {dados['creditos']}, Professor: {professor_nome}")
    else:
        print("Nenhum curso cadastrado.")


def exibir_notas():
    matricula = input("Digite a matrícula do estudante: ")
    if matricula in estudantes:
        print(f"Notas do estudante {estudantes[matricula]['nome']}:")
        if matricula in notas:
            for codigo_curso, nota in notas[matricula].items():
                print(f"Curso: {cursos[codigo_curso]['nome']}, Nota: {nota}")
        else:
            print("Este estudante ainda não possui notas registradas.")
    else:
        print("Estudante não encontrado!")


def verificar_admins():
    if not usuarios:
        print("Vamos cadastrar o primeiro administrador do sistema.")
        cadastrar_usuario("administrador")


def verificar_permissao(usuario, tipos_permitidos=["administrador"]):
    if usuarios[usuario]["tipo"] in tipos_permitidos:
        return True
    else:
        print("Acesso negado. Você não tem permissão para realizar esta ação.")
        return False


def menu():
    verificar_admins()

    usuario_logado = login()
    if not usuario_logado:
        return

    while True:
        print("\nMenu Acadêmico:")
        print("1 - Cadastrar estudante")
        print("2 - Cadastrar curso")
        print("3 - Cadastrar professor")
        print("4 - Registrar nota")
        print("5 - Exibir estudantes")
        print("6 - Exibir cursos")
        print("7 - Exibir professores")
        print("8 - Exibir notas de um estudante")
        print("9 - Cadastrar novo usuário (Administrador, Coordenador, Professor, Aluno)")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            if verificar_permissao(usuario_logado, ["administrador", "coordenador"]):
                cadastrar_estudante()
        elif opcao == '2':
            if verificar_permissao(usuario_logado, ["administrador", "coordenador"]):
                cadastrar_curso()
        elif opcao == '3':
            if verificar_permissao(usuario_logado, ["administrador", "coordenador"]):
                cadastrar_professor()
        elif opcao == '4':
            if verificar_permissao(usuario_logado, ["administrador", "professor"]):
                registrar_nota(usuario_logado)
        elif opcao == '5':
            if verificar_permissao(usuario_logado, ["administrador", "coordenador"]):
                exibir_estudantes()
        elif opcao == '6':
            exibir_cursos()
        elif opcao == '7':
            exibir_professores()
        elif opcao == '8':
            exibir_notas()
        elif opcao == '9':
            if verificar_permissao(usuario_logado, ["administrador"]):
                tipo = input("Digite o tipo de usuário a ser cadastrado (administrador, coordenador, professor, aluno): ").lower()
                if tipo in ["administrador", "coordenador", "professor", "aluno"]:
                    cadastrar_usuario(tipo)
                else:
                    print("Tipo de usuário inválido.")
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
