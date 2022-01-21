import Component from '@/interface/component';
import { componentNames } from '@/consts';

/**
 * Resize components
 * @param {Graphics} graphics - Graphics instance
 * @extends {Component}
 * @class Resize
 * @ignore
 */
class Resize extends Component {
  constructor(graphics) {
    super(componentNames.RESIZE, graphics);

    /**
     * Current dimensions
     * @type {Object}
     * @private
     */
    this._dimensions = null;

    /**
     * Original dimensions
     * @type {Object}
     * @private
     */
    this._originalDimensions = null;
  }

  /**
   * Get current dimensions
   * @returns {object}
   */
  getCurrentDimensions() {
    const canvasImage = this.getCanvasImage();
    if (!this._dimensions && canvasImage) {
      const { width, height } = canvasImage;
      this._dimensions = {
        width,
        height,
      };
    }

    return this._dimensions;
  }

  /**
   * Get original dimensions
   * @returns {object}
   */
  getOriginalDimensions() {
    return this._originalDimensions;
  }

  /**
   * Set original dimensions
   * @param {object} dimensions - Dimensions
   */
  setOriginalDimensions(dimensions) {
    this._originalDimensions = dimensions;
  }

  /**
   * Resize Image
   * @param {Object} dimensions - Resize dimensions
   * @returns {Promise}
   */
  resize(dimensions) {
    const canvasImage = this.getCanvasImage();
    const { width, height, scaleX, scaleY } = canvasImage;
    const { width: dimensionsWidth, height: dimensionsHeight } = dimensions;

    const scaleValues = {
      scaleX: dimensionsWidth ? dimensionsWidth / width : scaleX,
      scaleY: dimensionsHeight ? dimensionsHeight / height : scaleY,
    };

    if (scaleX !== scaleValues.scaleX || scaleY !== scaleValues.scaleY) {
      canvasImage.set(scaleValues).setCoords();

      this._dimensions = {
        width: canvasImage.width * canvasImage.scaleX,
        height: canvasImage.height * canvasImage.scaleY,
      };

      const objects = this.getCanvas().getObjects();
      // eslint-disable-next-line no-console
      console.log(objects);
      // eslint-disable-next-line guard-for-in
      // for (const i in objects) {
      //   objects[i].scaleX = scaleValues.scaleX;
      //   objects[i].scaleY = scaleValues.scaleY;
      //   objects[i].left = objects[i].left * scaleValues.scaleX;
      //   objects[i].top = objects[i].top * scaleValues.scaleY;
      //   objects[i].setCoords();
      // }
    }

    this.adjustCanvasDimensionBase();

    return Promise.resolve();
  }

  /**
   * Start resizing
   */
  start() {
    const dimensions = this.getCurrentDimensions();
    this.setOriginalDimensions(dimensions);
  }

  /**
   * End resizing
   */
  end() {}
}

export default Resize;
