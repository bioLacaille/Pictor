<template>
  <div :class="['dk-result', 'dk-result-' + state]">
    <div class="dk-result-icon"><i :class="'el-icon-' + state"></i></div>

    <h3 v-if="title" class="dk-result-title" v-html="title"></h3>
    <h3 v-else class="dk-result-title">{{ state.toLocaleUpperCase() }}</h3>
    <div v-if="content" class="dk-result-description" v-html="content"></div>
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "DkResult",
  props: {
    state: {
      type: String,
      default: "info", // 允许的值 info|question|warning|success|danger
    },
    // eslint-disable-next-line vue/require-default-prop
    title: String,
    // eslint-disable-next-line vue/require-default-prop
    content: String,
  },
};
</script>
