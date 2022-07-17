<template>
  <div class="d-flex flex-row justify-space-between" style="width: 100%; height: 100%">
    <ImageEditor ref="editor" :include-ui="useDefaultUI" :options="options"></ImageEditor>
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
      useDefaultUI: true,
      options: {
        // for tui-image-editor component's "options" prop
        cssMaxWidth: 700,
        cssMaxHeight: 1000,
        apiSendEdit: this.sendEdit.bind(this),
        apiLoadEdit: this.loadEdit.bind(this),
        apiAutoEdit: this.autoEdit.bind(this),
      },
      image_url: '',
      split: '',
    };
  },
  mounted() {
    this.loadImageInfo();
    this.split = this.$route.params.split;
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
        const res = await APIGetAnnotated(
          this.split,
          this.image_url,
          this.loadEditSuccess,
          this.loadEditFailed
        );
        const edit_url = res.data.data;
        if (!edit_url) {
          this.$root.finishProcessing();
          this.$root.alert('error', 'No previous annotation found');
        } else {
          // Don't change this.split and this.image_url here because they will be used
          // to get the next image
          sessionStorage.setItem('split', 'annotated');
          sessionStorage.setItem('image_url', edit_url);
          this.$refs.editor.initInstance();
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
        this.$refs.editor.initInstance();
        this.$root.finishProcessing();
        this.$root.alert('success', 'Automatic annotation applied.');
      } catch (error) {
        console.log(error);
        this.$root.finishProcessing();
        this.$root.alert('error', 'Failed to auto annotate');
      }
    },
    adjustImageSize() {
      this.$refs.editor.invoke('resize', { width: 500, height: 500 });
    },
    async sendEdit(image_base64) {
      this.$root.startProcessing(
        'The editing information of this image is being sent. Please wait...'
      );
      const image_url = sessionStorage.getItem('image_url') || '';
      const image_height = sessionStorage.getItem('image_height');
      const image_width = sessionStorage.getItem('image_width');
      const split = sessionStorage.getItem('split');
      try {
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
        this.$refs.editor.initInstance();
        this.loadImageInfo();
      } catch (error) {
        console.log(error);
        this.$root.alert('error', 'Failed to get next image');
      }
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
