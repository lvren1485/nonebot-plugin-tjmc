import random
import base64

from nonebot import get_plugin_config
from nonebot import on_fullmatch, on_notice, on_keyword, on_command, on_regex
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import *

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="bro",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

emotion2 = on_fullmatch(("急", "好急"), ignorecase=True, priority=9, block=True)
bro = on_fullmatch(("兄弟", "兄弟...", "兄弟。。。"), ignorecase=True, priority=1, block=False)
touch = on_notice()
leave = on_notice()
join = on_notice()
builder = on_keyword({"复原", "建筑", "原^", "次原", "原**"}, priority=10, block=False)
emotion1 = on_fullmatch(("别急", "你先别急", "真别急"), priority=10, block=False)
emotion3 = on_keyword({"早八"}, priority=9, block=False)
wallis = on_keyword({"华里士"}, priority=9, block=False)
snuggle = on_keyword({"贴贴"}, priority=9, block=False)
# \S表示非空白符
# xxx是(机器人)/(bot)吗/喵/咪/咩/么/嘛/汪...
is_bobot = on_regex(
    "^(\S*)([\u673a\u9e21(\U0001F414)(\U0001F423)(\U0001F424)(\U0001F425)]\u5668\u4eba|[Bb][Oo][Tt])[\u554a\u5417\u561b\u4e48\u55b5\u54aa\u54a9\u6c6a?\uff1f\uff01\u3002,\uff0c.\u9a6c\u54c7\u5594\u545c](\S*)$")
has_server = on_regex("^(\S*)有(\S*)服务器(\S*)$")
test = on_fullmatch(("!测试"), ignorecase=True, priority=9, block=True)
test2 = on_fullmatch(("!测试2"), ignorecase=True, priority=9, block=True)
tjmc = on_fullmatch(("-tjmc"), ignorecase=True, priority=9, block=True)
repeat = on_command("rpt", priority=10, block=True)
notice_manager = on_command(("notice"), priority=10, block=True)

bilibili = on_fullmatch(('社畜', 'Java教程', '高数'), ignorecase=True, priority=9, block=True)
# 用map来存发送的CQ消息，使代码更清晰易读
reserved_messages: dict[str, str] = {
    '高数': '[CQ:json,data={"ver":"1.0.0.19"&#44;"desc":"【处处吻】高等数学"&#44;"prompt":"&#91;QQ小程序&#93;【处处吻】高等数学"&#44;"config":{"type":"normal"&#44;"width":0&#44;"height":0&#44;"forward":1&#44;"autoSize":0&#44;"ctime":1713847796&#44;"token":"fad3a0cac628421e5882a8ea1df8374f"}&#44;"needShareCallBack":false&#44;"app":"com.tencent.miniapp_01"&#44;"view":"view_8C8E89B49BE609866298ADDFF2DBABA4"&#44;"meta":{"detail_1":{"appid":"1109937557"&#44;"appType":0&#44;"title":"哔哩哔哩"&#44;"desc":"【处处吻】高等数学"&#44;"icon":"http://miniapp.gtimg.cn/public/appicon/432b76be3a548fc128acaa6c1ec90131_200.jpg"&#44;"preview":"pubminishare-30161.picsz.qpic.cn/2a598954-bdf6-460c-a3c2-739b1af812a7"&#44;"url":"m.q.qq.com/a/s/e4678c6572564770fa95c1487bedd445"&#44;"scene":1036&#44;"host":{"uin":1694882069&#44;"nick":"祤麒今晚喝什么"}&#44;"shareTemplateId":"8C8E89B49BE609866298ADDFF2DBABA4"&#44;"shareTemplateData":{}&#44;"qqdocurl":"https://b23.tv/VFWexEi?share_medium=android&amp;share_source=qq&amp;bbid=XX58CB75AF5BD4C8F8673BF0ED1CC2DDA8AC3&amp;ts=1713847793210"&#44;"showLittleTail":""&#44;"gamePoints":""&#44;"gamePointsUrl":""}}}]',
    '社畜': '[CQ:json,data={"ver": "1.0.0.19"&#44;"desc": "【中日歌词】《乐意效劳》（はいよろこんで）"&#44;"prompt": "&#91;QQ小程序&#93;【中日歌词】《乐意效劳》（はいよろこんで）"&#44;"config": {"type": "normal"&#44;"width": 0&#44;"height": 0&#44;"forward": 1&#44;"autoSize": 0&#44;"ctime": 1721622641&#44;"token": "f1268a4448c2e48467f1efb8235f2f1d"}&#44;"needShareCallBack": false&#44;"app": "com.tencent.miniapp_01"&#44;"view": "view_8C8E89B49BE609866298ADDFF2DBABA4"&#44;"meta": {"detail_1": {"appid": "1109937557"&#44;"appType": 0&#44;"title": "哔哩哔哩"&#44;"desc": "【中日歌词】《乐意效劳》（はいよろこんで）"&#44;"icon": "http://miniapp.gtimg.cn/public/appicon/432b76be3a548fc128acaa6c1ec90131_200.jpg"&#44;"preview": "pubminishare-30161.picsz.qpic.cn/0eff9133-9df8-4e7a-bbbd-bfd41d64baee"&#44;"url": "m.q.qq.com/a/s/8d9f7afd06cb6db1472cd414ca789e19"&#44;"scene": 1036&#44;"host": {"uin": 1694882069&#44;"nick": "祤麒今晚喝什么"}&#44;"shareTemplateId": "8C8E89B49BE609866298ADDFF2DBABA4"&#44;"shareTemplateData": {}&#44;"qqdocurl": "https://b23.tv/YUcch7Z?share_medium=android&amp;share_source=qq&amp;bbid=XX58CB75AF5BD4C8F8673BF0ED1CC2DDA8AC3&amp;ts=1721622638164"&#44;"showLittleTail": ""&#44;"gamePoints": ""&#44;"gamePointsUrl": ""}}}]',
    'Java教程': '[CQ:json,data={"ver":"1.0.0.19"&#44;"prompt":"&#91;QQ小程序&#93;Java零基础教程视频（适合Java 0基础，Java初学入门）"&#44;"config":{"type":"normal"&#44;"width":0&#44;"height":0&#44;"forward":1&#44;"autoSize":0&#44;"ctime":1721625687&#44;"token":"46925ee621df47430623bb9e81273130"}&#44;"needShareCallBack":false&#44;"app":"com.tencent.miniapp_01"&#44;"view":"view_8C8E89B49BE609866298ADDFF2DBABA4"&#44;"meta":{"detail_1":{"appid":"1109937557"&#44;"appType":0&#44;"title":"哔哩哔哩"&#44;"desc":"Java零基础教程视频（适合Java 0基础，Java初学入门）"&#44;"icon":"https://open.gtimg.cn/open/app_icon/00/95/17/76/100951776_100_m.png?t=1721212395"&#44;"preview":"pubminishare-30161.picsz.qpic.cn/6d489207-c14b-4a42-868d-2eb52064b621"&#44;"url":"m.q.qq.com/a/s/dcf8ca512c089404f013e2266b5dc11c"&#44;"scene":1036&#44;"host":{"uin":1694882069&#44;"nick":"祤麒今晚喝什么"}&#44;"shareTemplateId":"8C8E89B49BE609866298ADDFF2DBABA4"&#44;"shareTemplateData":{}&#44;"qqdocurl":"https://b23.tv/ue8ML4n?share_medium=android&amp;share_source=qq&amp;bbid=XX58CB75AF5BD4C8F8673BF0ED1CC2DDA8AC3&amp;ts=1721625686023"&#44;"showLittleTail":""&#44;"gamePoints":""&#44;"gamePointsUrl":""}}}]',
    '-tjmc': ''}

reserved_images: dict[str, str] = {}
reserved_image_names: list[str] = ["bro.gif", "chillet_snuggle.gif", "chillet_jiggle.gif", "hurry.gif", "hurry2.gif",
                                   "no_hurry.jpg", "wallis.jpg", "welcome_to_fu_yuan.jpg", ]
for name in iter(reserved_image_names):
    with open(f"data/pic/{name}", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        reserved_images[name] = encoded_string


# 离开群聊提醒功能启用的群聊
'''
leave_notice_list: list[int] = [914071646, 824427638, ]  # 824427638 是测试群
join_notice_list: list[int] = [824427638, 750669570, 914071646, ]
'''
leave_notice_list: list[int] = []
join_notice_list: list[int] = []
open_builder_message = 1

with open("configs/join_notice_list.txt", "r", encoding="utf-8") as file:
    for line in file.readlines():
        line = line.strip('\n')
        join_notice_list.append(int(line))
with open("configs/leave_notice_list.txt", "r", encoding="utf-8") as file:
    for line in file.readlines():
        line = line.strip('\n')
        leave_notice_list.append(int(line))
with open("configs/open_builder_message.txt", "r", encoding="utf-8") as file:
    for line in file.readlines():
        line = line.strip('\n')
        open_builder_message = int(line)

# 管理员列表
operator_list: list[int] = [1694882069, 1216961922, 812584722, 2473930049, ]

'''
[CQ:xml,data=<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<msg serviceID="1">
<item>
<title>test title</title>
<summary>test content</summary>
</item>
<source name="官方认证消息" icon="https://qzs.qq.com/ac/qzone_v5/client/auth_icon.png" action="" appid="-1" />
</msg>]
'''


# 自行封装的发送群聊消息的函数
async def my_send_group_msg(bot: Bot, event: GroupMessageEvent, msg: str | Message):
    await bot.send_group_msg(group_id=event.group_id, message=msg, auto_escape=False)


# 自行封装的发送私聊消息的函数
async def my_send_private_msg(bot: Bot, event: PrivateMessageEvent, msg: str | Message):
    await bot.send_private_msg(user_id=event.user_id, message=msg, auto_escape=False)


async def my_send_msg(bot: Bot, event: Event, msg: str | Message, msg2: str | Message = "ignore"):
    if isinstance(event, GroupMessageEvent):
        await my_send_group_msg(bot, event, msg)
    elif isinstance(event, PrivateMessageEvent):
        if msg2 == "ignore":
            await my_send_private_msg(bot, event, msg)
        else:
            await my_send_private_msg(bot, event, msg2)

"""
复读消息的鸡肋功能(
TODO: 直接在指令后接上要复读的信息
"""
@repeat.got("message", prompt="请输入要复读的内容")
async def send_today_problem(bot: Bot, event: Event, state: T_State):
    try:
        await my_send_msg(bot, event, state["message"])
    except Exception as e:
        await my_send_msg(bot, event, "消息迷失在了世界线的缝隙中")

"""
发送关键词即发送预设视频
"""
@bilibili.handle()
async def send_video(bot: Bot, event: Event):
    await my_send_msg(bot, event, reserved_messages.get(event.get_message().extract_plain_text()))

"""
下方一堆函数都是相同逻辑，想办法提取一下逻辑塞进map里统一处理，我爱技术!
"""
@tjmc.handle()
async def send_tjmc(bot: Bot, event: Event, state: T_State):
    await my_send_msg(bot, event, "查询同济服务器更推荐使用!tj啾~", "查询同济服务器更推荐使用!tj喵~")


@is_bobot.handle()
async def send_denying(bot: Bot, event: Event, state: T_State):
    await my_send_msg(bot, event, "不是喵~")


@snuggle.handle()
async def chillet_snuggle(bot: Bot, event: Event, state: T_State):
    await my_send_msg(bot, event, f'[CQ:image,file=base64://{reserved_images.get("chillet_snuggle.gif")}]')


@bro.handle()
async def send_bro(bot: Bot, event: Event, state: T_State):
    await my_send_msg(bot, event, f'[CQ:image,file=base64://{reserved_images.get("bro.gif")}]')


@emotion3.handle()
async def send_emotion3(bot: Bot, event: Event, state: T_State):
    """
    60%概率发送"早八"
    """
    if random.randint(1, 10) > 4:
        return
    await my_send_msg(bot, event, "早八")


@emotion2.handle()
async def send_emotion2(bot: Bot, event: Event, state: T_State):
    match random.randint(1, 2):
        case 1:
            url = reserved_images.get("hurry.gif")
        case 2:
            url = reserved_images.get("hurry2.gif")
    await my_send_msg(bot, event, f'[CQ:image,file=base64://{url}]')


@wallis.handle()
async def send_wallis(bot: Bot, event: Event, state: T_State):
    await my_send_msg(bot, event, f'[CQ:image,file=base64://{reserved_images.get("wallis.jpg")}]')


@emotion1.handle()
async def send_emotion1(bot: Bot, event: Event, state: T_State):
    await my_send_msg(bot, event, f'[CQ:image,file=base64://{reserved_images.get("no_hurry.jpg")}]')

"""
机器人被戳一戳时反戳回去
(迁移LLonebot后本功能暂时失效，等待客户端更新后支持戳一戳)
"""
@touch.handle()
async def touch_too(bot: Bot, event: Event, state: T_State):
    if event.get_user_id() == bot.self_id:
        return
    if isinstance(event, PokeNotifyEvent):
        if event.group_id is not None:
            if event.target_id == bot.self_id:
                await bot.send_group_msg(group_id=event.group_id, message=f"[CQ:touch,id={event.user_id}]",
                                         auto_escape=False)
            elif random.randint(1, 100) % 10 <= 2:
                await bot.send_group_msg(group_id=event.group_id, message=f"[CQ:touch,id={event.user_id}]",
                                         auto_escape=False)
        else:
            await bot.send_private_msg(user_id=event.user_id, message=f"[CQ:touch,id={event.user_id}]",
                                       auto_escape=False)

"""
有人退群时提示信息
(令人悲伤的功能)
"""
@leave.handle()
async def member_leave(bot: Bot, event: Event):
    if not isinstance(event, GroupDecreaseNoticeEvent):
        return
    if event.is_tome() or event.group_id not in leave_notice_list:
        return
    try:
        info = await bot.get_stranger_info(user_id=event.user_id)
        if event.user_id == event.operator_id:
            s = f"{info['nick']}({event.user_id})褪裙了喵"
        else:
            s = f"{info['nick']}({event.user_id})被管理员移出了群聊"
        await my_send_group_msg(bot, event, s)
    except BaseException as e:
        pass

"""
新人入群欢迎信息
"""
@join.handle()
async def member_join(bot: Bot, event: Event):
    if not isinstance(event, GroupIncreaseNoticeEvent):
        return
    if event.is_tome() or event.group_id not in join_notice_list:
        return
    try:
        #info = await bot.get_stranger_info(user_id=event.user_id)
        #s = f"{info['nick']}({event.user_id})加入了群聊喵"
        s = f"[CQ:at,qq={event.user_id}] 欢迎新人喵！"
        await my_send_group_msg(bot, event, s)
        await my_send_group_msg(bot, event, f'[CQ:image,file=base64://{reserved_images.get("welcome_to_fu_yuan.jpg")}]')
    except BaseException as e:
        pass

"""
群聊各种类型通知开闭管理
!notice join/leave/builder enable/disable
"""
@notice_manager.handle()
async def manage_notice(bot: Bot, event: Event):

    global open_builder_message

    if not isinstance(event, MessageEvent):
        return
    if event.user_id not in operator_list:
        await my_send_msg(bot, event, "你没有权限执行该指令喵")
        return

    args = str(event.get_message()).split()
    if len(args) < 3 or len(args) > 4:
        await my_send_msg(bot, event, "指令有误喵")
        return
    if args[1] != "join" and args[1] != "leave" and args[1] != "builder":
        await my_send_msg(bot, event, "指令有误喵")
        return

    if isinstance(event, PrivateMessageEvent):
        if len(args) == 3:
            await my_send_private_msg(bot, event, "你没有输入要操作的群号")
            return
        elif not args[3].isdigit():
            await my_send_private_msg(bot, event, "你输入的群号有误")
            return
        target_group_id = int(args[3])
    elif isinstance(event, GroupMessageEvent):
        if len(args) == 3:
            target_group_id = event.group_id
        else:
            if not args[3].isdigit():
                await my_send_group_msg(bot, event, "你输入的群号有误")
                return
            else:
                target_group_id = int(args[3])

    if args[2] == "enable":
        if args[1] == "join":
            if target_group_id in join_notice_list:
                await my_send_msg(bot, event, "该群聊已在入群通知列表中")
            else:
                join_notice_list.append(target_group_id)
                await my_send_msg(bot, event, f"已将{target_group_id}添加至入群通知列表")
        elif args[1] == "leave":
            if target_group_id in leave_notice_list:
                await my_send_msg(bot, event, "该群聊已在退群通知列表中")
            else:
                leave_notice_list.append(target_group_id)
                await my_send_msg(bot, event, f"已将{target_group_id}添加至退群通知列表")
        elif args[1] == "builder":

            open_builder_message = 1
            await my_send_msg(bot, event, f"群{target_group_id}已开启超绝复原推送")
    elif args[2] == "disable":
        if args[1] == "join":
            if target_group_id not in join_notice_list:
                await my_send_msg(bot, event, "该群聊不在入群通知列表中")
            else:
                join_notice_list.remove(target_group_id)
                await my_send_msg(bot, event, f"已将{target_group_id}从入群通知列表中删除")
        elif args[1] == "leave":
            if target_group_id not in leave_notice_list:
                await my_send_msg(bot, event, "该群聊不在退群通知列表中")
            else:
                leave_notice_list.remove(target_group_id)
                await my_send_msg(bot, event, f"已将{target_group_id}从退群通知列表中删除")
        elif args[1] == "builder":
            open_builder_message = 0
            await my_send_msg(bot, event, f"群{target_group_id}已关闭超绝复原推送")
    else:
        await my_send_msg(bot, event, "指令有误喵")

    with open("configs/join_notice_list.txt", "w", encoding="utf-8") as f:
        for number in join_notice_list:
            f.write(f"{number}\n")
    with open("configs/leave_notice_list.txt", "w", encoding="utf-8") as f:
        for number in leave_notice_list:
            f.write(f"{number}\n")
    with open("configs/open_builder_message.txt", "w", encoding="utf-8") as f:
        f.write(f"{open_builder_message}")


"""
下面两个都是测试接口
随时删除
"""
@test2.handle()
async def send_test(bot: Bot, event: Event, state: T_State):
    if isinstance(event, GroupMessageEvent):
        m = Message([
            # MessageSegment(type="text", data={"text": "hello"}),
            # MessageSegment(type="markdown", data={"markup":"&#91;测试按钮&#93;(mqqapi://aio/inlinecmd?command=%E5%90%8C%E6%B5%8E%E7%B4%AB%E6%99%B6%E7%A4%BE%EF%BC%8C%E6%88%91%E4%BB%AC%E5%96%9C%E6%AC%A2%E4%BD%A0%F0%9F%A4%A4%0A%0A%E5%A4%A7%E5%AE%B6%E6%9D%A5%E5%8F%82%E5%8A%A0%E6%9D%8E%E5%BA%84%E5%A4%8D%E5%8E%9F%E6%B4%BB%E5%8A%A8%E5%96%B5&amp;reply=false&amp;enter=true)"})
            MessageSegment(type="xml", data={
                'data': '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><msg serviceID="1"><item><title>test title</title><summary>test content</summary></item><source name="官方认证消息" icon="https://qzs.qq.com/ac/qzone_v5/client/auth_icon.png" action="" appid="-1" /></msg>'})
        ])
        await bot.send_group_msg(group_id=event.group_id, message=m, auto_escape=False)
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=event.user_id,
                                   message="你，艾草！[CQ:markdown,content=&#91;测试按钮&#93;(mqqapi://aio/inlinecmd?command=%E5%90%8C%E6%B5%8E%E7%B4%AB%E6%99%B6%E7%A4%BE%EF%BC%8C%E6%88%91%E4%BB%AC%E5%96%9C%E6%AC%A2%E4%BD%A0%F0%9F%A4%A4%0A%0A%E5%A4%A7%E5%AE%B6%E6%9D%A5%E5%8F%82%E5%8A%A0%E6%9D%8E%E5%BA%84%E5%A4%8D%E5%8E%9F%E6%B4%BB%E5%8A%A8%E5%96%B5&amp;reply=false&amp;enter=true)]我，艾草！",
                                   auto_escape=False)


@test.handle()
async def send_test(bot: Bot, event: Event, state: T_State):
    if isinstance(event, GroupMessageEvent):
        await bot.send_group_msg(group_id=event.group_id,
                                 message="你，艾草！[CQ:markdown,content=&#91;测试按钮&#93;(mqqapi://aio/inlinecmd?command={urlencode(测试按钮)}&amp;reply=false&amp;enter=true)]你，艾草！",
                                 auto_escape=False)
    elif isinstance(event, PrivateMessageEvent):
        await bot.send_private_msg(user_id=event.user_id,
                                   message="你，艾草！[CQ:markdown,content=&#91;测试按钮&#93;(mqqapi://aio/inlinecmd?command=%E5%90%8C%E6%B5%8E%E7%B4%AB%E6%99%B6%E7%A4%BE%EF%BC%8C%E6%88%91%E4%BB%AC%E5%96%9C%E6%AC%A2%E4%BD%A0%F0%9F%A4%A4%0A%0A%E5%A4%A7%E5%AE%B6%E6%9D%A5%E5%8F%82%E5%8A%A0%E6%9D%8E%E5%BA%84%E5%A4%8D%E5%8E%9F%E6%B4%BB%E5%8A%A8%E5%96%B5&amp;reply=false&amp;enter=true)]我，艾草！",
                                   auto_escape=False)


"""
群聊中询问是否有服务器或执行!server指令时自动发送服务器信息一览
"""
@has_server.handle()
async def we_have_server(bot: Bot, event: Event, state: T_State):
    if not isinstance(event, GroupMessageEvent):
        return

    megs = """以下是紫晶社的服务器介绍
111
222
333"""
    await my_send_group_msg(bot, event, megs)


"""
群聊中发送“复原”等关键字时自动推送复原小广告
"""
@builder.handle()
async def please_join_builder(bot: Bot, event: Event, state: T_State):
    msgs: dict[int, str] = {
        1: "像素方块间，智慧之光照耀；虚拟校园中，澄澈梦想起航",
        2: "像素之下，是梦想的校园蓝图啾",
        3: "在虚拟与现实的交汇，寻找那片青春的校园",
        4: "建造元宇宙校园，构筑数字化教育新生态",
        5: "欢迎参加紫晶社的校园复原工程喵❤",
        6: "在Minecraft中，建设梦想校园，实现无限可能喵！",
        7: "用方块建起理想，用友谊铸就记忆，打造最棒嘟校园体验！",
        8: "在虚拟世界中，创造真实友谊，留下美好回忆，让我们的校园成为永恒传奇啾！",
        9: "每一个方块都是我们梦想的一部分喵",
        10: "用方块堆砌起紫晶社的未来啾",
        11: "神魂游荡方块处，一瞥复原中",
        12: "复原工程，启动汪！",
        13: "一砖一瓦，匠心独运，让同济大学在Minecraft里焕发新生喵！",
        14: "不只是游戏，是梦想的实践场！加入复原工程，共筑校园辉煌！",
        15: "从虚拟到现实，用方块搭建回忆，复原工程邀你同行！",
        16: "每一寸土地，每一座建筑，都在等待你的创造之手。参加复原工程，开启你的建筑传奇啾！",
        17: "用方块讲述我们的故事，让爱与梦想在校园中绽放！",
        18: "在复原工程中，领略不一样的大学风采喵",
    }
    if open_builder_message == 0:
        return

    await my_send_msg(bot, event, msgs.get(random.randint(1, 18)))

# ONLY TJMC
# BY LVREN - 2024/9/23
