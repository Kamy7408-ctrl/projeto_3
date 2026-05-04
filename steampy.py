from jogo import Jogo
from filabacklog import FilaBackLog
from pilharecentes import PilhaRecentes
from sessaojogo import SessaoJogo
from datetime import datetime


class SteamPy:
    def __init__(self):
        self.catalogo = []
        self.jogos_por_id = {}
        self.backlog = FilaBackLog()
        self.recentes = PilhaRecentes()
        self.historico = []
        self.tempos_por_jogo = {}

    def converter_float(self, valor):
        try:
            if valor == '':
                return 0.0
            return float(valor)
        except:
            return 0.0

    def carregar_jogos(self, nome_arquivo):
        try:
            arquivo = open(nome_arquivo, 'r', encoding='utf-8')
            linhas = arquivo.readlines()
            arquivo.close()

            self.catalogo = []
            self.jogos_por_id = {}

            for i in range(1, len(linhas)):
                linha = linhas[i].strip()

                if linha == '':
                    continue

                dados = linha.split(',')

                if len(dados) < 13:
                    continue

                id_jogo = i
                titulo = dados[1]
                console = dados[2]
                genero = dados[3]
                publisher = dados[4]
                developer = dados[5]
                critic_score = self.converter_float(dados[6])
                total_vendas = self.converter_float(dados[7])
                vendas_an = self.converter_float(dados[8])
                vendas_jp = self.converter_float(dados[9])
                vendas_eu = self.converter_float(dados[10])
                outras_vendas = self.converter_float(dados[11])
                data_lanc = dados[12]

                jogo = Jogo(id_jogo, titulo, console, genero, publisher,
                            developer, critic_score, total_vendas,
                            vendas_an, vendas_jp, vendas_eu,
                            outras_vendas, data_lanc)

                self.catalogo.append(jogo)
                self.jogos_por_id[id_jogo] = jogo

            print('Catálogo carregado com sucesso!')
            print(f'Total de jogos carregados: {len(self.catalogo)}')

        except FileNotFoundError:
            print('Arquivo não encontrado.')

    def listar_jogos(self):
        if len(self.catalogo) == 0:
            print('Nenhum jogo carregado.')
            return

        for jogo in self.catalogo:
            jogo.exibir()

    def buscar_por_nome(self, nome):
        encontrados = []

        for jogo in self.catalogo:
            if nome.lower() in jogo.titulo.lower():
                encontrados.append(jogo)

        self.mostrar_lista(encontrados)

    def filtrar_genero(self, genero):
        resultado = []

        for jogo in self.catalogo:
            if jogo.genero.lower() == genero.lower():
                resultado.append(jogo)

        self.mostrar_lista(resultado)

    def filtrar_console(self, console):
        resultado = []

        for jogo in self.catalogo:
            if jogo.console.lower() == console.lower():
                resultado.append(jogo)

        self.mostrar_lista(resultado)

    def filtrar_nota(self, nota):
        resultado = []

        for jogo in self.catalogo:
            if jogo.critic_score >= nota:
                resultado.append(jogo)

        self.mostrar_lista(resultado)

    def filtrar_vendas(self, vendas):
        resultado = []

        for jogo in self.catalogo:
            if jogo.total_vendas >= vendas:
                resultado.append(jogo)

        self.mostrar_lista(resultado)

    def filtrar_publisher(self, publisher):
        resultado = []

        for jogo in self.catalogo:
            if publisher.lower() in jogo.publisher.lower():
                resultado.append(jogo)

        self.mostrar_lista(resultado)

    def ordenar_catalogo(self, opcao):
        lista = self.catalogo.copy()

        if opcao == '1':
            lista.sort(key=lambda jogo: jogo.titulo)
        elif opcao == '2':
            lista.sort(key=lambda jogo: jogo.critic_score, reverse=True)
        elif opcao == '3':
            lista.sort(key=lambda jogo: jogo.total_vendas, reverse=True)
        elif opcao == '4':
            lista.sort(key=lambda jogo: jogo.data_lanc)
        elif opcao == '5':
            lista.sort(key=lambda jogo: jogo.console)
        elif opcao == '6':
            lista.sort(key=lambda jogo: jogo.genero)
        else:
            print('Opção inválida.')
            return

        self.mostrar_lista(lista)

    def mostrar_lista(self, lista):
        if len(lista) == 0:
            print('Nenhum resultado encontrado.')
            return

        for jogo in lista:
            jogo.exibir()

    def adicionar_backlog(self, id_jogo):
        if id_jogo not in self.jogos_por_id:
            print('Jogo não encontrado.')
            return

        if self.backlog.contem(id_jogo):
            print('Esse jogo já está no backlog.')
            return

        jogo = self.jogos_por_id[id_jogo]
        self.backlog.enqueue(jogo)
        print('Jogo adicionado ao backlog.')

    def ver_backlog(self):
        self.backlog.mostrar()

    def jogar_proximo_backlog(self):
        jogo = self.backlog.dequeue()

        if jogo is None:
            print('Backlog vazio.')
            return

        print('Iniciando jogo do backlog:')
        jogo.exibir()
        self.registrar_tempo_jogo_objeto(jogo)

    def ver_recentes(self):
        self.recentes.mostrar()

    def retomar_ultimo_jogo(self):
        jogo = self.recentes.topo()

        if jogo is None:
            print('Nenhum jogo recente para retomar.')
            return

        print('Retomando último jogo:')
        jogo.exibir()
        self.registrar_tempo_jogo_objeto(jogo)

    def registrar_tempo_jogo(self, id_jogo):
        if id_jogo not in self.jogos_por_id:
            print('Jogo não encontrado.')
            return

        jogo = self.jogos_por_id[id_jogo]
        self.registrar_tempo_jogo_objeto(jogo)

    def registrar_tempo_jogo_objeto(self, jogo):
        try:
            tempo = float(input('Quantas horas você jogou? '))
        except:
            print('Tempo inválido.')
            return

        if jogo.id_jogo not in self.tempos_por_jogo:
            self.tempos_por_jogo[jogo.id_jogo] = 0.0

        self.tempos_por_jogo[jogo.id_jogo] += tempo
        tempo_total = self.tempos_por_jogo[jogo.id_jogo]

        status = self.definir_status(tempo_total)
        data = datetime.now().strftime('%d/%m/%Y %H:%M')

        sessao = SessaoJogo(jogo, tempo, tempo_total, data, status)

        self.historico.append(sessao)
        self.recentes.push(jogo)

        print('Sessão registrada com sucesso!')
        sessao.exibir()

    def definir_status(self, tempo_total):
        if tempo_total < 2:
            return 'iniciado'
        elif tempo_total < 10:
            return 'em andamento'
        elif tempo_total < 20:
            return 'muito jogado'
        else:
            return 'concluído simbolicamente'

    def ver_historico(self):
        if len(self.historico) == 0:
            print('Histórico vazio.')
            return

        for sessao in self.historico:
            sessao.exibir()

    def ranking_pessoal(self):
        if len(self.tempos_por_jogo) == 0:
            print('Nenhum jogo jogado ainda.')
            return

        print('\n--- JOGOS MAIS JOGADOS ---')

        ranking = []

        for id_jogo, tempo in self.tempos_por_jogo.items():
            jogo = self.jogos_por_id[id_jogo]
            ranking.append([jogo, tempo])

        ranking.sort(key=lambda item: item[1], reverse=True)

        for item in ranking:
            print(f'{item[0].titulo} - {item[1]} horas')

        print('\n--- GÊNEROS MAIS JOGADOS ---')
        generos = {}

        for id_jogo in self.tempos_por_jogo:
            jogo = self.jogos_por_id[id_jogo]

            if jogo.genero not in generos:
                generos[jogo.genero] = 0

            generos[jogo.genero] += 1

        for genero, qtd in generos.items():
            print(f'{genero}: {qtd}')

        print('\n--- CONSOLES MAIS JOGADOS ---')
        consoles = {}

        for id_jogo in self.tempos_por_jogo:
            jogo = self.jogos_por_id[id_jogo]

            if jogo.console not in consoles:
                consoles[jogo.console] = 0

            consoles[jogo.console] += 1

        for console, qtd in consoles.items():
            print(f'{console}: {qtd}')

        print('\n--- TOP JOGOS POR NOTA NO HISTÓRICO ---')
        jogos_jogados = []

        for id_jogo in self.tempos_por_jogo:
            jogos_jogados.append(self.jogos_por_id[id_jogo])

        jogos_jogados.sort(key=lambda jogo: jogo.critic_score, reverse=True)

        for jogo in jogos_jogados[:10]:
            print(f'{jogo.titulo} - Nota: {jogo.critic_score}')

    def genero_favorito(self):
        generos = {}

        for id_jogo in self.tempos_por_jogo:
            jogo = self.jogos_por_id[id_jogo]

            if jogo.genero not in generos:
                generos[jogo.genero] = 0

            generos[jogo.genero] += self.tempos_por_jogo[id_jogo]

        if len(generos) == 0:
            return None

        return max(generos, key=generos.get)

    def console_favorito(self):
        consoles = {}

        for id_jogo in self.tempos_por_jogo:
            jogo = self.jogos_por_id[id_jogo]

            if jogo.console not in consoles:
                consoles[jogo.console] = 0

            consoles[jogo.console] += self.tempos_por_jogo[id_jogo]

        if len(consoles) == 0:
            return None

        return max(consoles, key=consoles.get)

    def recomendacoes(self):
        genero = self.genero_favorito()
        console = self.console_favorito()

        if genero is None or console is None:
            print('Ainda não há dados suficientes para recomendar jogos.')
            return

        sugestoes = []

        for jogo in self.catalogo:
            ja_jogado = jogo.id_jogo in self.tempos_por_jogo
            esta_backlog = self.backlog.contem(jogo.id_jogo)

            if jogo.genero == genero and jogo.console == console and jogo.critic_score >= 8:
                if not ja_jogado and not esta_backlog:
                    sugestoes.append(jogo)

        print('\n--- RECOMENDAÇÕES ---')
        print(f'Critérios usados: gênero {genero}, console {console}, nota acima de 8.0.')

        if len(sugestoes) == 0:
            print('Nenhuma recomendação encontrada.')
            return

        for jogo in sugestoes[:10]:
            jogo.exibir()

    def dashboard(self):
        print('\n--- DASHBOARD STEAMPY ---')

        total_catalogo = len(self.catalogo)
        total_backlog = self.backlog.tamanho()
        total_recentes = self.recentes.tamanho()
        total_sessoes = len(self.historico)

        tempo_total = 0
        for tempo in self.tempos_por_jogo.values():
            tempo_total += tempo

        jogo_mais_jogado = 'Nenhum'
        maior_tempo = 0

        for id_jogo, tempo in self.tempos_por_jogo.items():
            if tempo > maior_tempo:
                maior_tempo = tempo
                jogo_mais_jogado = self.jogos_por_id[id_jogo].titulo

        genero_fav = self.genero_favorito()
        console_fav = self.console_favorito()

        soma_notas = 0
        qtd_notas = 0

        for id_jogo in self.tempos_por_jogo:
            soma_notas += self.jogos_por_id[id_jogo].critic_score
            qtd_notas += 1

        if qtd_notas > 0:
            media_notas = soma_notas / qtd_notas
        else:
            media_notas = 0

        iniciados = 0
        andamento = 0
        concluidos = 0

        for id_jogo, tempo in self.tempos_por_jogo.items():
            status = self.definir_status(tempo)

            if status == 'iniciado':
                iniciados += 1
            elif status == 'em andamento':
                andamento += 1
            elif status == 'concluído simbolicamente':
                concluidos += 1

        if total_sessoes > 0:
            media_horas = tempo_total / total_sessoes
        else:
            media_horas = 0

        print(f'Total de jogos no catálogo: {total_catalogo}')
        print(f'Total de jogos no backlog: {total_backlog}')
        print(f'Total de jogos recentes: {total_recentes}')
        print(f'Total de sessões jogadas: {total_sessoes}')
        print(f'Tempo total jogado: {tempo_total} horas')
        print(f'Jogo mais jogado: {jogo_mais_jogado}')
        print(f'Gênero favorito: {genero_fav}')
        print(f'Console favorito: {console_fav}')
        print(f'Nota média dos jogos jogados: {media_notas:.2f}')
        print(f'Total de jogos iniciados: {iniciados}')
        print(f'Total de jogos em andamento: {andamento}')
        print(f'Total de jogos concluídos simbolicamente: {concluidos}')
        print(f'Média de horas por sessão: {media_horas:.2f}')

    def salvar_backlog(self):
        arquivo = open('backlog.txt', 'w', encoding='utf-8')

        for jogo in self.backlog.dados:
            arquivo.write(jogo.linha_backlog() + '\n')

        arquivo.close()
        print('Backlog salvo com sucesso.')

    def salvar_historico(self):
        arquivo = open('historico_jogo.txt', 'w', encoding='utf-8')

        for sessao in self.historico:
            arquivo.write(sessao.linha_arquivo() + '\n')

        arquivo.close()
        print('Histórico salvo com sucesso.')

    def salvar_recentes(self):
        arquivo = open('recentes.txt', 'w', encoding='utf-8')

        for jogo in self.recentes.dados:
            arquivo.write(jogo.linharecentes() + '\n')

        arquivo.close()
        print('Recentes salvos com sucesso.')