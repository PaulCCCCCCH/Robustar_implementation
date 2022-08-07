<template>
  <div
    class="tui-image-editor d-flex justify-center align-center"
    :style="{ width: width + 'px', height: height + 'px' }"
  ></div>
</template>

<script>
import ImageEditor from '@robustar/image-editor';
import '@robustar/image-editor/dist/tui-image-editor.css';
import { configs } from '@/configs.js';
import whiteTheme from './white-theme.js';

const getImage = () => ({
  path: `${configs.imagePathServerUrl}/${sessionStorage.getItem('image_url')}`,
  name: sessionStorage.getItem('image_url'),
});

const includeUIOptions = {
  includeUI: {
    initMenu: 'draw',
    theme: whiteTheme,
  },
};

const editorDefaultOptions = {
  cssMaxWidth: 1000,
  cssMaxHeight: 1000,
};

export default {
  name: 'ImageEditor',
  props: {
    includeUi: {
      type: Boolean,
      default: true,
    },
    options: {
      type: Object,
      default() {
        return editorDefaultOptions;
      },
    },
    cursor: {
      type: String,
      default: 'default',
    },
  },
  data() {
    return {
      editorInstance: null,
      width: 300,
      height: 300,
    };
  },
  watch: {
    cursor: function () {
      if (this.editorInstance) {
        this.editorInstance.changeCursor(this.cursor);
      }
    },
  },
  mounted() {
    this.initInstance();
  },
  destroyed() {
    this._clearAll();
  },
  methods: {
    reset() {
      this._clearAll();
      this.initInstance();
    },
    resize({ width, height }) {
      this.width = width;
      this.height = height;
      this.invoke('resize', { width, height });
    },
    toggleMove() {
      this.editorInstance.getActions().main.hand();
    },
    initInstance() {
      let options = editorDefaultOptions;
      if (this.includeUi) {
        options = Object.assign(includeUIOptions, this.options);
        options.includeUI.loadImage = getImage();
      }
      this.editorInstance = new ImageEditor('.tui-image-editor', options);
      if (!this.includeUi) {
        const { path, name } = getImage();
        this.editorInstance.loadImageFromURL(path, name).then(() => {
          this.editorInstance.clearUndoStack();
        });
      }
      this._addEventListener();
    },
    getRootElement() {
      return this.$refs.tuiImageEditor;
    },
    invoke(methodName, ...args) {
      let result = null;
      if (this.editorInstance[methodName]) {
        result = this.editorInstance[methodName](...args);
      } else if (methodName.indexOf('.') > -1) {
        const func = this._getMethod(this.editorInstance, methodName);

        if (typeof func === 'function') {
          result = func(...args);
        }
      }

      return result;
    },
    _clearAll() {
      Object.keys(this.$listeners).forEach((eventName) => {
        this.editorInstance.off(eventName);
      });
      this.editorInstance.destroy();
      this.editorInstance = null;
    },
    _addEventListener() {
      Object.keys(this.$listeners).forEach((eventName) => {
        this.editorInstance.on(eventName, (...args) => this.$emit(eventName, ...args));
      });
    },
    _getMethod(instance, methodName) {
      const { first, rest } = this._parseDotMethodName(methodName);
      const isInstance = instance.constructor.name !== 'Object';
      const type = typeof instance[first];
      let obj;

      if (isInstance && type === 'function') {
        obj = instance[first].bind(instance);
      } else {
        obj = instance[first];
      }

      if (rest.length > 0) {
        return this._getMethod(obj, rest);
      }

      return obj;
    },
    _parseDotMethodName(methodName) {
      const firstDotIdx = methodName.indexOf('.');
      let firstMethodName = methodName;
      let restMethodName = '';

      if (firstDotIdx > -1) {
        firstMethodName = methodName.substring(0, firstDotIdx);
        restMethodName = methodName.substring(firstDotIdx + 1, methodName.length);
      }

      return {
        first: firstMethodName,
        rest: restMethodName,
      };
    },
  },
};
</script>

<style scoped>
.tui-image-editor-range-wrap .range {
  color: black !important;
}

.tui-image-editor-range-wrap label {
  color: black !important;
}
</style>
