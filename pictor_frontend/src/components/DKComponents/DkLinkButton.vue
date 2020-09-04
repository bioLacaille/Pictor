<template>
  <router-link
    :class="[
      'el-button',
      'el-button--' + type,
      round ? 'is-round' : '',
      plain ? 'is-plain' : '',
      circle ? 'is-circle' : '',
      disabled ? 'is-disabled' : '',
      size ? 'el-button--' + size : '',
    ]"
    :to="to ? to : 'javascript:void(0);'"
    :target="target"
  >
    <i v-if="icon" :class="icon"></i>
    <span><slot></slot></span>
  </router-link>
</template>

<script>
export default {
  name: "DkLinkButton",
  // 配置同element ui的button组件
  props: {
    // eslint-disable-next-line vue/require-default-prop
    to: [String, Object],
    // eslint-disable-next-line vue/require-default-prop
    target: String,
    type: {
      type: String,
      default: "default",
    },
    // eslint-disable-next-line vue/require-default-prop
    size: String,
    plain: {
      type: Boolean,
      default: false,
    },
    round: {
      type: Boolean,
      default: false,
    },
    circle: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    // eslint-disable-next-line vue/require-default-prop
    icon: String,
  },
};
</script>

<style scoped></style>
