# jogo.py

import pygame
import json
import time
from pyfiglet import Figlet
from jogador import Jogador

# --- Configurações Iniciais do Pygame e Cores ---
pygame.init()

try:
    TELA = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    LARGURA, ALTURA = TELA.get_size()
except pygame.error as e:
    print(f"Erro ao inicializar em tela cheia: {e}. Tentando em modo janela.")
    LARGURA, ALTURA = 1280, 720
    TELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("Jornada Solitária")
RELOGIO = pygame.time.Clock()

COR_FUNDO = (20, 20, 30)
COR_TEXTO = (200, 200, 220)
COR_INPUT = (255, 255, 255)
COR_CURSOR = (255, 255, 0)

CORES_RICAS = {
    "yellow": (255, 255, 0), "red": (255, 100, 100), "green": (100, 255, 100),
    "blue": (100, 100, 255), "white": (255, 255, 255), "grey": (150, 150, 150)
}

# --- Fontes ---
try:
    FONTE_TEXTO = pygame.font.Font("font/FiraCode-Regular.ttf", 20)
    FONTE_STATUS = pygame.font.Font("font/FiraCode-Bold.ttf", 22)
except pygame.error:
    FONTE_TEXTO = pygame.font.SysFont("monospace", 18)
    FONTE_STATUS = pygame.font.SysFont("monospace", 20, bold=True)

# --- Definição das Zonas da Tela (Layout) ---
MARGEM_X = int(LARGURA * 0.02)
MARGEM_Y = int(ALTURA * 0.02)

HEADER_RECT = pygame.Rect(MARGEM_X, MARGEM_Y, LARGURA - (2 * MARGEM_X), FONTE_STATUS.get_height())
FOOTER_RECT = pygame.Rect(MARGEM_X, ALTURA - MARGEM_Y - (FONTE_TEXTO.get_height() + 20), LARGURA - (2 * MARGEM_X), FONTE_TEXTO.get_height() + 20)
BODY_RECT = pygame.Rect(MARGEM_X, HEADER_RECT.bottom + MARGEM_Y, LARGURA - (2 * MARGEM_X), FOOTER_RECT.top - HEADER_RECT.bottom - (2 * MARGEM_Y))

# --- Funções Auxiliares de Renderização ---

def renderizar_texto_rico(superficie, texto, pos, largura_max):
    palavras = texto.replace(">", "> ").replace("<", " <").split(' ')
    x, y = pos
    cor_atual = COR_TEXTO
    
    for palavra in palavras:
        if not palavra: continue
        if palavra.startswith("<c="):
            try:
                nova_cor_str = palavra.split('=')[1].replace('>', '').strip()
                cor_atual = CORES_RICAS.get(nova_cor_str, COR_TEXTO)
            except IndexError: cor_atual = COR_TEXTO
            continue
        if palavra == "</c>":
            cor_atual = COR_TEXTO
            continue

        palavra_surf = FONTE_TEXTO.render(palavra + " ", True, cor_atual)
        if x + palavra_surf.get_width() > largura_max:
            x = pos[0]
            y += FONTE_TEXTO.get_height()
        
        superficie.blit(palavra_surf, (x, y))
        x += palavra_surf.get_width()
    return y + FONTE_TEXTO.get_height()


# --- Classe Principal do Jogo ---

class JogoPygame:
    def __init__(self, arquivo_historia):
        self.historia = self.carregar_historia(arquivo_historia)
        self.jogador = Jogador()
        self.no_atual_id = "inicio"
        self.buffer_texto = []

        self.input_texto = ""
        self.input_ativo = True
        self.cursor_visivel = True
        self.cursor_timer = 0
        
        # Superfície do corpo para a rolagem de texto
        self.body_surface = pygame.Surface((BODY_RECT.width, ALTURA * 10)) # Superfície grande para o histórico
        self.scroll_y = 0
        self.altura_total_texto = 0

        self.adicionar_ao_buffer(Figlet(font='standard').renderText('Jornada Solitaria'), "yellow")
        self.processar_no_atual()

    def carregar_historia(self, arquivo_historia):
        """Carrega o arquivo JSON da história e o deserializa."""
        try:
            with open(arquivo_historia, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return dados
        except FileNotFoundError:
            print(f"Erro Crítico: O arquivo de história '{arquivo_historia}' não foi encontrado.")
            pygame.quit()
            exit()
        except json.JSONDecodeError:
            print(f"Erro Crítico: O arquivo '{arquivo_historia}' tem um erro de formatação JSON.")
            pygame.quit()
            exit()

    def adicionar_ao_buffer(self, texto, cor=None):
        if cor: texto = f"<c={cor}>{texto}</c>"
        self.buffer_texto.extend(texto.splitlines()) # Adiciona cada linha separadamente
        self.redesenhar_body_surface()

    def redesenhar_body_surface(self):
        self.body_surface.fill(COR_FUNDO)
        y = 0
        for linha in self.buffer_texto:
            y = renderizar_texto_rico(self.body_surface, linha, (0, y), BODY_RECT.width)
        self.altura_total_texto = y
        self.scroll_y = max(0, self.altura_total_texto - BODY_RECT.height)

    def processar_no_atual(self):
        no_atual = self.historia.get(self.no_atual_id)
        if not no_atual: self.adicionar_ao_buffer(f"Nó '{self.no_atual_id}' não encontrado", "red"); return

        self.adicionar_ao_buffer(f"\n<c=white>--- {self.no_atual_id.replace('_', ' ').title()} ---</c>")
        self.adicionar_ao_buffer(no_atual['descricao'])
        self.adicionar_ao_buffer("\n<c=white>Opções Sugeridas:</c>")
        for opcao in no_atual['opcoes']:
            self.adicionar_ao_buffer(f"  - {opcao['texto']}")
        self.adicionar_ao_buffer("") 
        self.redesenhar_body_surface()

    def processar_comando(self, comando):
        self.adicionar_ao_buffer(f"> {comando}", "yellow")
        
        no_atual = self.historia.get(self.no_atual_id)
        if not no_atual: return

        opcao_encontrada = None
        for opcao in no_atual['opcoes']:
            for palavra_chave in opcao.get('respostas_validas', []):
                if palavra_chave.lower() in comando.lower().strip():
                    opcao_encontrada = opcao; break
            if opcao_encontrada: break
        
        if opcao_encontrada:
            self.jogador.aplicar_efeito(opcao_encontrada.get('efeito'))
            self.no_atual_id = opcao_encontrada['proximo_no']
            self.processar_no_atual()
        else:
            self.adicionar_ao_buffer("Não entendi o que você quer dizer.", "red")
        
        if not self.jogador.esta_vivo():
            self.adicionar_ao_buffer("\n<c=red>Sua vida chegou a zero. FIM DE JOGO.</c>", "red")
            self.input_ativo = False
        self.redesenhar_body_surface()

    def rodar(self):
        rodando = True
        while rodando:
            # --- Eventos ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                    rodando = False
                if evento.type == pygame.MOUSEWHEEL: # Evento de scroll
                    self.scroll_y = max(0, min(self.scroll_y - evento.y * 30, self.altura_total_texto - BODY_RECT.height))
                if self.input_ativo and evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if self.input_texto: self.processar_comando(self.input_texto); self.input_texto = ""
                    elif evento.key == pygame.K_BACKSPACE: self.input_texto = self.input_texto[:-1]
                    else: self.input_texto += evento.unicode

            self.cursor_timer = (self.cursor_timer + RELOGIO.get_rawtime()) % 1000
            self.cursor_visivel = self.cursor_timer < 500

            # --- Renderização ---
            TELA.fill(COR_FUNDO)

            # 1. Cabeçalho (Header)
            status_surf = FONTE_STATUS.render(self.jogador.get_status_string(), True, COR_TEXTO)
            TELA.blit(status_surf, HEADER_RECT.topleft)

            # 2. Corpo (Body) - A área de rolagem
            TELA.blit(self.body_surface, BODY_RECT.topleft, (0, self.scroll_y, BODY_RECT.width, BODY_RECT.height))

            # 3. Rodapé (Footer) - A área de input
            pygame.draw.rect(TELA, COR_TEXTO, FOOTER_RECT, 1)
            prompt_surf = FONTE_TEXTO.render("> ", True, COR_INPUT)
            TELA.blit(prompt_surf, (FOOTER_RECT.x + 10, FOOTER_RECT.y + 10))
            input_surf = FONTE_TEXTO.render(self.input_texto, True, COR_INPUT)
            TELA.blit(input_surf, (FOOTER_RECT.x + 10 + prompt_surf.get_width(), FOOTER_RECT.y + 10))
            if self.cursor_visivel and self.input_ativo:
                cursor_x = FOOTER_RECT.x + 10 + prompt_surf.get_width() + input_surf.get_width()
                pygame.draw.line(TELA, COR_CURSOR, (cursor_x, FOOTER_RECT.y + 8), (cursor_x, FOOTER_RECT.y + 8 + FONTE_TEXTO.get_height()), 2)

            pygame.display.flip()
            RELOGIO.tick(60)

        pygame.quit()

if __name__ == "__main__":
    jogo = JogoPygame("historia/mundo.json")
    jogo.rodar()