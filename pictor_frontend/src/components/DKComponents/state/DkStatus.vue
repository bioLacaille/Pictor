<template>
  <span :class="['dk-status', 'dk-status-' + type]">
    <span
      :class="['dk-status-dot', processing ? 'dk-status-dot-processing' : '']"
    ></span>
    <span class="dk-status-text">{{ text }}</span>
  </span>
</template>

<script>
export default {
  name: "DkStatus",
  props: {
    type: {
      type: String,
      default: "primary", // 值：success|primary|info|danger|warning
    },
    // eslint-disable-next-line vue/require-default-prop
    text: String,
    processing: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped></style>
