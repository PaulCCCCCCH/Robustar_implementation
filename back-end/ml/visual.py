from lib.flashtorch_.utils import apply_transforms,load_image
from lib.flashtorch_.saliency import Backprop

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO

from nn import DataModel,torch,time

class Visual:
    data_model=DataModel()
    
    def get_model(self,modelid,datasetid):
        return self.data_model.get_model(modelid,datasetid)

    def get_dataset(self,datasetid,isTestset):
        return self.data_model.get_dataset(datasetid,isTestset)

    def top_acc(self,arr,count=10):
        narr=arr[0][:count]
        result=[]
        for a in narr:
            result.append(round(float(a*100),2))
        return result

    def visualize(self,mymodel,imgpath,imgsize):

        backprop=Backprop(mymodel)

        image=load_image(imgpath)
        image=apply_transforms(image,imgsize)


        t1=time.time()
        # image,_=get_random_img()
        modeloutput=backprop.model(image)
        modeloutput=torch.nn.functional.softmax(modeloutput,1)
        
        t2=time.time()
        _,predict=torch.max(modeloutput,1)
        images=backprop.visualize(image,predict,guided=True,return_image=True)
        
        t3=time.time()
        
        self.img_io = BytesIO()
        plt.savefig(self.img_io)
        
        #plt.savefig('img-v.png')
        plt.close('all')

        t4=time.time()
        
        print(t4-t3,t3-t2,t2-t1)

        return self.top_acc(modeloutput),int(predict)

    def get_path(self,dataset,imgid):
        if(len(dataset)<=imgid):
            imgid=len(dataset)-1

        return dataset.samples[imgid][0]

    def get_visual_img(self,imgid:int,modelid:int=0,datasetid:int=0,isTestset:bool=True):

        r"""Returns classes of the dataset, model output and label, the image will save into the file folder

        Args:
            imgid (int): id of the image
            modelid (int): 0 is normal 1 is pgd model
            datasetid (int): 0 is imagenet 1 is cifar10
            isTestset (boolean): 0 is trainset 1 is testset
        """
        dataset,imgsize,classes=self.data_model.get_dataset(datasetid,isTestset)
        datasetlength=len(dataset)
        if(datasetlength<=imgid):
            imgid=datasetlength-1
        imgpath=self.get_path(dataset,imgid)
        model=self.data_model.get_model(modelid,datasetid)

        model_output,model_predict=self.visualize(model,imgpath,imgsize)
        label=int(dataset[imgid][1])

        return classes,model_predict,label,model_output,datasetlength

visualObj=Visual()