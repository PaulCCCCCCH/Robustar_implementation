<template>
  <v-sheet rounded width="800" elevation="3" class="my-8 pa-4" style="margin: 0 auto">
    <div class="text-h4 text-center font-weight-medium">Configuration</div>
    <v-divider class="mt-4 mb-8"></v-divider>
    <v-simple-table class="pad">
      <template v-slot:default>
        <tbody>
          <tr v-for="(value, key) of configs">
            <td class="key">{{ key }}</td>
            <td class="value">{{ value }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-sheet>
</template>

<script>
import { APIGetConfig } from '@/services/config';
export default {
  name: 'Config',
  data() {
    return {
      configs: null,
      name: null,
    };
  },
  methods: {
    async startGettingConfig() {
      try {
        const res = await APIGetConfig();
        console.log(res);
        this.configs = res.data.data;
      } catch (error) {
        console.log(res);
        this.configs = undefined;
      }
    },
  },
  beforeMount() {
    this.startGettingConfig();
  },
};
</script>

<style>
.pad {
  margin: 0 auto;
  /* display: flex; */
  padding-top: 3px;
  /* border-collapse:separate; */
}

.key {
  font-size: 1.1rem !important;
  font-weight: 600;
  line-height: 1.7rem;
  letter-spacing: normal !important;
  text-align: center;
  border-right: 3px solid #74a2cf;
}
.value {
  font-size: 1rem !important;
  font-weight: 500;
  line-height: 1.7rem;
  letter-spacing: normal !important;
  text-align: right;
}
</style>
