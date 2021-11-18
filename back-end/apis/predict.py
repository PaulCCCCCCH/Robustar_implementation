from objects.RServer import RServer
from flask import jsonify
from utils.image_utils import get_dataset_file

app = RServer.getServer().getFlaskApp()



@app.route('/influence-img/<number>')
def get_random_influence_img(number):
    import random
    import math
    random_num = random.randint(1, 1000)
    random_num = math.floor(float(number)*1000)
    url = get_dataset_file('train'+'/'+str(random_num))
    # return redirect('/dataset/train/'+url)
    return '/dataset/train/' + url

# 将编号转化为图片路径
@app.route('/predictid/<folder>/<imageid>')
def get_predict_img_from_id(folder, imageid):
    url = get_dataset_file(folder+'/'+str(imageid))
    filePath = folder+'/'+url
    return get_predict_img(filePath)


@app.route('/getinfluence/<img_id>/<helpful_num>/<harmful_num>', methods=['POST', 'GET'])
def get_influence_dic(img_id, helpful_num, harmful_num):
    result = {}
    result['success'] = 1
    if(not check_influence(img_id)):
        result['success'] = 0
        return jsonify(result)
    helpful_num = int(helpful_num)
    harmful_num = int(harmful_num)

    helpful_list = get_helpful_list(img_id)
    harmful_list = get_harmful_list(img_id)
    influence_list = get_influence_list(img_id)

    helpful_list = helpful_list[:helpful_num]
    harmful_list = harmful_list[:harmful_num]
    helpful_influence = []
    harmful_influence = []
    for i in helpful_list:
        helpful_influence.append(influence_list[i])
    for i in harmful_list:
        harmful_influence.append(influence_list[i])
    result['helpful_list'] = helpful_list
    result['harmful_list'] = harmful_list
    result['helpful_influence'] = helpful_influence
    result['harmful_influence'] = harmful_influence

    return jsonify(result)

