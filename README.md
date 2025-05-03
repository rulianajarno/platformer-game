
# Platformer Game 🎮

Um jogo de plataforma, usando **Pygame Zero** feito através do MU editor. 


## 🧠 Sobre o projeto

Este é um jogo estilo plataforma com rolagem lateral infinita. O jogador pode andar, pular, atirar, coletar moedas e eliminar inimigos. A cada colisão com inimigos ou queda, o jogo reinicia. Há um menu inicial e uma tela de Game Over funcional.


---

## 🕹️ Controles do jogo

- **→**: Andar para a direita  
- **←**: Andar para a esquerda  
- **↑**: Pular   
- **Tecla R**: Reiniciar o jogo na tela de Game Over  
- **Botões na tela**: Menu com opções de iniciar, ativar ou desativar o som, e sair. 

---

## ✅ Requisitos

- **Mu Editor** instalado  
  Você pode baixar aqui: [https://codewith.mu](https://codewith.mu)

> O Mu já vem com o Pygame Zero embutido, é só selecionar o Modo Pygame Zero, então não precisa instalar mais nada.

---

## 🚀 Como rodar o jogo no Mu Editor

1. **Baixe o projeto**:
   - Clique em `Code > Download ZIP` no topo do repositório (caso esteja no GitHub).
   - Ou receba o `.zip` diretamente e extraia para uma pasta chamada `platformer`.

2. **Abra o Mu Editor**.

3. Clique em `Abrir` e selecione o arquivo `jogo.py` dentro da pasta `platformer`.

4. Clique em `Jogar` (ícone de de controle) no topo da tela.

5. **Pronto!** O jogo será iniciado.

---

### ✅ Opção 2: Usando VS Code ou PyCharm

Se utilizar uma IDE como o **VS Code** ou o **PyCharm**, siga os passos abaixo:

#### 1. Instale o Python:
- [https://www.python.org/downloads/](https://www.python.org/downloads/)

#### 2. Instale o Pygame Zero:
Abra o terminal ou prompt de comando e digite:
```bash
pip install pgzero
```

#### 3. Abra a pasta do projeto na IDE.

#### 4. Execute o jogo com o seguinte comando no terminal:
```bash
pgzrun jogo.py
```

> Importante: Não execute com `python jogo.py`, pois Pygame Zero exige o comando `pgzrun`.
---

## 💡 Dicas

- **Use os arquivos exatamente com os nomes minúsculos** (ex: `walk1.png`, não `Walk1.PNG`).
- Se aparecer algum erro, verifique se as pastas `images/` e `music/` estão na mesma pasta do `jogo.py`.

---

### 🖼️ Créditos:
- Código: Ruliana
- Assets gráficos: Platformer Art Deluxe (Kenney.nl)
- Música: Sci-fi Sounds (Kenney.nl)

## 📌 Observações

- Ideal para aprendizado de lógica de jogos e uso básico do PgZero.
- Sem dependências adicionais.
