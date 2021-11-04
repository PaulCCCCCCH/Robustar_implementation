var trainTestType="train"
var currentImgId=0
var viewImageCount=7;

function updateImageData(){
    for(var i=0;i<viewImageCount;i++){
        loadImageEnqueue(currentImgId-Math.floor(viewImageCount/2)+i)
    }
    updateCanvasImg();
    notifyUpdateImage();
    // viewImage(trainTestType,currentImgId)
}
function trainSetClick(){
    trainTestType="train"
    updateImageData()
}
function testSetClick(){
    trainTestType="test"
    updateImageData()
}
function correctSetClick(){
    trainTestType="test_correct"
    updateImageData()
    if(!getLeftHide())
        showHideLeft();
}
function mistakeSetClick(){
    trainTestType="test_mistake"
    updateImageData()

    if(getLeftHide())
        showHideLeft();
}
function nextImageClick(num){
    currentImgId+=num
    updateImageData()
}
function lastImageClick(num){
    currentImgId-=num
    updateImageData()
}