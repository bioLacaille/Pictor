<template>
  <div id="pictor">
    <router-view />
    <data-uploader @getForFileList="getForFileList"></data-uploader>
  </div>
</template>

<script>
import DataUploader from "@/components/DataUploader";
export default {
  name: "App",
  components: { DataUploader },
  mounted() {},
  methods: {
    getForFileList() {
      console.log("getForFileList router", this.$route.path);
      if (this.$route.path === "/dataset") {
        this.$baseEventBus.$emit("reloadRouterView");
      }
    },
  },
};
</script>
