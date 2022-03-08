/**
 * @author NHN. FE Development Team <dl_javascript@nhn.com>
 * @fileoverview ColorFilter extending fabric.Image.filters.BaseFilter
 */
import { fabric } from 'fabric';

/**
 * ColorFilter object
 * @class ColorFilter
 * @extends {fabric.Image.filters.BaseFilter}
 * @ignore
 */
const ColorFilter = fabric.util.createClass(
  fabric.Image.filters.BaseFilter,
  /** @lends BaseFilter.prototype */ {
    /**
     * Filter type
     * @param {String} type
     * @default
     */
    type: 'ColorFilter',

    /**
     * Constructor
     * @member fabric.Image.filters.ColorFilter.prototype
     * @param {Object} [options] Options object
     * @param {Number} [options.color='#FFFFFF'] Value of color (0...255)
     * @param {Number} [options.threshold=45] Value of threshold (0...255)
     * @override
     */
    initialize(options) {
      if (!options) {
        options = {};
      }
      this.color = options.color || '#FFFFFF';
      this.threshold = options.threshold || 45;
      this.x = Math.floor(options.x) || null;
      this.y = Math.floor(options.y) || null;
      this.appending = options.appending || false;
      this.filterId = options._filterId;
    },

    /**
     * Applies filter to canvas element
     * @param {Object} canvas Canvas object passed by fabric
     */
    // eslint-disable-next-line complexity
    applyTo(canvas) {
      const { imageData } = canvas;
      const { data } = imageData;
      const { threshold } = this;
      let i, len;
      const filterColor = this.color;

      for (i = 0, len = data.length; i < len; i += 4) {
        if (
          this._isOutsideThreshold(data[i], filterColor[0], threshold) ||
          this._isOutsideThreshold(data[i + 1], filterColor[1], threshold) ||
          this._isOutsideThreshold(data[i + 2], filterColor[2], threshold)
        ) {
          continue;
        }
        data[i] = data[i + 1] = data[i + 2] = data[i + 3] = 255;
      }
    },

    /**
     * Check color if it is within threshold
     * @param {Number} color1 source color
     * @param {Number} color2 filtering color
     * @param {Number} threshold threshold
     * @returns {boolean} true if within threshold or false
     */
    _isOutsideThreshold(color1, color2, threshold) {
      const diff = color1 - color2;

      return Math.abs(diff) > threshold;
    },
  }
);

export default ColorFilter;
