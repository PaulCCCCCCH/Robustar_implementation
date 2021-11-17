<template>
  <div style="height: 80%">
    <ImageEditor :include-ui="useDefaultUI" :options="options"></ImageEditor>
  </div>
</template>
<script>
import ImageEditor from '../components/image-editor/ImageEditor';
import { APISendEdit } from '@/apis/edit';

export default {
  components: {
    ImageEditor: ImageEditor,
  },
  data() {
    return {
      useDefaultUI: true,
      options: {
        // for tui-image-editor component's "options" prop
        cssMaxWidth: 700,
        cssMaxHeight: 1000,
        apiSendEdit: this.sendEdit,
      },
    };
  },
  methods: {
    sendEditSuccess() {
      // TODO: Edit success and jump to the next image or back to the image list
      console.log('Success!');
    },
    sendEditFailed() {
      // TODO:
      console.log('Failed!');
    },
    sendEdit(image_base64) {
      APISendEdit('train', '100', image_base64, this.sendEditSuccess, this.sendEditFailed);
    },
  },
};
</script>
