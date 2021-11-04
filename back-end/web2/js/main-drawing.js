var drawing;
var context;
var imageData;
var backData=[];
var err=1;
var mode=-1;

var save_mode=false;

var fixed=null;

var currentCanvasImg=null;

// FIXME: testing
var count = 0;
    
function sendImageData(requestOnly){
    //send image data to the server
    
    prepareData=[]
    d=imageData.data
    
    if (requestOnly!=1){
        for(var i=0;i<d.length;i+=4){
            for(var j=0;j<4;j++){
                prepareData.push(d[i+j]);
            }
        }
    }
    
    
    var uid='{{uid}}';
    
    $.ajax({
        tradition:true,
         type: "POST", 
         url: "/get_modify", 
         data: { img: prepareData,uid:uid,requestonly:requestOnly }      
      }).done(function(msg){
        if(msg=='success')
            displayImage();
      });

}

function displayImage(){
    allImages=document.querySelectorAll('.random-img')
    allImages[0].parentNode.removeAttribute('hidden')
    for(var i=0;i<allImages.length;i++){
        currentURL=allImages[i].getAttribute('name')
        allImages[i].setAttribute('src',currentURL+'/'+Math.random())
    }
}

function convertLocation(x,y){
    //convert the location to array index of image data
    if(x>=drawing.width||x<0)
        return 0
    return ((drawing.width * y) + x) * 4
}

function cloneImageData(){
    //read image data from backup data
    for(var i=0;i<imageData.data.length;i++){
        imageData.data[i]=backData[i];
    }
}

function clear(x,y){
    a=convertLocation(x,y)
    for (var i=0;i<4;i++)
        imageData.data[a+i]=0;
}

var adjacentList=[[1,0],[0,1],[-1,0],[0,-1],[1,1],[1,-1],[-1,-1],[-1,1]]

function checkColor(color,loc){	
    for(var i=0;i<4;i++){
        var currentErr=imageData.data[loc+i]-color[i];
        if(Math.abs(currentErr)>err)
            return false;
    }
    return true;
}

function checkAndClearColor(color,x,y){
    var same = checkColor(color,convertLocation(x,y))
    if(same)
        clear(x,y);
    return same;
}

function setMode(newmode){
    mode=newmode;
    updateSelection(fixed);
}

function setErr(newErr){
    err=newErr;
    updateSelection(fixed);
}

function clearAdjacentOptimize(x,y,color,directions=4){
    map=[]
    for(var i=0;i<drawing.width*drawing.height;i++)
        map[i]=0;
    list=[[x,y]]
    while(list.length!=0){
    x=list[0][0];
    y=list[0][1];
    list.shift();
    for(var i=0;i<directions;i++){
        currentx=x+adjacentList[i][0];
        currenty=y+adjacentList[i][1];
        loc=convertLocation(currentx,currenty);
        if(map[loc/4]!=0)continue;
        var same=checkColor(color,loc);
        if(same){
            clear(x,y);
            map[loc/4]=1;
            list.push([currentx,currenty]);
        }
    }
    }
}

function clearAdjacent(x,y,map,color,directions=4){
    for(var i=0;i<directions;i++){
        currentx=x+adjacentList[i][0];
        currenty=y+adjacentList[i][1];
        loc=convertLocation(currentx,currenty);
        if(map[loc]!=0)continue;
        var same=checkColor(color,loc);
        if(same){
            clear(x,y);
            map[loc]=1;
            clearAdjacent(currentx,currenty,map,color,directions);
        }
    }
}
function clearRange(x,y,radius){

    for(var i=-radius;i<radius;i++){
        for(var j=-radius;j<radius;j++){
            clear(x+i,y+j);
        }
    }
}

function clearCircleRange(x,y,radius){

    for(var i=-radius;i<radius;i++){
        for(var j=-radius;j<radius;j++){
            if(i*i+j*j<radius*radius){
                clear(x+i,y+j);
            }
        }
    }
}


function getColor(x,y){
    color=[]
    for (var i=0;i<4;i++){
        color[i]=imageData.data[convertLocation(x,y)+i];
    }
    return color;
}

function clearSimilar(x,y){
    color=getColor(x,y);
    
    for(var i=0;i<drawing.width;i++){
        for(var j=0;j<drawing.height;j++){
            checkAndClearColor(color,i,j);
        }
    }
}

function getMousePos(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: parseInt( evt.clientX - rect.left),
      y: parseInt(evt.clientY - rect.top)
    };
  }

function updateSelection(loc){
    if(loc==null)return;

    cloneImageData()
    //clearSimilar(loc.x,loc.y);

    switch (mode){
        case 0: clearAdjacentOptimize(loc.x,loc.y,getColor(loc.x,loc.y)); break;
        case 1: clearAdjacentOptimize(loc.x,loc.y,getColor(loc.x,loc.y),8); break;
        case 2: clearSimilar(loc.x,loc.y); break;
        case 3: clearRange(loc.x,loc.y,err); break;
        case 4: clearCircleRange(loc.x,loc.y,err); break;
        default: break;
    }
    context.putImageData(imageData,0,0)
    if(save_mode)
        backup_data()
}


function recordHistory(){
    allHistory=document.querySelector(".history-display");
    template=allHistory.children[0];
    newHistory=template.cloneNode(true);
    newHistory.querySelector("img").src=drawing.toDataURL();
    //newHistory.querySelector(".delete-button").setAttribute("style","");
    newHistory.querySelector("span").textContent=""+new Date().toString("H:mm:ss").split(' ')[4];
    allHistory.appendChild(newHistory);
}

function clearHistory(){
    var allHistory=document.querySelector(".history-display");
    while(allHistory.children.length!=1)
        allHistory.children[1].remove()
}

function sendCanvas(){
    postCanvas()
}

function toImage(){
    document.querySelector(".final-img").src = drawing.toDataURL();
}

function backup_data(){
    for(var i=0;i<imageData.data.length;i++)
        backData[i]=imageData.data[i];
}

function loadToCanvas(sourceimage,width,height){
    context.clearRect(0, 0, width,height);
    context.drawImage(sourceimage,0,0,width,height)
    imageData = context.getImageData(0, 0, width,height);
    backup_data();
}

firstImage=true

function canvasInitLoop(img,width){
    setTimeout(prepare_canvas,100,img,width)
}

function prepare_canvas(img,width){
    if(img!=null)
        currentCanvasImg=img;
    else
        img=currentCanvasImg;
    window.canvasSRC=img.getAttribute("src")
    drawingWidth=width
    drawingHeight=width*img.height/img.width

    if(! drawingHeight*drawingWidth>0 && firstImage){
        setTimeout(canvasInitLoop,100,img,width)
        return false;
    }
    firstImage=false

    drawing=document.querySelector('.main-select-canvas')
    drawingBoard=document.querySelector('.mid-group')

    drawing.width=drawingWidth
    drawing.height=drawingHeight
    
    context=drawing.getContext("2d");
    loadToCanvas(img,drawingWidth,drawingHeight);
    drawingBoard.removeEventListener("mousemove", doMouseMove);
    drawingBoard.addEventListener("mousemove",doMouseMove,false);

    drawingBoard.removeEventListener("mousedown", mouseDownAction);
    drawingBoard.addEventListener("mousedown", mouseDownAction);

    drawingBoard.removeEventListener("mouseup",mouseUpAction)
    drawingBoard.addEventListener("mouseup", mouseUpAction);
    return true;
}

function mouseUpAction(event){
    if(event.button==0){
        save_mode=false;
        recordHistory()
    }
    if(event.button==2){
    }
    count += 1
    console.log(count)
}

function mouseDownAction(event){
    if(event.button==0){
        save_mode=true;
    }
    if(event.button==2){
        if(fixed==null)fixed=getMousePos(drawing,event);
        else fixed=null;
    }
    count += 1
    console.log(count)
}

function doMouseMove(event) {
    if(fixed!=null)
        return;
    loc=getMousePos(drawing,event);
    updateSelection(loc);
}


function updateCanvasResize(){
    prepare_canvas(null,centerImgWidth)
}