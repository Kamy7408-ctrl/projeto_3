class SessaoJogo:
    def __init__(self, jogo, tempo_jogado, tempo_total, data_sessao, status):
        self.jogo = jogo
        self.tempo_jogado = tempo_jogado
        self.tempo_total = tempo_total
        self.data_sessao = data_sessao
        self.status = status

    def exibir(self):
        print(f'{self.jogo.titulo}; Sessão: {self.tempo_jogado}h; '
              f'Total: {self.tempo_total}h; Data: {self.data_sessao}; '
              f'Status: {self.status}')

    def linha_arquivo(self):
        return f'{self.jogo.id_jogo};{self.jogo.titulo};{self.tempo_jogado};{self.tempo_total};{self.data_sessao};{self.status}'