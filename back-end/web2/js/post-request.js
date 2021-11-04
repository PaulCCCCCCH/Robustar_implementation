function postCanvas() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/edit');

    // set headers
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.send("src=" + imgURL + "&content=" + window.mycanvas.getContext().getImageData(0, 0, 224, 224).data);

    // listen for `load` even
    xhr.onload = () => {
        console.log(xhr.responseText);
    }
    console.log(window.mycanvas.getContext().getImageData(0, 0, 224, 224).data)
}


function getCanvas() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/get-edit');

    // set headers
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    xhr.send("src=" + imgURL);

    // listen for `load` even
    xhr.onload = () => {
        newData = xhr.responseText.split(",")
        centerImgWidth = (newData.length / 4) ** 0.5;
        updateCanvasResize();
        for (var i = 0; i < imageData.data.length; i++) {
            imageData.data[i] = parseInt(newData[i])
        }
        context.putImageData(imageData, 0, 0)
        backup_data()
            //console.log(xhr.responseText);
    }

}