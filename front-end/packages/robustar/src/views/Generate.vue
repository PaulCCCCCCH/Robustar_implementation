<template>
  <div id="training-settings-page" class="container">
    <el-card class="box-card form-group">
      <div class="tab-pane" id="billing">
        <h3 class="t_title">Paired Data Generation Settings</h3>
        <hr />
        <form>
          <div class="form-group">
            <label class="sec">Specify the path to the dataset to be mirrored</label>
            <input
              type="text"
              class="form-control"
              v-model="generate_configs.mirrored_data_path"
              aria-describedby="fullNameHelp"
              placeholder="Enter a value"
              value="Robustar2/paired_images"
            />

            <small class="form-text text-muted">
              Note that the selected data set should immediately contain class
              folders. In other words, the input path should be the exact thing
              that you would pass to an ImageFolder constructor
            </small>
          </div>

          <div class="form-group">
            <label class="sec">Specify the path to the user-edit json file</label>
            <input
              type="text"
              class="form-control"
              v-model="generate_configs.user_edit_path"
              aria-describedby="fullNameHelp"
              placeholder="Enter a value"
              value="/Robustar2/user-edit.json"
            />
            <small class="form-text text-muted"></small>
          </div>
          <button
            class="btn btn-primary"
            @click="generate_paired_data"
            type="button"
          >
            generate paired dataset
          </button>
        </form>
      </div>

      <!-- <button class="btn btn-info" type="button">Save configs</button> -->
    </el-card>
  </div>
</template>

  <script>
import { APIGeneratePairedDataset } from "@/apis/generate";
export default {
  name: "TrainPad",
  data() {
    return {
      // Data generation configs
      generate_configs: {
        mirrored_data_path: "/Robustar2/dataset/train",
        user_edit_path: "/Robustar2/user-edit.json",
      },
    };
  },
  methods: {
   generate_paired_data() {
      const success = (response) => {
        // TODO: Error handling according to the code returned from the server
        console.log(response);
        alert(response.data.msg);
      };

      const failed = (err) => {
        console.log(err);
        alert("Server error. Check console.");
      };
      APIGeneratePairedDataset(
        this.generate_configs.mirrored_data_path,
        this.generate_configs.user_edit_path,
        success,
        failed
      );
    },
  },
};
</script>

<style type="text/css">
body {
  margin-top: 20px;
  color: #1a202c;
  text-align: left;
  background-color: #e2e8f0;
}

.main-body {
  padding: 15px;
}

.nav-link {
  color: #4a5568;
}

.card {
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

.card {
  position: relative;
  display: flex;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
  border: 0 solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
}

.card-body {
  flex: 1 1 auto;
  min-height: 1px;
  padding: 1rem;
}

.gutters-sm {
  margin-right: -8px;
  margin-left: -8px;
}

.gutters-sm > .col,
.gutters-sm > [class*="col-"] {
  padding-right: 8px;
  padding-left: 8px;
}

.mb-3,
.my-3 {
  margin-bottom: 1rem !important;
}

.bg-gray-300 {
  background-color: #e2e8f0;
}

.h-100 {
  height: 100% !important;
}

.shadow-none {
  box-shadow: none !important;
}

.btn{
  margin-top: 10px;
}
.sec{
  font-size: 20px;
  font-weight: 500;
}
.t_title{
  text-align: center;
}
</style>
