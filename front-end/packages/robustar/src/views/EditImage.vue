<template>
  <div style="height: 100%">
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

      imageId: '',
      imageUrl: '',
      sending: false, // sending image data
      snackbar: false,
      snackbarError: false,
    };
  },
  mounted() {
    const id = localStorage.getItem('image_id');
    const url = localStorage.getItem('image_url');
    this.imageId = id;
    this.imageUrl = url;
    // this.$refs.editor.invoke('loadImageFromURL', this.imageUrl, this.imageId);
  },
  beforeRouteEnter(to, from, next) {
    next((vm) => {
      vm.$refs.editor.initInstance();
    });
  },
  methods: {
    sendEditSuccess(res) {
      // TODO: Edit success and jump to the next image or back to the image list
      console.log(res);
      this.sending = false;
      this.snackbar = true;
    },
    sendEditFailed(res) {
      // TODO:
      console.log(res);
      this.sending = false;
      this.snackbarError = true;
    },
    sendEdit(image_base64) {
      this.sending = true;
      APISendEdit('train', this.imageId, image_base64, this.sendEditSuccess, this.sendEditFailed);
    },
  },
};
</script>
