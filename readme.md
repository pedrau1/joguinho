# Jornada Solitária: Um RPG de Texto (Pygame Edition)

**Um RPG de texto para um jogador, focado em narrativa, escolhas e exploração, agora com uma interface gráfica estilizada em Pygame, inspirado por jogos como *Roadwarden*.**

![Screenshot Conceitual](https://placehold.co/1280x720/2a2a3a/8b8ba3/png?text=Jornada+Solitaria+Pygame)
*Cenário conceitual de como a janela do jogo pode parecer.*

## Índice

- [Sobre o Jogo](#sobre-o-jogo)
- [Funcionalidades](#funcionalidades)
- [Requisitos](#requisitos)
- [Como Instalar e Jogar](#como-instalar-e-jogar)
- [Estrutura do Jogo (Para Desenvolvedores)](#estrutura-do-jogo-para-desenvolvedores)
- [Como Contribuir](#como-contribuir)
- [Planos Futuros](#planos-futuros)
- [Licença](#licença)

## Sobre o Jogo

Em **Jornada Solitária**, você é um viajante tentando sobreviver em uma terra hostil. Suas interações acontecem inteiramente através de comandos de texto, mas agora apresentados em uma janela dedicada do Pygame, com visuais aprimorados por fontes personalizadas, cores e a possibilidade de usar arte ASCII.

As decisões continuam moldando a história, seus relacionamentos e seu destino. O tempo e os recursos são cruciais, e cada escolha pode levá-lo a um novo caminho.

## Funcionalidades

-   **Interface Estilizada com Pygame**: Jogue em uma janela gráfica dedicada, com controle total sobre a apresentação do texto e input.
-   **Narrativa Ramificada**: Suas decisões têm consequências reais que alteram o desenrolar da história.
-   **Gerenciamento de Recursos**: Administre seus pontos de **Vida**, **Moral** e **Dinheiro**. Viajar e realizar ações custa tempo e recursos.
-   **Entrada de Texto Natural**: Interaja com o jogo digitando comandos em linguagem natural, que são interpretados pelo jogo.
-   **Renderização de Rich Text**: Descrições e diálogos com cores e estilos para melhorar a legibilidade e a imersão.
-   **Arte ASCII**: Utilize bibliotecas como `pyfiglet` para criar títulos e elementos visuais estilizados dentro do ambiente Pygame.
-   **Fácil de Expandir**: A história é escrita em arquivos JSON, permitindo que novas missões, locais e eventos sejam adicionados facilmente.

## Requisitos

-   Python 3.8+
-   **Dependências do Sistema (para Linux):**
    Para que o Pygame possa ser instalado corretamente (incluindo o suporte a fontes), você precisará dos pacotes de desenvolvimento da SDL2 e da SDL2_ttf. Instale-os usando o gerenciador de pacotes da sua distribuição:
    *   **Debian/Ubuntu/Mint:** `sudo apt-get install libsdl2-dev libsdl2-ttf-dev`
    *   **Fedora/CentOS/RHEL:** `sudo dnf install SDL2-devel SDL2_ttf-devel`
    *   **Arch Linux:** `sudo pacman -S sdl2 sdl2_ttf`

## Como Instalar e Jogar

Para rodar o jogo, você precisa configurar um ambiente virtual e instalar as dependências. As instruções variam ligeiramente dependendo do seu sistema operacional e se você deseja apenas rodar o jogo com Python ou criar um executável standalone.

### 1. Preparação Universal (Linux, macOS, Windows)

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/seu-usuario/jornada-solitaria.git
    cd jornada-solitaria
    ```

2.  **Crie e ative o ambiente virtual:**
    *   No **Linux / macOS**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   No **Windows (Prompt de Comando)**:
        ```bash
        py -m venv venv
        venv\Scripts\activate.bat
        ```
    *   No **Windows (PowerShell)**:
        ```powershell
        py -m venv venv
        .\venv\Scripts\Activate.ps1
        ```

3.  **Instale as dependências:**
    Com o ambiente virtual ativado:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Opcional: Adicione as fontes Fira Code (recomendado para melhor visual)**
    *   Crie uma pasta chamada `font` na raiz do projeto (`jornada-solitaria/font`).
    *   Baixe os arquivos `FiraCode-Regular.ttf` e `FiraCode-Bold.ttf` (você pode encontrá-los no GitHub do Fira Code) e coloque-os nesta pasta.

### 2. Rodando o Jogo

#### Para Desenvolvedores (Rodando com Python)

Com o ambiente virtual ativado:
```bash
python jogo.py
```
Uma janela do Pygame será aberta, e você poderá interagir com o jogo digitando comandos na área de input.

#### Para Usuários Finais (Criando um Executável Standalone)

Para distribuir o jogo sem que os usuários precisem instalar Python, você pode criar um executável (`.exe` para Windows, binário para Linux/macOS) usando o **PyInstaller**.

1.  **Instale o PyInstaller:**
    Com o ambiente virtual ativado:
    ```bash
    pip install pyinstaller
    ```

2.  **Crie o executável:**
    Execute o comando na raiz do seu projeto. Lembre-se que o PyInstaller só consegue criar executáveis para o sistema operacional em que está sendo executado.
    
    *   **Para Windows (`.exe`):** Execute este comando em um sistema Windows.
        ```bash
        pyinstaller --windowed --onefile --add-data "historia:historia" --add-data "font:font" jogo.py
        ```
    *   **Para Linux (binário):** Execute este comando em um sistema Linux.
        ```bash
        pyinstaller --windowed --onefile --add-data "historia:historia" --add-data "font:font" jogo.py
        ```
    
    **Explicação dos Parâmetros:**
    *   `--windowed`: Garante que o jogo abra sem uma janela de console preta separada.
    *   `--onefile`: Empacota todo o jogo e suas dependências em um único arquivo executável (o que pode tornar o arquivo grande e um pouco mais lento para iniciar).
    *   `--add-data "origem:destino"`: Instruções para o PyInstaller incluir arquivos ou pastas que seu jogo usa.
        *   `"historia:historia"`: Inclui a pasta `historia` (e seu conteúdo) no executável, acessível como `historia/`.
        *   `"font:font"`: Inclui a pasta `font` (e seu conteúdo) no executável, acessível como `font/`.

3.  **Localize o Executável:**
    O executável será gerado na pasta `dist/` dentro do diretório do seu projeto. Por exemplo, em Windows, você encontrará `dist/jogo.exe`.

## Estrutura do Jogo (Para Desenvolvedores)

-   `jogo.py`: O motor principal do jogo em Pygame, gerenciando a janela, eventos, renderização do buffer de texto, campo de input e a lógica central do jogo.
-   `jogador.py`: Define a classe `Jogador` e seus atributos (vida, moral, dinheiro, tempo).
-   `historia/mundo.json`: O arquivo JSON que contém toda a estrutura narrativa do jogo (descrições, opções, efeitos, palavras-chave para input).
-   `requirements.txt`: Lista de dependências Python.
-   `font/`: Diretório opcional para fontes customizadas (ex: Fira Code).

## Como Contribuir

Este é um projeto de código aberto e a ajuda é bem-vinda!

1.  **Crie um Fork** do projeto.
2.  **Adicione novos nós** (locais, eventos, personagens) ao arquivo `historia/mundo.json`, certificando-se de incluir `respostas_validas` para cada opção.
3.  **Teste suas adições** para garantir que todas as opções funcionam e que o texto rico é renderizado corretamente.
4.  **Abra um Pull Request** com suas mudanças.

Se encontrar um bug ou tiver uma ideia para uma nova mecânica, sinta-se à vontade para abrir uma *Issue*.

## Planos Futuros

-   [ ] Melhorar a renderização de rich text com mais estilos (sublinhado, negrito, etc.).
-   [ ] Integrar mais arte ASCII ou gráficos pixel art para ilustrar locais/personagens.
-   [ ] Implementar um sistema de inventário mais robusto e interativo.
-   [ ] Adicionar um sistema de reputação com facções.
-   [ ] Criar um mecanismo de salvamento/carregamento de jogo.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.