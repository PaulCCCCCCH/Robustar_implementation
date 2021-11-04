class ImageIdConvertor:
    dic_id_path=None
    dic_path_id=None

    def get_id_dic(self,dataset,name,dic_id_path,dic_path_id):
        for i in range(len(dataset.samples)):
            current_id=name+'-'+str(i)
            current_path=dataset.samples[i][0].replace("\\","/")
            dic_id_path[current_id]=current_path
            dic_path_id[current_path]=current_id
        return dic_id_path,dic_path_id


    def __init__(self,trainset,testset):
        if ImageIdConvertor.dic_id_path is None and ImageIdConvertor.dic_path_id is None:
            dic_id_path,dic_path_id={},{}

            self.get_id_dic(trainset,'train',dic_id_path,dic_path_id)
            self.get_id_dic(testset,'test',dic_id_path,dic_path_id)

            ImageIdConvertor.dic_id_path=dic_id_path
            ImageIdConvertor.dic_path_id=dic_path_id