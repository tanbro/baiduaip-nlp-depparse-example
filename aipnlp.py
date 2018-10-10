from aip import AipNlp
from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, jsonify, send_from_directory, abort, make_response
import yaml

POSTAGS = {
    'Ag': '形语素',
    'g': '语素',
    'ns': '地名',
    'u': '助词',
    'a': '形容词',
    'h': '前接成分',
    'nt': '机构团体',
    'vg': '动语素',
    'ad': '副形词',
    'i': '成语',
    'nz': '其他专名',
    'v': '动词',
    'an': '名形词',
    'j': '简称略语',
    'o': '拟声词',
    'vd': '副动词',
    'b': '区别词',
    'k': '后接成分',
    'p': '介词',
    'vn': '名动词',
    'c': '连词',
    'l': '习用语',
    'q': '量词',
    'w': '标点符号',
    'dg': '副语素',
    'm': '数词',
    'r': '代词',
    'x': '非语素字',
    'd': '副词',
    'Ng': '名语素',
    's': '处所词',
    'y': '语气词',
    'e': '叹词',
    'n': '名词',
    'tg': '时语素',
    'z': '状态词',
    'f': '方位词',
    'nr': '人名',
    't': '时间词',
    'un': '未知词',
}

DEPRELS = {
    'ATT': '定中关系',
    'QUN': '数量关系',
    'COO': '并列关系',
    'APP': '同位关系',
    'ADJ': '附加关系',
    'VOB': '动宾关系',
    'POB': '介宾关系',
    'SBV': '主谓关系',
    'SIM': '比拟关系',
    'TMP': '时间关系',
    'LOC': '处所关系',
    'DE': '“的”字结构',
    'DI': '“地”字结构',
    'DEI': '“得”字结构',
    'SUO': '“所”字结构',
    'BA': '“把”字结构',
    'BEI': '“被”字结构',
    'ADV': '状中结构',
    'CMP': '动补结构',
    'DBL': '兼语结构',
    'CNJ': '关联词',
    'CS': '关联结构',
    'MT': '语态结构',
    'VV': '连谓结构',
    'HED': '核心',
    'FOB': '前置宾语',
    'DOB': '双宾语',
    'TOP': '主题',
    'IS': '独立结构',
    'IC': '独立分句',
    'DC': '依存分句',
    'VNV': '叠词关系',
    'YGC': '一个词',
    'WP': '标点',
}


app = Flask(__name__, static_url_path='')
app.config.update(yaml.load(open('config.yml')))
app.jinja_loader = FileSystemLoader('templates')


@app.route('/node_modules/<path:path>', methods=['GET'])
def serve_js(path):
    return send_from_directory('node_modules', path)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/visualize', methods=['POST'])
def visualize():
    req_data = request.get_json()

    # 调用依存句法分析
    nlp = AipNlp(app.config['APP_ID'], app.config['API_KEY'], app.config['SECRET_KEY'])
    deparse_result = nlp.depParser(req_data['text'], req_data.get('options', {}))

    if 'error_code' in deparse_result:
        return jsonify(deparse_result)

    res_data = render_template(
        'dependency_parsing.dot.jinja2',
        text=deparse_result['text'], items=deparse_result['items'], postags=POSTAGS, deprels=DEPRELS
    )
    return jsonify(result=res_data)
