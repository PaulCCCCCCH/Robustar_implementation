<template>
  <div style="height: 100%">
    <!-- <v-btn depressed color="#FDBA3B" class="white--text float-button" @click="adjustImageSize">
      adjust
    </v-btn> -->
    <!-- <div style="position: absolute; top: 50px; width: 100%"> -->
    <div class="d-flex flex-row justify-space-between" style="width: 100%; height: 100%">
      <ImageEditor ref="editor" :include-ui="useDefaultUI" :options="options"></ImageEditor>
      <Visualizer :image_id="image_id" :split="split" />
    </div>
  </div>
</template>
<script>
import ImageEditor from '@/components/image-editor/ImageEditor';
import { APISendEdit } from '@/apis/edit';
import { APIGetAnnotated } from '@/apis/images';
import { getNextImageByIdAndURL, replaceSplitAndId } from '@/utils/image_utils';
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
        apiLoadEdit: this.loadEdit.bind(this),
      },
      image_id: '', // corresponding training set id
      image_url: '',
      split: '',
      edit_id: '', // corresponding paired set id
    };
  },
  mounted() {
    this.loadImageInfo();
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      // vm.$refs.editor.initInstance();
    });
  },
  methods: {
    loadImageInfo() {
        this.image_id = sessionStorage.getItem('image_id');
        this.image_url = sessionStorage.getItem('image_url');
        this.split = sessionStorage.getItem('split');
        if (this.split === 'annotated') {
          this.split = 'train'
        }
    },
    loadEditSuccess(res) {
      const edit_id = res.data.data
      console.log(edit_id)
      if (edit_id === -1) {
        this.$root.finishProcessing();
        this.$root.alert('error', 'No previous annotation found');
      } else {
        sessionStorage.setItem('image_id', edit_id);
        sessionStorage.setItem('split', 'annotated');
        sessionStorage.setItem('image_url', replaceSplitAndId(this.image_url, 'annotated', edit_id)); 
        this.$refs.editor.initInstance();
        this.$root.finishProcessing();
        this.$root.alert('success', 'Previous annotation loaded');
      }
    },
    loadEditFailed(res) {
      console.log(res);
      this.$root.finishProcessing();
      this.$root.alert('error', 'No');
    },
    loadEdit() {
      this.$root.startProcessing(
        'Loading previous annotation. Please wait...'
      );
      APIGetAnnotated(this.image_id, this.loadEditSuccess, this.loadEditFailed)
    },
    adjustImageSize() {
      this.$refs.editor.invoke('resize', { width: 500, height: 500 });
    },
    sendEditSuccess(res) {
      // TODO: Edit success and jump to the next image or back to the image list
      console.log(res);
      const [newId, newUrl] = getNextImageByIdAndURL(this.image_id, this.image_url);
      this.image_id = `${newId}`;
      this.image_url = `${newUrl}`;
      sessionStorage.setItem('image_id', newId);
      sessionStorage.setItem('image_url', newUrl);
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
      const image_id = sessionStorage.getItem('image_id') || '';
      const height = sessionStorage.getItem('image_height');
      const width = sessionStorage.getItem('image_width');
      const split = sessionStorage.getItem('split');
      APISendEdit(
        split,
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
