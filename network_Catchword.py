from hoshino import Service, priv, logger
from hoshino.typing import CQEvent
from bs4 import BeautifulSoup
import requests
sv_help = """
[网络词典] 不懂就问: 
xxx是什么意思(?)
xxx是什么梗(?)
""".strip()

sv = Service(
    name="网络词典",  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=True,  # 默认启用
    bundle="娱乐",  # 分组归类
    help_=sv_help,  # 帮助说明
)

# r = requests.get(f"https://jikipedia.com/search?phrase=%E6%98%93%E5%A4%A7%E5%B1%B1&category=definition")
# print(page)

@sv.on_suffix(("是什么意思", "是什么意思？", "是什么意思?", "是什么梗", "是什么梗？", "是什么梗?"))
async def search_keyword(bot, ev: CQEvent):
    _KEYWORD = ev.message.extract_plain_text().strip()


    if _KEYWORD == "":
        await bot.send("查询格式错误, 请按照如下格式查询")
        await bot.send(sv_help)
        return 


    _URL = "https://jikipedia.com/search?phrase="
    _URL += _KEYWORD
    _URL += "&category=definition"
    

    try:
        r = requests.get(_URL)
    except Exception as ex:
        print("[Err]: " + ex)
        logger.exception(ex)
        await bot.send("查询失败, 请查看log输出")
        return 


    soup = BeautifulSoup(r.text, "html.parser")


    result = ""
    for tag in soup.findAll("a"):
        if ("title=\"" + _KEYWORD) in str(tag): # tag: <a>
        # if _KEYWORD in tag.text: # tag: <a>
            for content in tag.contents: # content: <span>
                result += content.text


    if len(result):    
        await bot.send(ev, result, at_sender=True)
    else:    
        await bot.send(ev, "没有找到这个词哦", at_sender=True)
