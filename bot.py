
import os
import json
import asyncio
import discord
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
SENHA = os.getenv("SENHA")

ARQUIVO_AUDIO = "audio.mp3"
ARQUIVO_JSON = "amigos.json"

IDS_PADRAO = [
    int(id.strip())
    for id in os.getenv("IDS_PADRAO", "").split(",")
    if id.strip().isdigit()
]

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = discord.Client(intents=intents)


def carregar_amigos():
    if not os.path.exists(ARQUIVO_JSON):
        salvar_amigos(IDS_PADRAO)
        return IDS_PADRAO.copy()

    try:
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, list):
            raise ValueError("O JSON precisa conter uma lista de IDs.")

        ids = list(dict.fromkeys(
            int(item)
            for item in dados
            if isinstance(item, int)
            and not isinstance(item, bool)
            and item > 0
        ))

        return ids

    except (json.JSONDecodeError, ValueError, OSError) as erro:
        raise RuntimeError(
            f"Não foi possível carregar {ARQUIVO_JSON}: {erro}"
        ) from erro


def salvar_amigos(ids):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(ids, arquivo, indent=4)


ID_DO_AMIGO = carregar_amigos()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    print(f"Amigos inclusos: {len(ID_DO_AMIGO)}")



async def finalizar_audio(voz, erro):
    if erro:
        print(f"Erro na reprodução: {erro}")
    else:
        print("Áudio terminou.")

    try:
        if voz.is_connected():
            await voz.disconnect()
            print("Bot saiu do canal de voz.")

    except (discord.ClientException, discord.HTTPException) as erro:
        print(f"Erro ao desconectar: {erro}")



@bot.event
async def on_message(message):
    if message.author.bot:
        return

    autor_id = message.author.id


    if autor_id == ADMIN_ID:

        conteudo = message.content.strip()
        partes = conteudo.split()

        if len(partes) > 0 and partes[0] == SENHA:

            if len(partes) != 3:
                await message.channel.send(
                    f"Uso:\n"
                    f"`{SENHA} add <id>`\n"
                    f"`{SENHA} remove <id>`"
                )
                return

            senha_digitada = partes[0]
            acao = partes[1].lower()
            texto_id = partes[2]

            if not texto_id.isdigit():
                await message.channel.send(
                    "O ID deve conter apenas números."
                )
                return

            id_usuario = int(texto_id)

            if acao == "add":

                if id_usuario in ID_DO_AMIGO:
                    await message.channel.send(
                        "Esse ID já está cadastrado."
                    )
                    return

                ID_DO_AMIGO.append(id_usuario)

                try:
                    salvar_amigos(ID_DO_AMIGO)
                except OSError as erro:
                    ID_DO_AMIGO.remove(id_usuario)
                    print(erro)
                    await message.channel.send(
                        "Erro ao salvar o arquivo."
                    )
                    return

                await message.channel.send(
                    f"ID `{id_usuario}` adicionado com sucesso."
                )

                print(f"ID adicionado: {id_usuario}")
                return

            elif acao == "remove":

                if id_usuario not in ID_DO_AMIGO:
                    await message.channel.send(
                        "Esse ID não está cadastrado."
                    )
                    return

                ID_DO_AMIGO.remove(id_usuario)

                try:
                    salvar_amigos(ID_DO_AMIGO)
                    
                except OSError as erro:
                    ID_DO_AMIGO.append(id_usuario)
                    print(erro)
                    await message.channel.send(
                        "Erro ao salvar o arquivo."
                    )
                    return

                await message.channel.send(
                    f"ID `{id_usuario}` removido com sucesso."
                )

                print(f"ID removido: {id_usuario}")
                return

            else:
                await message.channel.send(
                    "Use apenas `add` ou `remove`."
                )
                return  


    if autor_id not in ID_DO_AMIGO:
        return


    if not os.path.isfile(ARQUIVO_AUDIO):
        print(f"Arquivo não encontrado: {ARQUIVO_AUDIO}")
        return

    try:
        await message.channel.send(
            content="🔊 Deixa de falar merda!",
            file=discord.File(ARQUIVO_AUDIO)
        )

        print("Áudio enviado no chat.")

    except discord.HTTPException as erro:
        print(f"Erro ao enviar no chat: {erro}")
        return

    if not isinstance(message.author, discord.Member):
        return

    if message.guild is None:
        return

    if message.author.voice is None:
        print("Seu amigo não está em uma sala de voz.")
        return

    canal_voz = message.author.voice.channel

    try:
        voz = message.guild.voice_client

        if voz is None:
            voz = await canal_voz.connect()

        elif voz.channel != canal_voz:
            await voz.move_to(canal_voz)

        if voz.is_playing():
            print("Já existe um áudio tocando na sala.")
            return

        fonte = discord.FFmpegPCMAudio(ARQUIVO_AUDIO)

        voz.play(
            fonte,
            after=lambda erro: asyncio.run_coroutine_threadsafe(
                finalizar_audio(voz, erro),
                bot.loop
            )
        )

        print(f"Tocando áudio na sala: {canal_voz.name}")

    except (
        discord.ClientException,
        discord.Forbidden,
        discord.HTTPException,
        OSError,
        RuntimeError
    ) as erro:
        print(f"Erro ao entrar ou tocar áudio: {erro}")


if not TOKEN:
    raise RuntimeError(
        "Configure DISCORD_TOKEN no arquivo .env"
    )

bot.run(TOKEN)
