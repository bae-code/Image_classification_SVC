from tkinter.messagebox import NO
from flask import Flask, render_template,Blueprint
import collections
from pymongo import MongoClient


client = MongoClient('mongodb+srv://test:sparta@cluster0.0pi7g.mongodb.net/Cluster0?retryWrites=true&w=majority') # 클라이언트 설정시 작성
db = client.TEKKEN


bp = Blueprint("char_result", __name__, url_prefix="/char_result", static_folder="static", template_folder="templates")


@bp.route('/<result>')
def home(result):
    try:
        char = db.char.find_one({'name': result})

        name = char['name']
        face = char['Face']
        result_list = list(db.compared_face_result.find({},{'_id':False}))

        all_result= len(result_list)
        
        
        ### 결과값만 저장하는 list
        top_list = []
        for i in result_list:
            name = i['result']
            top_list.append(name)
        ### 리스트에 있는 객체 카운트하면서 최상위부터 순서대로 정렬.
        counts = collections.Counter(top_list)
        ### 카운트한 순서의 .most_common(뽑으려고하는 개수)
        rank = counts.most_common(51)

        all_rank = {}
        tr = 0
        while tr < 51:
            try:
                all_rank["rank{0}".format(tr)] = rank[tr][0] , "%.2f" % (rank[tr][1] * 100 / all_result)
                tr = tr+1
            except:
                break



        return render_template('result.html', name = name, face = face ,all_result = all_result, first=all_rank["rank0"],sec=all_rank["rank1"],thd=all_rank["rank2"])
    except:
        return render_template('error.html')
