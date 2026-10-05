<div align="center">

  <img src="assets/logo2.png" alt="DitPlex Logo" width="200" />

  # DitPlex

  **CLI Morse Academy • Transmissor e Decodificador em Linha de Comando**





![Plataforma](https://img.shields.io/badge/OS-WINDOWS%20%7C%20LINUX-green)





![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)




![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)




![Versão](https://img.shields.io/badge/Versão-1.5.0-blue?style=for-the-badge)





</div>

---

## Sobre

O **DitPlex** é uma ferramenta de linha de comando leve para conversão entre texto e Código Morse — sem depender de sites ou apps externos, direto no seu terminal.

Este projeto é desenvolvido com apoio de IA.
**Claude e Gemini**
## Funcionalidades

- **Tradução Bidirecional:**
  - **Texto ➔ Morse:** Converte letras, números e símbolos (`. , ? ' ! ( ) & : ; = + - _ " $ @`) para sequências de pontos (`.`) e traços (`-`).
  - **Morse ➔ Texto:** Traduz sequências em Morse de volta para caracteres de texto.
- **Arquivos `.txt`:** Converte um arquivo inteiro, linha por linha, detectando sozinho se o conteúdo é texto ou Morse.
- **Salvar o resultado:** Grava a tradução em um arquivo.
- **Área de transferência:** Copia o resultado, pelo menu ou pela linha de comando.
- **Cores:** Seis cores para a interface, salvas entre as sessões.
- **Regras de Espaçamento:**
  - Separador de caracteres: Espaço simples (` `).
  - Separador de palavras: Barra (`/`).

## Preview

<img src="assets/menu.jpg" alt="Imagem do Menu" width="auto" height="auto"/>

---

## Instalação

Baixe o executável para o seu sistema direto na aba **[Releases](../../releases)** do repositório:

- **Windows:** `.exe` pronto para uso
- **Linux:** pacotes `.deb`, `.rpm`, `.tar` (Arch) ou Flatpak

Nenhuma instalação de Python é necessária ao usar os binários pré-compilados.

No Linux, o recurso de copiar precisa de `wl-clipboard`, `xclip` ou `xsel` instalado.

## Como usar

- Use `--help` para ver a forma correta de utilizar o comando.
- Para rodar a partir do código-fonte, instale o Python 3.x e a dependência `platformdirs`:

      pip install platformdirs
      python src/main.py

---

## Uso pela linha de comando

Sem argumentos, o DitPlex abre o menu interativo. Com argumentos, ele converte direto e sai:

| Opção | O que faz |
|---|---|
| `-t`, `--text <texto>` | Converte texto em Morse |
| `-m`, `--morse <morse>` | Converte Morse em texto |
| `-f`, `--file <arquivo>` | Converte um arquivo `.txt`, detectando se é texto ou Morse |
| `-o`, `--output [arquivo]` | Salva o resultado em um arquivo (sem nome: `dados_<data>_<hora>.txt`) |
| `-c`, `--copy` | Copia o resultado para a área de transferência |
| `-v`, `--version` | Mostra versão, sistema/arquitetura e licença |
| `-h`, `--help` | Mostra a ajuda |

### Exemplos

    DitPlex -t "SOS"
    ... --- ...

    DitPlex -m "... --- ..."
    SOS

    DitPlex -f notas.txt
    DitPlex -f notas.txt -o saida.txt
    DitPlex -c -t "SOS"
    DitPlex -o saida.txt -t "SOS"

    DitPlex --version
    [Version]: 1.5.0 [OS/Arch]: linux/x86_64 [License]: MIT

### Regras
- Letras separadas por espaço e palavras por `/`.
- Tudo que vem depois de `-t` ou `-m` é lido como conteúdo, então `DitPlex -m -.-. .-` funciona sem aspas. Por isso `-c` e `-o` precisam vir **antes** de `-t` ou `-m`.
- Com `-f`, o sentido da conversão é detectado sozinho, então ele não se combina com `-t` ou `-m`.
- Se o arquivo de saída já existir, o DitPlex pergunta antes de sobrescrever.
- Ao converter Morse em texto, o resultado sai em maiúsculas e sem acentos.
- As opções diferenciam maiúsculas de minúsculas (`-v`, não `-V`).
- Em caso de erro, a mensagem aparece em vermelho e o programa sai com código 1.

---

## Futuras Implementações

- [ ] **Sinais Sonoros:** Reprodução de áudio dos impulsos de frequência para cada ponto e traço. *(previsto para v1.6.0)*
- [ ] **Ajuste de Velocidade (WPM):** Simulação do Morse em diferentes velocidades de transmissão. *(previsto para v1.6.0)*
- [ ] **Prosigns:** Suporte a sinais processuais do Morse (SOS, AR, SK, entre outros), com opção para consultar o significado de cada um. *(previsto para v1.6.0)*
- [ ] **Testes Automatizados:** Suíte de testes rodando no GitHub Actions. *(previsto para v1.7.0)*
- [ ] **Histórico de Conversões:** Registro das traduções feitas. *(previsto para v1.7.0)*
- [ ] **Modo de Aprendizado:** O projeto ainda não possui um módulo de treinamento. Caso haja interesse da comunidade, essa função poderá ser desenvolvida no futuro.

---

## Compilação e Build

Para compilar a partir do código-fonte, o repositório inclui o script `build.py`, que automatiza a geração do executável usando um ambiente virtual isolado — isso remove dependências desnecessárias do Python global e reduz o tamanho do arquivo final.

---

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).