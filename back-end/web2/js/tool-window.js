function squareToolClick(){
    setCursor('\uf096');
    setMode(3)
    showAdjustBar();
}

function circleToolClick(){
    setCursor('\uf10c');
    setMode(4)
    showAdjustBar();
}

function adjacentToolClick(){
    setCursor('\uf067');
    setMode(0)
    showAdjustBar();
}

function nearToolClick(){
    setCursor('\uf013');
    setMode(1)
    showAdjustBar();
}

function allToolClick(){
    setCursor('\uf03e');
    setMode(2)
    showAdjustBar();
}

function resetToolClick(){
    resetCursor();
    setMode(-1)
    hideAdjustBar();
}

function showAdjustBar(){
    document.querySelector(".adjust-bar").removeAttribute("hidden")
}

function hideAdjustBar(){
    document.querySelector(".adjust-bar").setAttribute("hidden","hidden")
}