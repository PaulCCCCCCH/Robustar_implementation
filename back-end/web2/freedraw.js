(function() {
  var $ = function(id){return document.getElementById(id)};

  var canvas = this.__canvas = new fabric.Canvas('c', {
    isDrawingMode: true
  });


  fabric.Object.prototype.transparentCorners = false;

  var defaultColor = "#FFFFFFFF";

  var drawingColorEl = $('drawing-color'),
      drawingShadowColorEl = $('drawing-shadow-color'),
      drawingLineWidthEl = $('drawing-line-width'),
      deleteSelection = $('delete-selection'),
      pencilSelect = $('pencil_select');
      colorRegionSelect = $('color_region_select');
      brushSelect = $('brush_select');
      moveModeSelect = $('move_mode_select');
      drawModeSelect = $('draw_mode_select');
      changeEditMode = $('change_edit_mode_button');
      clearEl = $('clear-canvas');
      colorTollarance = $('color-tollarance');

  colorTollarance.onchange = function(){
    window.findColorTollarance=colorTollarance.value;
  }
  clearEl.onclick = function() { 
    while(canvas.getObjects().length > 1){
      canvas.remove(canvas.getObjects()[1]);
    }
    // canvas.clear(); 
  };

  pencilSelect.onclick = function() {
    window.findColorMode=undefined;
    canvas.freeDrawingBrush = new fabric['PencilBrush'](canvas);
    var brush = canvas.freeDrawingBrush;
    brush.width = 10;
    brush.color = "#FFFFFFFF";
  }
  colorRegionSelect.onclick = function() {
    window.findColorMode=1;
    window.findColorTollarance=colorTollarance.value;
  }
  brushSelect.onclick = function() {
    window.findColorMode=undefined;
    canvas.freeDrawingBrush = new fabric['SquareBrush'](canvas);
    var brush = canvas.freeDrawingBrush;
    brush.width = 10;
    brush.color = "#FFFFFFFF";
  }

  moveModeSelect.onclick = function(){
    window.findColorMode=undefined;
    canvas.isDrawingMode = false;
  }
  drawModeSelect.onclick = function(){
    window.findColorMode=undefined;
    canvas.isDrawingMode = true;
  }
  changeEditMode.onclick = function(){
    window.findColorMode=undefined;
    canvas.isDrawingMode = !canvas.isDrawingMode;

    if(canvas.isDrawingMode){
      deleteSelection.hidden=true;
    }else{
      deleteSelection.hidden=false;
    }

    changeEditMode.innerHTML = canvas.isDrawingMode? "Exit Edit" : "Enter Edit";
  }

  $('drawing-mode-selector').onchange = function() {
    //pencil circle spary pattern
      canvas.freeDrawingBrush = new fabric[this.value + 'Brush'](canvas);

    if (canvas.freeDrawingBrush) {
      var brush = canvas.freeDrawingBrush;
      brush.color = defaultColor;
      if (brush.getPatternSrc) {
        brush.source = brush.getPatternSrc.call(brush);
      }
      brush.width = parseInt(drawingLineWidthEl.value, 10) || 1;
      brush.shadow = new fabric.Shadow({
        offsetX: 0,
        offsetY: 0,
        affectStroke: true,
        color: drawingShadowColorEl.value,
      });
    }
  };

  function setBrushColor(color) {
    var brush = canvas.freeDrawingBrush;
    brush.color = color;
    if (brush.getPatternSrc) {
      brush.source = brush.getPatternSrc.call(brush);
    }
  };
  
  drawingLineWidthEl.onchange = function() {
    canvas.freeDrawingBrush.width = parseInt(this.value, 10) || 1;
    this.previousSibling.innerHTML = this.value;
  };

  if (canvas.freeDrawingBrush) {
    canvas.freeDrawingBrush.color = defaultColor;
    canvas.freeDrawingBrush.width = parseInt(drawingLineWidthEl.value, 10) || 1;
  }

  function addImage(url) {

    var redirectPage = decodeURIComponent(url);
    console.log("donlin test",redirectPage);

    fabric.Image.fromURL(url, function(image) {
      canvas.setWidth(image.width)
      canvas.setHeight(image.height)
      canvas.renderAll();

      image.set({
        left: 0,
        top: 0,
        angle: 0
      })
      .scale(1)
      .setCoords();

      canvas.add(image);
    });
  };

  deleteSelection.onclick=function(){
    canvas.remove(canvas.getActiveObject());
  }

  // addImage("a.jpg",1);

  window.mycanvas=canvas;
  window.addImage=addImage;
})();