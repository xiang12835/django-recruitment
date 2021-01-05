import json
import requests


# 机器人的链接
wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=cc41413d-6a15-4fe0-ba3d-8d666f44ca59"


def send_msg(_content="Hello WeChat"):

    # json格式化发送的数据信息
    data = json.dumps({
        "msgtype": "text",
        "text": {
            "content": _content,  # 发送的消息内容
            "mentioned_list": ["@all"]  # 圈出所有人
        }
    })

    # 指定机器人发送消息
    r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
    print(r.json)

    # headers = {"Content-Type": "text/plain"}
    # data = {
    #     "msgtype": "text",
    #     "text": {"content": _content}
    # }
    #
    # ret = requests.post(
    #     url=wx_url,
    #     # 此处为新建机器人以后生成的链接
    #     headers=headers,
    #     json=data
    # )
    #
    # print(ret.text)  # 成功后的打印结果：{"errcode":0,"errmsg":"ok"}


if __name__ == '__main__':
    send_msg()
