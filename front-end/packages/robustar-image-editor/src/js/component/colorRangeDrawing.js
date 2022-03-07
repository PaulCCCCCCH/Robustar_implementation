/**
 * @author Chonghan Chen <chonghac@andrew.cmu.edu>
 * @fileoverview Color range drawing module.
 * @reference Color picker example
 *            https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas#a_color_picker
 */
import Component from '@/interface/component';
import { componentNames } from '@/consts';
// import { imageDataToColorString } from '@/util';

/**
 * Line
 * @class Line
 * @param {Graphics} graphics - Graphics instance
 * @extends {Component}
 * @ignore
 */
class ColorRangeDrawing extends Component {
  constructor(graphics) {
    super(componentNames.COLOR_RANGE_DRAWING, graphics);

    /**
     * The range of color to be edited together
     * @type {number}
     * @private
     */
    this._threshold = 10;

    /**
     * The positions where mouse-down event happens
     * @type {number}
     */
    this._mouseDownX = 0;
    this._mouseDownY = 0;

    /**
     * Listeners
     * @type {object.<string, function>}
     * @private
     */
    this._listeners = {
      mousedown: this._onFabricMouseDown.bind(this),
      mousemove: this._onFabricMouseMove.bind(this),
      mouseup: this._onFabricMouseUp.bind(this),
    };
  }

  /**
   * Start drawing line mode
   * @param {{width: ?number, color: ?string}} [setting] - Brush width & color
   */
  start() {
    const canvas = this.getCanvas();
    canvas.defaultCursor = 'crosshair';
    canvas.selection = false;

    // this.setHeadOption(setting);

    canvas.forEachObject((obj) => {
      obj.set({
        evented: false,
      });
    });

    canvas.on({
      'mouse:down': this._listeners.mousedown,
    });
  }

  /**
   * End drawing line mode
   */
  end() {
    const canvas = this.getCanvas();

    canvas.defaultCursor = 'default';
    canvas.selection = true;

    canvas.forEachObject((obj) => {
      obj.set({
        evented: true,
      });
    });

    canvas.off('mouse:down', this._listeners.mousedown);
  }

  /**
   * Mousedown event handler in fabric canvas
   * @param {{target: fabric.Object, e: MouseEvent}} fEvent - Fabric event object
   * @private
   */
  _onFabricMouseDown(fEvent) {
    const canvas = this.getCanvas();
    const editor = this.getEditor();
    const filterAction = editor.getActions().filter;
    const { x, y } = canvas.getPointer(fEvent.e);
    // this._filter = new ColorFilter({
    //   threshold: this._threshold,
    //   x,
    //   y,
    // });
    // this._filter.add();
    // canvas.add(this._filter);
    // const filter = this.graphics.getComponent(componentNames.FILTER);
    // filter.add('colorFilter', {
    //   threshold: this._threshold,
    //   x,
    //   y,
    // });
    // this.applyFilter('colorFilter', { threshold: this._threshold, x, y }, true);
    // alert(this.getEditor()._actions);
    // filterAction.applyFilter(
    //   true,
    //   'colorFilter',
    //   { threshold: this._threshold, x: 10, y: 10 },
    //   false
    // );
    // filterAction.applyFilter(true, 'colorFilter', { threshold: this._threshold, x, y }, false);
    // filterAction(true, 'colorFilter', { threshold: this._threshold, x, y }, false);
    // editor.fire(eventNames.INPUT_BOX_EDITING_STARTED);
    // const canvasEl = this.getCanvasElement();
    // const context = canvasEl.getContext('2d');
    // const imageDataArray = context.getImageData(x, y, 1, 1).data;
    // const colorString = imageDataToColorString(imageDataArray);
    // filterAction.applyFilter(true, 'removeColor', { color: colorString, distance: 0.2 }, false);
    // filterAction.applyFilter(true, 'colorFilter', { color: colorString, distance: 0.2 }, false);
    filterAction.applyFilter(
      true,
      'colorFilter',
      {
        threshold: this._threshold,
        x,
        y,
      },
      false
    );

    // Record starting points
    this._mouseDownX = x;
    this._mouseDownY = y;

    canvas.on({
      'mouse:move': this._listeners.mousemove,
      'mouse:up': this._listeners.mouseup,
    });

    // this.fire(eventNames.ADD_OBJECT, this._createLineEventObjectProperties());
  }

  /**
   * Mousemove event handler in fabric canvas
   * @param {{target: fabric.Object, e: MouseEvent}} fEvent - Fabric event object
   * @private
   */
  _onFabricMouseMove(fEvent) {
    const canvas = this.getCanvas();

    const { x, y } = canvas.getPointer(fEvent.e);
    this._threshold = this._distanceToRange(this.mouseDownX, this.mouseDownY, x, y);

    canvas.renderAll();
  }

  /**
   * Mouseup event handler in fabric canvas
   * @private
   */
  _onFabricMouseUp() {
    const canvas = this.getCanvas();

    // this.fire(eventNames.OBJECT_ADDED, this._createLineEventObjectProperties());

    canvas.off({
      'mouse:move': this._listeners.mousemove,
      'mouse:up': this._listeners.mouseup,
    });
  }

  /**
   * Convert the distance of mouse move into color range
   */
  _distanceToRange(mouseDownX, mouseDownY, x, y) {
    return (mouseDownX - x) ** 2 + (mouseDownY - y) ** 2;
  }
}

export default ColorRangeDrawing;
