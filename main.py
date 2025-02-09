from flask import *
from flask_cors import CORS
from urllib.parse import quote, unquote
import file, ErrorHook
import json, requests, time, random, math, hashlib, os, operator, base64, uuid, threading

app = Flask(__name__)
CORS(app)
browser = "C:\Program Files\Google\Chrome\Application\chrome.exe"
dataPath="\\data_"

# File Start
@app.route("/layui/<path:filename>")
def layuiJs(filename):
    return send_from_directory("layui", filename)


@app.route("/layui/<path:pathname>/<path:filename>")
def layui(pathname, filename):
    return send_from_directory("layui\\" + pathname, filename)


# File End


@app.route("/")
def _():
    return redirect("/index")


@app.route("/index")
def _index():
    hide = False
    for i, j in seted.items():
        hide = hide or j
    return render_template(
        "index.html",
        luogu=seted["luogu"],
        hide=("none" if hide else ""),
        unhide=("" if hide else "none"),
    )


@app.route("/record")
def record():
    return render_template("record.html", oj_type=request.args.get("oj", 'luogu'),
                    hide=request.args.get('hide','no'),height=request.args.get('height','75%'))

@app.route("/luoguProblem")
def luoguRecord():
    data=luogu_problem()
    pre=data['currentData']['record']['sourceCode']
    subtasks=data['currentData']['record']['detail']['judgeResult']['subtasks']
    message=data['currentData']['record']['detail']['compileResult']['message']
    # print(data)
    return render_template("luoguProblem.html",
        pre=pre,
        subtasks=subtasks,
        message=message.replace('\\','\\\\').replace('\n','\\n') if message!=None else "",
        )

@app.route("/newOJ", methods=["GET", "POST"])
def newOJ():
    global user,cookie
    if request.method == "GET":
        return render_template("newOJ.html")
    else:
        oj_type = request.form.get("oj_type")
        user[oj_type] = request.form.get("uid")
        cookie[oj_type] = request.form.get("cookie")
        return "ok"


@app.route("/checkOJ")
def checkOJ():
    global user,cookie,seted
    try:
        oj_type = request.args.get("oj_type")
        parse[oj_type](1, True)
    except:
        return "Error"
    seted[oj_type] = True
    File.save(dataPath+"\\cookie.json", cookie)
    File.save(dataPath+"\\user.json", user)
    File.save(dataPath+"\\seted.json", seted)
    return "ok"


debug = True
File = file.File("json")
FileText = file.File("plain")
cookie = File.read(dataPath+"\\cookie.json")
user = File.read(dataPath+"\\user.json")
seted = File.read(dataPath+"\\seted.json")
lastupd = FileText.read(dataPath+"\\lastupd.file")


def luogu_parse(page, check=False):
    global lastupd
    # return jsonify({'code':429,'msg':'429 Too Many Requests<br>请求过快'})
    if not check:
        if time.time() - float(lastupd) > 0.8:
            lastupd = time.time()
            FileText.save(dataPath+"\\lastupd.file", lastupd)
        else:
            return jsonify(
                {
                    "code": 429,
                    "msg": '429 Too Many Requests<br>请求过快<br><button onclick="window.location.reload()" class="layui-btn">刷新</button>',
                }
            )
    req = requests.get(
        "https://www.luogu.com.cn/record/list?user={}&page={}&_contentOnly=1".format(
            user["luogu"], page
        ),
        headers={
            "Host": "www.luogu.com.cn",
            "Cookie": cookie["luogu"],
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        },
    )
    # ans=req.text.split('"));')[0].split('JSON.parse(decodeURIComponent("')[-1]
    ans = req.text
    # Cookie update
    for key, item in req.cookies.items():
        cookie[key] = item
    data = json.loads(unquote(ans))
    # print(data)
    data_ = {"code": 0, "count": data["currentData"]["records"]["count"], "data": []}
    for i in data["currentData"]["records"]["result"]:
        i["oj"] = "https://www.luogu.com.cn/problem/pid"
        data_["data"].append(i)
    if check:
        if data["code"] != 200:
            raise
        return "ok"
    return jsonify(data_)

# @app.route('/getLuoguProblem')
def luogu_problem():
    id=request.args.get('id')
    req=requests.get('https://www.luogu.com.cn/record/{}?_contentOnly=1'.format(id),
        headers={
            "Host": "www.luogu.com.cn",
            "Cookie": cookie["luogu"],
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        },
    )
    # print(req.text)
    return json.loads(req.text)

parse = {"luogu": luogu_parse}


@app.route("/getLuogu")
def getLuogu():
    if seted["luogu"]:
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 20, type=int)
        return luogu_parse(page)
    else:
        return {"code": 0}


@app.route("/favicon.ico")
def favicon():
    return send_from_directory("file", "favicon.ico")


if __name__ == "__main__":
    if not debug:
        threading.Thread(
            target=lambda: os.system('"' + browser + '" --app=http://127.0.0.1:8888')
        ).start()
    app.run(port=8888, debug=debug)
