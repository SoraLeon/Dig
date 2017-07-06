import discord
from discord.ext import commands
from PIL import Image
import os
import random
import requests
import io
import urllib

from config import *
from utils import checks

from utils.general import is_numeric, get_time_diff, join_list, get_brasilia_time_zone, log
from utils.messages import EMOJI, split_message
from utils.discord import get_member_by_name, get_user_color, get_member, get_channel_by_name, get_user_servers, FIELD_VALUE_LIMIT
from utils.paginator import Paginator, CannotPaginate
from utils.pobre import *
from urllib import parse

# Commands
class Pobre:
    """Pobre related commands."""
    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.parsing_count = 0    

    @commands.command(pass_context=True, aliases=['tool', 'ferramenta'])
    @asyncio.coroutine
    def utilitario(self, ctx, *, name: str=None):
        """Pesquisa utilitários no PO.B.R.E."""

        permissions = ctx.message.channel.permissions_for(get_member(self.bot, self.bot.user.id, ctx.message.server))
        if not permissions.embed_links:
            yield from self.bot.say("Foi mal, eu preciso de permissões de `Embed Links` para executar este comando.")
            return

        if name is None:
            yield from self.bot.say("Diga-me o nome do utilitário que desejas pesquisar.")
            return
        tool = yield from get_search(parse.quote(name.replace(' ', '+').encode('iso-8859-1'), safe='+'), "26", '0')
        if tool is None or len(tool) == 0:
            yield from self.bot.say("Não encontrei nada com este nome.")
            return
        long = ctx.message.channel.is_private or ctx.message.channel.name == ask_channel_name
        embed = self.get_tool_embed(ctx, tool, long)
        if len(tool) > 1:                        
            yield from self.bot.say("Eu trouxe uma lista que bate com o termo pesquisado, mas se me passar o nome mais detalhado, posso trazer mais detalhes.", embed=embed)
        else:
            yield from self.bot.say(embed=embed)

            # Attach item's image only if the bot has permissions
            permissions = ctx.message.channel.permissions_for(get_member(self.bot, self.bot.user.id, ctx.message.server))
            trad = tool[0]
            item = dict()
            if "details" in trad:
                if "imagens" in trad["details"]:
                    for image in trad["details"]["imagens"]:
                        if permissions.attach_files and image != 0:                                                                                  
                            filename = 'temp.png'
                            while os.path.isfile(filename):
                                filename = "_" + filename
                            with open(filename, "w+b") as f:
                                f.write(image)
                                f.close()

                            with open(filename, "r+b") as f:
                                yield from self.bot.upload(f)
                                f.close()
                            os.remove(filename)

    @commands.command(pass_context=True, aliases=['translate', 'patch'])
    @asyncio.coroutine
    def traducao(self, ctx, *, name: str=None):
        """Pesquisa traduções no PO.B.R.E."""

        permissions = ctx.message.channel.permissions_for(get_member(self.bot, self.bot.user.id, ctx.message.server))
        if not permissions.embed_links:
            yield from self.bot.say("Foi mal, eu preciso de permissões de `Embed Links` para executar este comando.")
            return

        if name is None:
            yield from self.bot.say("Diga-me o nome da tradução que desejas pesquisar.")
            return
        traducao = yield from get_search(parse.quote(name.replace(' ', '+').encode('iso-8859-1'), safe='+'), "23", '0')
        if traducao is None or len(traducao) == 0:
            yield from self.bot.say("Não encontrei nenhuma tradução.")
            return
        long = ctx.message.channel.is_private or ctx.message.channel.name == ask_channel_name
        embed = self.get_traducao_embed(ctx, traducao, long)
        if len(traducao) > 1:                        
            yield from self.bot.say("Não pude trazer os detalhes desta tradução, mas eu trouxe uma lista com possíveis resultados:", embed=embed)
        else:
            yield from self.bot.say(embed=embed) 

            # Attach item's image only if the bot has permissions
            permissions = ctx.message.channel.permissions_for(get_member(self.bot, self.bot.user.id, ctx.message.server))
            trad = traducao[0]
            item = dict()
            if "details" in trad:
                if "imagens" in trad["details"]:
                    for image in trad["details"]["imagens"]:
                        if permissions.attach_files and image != 0:                                                                                  
                            filename = 'temp.png'                            
                            while os.path.isfile(filename):
                                filename = "_" + filename
                            with open(filename, "w+b") as f:
                                f.write(image)
                                f.close()

                            with open(filename, "r+b") as f:
                                yield from self.bot.upload(f)
                                f.close()
                            os.remove(filename)
            

    @commands.command(pass_context=True, aliases=['documento'])
    @asyncio.coroutine
    def tutorial(self, ctx, *, name: str=None):
        """Pesquisa tutoriais no PO.B.R.E."""

        permissions = ctx.message.channel.permissions_for(get_member(self.bot, self.bot.user.id, ctx.message.server))
        if not permissions.embed_links:
            yield from self.bot.say("Foi mal, eu preciso de permissões de `Embed Links` para executar este comando.")
            return

        if name is None:
            yield from self.bot.say("Diga-me o nome do tutorial que desejas pesquisar.")
            return
        tutorial = yield from get_search(parse.quote(name.replace(' ', '+').encode('iso-8859-1'), safe='+'), "19", '0')
        if tutorial is None or len(tutorial) == 0:
            yield from self.bot.say("Não encontrei nenhum tutorial.")
            return
        long = ctx.message.channel.is_private or ctx.message.channel.name == ask_channel_name
        embed = self.get_tutorial_embed(ctx, tutorial, long)
        if len(tutorial) > 1:                        
            yield from self.bot.say("Não pude trazer os detalhes deste tutorial, mas eu trouxe uma lista com possíveis resultados:", embed=embed)
        else:
            yield from self.bot.say(embed=embed)  

            # Attach item's image only if the bot has permissions
            permissions = ctx.message.channel.permissions_for(get_member(self.bot, self.bot.user.id, ctx.message.server))
            trad = tutorial[0]
            item = dict()
            if "details" in trad:
                if "imagens" in trad["details"]:
                    for image in trad["details"]["imagens"]:
                        if permissions.attach_files and image != 0:                                                                                  
                            filename = 'temp.png'                            
                            while os.path.isfile(filename):
                                filename = "_" + filename
                            with open(filename, "w+b") as f:
                                f.write(image)
                                f.close()

                            with open(filename, "r+b") as f:
                                yield from self.bot.upload(f)
                                f.close()
                            os.remove(filename)      

    @staticmethod
    def get_tool_embed(ctx, tool, long):
        """Gets the tool embed to show in /utilitario command"""
        short_limit = 5
        long_limit = 40

        title = "Ferramentas"

        desc = ""
        for i in tool[:10]:
            desc += "[{0}]({1})\n".format(i["name"], i["link"])

            if "details" in i and len(i["details"]) > 0:
                if "autor" in i["details"]:
                    desc += "**Autor:** {0}\n".format(i["details"]["autor"])
                if "sistema" in i["details"]:    
                    desc += "**Sistema:** {0}\n".format(i["details"]["sistema"])
                if "versao" in i["details"]:
                    desc += "**Versão:** {0}\n".format(i["details"]["versao"])
                if "lancamento" in i["details"]:
                    desc += "**Lançamento:** {0}\n".format(i["details"]["lancamento"])
                if "download" in i["details"]:
                    desc += "**Download:** [Link]({0})\n".format(i["details"]["download"])
                if "descricao" in i["details"]:
                    desc += "**Descrição:** {0}\n".format(i["details"]["descricao"])              
                title = "Detalhes da ferramenta"          
        
        embed = discord.Embed(title=title, description=desc)      
        return embed            

    @staticmethod
    def get_traducao_embed(ctx, traducao, long):
        """Gets the tool embed to show in /traducao command"""
        short_limit = 5
        long_limit = 40

        title = "Traduções"

        desc = ""
        for i in traducao[:10]:
            desc += "[{0}]({1})\n".format(i["name"], i["link"]) 

            if "details" in i and len(i["details"]) > 0:
                if "sistema" in i["details"]:    
                    desc += "**Sistema:** {0}\n".format(i["details"]["sistema"])
                if "autor" in i["details"]:
                    desc += "**Autor:** {0}\n".format(i["details"]["autor"])
                if "grupo" in i["details"]:
                    desc += "**Grupo:** {0}\n".format(i["details"]["grupo"])                    
                if "versao" in i["details"]:
                    desc += "**Versão:** {0}\n".format(i["details"]["versao"])
                if "lancamento" in i["details"]:
                    desc += "**Lançamento:** {0}\n".format(i["details"]["lancamento"])
                if "distribuicao" in i["details"]:
                    desc += "**Distribuição:** {0}\n".format(i["details"]["distribuicao"])
                if "progresso" in i["details"]:
                    desc += "**Progresso:** {0}\n".format(i["details"]["progresso"])          
                if "download" in i["details"]:
                    desc += "**Download:** [Link]({0})\n".format(i["details"]["download"])
                if "descricao" in i["details"]:
                    desc += "**Descrição:** {0}\n".format(i["details"]["descricao"])  
                if "consideracoes" in i["details"]:
                    desc += "**Considerações:** {0}\n".format(i["details"]["consideracoes"])                  
                title = i["name"]    
        
        embed = discord.Embed(title=title, description=desc)      
        return embed   

    @staticmethod
    def get_tutorial_embed(ctx, tutorial, long):
        """Gets the tool embed to show in /tutorial command"""
        short_limit = 5
        long_limit = 40

        title = "Tutoriais"

        desc = ""
        for i in tutorial[:10]:
            desc += "[{0}]({1})\n".format(i["name"], i["link"])   

            if "details" in i and len(i["details"]) > 0:
                if "sistema" in i["details"]:    
                    desc += "**Sistema:** {0}\n".format(i["details"]["sistema"])
                if "autor" in i["details"]:
                    desc += "**Autor:** {0}\n".format(i["details"]["autor"])
                if "grupo" in i["details"]:
                    desc += "**Grupo:** {0}\n".format(i["details"]["grupo"])                    
                if "versao" in i["details"]:
                    desc += "**Versão:** {0}\n".format(i["details"]["versao"])
                if "lancamento" in i["details"]:
                    desc += "**Lançamento:** {0}\n".format(i["details"]["lancamento"])
                if "distribuicao" in i["details"]:
                    desc += "**Distribuição:** {0}\n".format(i["details"]["distribuicao"])
                if "progresso" in i["details"]:
                    desc += "**Progresso:** {0}\n".format(i["details"]["progresso"])          
                if "download" in i["details"]:
                    desc += "**Download:** [Link]({0})\n".format(i["details"]["download"])
                if "descricao" in i["details"]:
                    desc += "**Descrição:** {0}\n".format(i["details"]["descricao"])  
                if "consideracoes" in i["details"]:
                    desc += "**Considerações:** {0}\n".format(i["details"]["consideracoes"])                  
                title = i["name"]  
        
        embed = discord.Embed(title=title, description=desc)      
        return embed            

def setup(bot):
    bot.add_cog(Pobre(bot))

if __name__ == "__main__":
    input("To run Monkey Slave, run rh.py")
