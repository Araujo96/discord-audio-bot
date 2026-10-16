# Discord Audio Bot

Bot de Discord escrito em Python que reage a mensagens de usuários previamente cadastrados: envia um arquivo de áudio no chat e, se o usuário estiver em um canal de voz, entra na sala, reproduz o áudio e sai em seguida.

## Funcionalidades

- Envio do áudio no canal de texto quando um usuário cadastrado escreve uma mensagem.
- Reprodução do áudio no canal de voz em que o usuário estiver conectado.
- Desconexão automática do canal ao final da reprodução.
- Cadastro de novos usuários por ID, feito diretamente pelo Discord por um administrador.
- Persistência da lista de IDs em arquivo JSON.
- Configuração por variáveis de ambiente.

## Requisitos

- Python 3.8 ou superior
- FFmpeg instalado e disponível no PATH
- Um bot criado no [Discord Developer Portal](https://discord.com/developers/applications)

## Configuração do bot no Discord

1. Crie uma aplicação no Developer Portal e adicione um bot a ela.
2. Em **Bot**, ative a opção **Message Content Intent**.
3. Copie o token do bot.
4. Convide o bot para o servidor com as permissões de visualizar canais, enviar mensagens, anexar arquivos, conectar e falar em canais de voz.

## Instalação

```bash
git clone https://github.com/Araujo96/discord-audio-bot.git
cd discord-audio-bot
pip install discord.py[voice] python-dotenv
```

O pacote `discord.py[voice]` instala o PyNaCl, necessário para a reprodução de áudio em canais de voz.

## Configuração

Copie o arquivo de exemplo e preencha os valores:

```bash
cp .env.example .env
```

| Variável        | Descrição                                                                 |
| --------------- | ------------------------------------------------------------------------- |
| `DISCORD_TOKEN` | Token do bot, obtido no Developer Portal.                                 |
| `ADMIN_ID`      | ID do usuário autorizado a cadastrar novos IDs.                           |
| `SENHA`         | Mensagem usada pelo administrador para iniciar o cadastro de um novo ID.  |
| `IDS_PADRAO`    | Lista de IDs iniciais separados por vírgula (ex.: `123456,789012`).       |

Para obter um ID de usuário, ative o Modo Desenvolvedor nas configurações do Discord, clique com o botão direito no usuário e selecione "Copiar ID do usuário".

Coloque na raiz do projeto o arquivo de áudio com o nome definido na constante `ARQUIVO_AUDIO` em `bot.py`.

## Execução

```bash
python bot.py
```

## Uso

**Reprodução automática**

Quando um usuário cujo ID está cadastrado envia uma mensagem em qualquer canal visível ao bot, o bot responde com o áudio anexado. Se esse usuário estiver em um canal de voz, o bot também entra nele, toca o áudio e se desconecta.

**Cadastro de novos IDs**

1. O administrador (`ADMIN_ID`) envia no chat a mensagem definida em `SENHA`.
2. O bot solicita o novo ID.
3. O administrador responde com o ID numérico ou com `cancelar` para abortar.

O cadastro expira após 60 segundos sem resposta. Os IDs são gravados em `amigos.json`.

## Estrutura do projeto

```
discord-audio-bot/
├── bot.py          # Lógica principal do bot
├── .env.example    # Modelo das variáveis de ambiente
├── .gitignore
└── README.md
```

Arquivos gerados ou fornecidos em tempo de execução:

- `.env`: variáveis de ambiente (não versionado).
- `amigos.json`: lista de IDs cadastrados, criada automaticamente na primeira execução.
- Arquivo de áudio: deve ser adicionado manualmente à raiz do projeto.

## Tecnologias

- [Python](https://www.python.org/)
- [discord.py](https://github.com/Rapptz/discord.py)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [FFmpeg](https://ffmpeg.org/)

## Segurança

- Nunca publique o arquivo `.env` nem o token do bot. Caso o token seja exposto, gere um novo no Developer Portal.
- Use o bot apenas em servidores onde os participantes concordem com a brincadeira.
