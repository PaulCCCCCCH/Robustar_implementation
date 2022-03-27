/**
 * @author NHN. FE Development Team <dl_javascript@nhn.com>
 * @fileoverview FreeDrawingMode class
 */
import DrawingMode from '@/interface/drawingMode';
import { drawingModes, componentNames as components } from '@/consts';

/**
 * FreeDrawingMode class
 * @class
 * @ignore
 */
class ColorRangeDrawingMode extends DrawingMode {
  constructor() {
    super(drawingModes.COLOR_RANGE_DRAWING);
  }

  /**
   * start this drawing mode
   * @param {Graphics} graphics - Graphics instance
   * @param {{width: ?number, color: ?string}} [options] - Brush width & color
   * @override
   */
  start(graphics, options) {
    const colorRangeDrawing = graphics.getComponent(components.COLOR_RANGE_DRAWING);
    colorRangeDrawing.start(options);
  }

  /**
   * stop this drawing mode
   * @param {Graphics} graphics - Graphics instance
   * @override
   */
  end(graphics) {
    const colorRangeDrawing = graphics.getComponent(components.COLOR_RANGE_DRAWING);
    colorRangeDrawing.end();
  }
}

export default ColorRangeDrawingMode;
