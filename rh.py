import asyncio
import random
import re
import sys
import time
import traceback
from datetime import timedelta, datetime

import discord
import psutil
from discord.ext import commands

from config import *
from utils import checks
from utils.database import init_database, userDatabase, reload_worlds, tracked_worlds, tracked_worlds_list, \
    reload_welcome_messages, welcome_messages, reload_announce_channels
from utils.discord import get_member, send_log_message, get_region_string, get_channel_by_name, get_user_servers, \
    clean_string, get_role_list, get_member_by_name, get_announce_channel, get_user_worlds
from utils.general import command_list, join_list, get_uptime, TimeString, \
    single_line, is_numeric, getLogin, start_time, global_online_list
from utils.general import log
from utils.help_format import NabHelpFormat
from utils.messages import decode_emoji, deathmessages_player, deathmessages_monster, EMOJI, levelmessages, \
    weighedChoice, formatMessage
from utils.tibia import get_server_online, get_character, ERROR_NETWORK, ERROR_DOESNTEXIST, \
    get_voc_abb, get_highscores, tibia_worlds, get_pronouns, parse_tibia_time, get_voc_emoji

description = '''Mission: Destroy all humans.'''
bot = commands.Bot(command_prefix=["/"], description=description, pm_help=True, formatter=NabHelpFormat())
# We remove the default help command so we can override it
bot.remove_command("help")