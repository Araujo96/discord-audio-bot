
import os
import json
import asyncio
import discord
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID"))
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

usuarios_em_cadastro = set()


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

    if autor_id in usuarios_em_cadastro:
        return


    if autor_id == ADMIN_ID and message.content == SENHA:
        canal = message.channel

        usuarios_em_cadastro.add(autor_id)

        try:
            await canal.send(
                "Informe o novo ID do amigo ou digite "
                "`cancelar` para abortar."
            )

            def verificar(m):
                return (
                    m.author.id == autor_id
                    and m.channel.id == canal.id
                    and not m.author.bot
                )

            try:
                resposta = await bot.wait_for(
                    "message",
                    check=verificar,
                    timeout=60
                )

            except asyncio.TimeoutError:
                await canal.send("Tempo esgotado. Cadastro cancelado.")
                return

            texto = resposta.content.strip()

            if texto.lower() == "cancelar":
                await canal.send("Operação cancelada.")
                return

            if not texto.isascii() or not texto.isdigit():
                await canal.send(
                    "ID inválido! O ID deve conter apenas números."
                )
                return

            novo_id = int(texto)

            if novo_id <= 0:
                await canal.send("ID inválido.")
                return

            if novo_id in ID_DO_AMIGO:
                await canal.send("Esse ID já está incluso.")
                return

            ID_DO_AMIGO.append(novo_id)

            try:
                salvar_amigos(ID_DO_AMIGO)

            except OSError as erro:
                ID_DO_AMIGO.remove(novo_id)
                print(f"Erro ao salvar JSON: {erro}")
                await canal.send(
                    "Erro ao salvar o ID. Tente novamente."
                )
                return

            await canal.send(
                f"Amigo adicionado com sucesso! ID: `{novo_id}`"
            )

            print(f"Novo id adicionado: {novo_id}")

        finally:
            usuarios_em_cadastro.discard(autor_id)

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
