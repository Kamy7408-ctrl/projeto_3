from steampy import SteamPy


def menu():
    sistema = SteamPy()
    sistema.carregar_jogos('games.csv')

    while True:
        print('\n====== STEAMPY ======')
        print('1 - Listar jogos')
        print('2 - Buscar jogo por nome')
        print('3 - Filtrar por gênero')
        print('4 - Filtrar por console')
        print('5 - Filtrar por nota mínima')
        print('6 - Filtrar por vendas mínimas')
        print('7 - Filtrar por publisher')
        print('8 - Ordenar catálogo')
        print('9 - Adicionar jogo ao backlog')
        print('10 - Ver backlog')
        print('11 - Jogar próximo do backlog')
        print('12 - Ver jogos recentes')
        print('13 - Retomar último jogo')
        print('14 - Registrar tempo de jogo')
        print('15 - Ver histórico completo')
        print('16 - Ver recomendações')
        print('17 - Ver ranking pessoal')
        print('18 - Ver dashboard')
        print('19 - Salvar dados')
        print('20 - Sair')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            sistema.listar_jogos()

        elif opcao == '2':
            nome = input('Digite parte do nome do jogo: ')
            sistema.buscar_por_nome(nome)

        elif opcao == '3':
            genero = input('Digite o gênero: ')
            sistema.filtrar_genero(genero)

        elif opcao == '4':
            console = input('Digite o console: ')
            sistema.filtrar_console(console)

        elif opcao == '5':
            try:
                nota = float(input('Digite a nota mínima: '))
                sistema.filtrar_nota(nota)
            except:
                print('Nota inválida.')

        elif opcao == '6':
            try:
                vendas = float(input('Digite as vendas mínimas: '))
                sistema.filtrar_vendas(vendas)
            except:
                print('Valor inválido.')

        elif opcao == '7':
            publisher = input('Digite o publisher: ')
            sistema.filtrar_publisher(publisher)

        elif opcao == '8':
            print('1 - Título')
            print('2 - Nota')
            print('3 - Vendas totais')
            print('4 - Data de lançamento')
            print('5 - Console')
            print('6 - Gênero')
            escolha = input('Ordenar por: ')
            sistema.ordenar_catalogo(escolha)

        elif opcao == '9':
            try:
                id_jogo = int(input('Digite o ID do jogo: '))
                sistema.adicionar_backlog(id_jogo)
            except:
                print('ID inválido.')

        elif opcao == '10':
            sistema.ver_backlog()

        elif opcao == '11':
            sistema.jogar_proximo_backlog()

        elif opcao == '12':
            sistema.ver_recentes()

        elif opcao == '13':
            sistema.retomar_ultimo_jogo()

        elif opcao == '14':
            try:
                id_jogo = int(input('Digite o ID do jogo: '))
                sistema.registrar_tempo_jogo(id_jogo)
            except:
                print('ID inválido.')

        elif opcao == '15':
            sistema.ver_historico()

        elif opcao == '16':
            sistema.recomendacoes()

        elif opcao == '17':
            sistema.ranking_pessoal()

        elif opcao == '18':
            sistema.dashboard()

        elif opcao == '19':
            sistema.salvar_backlog()
            sistema.salvar_historico()
            sistema.salvar_recentes()

        elif opcao == '20':
            sistema.salvar_backlog()
            sistema.salvar_historico()
            sistema.salvar_recentes()
            print('Saindo do sistema...')
            break

        else:
            print('Opção inválida.')


menu()