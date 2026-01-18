# jogador.py

class Jogador:
    """
    Representa o jogador e seus atributos no jogo.
    """
    def __init__(self, vida=100, moral=100, dinheiro=10, tempo=0):
        """
        Inicializa o estado do jogador.
        - vida: A saúde do jogador. Se chegar a 0, o jogo acaba.
        - moral: O estado mental do jogador. Pode afetar certas escolhas.
        - dinheiro: Usado para comprar itens ou serviços.
        - tempo: Um contador de horas ou dias, para eventos baseados no tempo.
        """
        self.vida = vida
        self.moral = moral
        self.dinheiro = dinheiro
        self.tempo = tempo

    def aplicar_efeito(self, efeito):
        """
        Aplica um dicionário de efeitos ao jogador.
        Exemplo de efeito: {"vida": -10, "dinheiro": 5}
        """
        if efeito is None:
            return

        if 'vida' in efeito:
            self.vida += efeito['vida']
        if 'moral' in efeito:
            self.moral += efeito['moral']
        if 'dinheiro' in efeito:
            self.dinheiro += efeito['dinheiro']
        if 'tempo' in efeito:
            self.tempo += efeito['tempo']
        
        # Garante que a vida não passe de 100
        if self.vida > 100:
            self.vida = 100

    def get_status_string(self):
        """
        Retorna o status atual do jogador como uma string formatada.
        """
        return f"❤️  Vida: {self.vida}/100  |  🙂 Moral: {self.moral}  |  💰 Dinheiro: {self.dinheiro} moedas  |  ⏳ Tempo Passado: {self.tempo}h"

    def esta_vivo(self):
        """
        Verifica se o jogador ainda tem pontos de vida.
        """
        return self.vida > 0
