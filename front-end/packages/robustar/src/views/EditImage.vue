<template>
  <div class="d-flex justify-space-between" style="width: 100%; height: 100%">
    <div
      class="d-flex flex-column justify-space-between align-center pt-12"
      style="width: 100%; height: 100%"
    >
      <div>
        <div class="d-flex justify-center mb-8">
          <v-btn
            depressed
            color="warning"
            class="mr-4"
            @click="sendEdit"
            data-test="tui-image-editor-send-edit-btn"
            >Send Edit</v-btn
          >
          <v-btn depressed class="mr-4" @click="adjustImageSize">Adjust Size</v-btn>
          <v-btn depressed class="mr-4" @click="loadEdit">Load Edit</v-btn>
          <v-btn depressed @click="autoEdit">Auto Edit</v-btn>
        </div>
        <div class="d-flex">
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                :color="mode === 'zoomIn' ? 'primary' : ''"
                icon
                large
                @click="mode = mode === 'zoomIn' ? '' : 'zoomIn'"
                v-bind="attrs"
                v-on="on"
                ><v-icon>mdi-magnify-plus-outline</v-icon></v-btn
              >
            </template>
            <span>zoom in</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                :color="mode === 'zoomOut' ? 'primary' : ''"
                icon
                large
                class="mx-4"
                @click="mode = mode === 'zoomOut' ? '' : 'zoomOut'"
                v-bind="attrs"
                v-on="on"
                ><v-icon>mdi-magnify-minus-outline</v-icon></v-btn
              >
            </template>
            <span>zoom out</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                :color="mode === 'move' ? 'primary' : ''"
                icon
                large
                @click="
                  mode = mode === 'move' ? '' : 'move';
                  $refs['editor'].toggleMove();
                "
                v-bind="attrs"
                v-on="on"
                ><v-icon>mdi-drag-variant</v-icon></v-btn
              >
            </template>
            <span>move</span>
          </v-tooltip>
          <v-divider vertical inset class="mx-8"></v-divider>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon large class="mr-4" v-bind="attrs" v-on="on"
                ><v-icon>mdi-history</v-icon></v-btn
              >
            </template>
            <span>history</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                large
                class="mr-4"
                v-bind="attrs"
                v-on="on"
                @click="$refs['editor'].invoke('undo')"
                ><v-icon>mdi-arrow-u-left-top</v-icon></v-btn
              >
            </template>
            <span>undo</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                large
                class="mr-4"
                v-bind="attrs"
                v-on="on"
                @click="$refs['editor'].invoke('redo')"
                ><v-icon>mdi-arrow-u-right-top</v-icon></v-btn
              >
            </template>
            <span>redo</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn icon large v-bind="attrs" v-on="on" @click="$refs['editor'].reset()"
                ><v-icon>mdi-cached</v-icon></v-btn
              >
            </template>
            <span>reset</span>
          </v-tooltip>
          <v-divider vertical inset class="mx-8"></v-divider>
          <v-tooltip bottom>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                large
                v-bind="attrs"
                v-on="on"
                @click="
                  $refs['editor'].invoke('removeActiveObject');
                  $refs['editor'].invoke('clearObjects');
                "
                ><v-icon>mdi-trash-can-outline</v-icon></v-btn
              >
            </template>
            <span>delete</span>
          </v-tooltip>
        </div>
      </div>
      <!-- <v-btn color="success" @click="$refs['editor'].invoke('startDrawingMode', 'ZOOM')"
        >text</v-btn
      > -->
      <ImageEditor
        ref="editor"
        :include-ui="useDefaultUI"
        :options="options"
        :cursor="cursorIcon"
        @mousedown="mousedown"
      ></ImageEditor>
      <div class="d-flex flex-column align-center" style="width: 100%">
        <div v-if="mode === 'resize'" style="width: 500px" class="d-flex flex-column align-center">
          <div class="d-flex align-center mb-2" style="width: 100%">
            <span class="mr-4 font-weight-medium" style="width: 45px">Width</span>
            <v-slider v-model="tempWidth" class="align-center" max="1000" min="30" hide-details>
              <template v-slot:append>
                <div class="d-flex align-center">
                  <v-text-field
                    v-model="tempWidth"
                    class="mt-0 pt-0 mx-2"
                    hide-details
                    single-line
                    outlined
                    dense
                    type="number"
                    style="width: 80px"
                  ></v-text-field>
                  <span>px</span>
                </div>
              </template>
            </v-slider>
          </div>
          <div class="d-flex align-center" style="width: 100%">
            <span class="mr-4 font-weight-medium" style="width: 45px">Height</span>
            <v-slider v-model="tempHeight" class="align-center" max="1000" min="30" hide-details>
              <template v-slot:append>
                <div class="d-flex align-center">
                  <v-text-field
                    v-model="tempHeight"
                    class="mt-0 pt-0 mx-2"
                    hide-details
                    single-line
                    outlined
                    dense
                    type="number"
                    style="width: 80px"
                  ></v-text-field>
                  <span>px</span>
                </div>
              </template>
            </v-slider>
          </div>
          <v-checkbox v-model="lockAspectRatio" label="Lock Aspect Ratio" hide-details></v-checkbox>
          <div class="mt-6 mb-8">
            <v-btn
              text
              @click="
                imageWidth = tempWidth;
                imageHeight = tempHeight;
                mode = '';
              "
            >
              <v-icon class="mr-2">mdi-check</v-icon>Apply
            </v-btn>
            <v-btn
              text
              color="grey"
              @click="
                $refs.editor.resize({ width: imageWidth, height: imageHeight });
                mode = '';
              "
            >
              <v-icon class="mr-2">mdi-close</v-icon>Cancel
            </v-btn>
          </div>
        </div>
        <div v-if="mode === 'draw'" class="d-flex align-center mb-8" style="width: 500px">
          <span class="mr-4 font-weight-medium" style="width: 100px">Brush Width</span>
          <v-slider
            v-model="brushWidth"
            class="align-center"
            max="100"
            min="1"
            hide-details
            @change="
              (width) =>
                $refs['editor'].invoke('setBrush', {
                  width,
                  color: 'FFFFFF',
                })
            "
          >
            <template v-slot:append>
              <v-text-field
                v-model="brushWidth"
                class="mt-0 pt-0 mx-2"
                hide-details
                single-line
                outlined
                dense
                type="number"
                style="width: 80px"
                @change="
                  (width) =>
                    $refs['editor'].invoke('setBrush', {
                      width,
                      color: 'FFFFFF',
                    })
                "
              ></v-text-field>
            </template>
          </v-slider>
        </div>
        <v-sheet
          class="d-flex justify-center align-center"
          color="primary"
          width="100%"
          height="70"
        >
          <v-btn color="white" :text="mode !== 'resize'" large depressed @click="toggleResize"
            ><v-icon class="mr-2">mdi-resize</v-icon>Resize</v-btn
          >
          <v-btn
            class="mx-8"
            color="white"
            :text="mode !== 'draw'"
            large
            @click="toggleDraw"
            depressed
            ><v-icon class="mr-2">mdi-draw</v-icon>Draw</v-btn
          >
          <v-btn
            color="white"
            :text="mode !== 'colorRange'"
            large
            depressed
            @click="toggleColorRange"
            ><v-icon class="mr-2">mdi-image-filter-center-focus-strong-outline</v-icon>Color
            Range</v-btn
          >
        </v-sheet>
      </div>
    </div>
    <Visualizer
      :is-active="image_url !== ''"
      :image_url="image_url"
      :split="split"
      @open="loadImageInfo"
      @close="image_url = ''"
    />
  </div>
</template>
<script>
import ImageEditor from '@/components/image-editor/ImageEditor';
import { APISendEdit, APIGetProposedEdit } from '@/services/edit';
import { APIGetAnnotated, APIGetNextImage } from '@/services/images';
import Visualizer from '@/components/prediction-viewer/Visualizer';

/**
 * The implementation for this component is tricky, because after a `loadEdit` or `autoEdit` call
 * (and session storage is set to point to an annoated image), when you try to get next image, you should be able
 * to fetch the next **train** image instead of **annotated** image.
 *
 * This is achieved by always using this.split and this.image_url when getting next image, and using
 * session storage only for loading image. Sync the two when an image is just loaded, but don't sync them
 * when loading an image after `loadEdit` or `autoEdit` call
 *
 */
export default {
  components: {
    ImageEditor,
    Visualizer,
  },
  data() {
    return {
      useDefaultUI: false,
      options: {
        // for tui-image-editor component's "options" prop
        cssMaxWidth: 700,
        cssMaxHeight: 1000,
      },
      image_url: '',
      split: '',
      mode: '',
      zoomLevel: 1,
      brushWidth: 10,
      imageWidth: 224,
      tempWidth: 224,
      imageHeight: 224,
      tempHeight: 224,
      lockAspectRatio: false,
    };
  },
  computed: {
    cursorIcon() {
      switch (this.mode) {
        case 'zoomIn':
          return 'zoom-in';
        case 'zoomOut':
          return 'zoom-out';
        case 'move':
          return 'move';
        case 'colorRange':
          return 'crosshair';
        default:
          return 'default';
      }
    },
  },
  watch: {
    tempWidth() {
      if (this.mode === 'resize') {
        if (this.lockAspectRatio) {
          this.tempHeight = this.tempWidth;
        }
        setTimeout(() => {
          this.$refs.editor.resize({ width: this.tempWidth, height: this.tempHeight });
        }, 0);
      }
    },
    tempHeight() {
      if (this.mode === 'resize') {
        if (this.lockAspectRatio) {
          this.tempWidth = this.tempHeight;
        }
        setTimeout(() => {
          this.$refs.editor.resize({ width: this.tempWidth, height: this.tempHeight });
        }, 0);
      }
    },
    mode(newValue, oldValue) {
      if (
        (oldValue === 'draw' || oldValue === 'colorRange') &&
        newValue !== 'draw' &&
        newValue !== 'colorRange'
      ) {
        this.$refs['editor'].invoke('stopDrawingMode');
      }
    },
  },
  mounted() {
    this.loadImageInfo();
    this.split = this.$route.params.split;
    this.toggleDraw();
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      // vm.$refs.editor.initInstance();
    });
  },
  methods: {
    loadImageInfo() {
      this.image_url = sessionStorage.getItem('image_url');
    },
    async loadEdit() {
      this.$root.startProcessing('Loading previous annotation. Please wait...');
      try {
        const res = await APIGetAnnotated(this.split, this.image_url);
        const edit_url = res.data.data;
        if (!edit_url) {
          this.$root.finishProcessing();
          this.$root.alert('error', 'No previous annotation found');
        } else {
          // Don't change this.split and this.image_url here because they will be used
          // to get the next image
          sessionStorage.setItem('split', 'annotated');
          sessionStorage.setItem('image_url', edit_url);
          this._reset();
          this.$root.finishProcessing();
          this.$root.alert('success', 'Previous annotation loaded');
        }
      } catch (error) {
        this.$root.finishProcessing();
        this.$root.alert('error', 'Failed to load previous annotation');
      }
    },
    async autoEdit() {
      this.$root.startProcessing('Auto-annotating...');
      try {
        const res = await APIGetProposedEdit(this.split, this.image_url);
        const proposed_url = res.data.data;
        // Same as above, don't change this.split and this.image_url here because they will be used
        // to get the next image
        sessionStorage.setItem('image_url', proposed_url);
        sessionStorage.setItem('split', 'proposed');
        this._reset();
        this.$root.finishProcessing();
        this.$root.alert('success', 'Automatic annotation applied.');
      } catch (error) {
        console.log(error);
        this.$root.finishProcessing();
        this.$root.alert('error', 'Failed to auto annotate');
      }
    },
    adjustImageSize() {
      this.imageWidth = 500;
      this.imageHeight = 500;
      this.$refs.editor.resize({ width: 500, height: 500 });
      // this.$refs['editor'].invoke('resizeCanvasDimension', { width: 500, height: 500 });
    },
    async sendEdit() {
      this.$root.startProcessing(
        'The editing information of this image is being sent. Please wait...'
      );
      const image_url = sessionStorage.getItem('image_url') || '';
      const image_height = sessionStorage.getItem('image_height');
      const image_width = sessionStorage.getItem('image_width');
      const split = sessionStorage.getItem('split');
      try {
        const image_base64 = this.$refs['editor'].invoke('toDataURL');
        await APISendEdit({ split, image_url, image_height, image_width, image_base64 });
        this.$root.finishProcessing();
        this.$root.alert('success', 'Sending succeeded');
      } catch (error) {
        console.log(error);
        this.$root.finishProcessing();
        this.$root.alert('error', 'Sending failed');
      }
      try {
        const res = await APIGetNextImage(this.split, this.image_url);
        sessionStorage.setItem('image_url', res.data.data);
        this._reset();
        this.loadImageInfo();
      } catch (error) {
        console.log(error);
        this.$root.alert('error', 'Failed to get next image');
      }
    },
    mousedown(event, originPointer) {
      switch (this.mode) {
        case 'zoomIn':
          this.zoomLevel++;
          this.$refs['editor'].invoke('zoom', {
            x: originPointer.x,
            y: originPointer.y,
            zoomLevel: this.zoomLevel,
          });
          break;
        case 'zoomOut':
          if (this.zoomLevel == 1) return;
          this.zoomLevel--;
          this.$refs['editor'].invoke('zoom', {
            x: originPointer.x,
            y: originPointer.y,
            zoomLevel: this.zoomLevel,
          });
          break;
        default:
          break;
      }
    },
    toggleResize() {
      if (this.mode === 'resize') {
        this.mode = '';
      } else {
        this.mode = 'resize';
        this.tempWidth = this.imageWidth;
        this.tempHeight = this.imageHeight;
      }
    },
    toggleDraw() {
      if (this.mode === 'draw') {
        this.mode = '';
        this.$refs['editor'].invoke('stopDrawingMode');
      } else {
        this.mode = 'draw';
        this.$refs['editor'].invoke('startDrawingMode', 'FREE_DRAWING');
        this.$refs['editor'].invoke('setBrush', {
          width: this.brushWidth,
          color: 'FFFFFF',
        });
        this.$refs['editor'].invoke('changeSelectableAll', true);
      }
    },
    toggleColorRange() {
      if (this.mode === 'colorRange') {
        this.mode = '';
        this.$refs['editor'].invoke('stopDrawingMode');
      } else {
        this.mode = 'colorRange';
        this.$refs['editor'].invoke('startDrawingMode', 'COLOR_RANGE_DRAWING');
      }
    },
    _reset() {
      this.$refs.editor.reset();
      Object.assign(this, {
        mode: '',
        zoomLevel: 1,
        brushWidth: 10,
        imageWidth: 224,
        tempWidth: 224,
        imageHeight: 224,
        tempHeight: 224,
        lockAspectRatio: false,
      });
      this.toggleDraw();
    },
  },
};
</script>

<style scoped>
.float-button {
  position: fixed;
  bottom: 120px;
  right: -80px;
  z-index: 9999;
}

.float-button:hover {
  transform: translateX(-90px);
}
</style>
