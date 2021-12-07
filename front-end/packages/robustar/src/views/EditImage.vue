<template>
  <div style="height: 100%">
    <!-- <v-btn depressed color="#FDBA3B" class="white--text float-button" @click="adjustImageSize">
      adjust
    </v-btn> -->

    <ImageEditor ref="editor" :include-ui="useDefaultUI" :options="options"></ImageEditor>

    <v-overlay :value="sending" opacity="0.7">
      <v-progress-circular indeterminate size="30" class="mr-4"></v-progress-circular>
      <span style="vertical-align: middle">
        The editing information of this image is being sent. Please wait...
      </span>
    </v-overlay>

    <!-- sending succeeded -->
    <v-snackbar
      rounded
      dark
      right
      v-model="snackbar"
      timeout="3000"
      elevation="3"
      transition="slide-x-reverse-transition"
      class="mb-2 mr-2"
    >
      <div class="white--text">Sending succeeded</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="accent" text v-bind="attrs" @click="snackbar = false"> Close </v-btn>
      </template>
    </v-snackbar>

    <!-- sending failed -->
    <v-snackbar
      rounded
      dark
      right
      v-model="snackbarError"
      timeout="3000"
      elevation="3"
      transition="slide-x-reverse-transition"
      class="mb-2 mr-2"
    >
      <div class="white--text">Sending failed</div>
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbarError = false"> Close </v-btn>
      </template>
    </v-snackbar>
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
        apiSendEdit: this.sendEdit.bind(this),
      },

      sending: false, // sending image data
      snackbar: false,
      snackbarError: false,
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
      const newId = Number(id) + 1;
      const arr = url.split('/');
      const newUrl = arr.slice(0, arr.length - 1).join('/') + `/${newId}`;
      localStorage.setItem('image_id', newId);
      localStorage.setItem('image_url', newUrl);
      this.$refs.editor.initInstance();
      this.sending = false;
      this.snackbar = true;
    },
    sendEditFailed(res) {
      console.log(res);
      this.sending = false;
      this.snackbarError = true;
    },
    sendEdit(image_base64) {
      this.sending = true;
      const image_id = localStorage.getItem('image_id') || '';
      APISendEdit('train', image_id, image_base64, this.sendEditSuccess, this.sendEditFailed);
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
