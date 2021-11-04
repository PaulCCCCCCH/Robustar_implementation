
    var firstShowMenu=false

	//显示菜单
    function showMenu(leftPosition,buttonNames,clickEvents){
        menu.style.setProperty("left",leftPosition)
        
        menu.innerHTML=''//清除原本菜单中的内容
        for(var i=0;i<buttonNames.length;i++){
            button=document.createElement("button")
            button.textContent=buttonNames[i]

            if(clickEvents!=undefined)
                button.setAttribute("onclick",clickEvents[i])

            br=document.createElement("br")
            menu.appendChild(button)
            menu.appendChild(br)
        }
        menu.classList.remove("hide")
        menu.removeAttribute("hidden")

        firstShowMenu=true
        document.addEventListener('click',pageClickListener)
    }
	//如果点击了页面的其他地方，就收起菜单
    function pageClickListener(e){
        if(firstShowMenu){
            firstShowMenu=false
            return
        }
        if(!menu.contains(e.target)){
            hideMenu()
        document.removeEventListener('click',pageClickListener)
        }
    }
	//重置所有窗口的状态
    function resetWindow(){
        if(leftGroup.getAttribute("hidden")=="hidden")
            showHideLeft();
        if(foot.getAttribute("hidden")=="hidden")
            showHideFoot();
        if(rightGroup.getAttribute("hidden")=="hidden")
            showHideRight();
    }
	//点击了hide按钮
    function hideMenu(){
        menu.classList.add("hide")
        setTimeout(function(){menu.setAttribute("hidden","hidden")},300)
    }
	//点击了file按钮
    function fileClick(fileButton){
        buttonNames=["chart type"]
        buttonClicks=["barChartType=1-barChartType;drawBarChart();"]
        showMenu(getLeft(fileButton)+"px",buttonNames,buttonClicks)
    }
	//点击了edit按钮
    function editClick(editButton){
        buttonNames=["record","clear","send","load"]
        buttonClicks=["recordHistory()","clearHistory()","sendCanvas()","getCanvas()"]
        showMenu(getLeft(editButton)+"px",buttonNames,buttonClicks)
    }
	//点击了window按钮
    function windowClick(windowButton){
        buttonNames=["left","right","bottom","reset","fullscreen"]
        buttonClicks=["showHideLeft()","showHideRight()","showHideFoot()","resetWindow()","document.documentElement.requestFullscreen()"]
        showMenu(getLeft(windowButton)+"px",buttonNames,buttonClicks)
    }
	//点击了data按钮
    function dataClick(dataButton){
        buttonNames=["train set","test set","error classification","correct classification","goto"]
        buttonClicks=["trainSetClick()","testSetClick()","mistakeSetClick()","correctSetClick()","prompt('please input')"]
        showMenu(getLeft(dataButton)+"px",buttonNames,buttonClicks)
    }