# -*- coding: utf-8 -*-
import sys,time,threading,os
import re
from generate import generate_paired_data
from datetime import timedelta
import json

from werkzeug.serving import make_server

def ml_initialize(configs):
    from ml import DataSet,PairedDataset,Model,Trainer

    #这里用来分类正确和错误的图像
    batch_size=int(configs['batchSize'])
    learn_rate=float(configs['learn_rate'])
    num_workers=int(configs['thread'])
    shuffle=True if configs['shuffle'] == "yes" else False
    save_dir=configs['save_to'] if configs['save_to'] else './temp_path'
    use_paired_train=True if configs['paired_train'] == 'yes' else False
    paired_train_reg_coeff=float(configs['paired_train_reg_coeff'])
    paired_train_mode=configs['paired_train_mode']
    image_size=int(configs['image_size'])
    classes_path=configs['classes']
    trainset=configs['trainset']
    testset=configs['testset']

    from visual import visualObj

    if use_paired_train:
        paired_path = '/'.join(trainset.split('/')[:-1]) + '/paired'
        train_set = PairedDataset(trainset, paired_path, image_size, classes_path, paired_train_mode)
    else:
        train_set = DataSet(trainset,image_size,classes_path)

    test_set = DataSet(testset,image_size=int(configs['image_size']),classes_path=configs['classes'])

    model=Model(configs['model'],configs['weight'],'cuda',configs['pretrain'])


    trainer=Trainer(model.net,train_set,test_set,batch_size,
                    shuffle,num_workers,'cuda',learn_rate,True,
                    save_dir,model.network_type,
                    use_paired_train=use_paired_train,
                    paired_reg=paired_train_reg_coeff)

    return train_set,test_set,model,trainer


def run(configs):
    from server import app,get_correct
    print("configs:",configs)

    train_set,test_set,model,trainer=ml_initialize(configs)

    app.train_set = train_set
    app.test_set = test_set
    app.model=model
    app.trainer=trainer
    get_correct(True,0)

    from ml import Model
    model=Model(configs['model'],configs['weight'],configs['device'],configs['pretrain'])

    app.model=model
    app.run(port=int(configs['port']),host="0.0.0.0",debug=False)

#多进程启动服务器
class ServerProcess():
    def start(self,config_dic):
        from multiprocessing  import Process
        self.ps = Process(target=run,args=(config_dic,))
        self.ps.start()

    def shutdown(self):
        self.ps.terminate()


    # TODO: These should really be the trainer's method
    # def closeEvent(self, event):
    #     self.train_thread._stop() 

    # def start_train(self):
    #     from ml import DataSet,Model,Trainer
    #     import math
    #     configs=self.configs

    #     train_set,test_set,model,trainer=ml_initialize(configs)

    #     self.iter_per_epoch=math.ceil(1.0*len(train_set)/int(configs['batchSize']))
    #     self.start_train_time=time.time()
    #     import threading
    #     self.train_thread=threading.Thread(target=trainer.start_train, args=(self.update_info,int(configs['epoch']),configs['auto_save_model']=='yes'))
    #     self.train_thread.start()
    #     if self.exit_when_finish:
    #         self.train_thread.join()
    #         sys.exit()



#记录日志，并且在主界面上显示
class Log():
    outputText=None
    
    #不带有时间的记录
    @staticmethod
    def log(text):
        Log.outputText.append(text)

    #带有时间的记录
    @staticmethod
    def t(text):
        Log.outputText.append(time.strftime("%H:%M:%S")+" "+text)  




#主界面
class MyGUI(QTabWidget):
    CONFIG_FILE='config.json'

    def __init__(self):
        self.load_config()

    #选择权重文件
    def select_weight(self,e):
        ## TODO: 权重文件从config中读取
        weightPath=QFileDialog.getOpenFileName(self,'choose a weight file','' ,'PyTorch weight files(*.pth)')
        weightPath=str(weightPath[0])
        if len(weightPath) > 0:
            self.weightEdit.setText(weightPath)

    #选择保存模型的文件夹
    def select_save_folder(self, e):
        # TODO: read dest dir from config
        # No need to do error checking here
        pass

    #选择被镜像的数据集
    def select_mirror_folder(self,e):
        # TODO: read from config
        mirrorFolder = None
        if mirrorFolder:
            self.mirroredDatasetPathEdit.setText(mirrorFolder)

    #选择JSON文件
    def select_user_edit(self,e):
        # TODO: read from config
        userEditFilePath = None
        if len(userEditFilePath) > 0:
            self.jsonFileEdit.setText(userEditFilePath)

    #选择数据集    
    def select_trainset(self,e):
        # TODO: read from config
        datasetFolder = None
        if(len(datasetFolder)>0):
            self.trainsetEdit.setText(datasetFolder)
    def select_testset(self,e):
        # TODO: read from config
        datasetFolder = None
        if(len(datasetFolder)>0):
            self.testsetEdit.setText(datasetFolder)
    
    def select_class(self,e):
        # TODO: read from config
        classPath = None
        classPath=str(classPath[0])
        if(len(classPath)>0):
            self.classesEdit.setText(classPath)
    

    #初始化服务器设置界面
    def _init_server_ui(self):
        """
        网格布局 跨越 多行 或者 多列
        :return:
        """
   
    # TODO: what does this do?
    def classify_all(self,e):
        configs=self.get_config_dic()
        train_set,test_set,model,trainer=ml_initialize(configs)

        classify_result=trainer.get_test_result()
        with open("classify.json",'w') as json_file:
            json.dump(classify_result,json_file)

    def save_config(self):
        import json
        configs=self.get_config_dic()
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(configs, f)
    
    def load_config(self):
        if not os.path.exists(self.CONFIG_FILE):
            return
        import json
        with open(self.CONFIG_FILE, 'r') as f:
            configs = json.load(f)
            self.set_config_dic(configs)


    def set_config_dic(self,configs):

        #安全地获取config内容，防止加入新配置后出现keyError的情况
        def get_config(configs,field):
            if field not in configs:
                return ""
            return configs[field]

        self.modelEdit.setCurrentText(get_config(configs, 'model'))
        self.weightEdit.setText(get_config(configs, 'weight'))
        self.saveToEdit.setText(get_config(configs, 'save_to'))
        self.trainsetEdit.setText(get_config(configs, 'trainset'))
        self.testsetEdit.setText(get_config(configs, 'testset'))
        self.classesEdit.setText(get_config(configs, 'classes'))
        self.portEdit.setText(get_config(configs, 'port'))
        self.pairedTrainEdit.setCurrentText(get_config(configs, 'paired_train'))
        self.pairedTrainRegCoeffEdit.setText(get_config(configs, 'paired_train_reg_coeff'))
        self.pairedTrainModeEdit.setCurrentText(get_config(configs, 'paired_train_mode'))
        self.pgdEdit.setCurrentText(get_config(configs, 'pgd'))
        self.learnRateEdit.setText(get_config(configs, 'learn_rate'))
        self.epochEdit.setText(get_config(configs, 'epoch'))
        self.imageSieEdit.setText(get_config(configs, 'image_size'))
        self.shuffleEdit.setCurrentText(get_config(configs, 'shuffle'))
        self.pretrainEdit.setCurrentText(get_config(configs, 'pretrain'))
        self.autoSaveEdit.setCurrentText(get_config(configs, 'auto_save_model'))
        self.deviceEdit.setCurrentText(get_config(configs, 'device'))
        self.threadEdit.setText(get_config(configs, 'thread'))
        self.batchSizeEdit.setText(get_config(configs, 'batchSize'))

    def get_config_dic(self):
        result={}
        result['model']=self.modelEdit.currentText()
        result['weight']=self.weightEdit.text()
        result['save_to']=self.saveToEdit.text()
        result['trainset']=self.trainsetEdit.text()
        result['testset']=self.testsetEdit.text()
        result['classes']=self.classesEdit.text()
        result['port']=self.portEdit.text()
        result['paired_train']=self.pairedTrainEdit.currentText()
        result['paired_train_reg_coeff']=self.pairedTrainRegCoeffEdit.text()
        result['paired_train_mode']=self.pairedTrainModeEdit.currentText()
        result['pgd']=self.pgdEdit.currentText()
        result['learn_rate']=self.learnRateEdit.text()
        result['epoch']=self.epochEdit.text()
        result['image_size']=self.imageSieEdit.text()
        result['shuffle']=self.shuffleEdit.currentText()
        result['pretrain']=self.pretrainEdit.currentText()
        result['auto_save_model']=self.autoSaveEdit.currentText()
        result['device']=self.deviceEdit.currentText()
        result['thread']=self.threadEdit.text()
        result['batchSize']=self.batchSizeEdit.text()
        return result

    # TODO: This list may be useful
    def _init_library_ui(self):
        
        librariesInstall=['numpy','matplotlib','Flask','opencv_python','flashtorch','importlib_resources','Pillow','pytorch_influence_functions','PyYAML','torch','torchattacks','torchvision','pyqt','pyqtgraph']
        
        librariesImport=['numpy','matplotlib','flask','cv2','flashtorch','importlib_resources','PIL','pytorch_influence_functions','yaml','torch','torchattacks','torchvision','PyQt5','pyqtgraph']
    

#处理需要加载json的情况
def deal_json(arg_list):
    for i in arg_list:
        if i.find('.json')>0:
            MyGUI.CONFIG_FILE=i

# FIXME: Not used
def is_paired_image(imgPath1, imgPath2):
    tokens1 = re.split('[/(\\\\)]', imgPath1)
    tokens2 = re.split('[/(\\\\)]', imgPath2)
    return len(tokens1) == len(tokens2) and all(t1[i] == t2[i] for t1, t2 in zip(tokens1, tokens2))

# TODO: Should not do anything when the file is directly executed
if __name__ == '__main__':
    mainUI.start_train(None)
