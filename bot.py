import os
import discord
from openai import OpenAI

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client_ai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"機器人已登入：{bot.user}")


@bot.event
async def on_message(message):
    # 不回覆自己
    if message.author == bot.user:
        return

    # 只有被 @ 才回答
    if bot.user in message.mentions:

        question = message.content.replace(
            f"<@{bot.user.id}>", ""
        ).strip()

        if not question:
            await message.reply("你想問我什麼？")
            return

        async with message.channel.typing():
            try:
                response = client_ai.responses.create(
                    model="gpt-5-mini",
                    input=question
                )

                answer = response.output_text

                # Discord 單則訊息有長度限制
                if len(answer) > 1900:
                    answer = answer[:1900] + "\n\n（回答太長，已截短）"

                await message.reply(answer)

            except Exception as e:
                print(f"AI Error: {e}")
                await message.reply("AI 暫時發生錯誤，請稍後再試。")


if not DISCORD_TOKEN:
    raise ValueError("找不到 DISCORD_TOKEN")

if not OPENAI_API_KEY:
    raise ValueError("找不到 OPENAI_API_KEY")

bot.run(DISCORD_TOKEN)
