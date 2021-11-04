var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }
 
        anHttpRequest.open( "GET", aUrl, true );    
        anHttpRequest.send( null );
    }
}

var imageFileNameHistory=[]

function notifyUpdateImage(){
    imgs=foot.querySelectorAll("img")
    for(var i=0;i<viewImageCount;i++){
        currentId=currentImgId-Math.floor(viewImageCount/2)+i
        requestURL="/dataset-info/"+trainTestType+"/"+currentId
        if(typeof(imageFileNameHistory[requestURL])=="string")
            imgs[i].setAttribute("src","/dataset/"+trainTestType+"/"+imageFileNameHistory[requestURL])

    }
    //test data
    allimg=document.querySelectorAll(".influence img");
    for(var i=0;i<3;i++){
        //allimg[i].setAttribute("src",imgs[i].getAttribute("src"))
        allimg[i].setAttribute("src",'/influence-img/'+Math.random())
    }
    //end test
    prepare_canvas(imgs[Math.floor(viewImageCount/2)],centerImgWidth)
    refershChartData(imgs[Math.floor(viewImageCount/2)].src)
    rightGroup.querySelector(".title-info").textContent=trainTestType+"-"+currentImgId
    drawBarChart()
}

function loadImageEnqueue(id){
    var requestURL="/dataset-info/"+trainTestType+"/"+id
    if(imageFileNameHistory[requestURL]!=undefined)
        return;
    imageFileNameHistory[requestURL]=true
    var client = new HttpClient();
    client.get(requestURL, function(path) {
        imageFileNameHistory[requestURL]=path
        notifyUpdateImage()
    });        
}