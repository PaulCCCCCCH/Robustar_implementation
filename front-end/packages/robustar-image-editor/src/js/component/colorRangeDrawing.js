/**
 * @author Chonghan Chen <chonghac@andrew.cmu.edu>
 * @fileoverview Color range drawing module.
 * @reference Color picker example
 *            https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Pixel_manipulation_with_canvas#a_color_picker
 */

/* eslint-disable*/
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
    this._threshold = 0;

    /**
     * Current color
     * @type {String}
     * @private
     */
    this._color = 0;

    /**
     * Initial threshold (threshold will be reset to this number on mouse down)
     * @type {number}
     * @private
     */
    this._initThreshold = 0;

    /**
     * Filter Id. Uniquely identifies a color filter drawing.
     * @type {number}
     * @private
     */
    this._filterId = 0;

    /**
     * Maximum _filterId value.
     * @type {number}
     * @private
     */
    this._maxFilterId = Number.MAX_SAFE_INTEGER;

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
    const { x, y } = canvas.getPointer(fEvent.e);
    this._color = this._getPointerColor(canvas, x, y);

    // Record starting points
    this._mouseDownX = x;
    this._mouseDownY = y;
    this._threshold = this._initThreshold;
    this._filterId = (this._filterId + 1) % this._maxFilterId;

    // this._applyFilter(false);

    canvas.on({
      'mouse:move': this._listeners.mousemove,
      'mouse:up': this._listeners.mouseup,
    });
  }

  /**
   * Mousemove event handler in fabric canvas
   * @param {{target: fabric.Object, e: MouseEvent}} fEvent - Fabric event object
   * @private
   */
  _onFabricMouseMove(fEvent) {
    const canvas = this.getCanvas();

    const { x, y } = canvas.getPointer(fEvent.e);
    this._threshold = this._distanceToRange(this._mouseDownX, this._mouseDownY, x, y);
    this._applyFilter(false);

    // canvas.renderAll();
  }

  /**
   * Mouseup event handler in fabric canvas
   * @private
   */
  _onFabricMouseUp() {
    const canvas = this.getCanvas();
    this._applyFilter(true);

    canvas.off({
      'mouse:move': this._listeners.mousemove,
      'mouse:up': this._listeners.mouseup,
    });
  }

  /**
   * Convert the distance of mouse move into color range
   */
  _distanceToRange(mouseDownX, mouseDownY, x, y) {
    // return Math.sqrt((mouseDownX - x) ** 2 + (mouseDownY - y) ** 2) / 10;
    return Math.sqrt((mouseDownX - x) ** 2 + (mouseDownY - y) ** 2) / 1000;
  }

  // _getPointerColor(canvas, x, y) {
  //   const context = canvas.getContext('2d');
  //   const { width, height } = canvas;
  //   const data = context.getImageData(0, 0, width, height).data;
  //   const bytes = 4;
  //   const color = [0, 0, 0, 0];

  //   const position = (width * Math.floor(y) + Math.floor(x)) * bytes;
  //   color[0] = data[position];
  //   color[1] = data[position + 1];
  //   color[2] = data[position + 2];
  //   color[3] = data[position + 3];

  //   return color;
  // }

  _getPointerColor(canvas, x, y) {
    const context = canvas.getContext('2d');
    const { width, height } = canvas;
    const data = context.getImageData(0, 0, width, height).data;
    const bytes = 4;

    const position = (width * Math.floor(y) + Math.floor(x)) * bytes;

    return 'rgb(' + [data[position], data[position + 1], data[position + 2]].join(', ') + ')';
  }

  _applyFilter(isLast) {
    const editor = this.getEditor();
    const filterAction = editor.getActions().filter;

    // filterAction.applyFilter(
    //   true,
    //   'colorFilter',
    //   {
    //     filterId: this._filterId,
    //     threshold: this._threshold,
    //     x: this._mouseDownX,
    //     y: this._mouseDownY,
    //     appending: isLast,
    //     color: this._color,
    //   },
    //   !isLast
    // );
    filterAction.applyFilter(
      true,
      'removeColor',
      {
        filterId: this._filterId,
        distance: this._threshold,
        color: this._color,
        appending: isLast,
      },
      !isLast
    );
  }
}

export default ColorRangeDrawing;
