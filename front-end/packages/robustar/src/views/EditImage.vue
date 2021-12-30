<template>
  <div style="height: 100%">
    <!-- <v-btn depressed color="#FDBA3B" class="white--text float-button" @click="adjustImageSize">
      adjust
    </v-btn> -->
    <div style="position: absolute; top: 50px; width: 100%">
      <Visualizer />
    </div>
    <ImageEditor ref="editor" :include-ui="useDefaultUI" :options="options"></ImageEditor>
  </div>
</template>
<script>
import ImageEditor from '@/components/image-editor/ImageEditor';
import { APISendEdit } from '@/apis/edit';
import { getNextImageByIdAndURL } from '@/utils/image_utils';
import Visualizer from '@/components/prediction-viewer/Visualizer';

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
      },
    };
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      // vm.$refs.editor.initInstance();
    });
  },
  methods: {
    adjustImageSize() {
      this.$refs.editor.invoke('resize', { width: 500, height: 500 });
    },
    sendEditSuccess(res) {
      // TODO: Edit success and jump to the next image or back to the image list
      console.log(res);
      const id = localStorage.getItem('image_id');
      const url = localStorage.getItem('image_url');
      const [newId, newUrl] = getNextImageByIdAndURL(id, url);
      localStorage.setItem('image_id', newId);
      localStorage.setItem('image_url', newUrl);
      this.$refs.editor.initInstance();
      this.$root.finishProcessing();
      this.$root.alert('success', 'Sending succeeded');
    },
    sendEditFailed(res) {
      console.log(res);
      this.$root.finishProcessing();
      this.$root.alert('error', 'Sending failed');
    },
    sendEdit(image_base64) {
      this.$root.startProcessing(
        'The editing information of this image is being sent. Please wait...'
      );
      const image_id = localStorage.getItem('image_id') || '';
      const height = localStorage.getItem('image_height');
      const width = localStorage.getItem('image_width');
      APISendEdit(
        'train',
        image_id,
        height,
        width,
        image_base64,
        this.sendEditSuccess,
        this.sendEditFailed
      );
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
