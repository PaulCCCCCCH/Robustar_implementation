influence_dic=None
import json
def load_influence():
    global influence_dic
    try:
        with open('influence/influence_results.json') as f:
            influence_dic = json.load(f)
    except:
        influence_dic = None
    
    if(influence_dic==None):
        print("fail to load influence data, please ensure ./influence/influence_results.json exist")
    else:
        print("load influence data success,",str(len(influence_dic)),"images data were loaded")

def check_influence(img_id):
    if(influence_dic != None):
        if(len(influence_dic)>1):
            if(len(influence_dic)>int(img_id)):
                return True
    return False

def get_helpful_list(img_id):
    img_id=str(img_id)
    if(influence_dic.get(img_id)):
        return influence_dic[img_id]['helpful']

def get_harmful_list(img_id):
    img_id=str(img_id)
    if(influence_dic.get(img_id)):
        return influence_dic[img_id]['harmful']


def get_influence_list(img_id):
    img_id=str(img_id)
    if(influence_dic.get(img_id)):
        return influence_dic[img_id]['influence']