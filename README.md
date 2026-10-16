# Discord Audio Bot

Bot de Discord escrito em Python que reage a mensagens de usuários
previamente cadastrados: envia um arquivo de áudio no chat e, se o
usuário estiver em um canal de voz, entra na sala, reproduz o áudio e
sai em seguida.

A lista de usuários autorizados pode ser gerenciada diretamente pelo
Discord através de comandos administrativos protegidos por senha.

## Funcionalidades

-   Envio do áudio no canal de texto quando um usuário cadastrado
    escreve uma mensagem.
-   Reprodução do áudio no canal de voz em que o usuário estiver
    conectado.
-   Desconexão automática do canal ao final da reprodução.
-   Gerenciamento de usuários autorizados através de comandos
    administrativos.
-   Adição de novos usuários por ID utilizando comando `add`.
-   Remoção de usuários por ID utilizando comando `remove`.
-   Persistência da lista de IDs em arquivo JSON.
-   Configuração por variáveis de ambiente.

## Requisitos

-   Python 3.8 ou superior
-   FFmpeg instalado e disponível no PATH
-   Um bot criado no Discord Developer Portal

## Configuração do bot no Discord

1.  Crie uma aplicação no Developer Portal e adicione um bot a ela.
2.  Em **Bot**, ative a opção **Message Content Intent**.
3.  Copie o token do bot.
4.  Convide o bot para o servidor com as permissões de visualizar
    canais, enviar mensagens, anexar arquivos, conectar e falar em
    canais de voz.

## Instalação

``` bash
git clone https://github.com/Araujo96/discord-audio-bot.git
cd discord-audio-bot
pip install discord.py[voice] python-dotenv
```

O pacote `discord.py[voice]` instala o PyNaCl, necessário para a
reprodução de áudio em canais de voz.

## Configuração

Copie o arquivo de exemplo e preencha os valores:

``` bash
cp .env.example .env
```

  -----------------------------------------------------------------------
  Variável                            Descrição
  ----------------------------------- -----------------------------------
  `DISCORD_TOKEN`                     Token do bot, obtido no Developer
                                      Portal.

  `ADMIN_ID`                          ID do usuário autorizado a executar
                                      comandos administrativos.

  `SENHA`                             Senha utilizada nos comandos
                                      administrativos.

  `IDS_PADRAO`                        Lista de IDs iniciais separados por
                                      vírgula.
  -----------------------------------------------------------------------

Para obter um ID de usuário, ative o Modo Desenvolvedor nas
configurações do Discord, clique com o botão direito no usuário e
selecione "Copiar ID do usuário".

Coloque na raiz do projeto o arquivo de áudio com o nome definido na
constante `ARQUIVO_AUDIO` em `bot.py`.

## Execução

``` bash
python bot.py
```

## Uso

### Reprodução automática

Quando um usuário cujo ID está cadastrado envia uma mensagem em qualquer
canal visível ao bot, o bot responde com o áudio anexado.

Se esse usuário estiver conectado em um canal de voz, o bot também entra
no canal, reproduz o áudio e se desconecta automaticamente após
finalizar.

### Gerenciamento de usuários

Apenas o usuário definido em `ADMIN_ID` pode executar comandos
administrativos.

Os comandos seguem o formato:

``` text
SENHA add ID
```

Adiciona um usuário autorizado.

Exemplo:

``` text
minhasenha add 123456789012345678
```

Para remover:

``` text
SENHA remove ID
```

Exemplo:

``` text
minhasenha remove 123456789012345678
```

As alterações são salvas automaticamente no arquivo `amigos.json`.

## Estrutura do projeto

``` text
discord-audio-bot/
├── bot.py
├── .env.example
├── .gitignore
└── README.md
```

Arquivos gerados ou fornecidos em tempo de execução:

-   `.env`: variáveis de ambiente (não versionado).
-   `amigos.json`: lista de IDs cadastrados, criada automaticamente na
    primeira execução.
-   Arquivo de áudio: deve ser adicionado manualmente à raiz do projeto.

## Tecnologias

-   Python
-   discord.py
-   python-dotenv
-   FFmpeg

## Segurança

-   Nunca publique o arquivo `.env` nem o token do bot.
-   Caso o token seja exposto, gere um novo no Developer Portal.
-   Mantenha o `ADMIN_ID` restrito a usuários confiáveis.
-   Use o bot apenas em servidores onde os participantes concordem com a
    brincadeira.
