from nonebot import get_plugin_config
from nonebot.log import logger
from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import *

from .config import Config, SAVE_TMP_PATH, FONTS_PATH, ROOT_PATH, font_syht_m
from typing import Union, Any, Dict
from PIL import Image, ImageDraw, ImageFont

import base64
import re
import os
from io import BytesIO
import json
import requests
import aiohttp, asyncio
import nest_asyncio

#nest_asyncio.apply()

__plugin_meta__ = PluginMetadata(
    name="tjmc",
    description="获取TJMC服务器信息",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

MINECRAFT_COLOR_CODES = {
    '0': (0, 0, 0, 255),
    '1': (0, 0, 170, 255),
    '2': (0, 170, 0, 255),
    '3': (0, 170, 170, 255),
    '4': (170, 0, 0, 255),
    '5': (170, 0, 170, 255),
    '6': (255, 170, 0, 255),
    '7': (170, 170, 170, 255),
    '8': (85, 85, 85, 255),
    '9': (85, 85, 255, 255),
    'a': (85, 255, 85, 255),
    'b': (85, 255, 255, 255),
    'c': (255, 85, 85, 255),
    'd': (255, 85, 255, 255),
    'e': (255, 255, 85, 255),
    'f': (255, 255, 255, 255),
}

server_group = "TJMC"
offline_mode_args = {"-a", "all"}
unknown_server_info = '''
{
  "favicon": "https://patchwiki.biligame.com/images/mc/a/a5/tuovefzxjbi9knmyh1so5m7mamnzwh4.png",
  "description": {
    "text": "服务器已离线..."
  },
  "online": false,
  "players": {
    "online": 0,
    "max": 0
  },
  "display_title": "",
  "only_display_first_line": true
}
'''
unknown_server = json.loads(unknown_server_info)
tjmc = on_command("tj", aliases={"tjmc", "TJ", "TJMC"}, priority = 10, block = True)

@tjmc.handle()
async def get_server_status(bot: Bot, event: Event, state: T_State):
    # 获取指令参数列表，args[0]为指令本身
    args = str(event.get_message()).split()
    offline_mode = False
    if len(args) > 1 and args[1] in offline_mode_args:
        offline_mode = True
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id, message="正在获取同济MC服务器状态喵")
        try:
            imgPath = draw_tjmc_info(aio_get_tjmc_info(), server_group, offline_mode)
            #imgPath = imgPath if os.path.isabs(imgPath) else os.path.join(ROOT_PATH, imgPath)
            with open("data/tmp/tjmc_status_TJMC.png", "rb") as image_file:
                # 二进制形式，需要转码!
                encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.decode("utf-8")
            await bot.send_group_msg(group_id=event.group_id, message=f'[CQ:image,file=base64://{encoded_string}]', auto_escape=False)
        except BaseException as e:
            await bot.send_group_msg(group_id=event.group_id, message="internal error while getting tjmc")
            logger.warning("basic exception in ShowTjmcStatus: {}".format(e))
        return "OK"
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=event.user_id, message="正在获取同济MC服务器状态喵")
        try:
            imgPath = draw_tjmc_info(aio_get_tjmc_info(), server_group, offline_mode)
            #imgPath = imgPath if os.path.isabs(imgPath) else os.path.join(ROOT_PATH, imgPath)
            with open("data/tmp/tjmc_status_TJMC.png", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            encoded_string = encoded_string.decode("utf-8")
            await bot.send_private_msg(user_id=event.user_id, message=f'[CQ:image,file=base64://{encoded_string}]', auto_escape=False)
        except BaseException as e:
            await bot.send_private_msg(user_id=event.user_id, message="internal error while getting tjmc")
            logger.warning("basic exception in ShowTjmcStatus: {}".format(e))
        return "OK"

def fetch_server_list() -> Union[None, Dict[str, Any]]:
    file_path = "configs/tjmc_server.json"
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
    server_list = json.loads(content)
    for server in server_list:
        if 'ip' not in server:
            return None
    return server_list

def aio_get_tjmc_info():
    #print(1111)
    async def get_page(i, addr):
        #print(i, addr)
        #print(2222)
        url=f"https://mc.sjtu.cn/custom/serverlist/?query={addr}"
        async with aiohttp.request('GET', url) as req:
            status = await req.json()
            return i, status
    server_list = fetch_server_list()
    loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # fixec
    nest_asyncio.apply()
    tasks = [loop.create_task(get_page(i, server['ip'])) for i, server in enumerate(server_list)]
    result = loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    result = [r.result() for r in result[0]]
    result = sorted(result, key=lambda x: x[0])
    result = [r[1] for r in result]
    #result = []
    i = 0
    for server in server_list:
        #print(f"server {i} start process")
        tmp = result[i]
        tmp["display_ip"] = server["ip"]
        tmp["display_title"] = server["title"]
        tmp["display_custom_domain"] = server["display_custom_domain"]
        tmp["display_custom_title"] = server["display_custom_title"]
        tmp["only_display_first_line"] = server["only_display_first_line"]
        #tmp = json.loads(str(get_tjmc_page(server["ip"])).replace("'", "\""))
        #result[i] = tmp
        #print(f"server {i} over")
        i += 1

    return result

def get_tjmc_page(addr):
    url = f"https://mc.sjtu.cn/custom/serverlist/?query={addr}"
    result = requests.get(url)
    return result.content.decode("raw_unicode_escape")

def draw_tjmc_info(dat1, server_group, offline_mode: bool):
    # 在线模式
    if not offline_mode:
        dat = [res for res in dat1 if res['online']]
        if len(dat) == 0:
            dat.append(unknown_server)
    # 离线模式
    else:
        dat = dat1
    j = sum([res['online'] and res['players']['online'] != 0 for res in dat])
    j1 = 0
    FONTS_PATH = 'resources/fonts'
    white, grey, green, red = (255, 255, 255, 255), (128, 128, 128, 255), (0, 255, 33, 255), (255, 85, 85, 255)
    font_mc_l = ImageFont.truetype(os.path.join(FONTS_PATH, 'Minecraft AE.ttf'), 30)
    font_mc_m = ImageFont.truetype(os.path.join(FONTS_PATH, 'Minecraft AE.ttf'), 20)
    font_mc_s = ImageFont.truetype(os.path.join(FONTS_PATH, 'Minecraft AE.ttf'), 16)
    font_mc_xl = ImageFont.truetype(os.path.join(FONTS_PATH, 'Minecraft AE.ttf'), 39)
    width = 860
    height = 215 + len(dat) * 140 + j * 35
    img = Image.new('RGBA', (width, height), (46, 33, 23, 255))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 120, width, height - 80), fill=(15, 11, 7, 255))
    if offline_mode:
        draw.text((width - 140 - draw.textsize(f"{server_group}服务器状态", font=font_mc_xl)[0], 42), f"{server_group}服务器状态", fill=(255, 255, 255, 255), font=font_mc_xl)
    else:
        draw.text((width - 140 - draw.textsize(f"{server_group}在线服务器状态", font=font_mc_xl)[0], 42), f"{server_group}在线服务器状态", fill=(255, 255, 255, 255), font=font_mc_xl)
    draw.text((width - 120, 36), "LITTLE\nUNIkeEN", fill=(255, 255, 255, 255), font=font_syht_m)
    #draw.text((width - 120, 44), "LITTLE\nUNIkeEN", fill=(255, 255, 255, 255), font=font_syht_m)

    # 绘制带颜色标题
    def draw_colored_title(draw, text, position, font, default_color=(255, 255, 255, 255)):
        x, y = position
        current_color = default_color
        buffer_text = ''
        i = 0
        while i < len(text):
            if text[i] == '§':
                if buffer_text:
                    draw.text((x, y), buffer_text, fill=current_color, font=font)
                    size = draw.textsize(buffer_text, font=font)
                    x += size[0]
                    buffer_text = ''
                if i + 1 < len(text) and text[i + 1].lower() in MINECRAFT_COLOR_CODES:
                    current_color = MINECRAFT_COLOR_CODES.get(text[i + 1].lower(), default_color)
                i += 2
            else:
                buffer_text += text[i]
                i += 1
        #if buffer_text:
        #    draw.text((x, y), buffer_text, fill=current_color, font=font)
        if not buffer_text or buffer_text.strip() == "":
            buffer_text = "紫晶社：未知服务器"
        draw.text((x, y), buffer_text, fill=current_color, font=font)
    #print("each server start drawing!")
    for i, res in enumerate(dat):
        fy = 160 + i * 140 + j1 * 31
        if res["online"]:
            # 是否显示自定义标题
            if res["display_custom_title"]:
                title = title = res["display_title"]
            else:
                try:
                    title = res['description']
                    if not isinstance(title, str):
                        title = title['text']
                    title = re.sub(r'§[klmnor]', '', title)
                    title = title.replace('|', ' | ', 1)
                    if res["only_display_first_line"]:
                        title = title.split('\n')[0]
                    else:
                        title = title.replace('\n', '  |  ', 1)
                    title = title.replace('服务器已离线...', '')
                except:
                    title = 'Unknown Server Name'
        else:
            title = res["display_title"]
        draw_colored_title(draw, title, (160, fy), font=font_mc_l)

        # 绘制图标
        try:
            icon_url = res['favicon']
            if icon_url[:4] == "data":
                img_avatar = Image.open(decode_image(icon_url)).resize((80, 80))
                if img_avatar != None:
                    img.paste(img_avatar, (60, fy))
            else:
                url_avatar = requests.get(icon_url)
                if url_avatar.status_code != requests.codes.ok:
                    img_avatar = None
                else:
                    img_avatar = Image.open(BytesIO(url_avatar.content)).resize((80, 80))
                    img.paste(img_avatar, (60, fy))
        except KeyError as e:
            logger.warning("key error in sjmc draw icon: {}".format(e))
        except BaseException as e:
            logger.warning("base exception in sjmc draw icon: {}".format(e))

        if res['online']:
            if res["display_custom_domain"]:
                res["hostname"] = res["display_ip"].replace('.', ' . ').replace(':', ' : ')
            else:
                res['hostname'] = res['hostname'].replace('.', ' . ')
                if 'port' in res.keys() and res['port'] != None:
                    port = str(res['port']).strip()
                    if port != '25565':
                        res['hostname'] += ' : ' + port
            draw.text((160, fy + 45), res['hostname'], fill=grey, font=font_mc_m)
            txt_size = draw.textsize(f"{res['ping']}ms", font=font_mc_m)
            ping = int(res['ping'])
            clr = red if ping >= 100 else green
            draw.text((width - 60 - txt_size[0], fy), f"{res['ping']}ms", fill=clr, font=font_mc_m)
            txt_size = draw.textsize(f"{res['players']['online']}/{res['players']['max']}", font=font_mc_m)
            draw.text((width - 60 - txt_size[0], fy + 32), f"{res['players']['online']}/{res['players']['max']}",
                      fill=grey, font=font_mc_m)
            txt_size = draw.textsize(res['version'], font=font_mc_m)
            draw.text((width - 60 - txt_size[0], fy + 64), res['version'], fill=grey, font=font_mc_m)
            if res['players']['online'] != 0:
                j1 += 1
                txt_plr = ""
                try:
                    for player in res['players']['sample']:
                        if draw.textsize(txt_plr + player['name'] + '、', font=font_mc_s)[0] >= width - 300:
                            txt_plr = txt_plr[:-1] + '等 '
                            break
                        txt_plr += (player['name'] + '、')
                    txt_plr = txt_plr[:-1] + ' 正在游玩'
                except:
                    txt_plr = '( 玩家信息获取失败qwq )'
                txt_size = draw.textsize(txt_plr, font=font_mc_s)
                txt_size_2 = draw.textsize('●', font=font_mc_s)
                draw.text((width - 68 - txt_size[0] - txt_size_2[0], fy + 96), txt_plr, fill=grey, font=font_mc_s)
                draw.text((width - 60 - txt_size_2[0], fy + 96), '●', fill=green, font=font_mc_s)
        else:
            txt_size = draw.textsize("offline", font=font_mc_m)
            draw.text((width - 60 - txt_size[0], fy), "offline", fill=red, font=font_mc_m)
            txt_size = draw.textsize("服务器离线", font=font_mc_m)
            draw.text((width - 60 - txt_size[0], fy + 32), "服务器离线", fill=grey, font=font_mc_m)
    draw.text((60, height - 50), "欢迎加入同济 Minecraft 交流群！群号 750669570", fill=white, font=font_mc_m)
    save_path = os.path.join(SAVE_TMP_PATH, 'tjmc_status_{}.png'.format(server_group))
    img.save(save_path)
    return save_path


def decode_image(src) -> Union[None, BytesIO]:
    """
    解码图片
    :param src: 图片编码
        eg:
            src="data:image/gif;base64,R0lGODlhMwAxAIAAAAAAAP///
                yH5BAAAAAAALAAAAAAzADEAAAK8jI+pBr0PowytzotTtbm/DTqQ6C3hGX
                ElcraA9jIr66ozVpM3nseUvYP1UEHF0FUUHkNJxhLZfEJNvol06tzwrgd
                LbXsFZYmSMPnHLB+zNJFbq15+SOf50+6rG7lKOjwV1ibGdhHYRVYVJ9Wn
                k2HWtLdIWMSH9lfyODZoZTb4xdnpxQSEF9oyOWIqp6gaI9pI1Qo7BijbF
                ZkoaAtEeiiLeKn72xM7vMZofJy8zJys2UxsCT3kO229LH1tXAAAOw=="

    :return: 图片的BytesIO
    """
    # 1、信息提取
    result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", src, re.DOTALL)
    if result:
        ext = result.groupdict().get("ext")
        data = result.groupdict().get("data")
    else:
        return None
    # 2、base64解码
    return BytesIO(base64.urlsafe_b64decode(data))

# ONLY TJMC
# BY LVREN
