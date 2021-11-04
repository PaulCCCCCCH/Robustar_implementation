//存储html中的几个关键部分
var menu=document.querySelector(".menu")
var leftGroup=document.querySelector(".left-group")
var rightGroup=document.querySelector(".right-group")
var foot=document.querySelector(".foot")
var container=document.querySelector(".container")
//获得元素的x坐标
function getLeft(e){
    var offset=e.offsetLeft;
    if(e.offsetParent!=null) offset+=getLeft(e.offsetParent);
    return offset;
}

function getLeftHide(){
    return leftGroup.getAttribute("hidden")=="hidden"
}

//展示与隐藏左边
function showHideLeft(){
    if(leftGroup.getAttribute("hidden")!="hidden"){
        leftGroup.classList.add("hide")
        setTimeout(function(){leftGroup.setAttribute("hidden","hidden")},1000)
    }else{
        leftGroup.classList.remove("hide")
        leftGroup.removeAttribute("hidden")
    }
}
//展示与隐藏右边
function showHideRight(){
    if(rightGroup.getAttribute("hidden")!="hidden"){
        rightGroup.classList.add("hide")
        setTimeout(function(){rightGroup.setAttribute("hidden","hidden")},1000)
    }else{
        rightGroup.classList.remove("hide")
        rightGroup.removeAttribute("hidden")
    }
}
//展示与隐藏底部
function showHideFoot(){
    if(foot.getAttribute("hidden")!="hidden"){
        foot.classList.add("hide")
        setTimeout(function(){foot.setAttribute("hidden","hidden")
        container.style.setProperty("bottom","0px")},1000)
    }else{
        foot.classList.remove("hide")
        foot.removeAttribute("hidden")
        container.style.setProperty("bottom","100px")
    }
}