<template>
  <div style="height: 80%">
    <ImageEditor
      :include-ui="useDefaultUI"
      :options="options"
    ></ImageEditor>
  </div>
</template>
<script>
import ImageEditor from '../components/image-editor/ImageEditor'

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
      },
    };
  },
};
</script>