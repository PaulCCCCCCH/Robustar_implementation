# Image Editor Code Walk Through

## `src/`
- `src/index.js`: entry point. Exports the entire image editor so that others can import.
- `src/css/`: style definitions
- `src/svg/`: svgs
- `src/js/`: main code


## `src/js`
- `src/js/imageEditor.js`: 
  - Defines `ImageEditor` object, which is an aggregation of an `UI` instance (in `ui.js`), a `Graphics` instance (in `graphics.js`), and an `Invoker` instance (in `invoker.js`).
  - Defines a set of event handlers and attaches events to objects (with `ui.on`, `graphics.on`, etc.). Events are divided into three categories
    1. **Invoker events**. These are editor actions that we can redo/undo (e.g. draw a stroke, zoom in, etc.)
    2. **Graphics events**. These represnet UI changes (e.g. what happens when you click on color picker).
    3. **DOM events**. Monitor keyboard inputs. There is only a `keydown` event in this category.
  - Have `CustomEvents` (last 3 lines) mixed in and uses it's `fire` method to invoke events. See [here](https://github.com/nhn/tui.code-snippet/blob/master/customEvents/customEvents.js)

- `src/js/ui.js`:
  - Sets UI styles and add DOM elements dynamically. Controls transitions, etc.
  - Binds events to buttons (`activeMenuEvent()`). So if you want to add a button that does something, modify this file. Note that it only **binds** buttons to actions. It does not define actions. Actions are defined in `actions.js` (see below).
  - Defines sub menus (`_makeSubMenu()`), with the list of menus initialized in `_initializeOption()`.
  - Set the default image for `Canvas` object (`initCanvas()`).  
  
- `src/js/graphics.js`:
  - Manages drawings (i.e. things inside the canvas element) and style settings, keeps a reference to `Fabric.Canvas` object, delegate operations on `Canvas` using the library [Fabric.js](https://github.com/fabricjs/fabric.js).
  - Strokes drawn are managed as `objects`. Many functions are provided to manipulate them. Selected object will be `active`.
  - **Important**: Exports the image in the canvas through `toDataURL()`, load an image to canvas through `setCanvasImage()`
  - Initializes drawing modes

- `src/js/invoker.js`:
  - Maintains stacks of actions for redo/undo operations.
  - Provides an `execute` function that execute a command, pushes it to undo stack, and clears redo stack. Most canvas operations should be passed to it.

- `src/js/action.js`:
  - Defines UI-related actions (e.g. download, load image, switch to drawing mode, hide menu, etc.). The actions are bind to buttons in `ui.js`. 
  - Implement action logic in this file.

- `src/js/polyfill.js`: JS library for backward compatibility. Please ignore this.

- `src/js/consts.js`: defines constants.

- `src/js/utils.js`: utility functions.


## `src/js/component`
- Each file defines a drawing tool. This is the lowest level above `Fabric` layer, which provides an abstraction of a specific drawing operation. 
- You need to bind key events to `fabric` object with 
  `fabric.util.addListener(document, 'keydown', function)`, and remove it later with
  `fabric.util.removeListener(document, 'keydown', function)`.
- You need to bind mouse events to `canvas` object with 
  `canvas.on({ 'mouse:move': function, 'mouse:down': function})`, and remove it later with
  `canvas.off({ 'mouse:move': function, 'mouse:down': function})`
- The event that should be externally transmitted from the component is passed through the `Canvas`. The `Canvas` passes the event back if it is registered outside Canvas.


## `src/js/command`
- Independent unit of execution for performing specific functions
- Defines `execute` and `undo` functions. 
- Call `graphics.getComponent(...)` and call component methods here.
- Command instance is managed as a stack in the `Invoker`.
- Uses `Canvas` to manage various components.

## `src/js/factory`

- Command factory interface for command registration and creation

## `src/js/drawingMode`
- Triggers for corresponding component for each drawing mode. Defines `start` and `end` actions. To add new drawing mode, just follow the templates.
- **Important**: only one drawing mode should be activated at a time, which means drawing modes are mutually exclusive.

## `src/js/ui`

- Traditional event-driven implementation of interfaces of different tools

## `src/js/extension`

- Extends functionalities of Fabric image filters.

## `src/js/helper`

- Helper functions for some components

# Implementation of Drawing Lines

## Binding Drawing Event
Drawing mode selection:
- In `action.js`, `_drawAction()` returns actions for three different modes.
- `_addSubMenuEvent()` in `ui.js` calls `addEvent()` of `ui/draw.js`, passing in an `drawAction` object.
- `addEvent()` in `ui/draw.js` binds `_changeDrawType()` to mode selection icons.
- `_changeDrawType()` calls `setDrawMode()` (defined in `action.js`)

Drawing:
- TODO

## Triggering Event
TODO

# Implementation of Applying Filters

## Binding Event

- In `action.js`, `_filterAction()` returns `applyFilter(applying, type, options, isSilent)` function.
- `_addSubMenuEvent()` in `ui.js` calls `addEvent()` of `ui/filter.js`, passing in an `applyFilter()` function.
- `addEvent()` in `ui/filter.js` binds `changeFilterState()` to checkboxes and `changeFilterStateForRange` to range bars.

## Triggering Event
- User click on checkbox.
- `_changeFilterState` in `ui/filter.js` is called.
- `applyFilter()` (binded by `addEvent` previously) was called.
- `applyFilter()` in `imageEditor.js` is called.
- `execute()` or `executeSilent()` in `invoker.js` is called.


# Mixin Relations
- `ImageEditor` has `actions` mixed in.
- `actions` has `ImageEditor` mixed in.
- Many components `CustomEvents` mixed in.

---

# Reference

Official introduction of project structure: [tui.image-editor/Structure.md at master · nhn/tui.image-editor (github.com)](https://github.com/nhn/tui.image-editor/blob/master/docs/Structure.md)

