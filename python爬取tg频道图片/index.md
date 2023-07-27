# Python爬取TG频道图片

转载自：https://binbla.com/?p=339
```python
import asyncio
import logging
import socks
import telethon.tl.types
from aiofile import AIOFile, Writer
from telethon import TelegramClient, events
from telethon.tl.types import PeerChannel
"""
-> 这是一个Telegram机器人项目

-> 实现的功能：爬取Telegram中频道的图片
-> 注意：由于机器人无法加入其他人的频道，所以扒频道的图只能交给主体账户来进行（不会影响主账户的登录）
"""
# 网友反馈：申请需要填个人网站，应该是随便填一个能正常访问的网址就行
# your telegram api id
api_id = xxxxxxx
# your telegram api hash
api_hash = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'
# get form https://my.telegram.org/apps



# your chat id
admin_id = xxxxxxxx
# get from https://telegram.me/getidsbot
# 暂时不用填
# your bot_token
bot_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'
# get from https://telegram.me/botfather

# file save path
save_path = '/home/admin/Telegram/'

# proxy
proxy_type = socks.SOCKS5
proxy_addr = 'localhost'
proxy_port = 20170

# 要监视下载的频道,名字（键名）无实际代码作用，不要重复就行
channel = {
    "少女情怀总是诗": 1336617732,
    "咸鱼的杂货铺 ASWL": 1445018107,
    "白丝即正义": 1088679595,
    "For world|精选|收集器": 1109579085,
    "奇闻异录 与 沙雕时刻": 1214996122
    }

# 接受监视的媒体格式(tg里面直接发送gif最后是mp4格式！)
accept_file_format = ["image/jpeg", "image/gif", "image/png"]

# Mirai机器人插件的地址和端口
target_addr = "localhost"
target_port = 13131

# bot登陆：留作将来开发控制程序
# bot = TelegramClient('transferBot', api_id, api_hash, proxy=(proxy_type, proxy_addr, proxy_port)).start(
#     bot_token=bot_token).start()

# 用户登陆
client = TelegramClient('transfer', api_id, api_hash, proxy=(proxy_type, proxy_addr, proxy_port)).start()
# client = TelegramClient('transfer', api_id, api_hash).start()
# 列表推导式 获取频道对象列表
channel_list = [PeerChannel(channel[channel_name]) for channel_name in channel]


# 过滤出监视下载的频道，如果有媒体消息就下载
@client.on(events.NewMessage(from_users=channel_list))
async def event_handler(event):
    # 获取对话
    # chat = await event.get_chat()

    # 获取message内容
    message = event.message

    # 判断是否有媒体
    if message.media is not None:
        print("发现媒体")
        await download_image(message)


# 下载媒体的具体方法
async def download_image(message):
    # 如果是网页
    is_webpage = isinstance(message.media,telethon.tl.types.MessageMediaWebPage)
    # 如果媒体是照片则直接下载
    is_photo = isinstance(message.media, telethon.tl.types.MessageMediaPhoto)
    # 如果媒体是文件则检查是否是可接受的文件格式，这里用的否定表达，不好读！建议跳过或者自己写一个
    is_doc = isinstance(message.media, telethon.tl.types.MessageMediaDocument)

    if not (is_photo or is_webpage):
        if is_doc:
            is_accept_media = message.media.document.mime_type in accept_file_format
            if not is_accept_media:
                print("不可接受")
                return

    # 这里由于download_media()可以自动命名
    # 所以，判断重复有点难搞，不过频道应该不怎么发重复内容
    # 那就这样吧!不写了
    # if os.path.exists(filename):
    #     print("文件已存在")
    #     return

    # 这个方法下载成功后会返回文件的保存名
    filename = await client.download_media(message, save_path)
    if filename is None:
        print("下载失败")
        return
    print("下载完成")
    # 下面注释的代码不知道什么原因无法在文件不存在的情况下新建文件
    # async with async_open(save_path + "1.txt", "a") as f:
    #     await f.write(filename + "\n")
    print(message.sender.id,message.raw_text)
    # 通知mirai机器人干活，没有mirai机器人就注释下下面一行代码
    await send_to_mirai(message.sender.id,message.sender.title, message.raw_text, filename)

    #socket通信通知QQ机器人（机器人插件见另一篇）
async def send_to_mirai(from_id, from_title, raw_text, filename):
    msg = str(from_id)+"\t"+filename+"\t"+from_title+"\t"+raw_text
    try:
        reader, writer = await asyncio.open_connection(target_addr, target_port)
        writer.write(msg.encode("utf-8"))
        writer.close()
        print("已通知mirai干活")
        print("-----*****-----")
    except Exception as e:
        print(e)
        print('socket通信失败！')
        await write_to_list(msg)


async def write_to_list(msg):
    async with AIOFile(save_path + "unprocessed_list.txt", "a") as list_file:
        write = Writer(list_file)
        await write(msg + "\n")
        print(msg)
        print("写入列表")
        print("-----*****-----")



async def bot_main():
    pass


# 展示登陆的信息
def show_my_inf(me):
    print("-----****************-----")
    print("Name:", me.username)
    print("ID:", me.id)
    print("-----login successful-----")


async def client_main():
    print("-client-main-")
    me = await client.get_me()
    show_my_inf(me)

    # 这个方法是一直连着直到断开，我没有写断开的代码，所以程序应该会一直运行
    await client.run_until_disconnected()


# 日志，这个是文档里建议使用的，但是我没有实际使用上
logging.basicConfig(format='[%(debug) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# 主函数入口
if __name__ == '__main__':
    with client:
        # 开启异步任务
        client.loop.run_until_complete(client_main())
```
