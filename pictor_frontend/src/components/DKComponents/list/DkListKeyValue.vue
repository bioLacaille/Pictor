<template>
  <el-row
    :gutter="0"
    :class="[
      'dk-list-key-value',
      isButton ? 'dk-list-key-value-is-button' : '',
    ]"
  >
    <slot name="prepend"></slot>
    <el-col
      v-for="(item, index) in isSingleData ? [list] : list"
      :key="index"
      :xs="xs"
      :sm="sm"
      :md="md"
      :lg="lg"
      :xl="xl"
      :span="
        span ? span : !xs && !sm && !md && !lg && !xl ? 24 / list.length : span
      "
      :class="['dk-list-item', 'dk-text-' + align]"
    >
      <div class="dk-list-key" v-html="item.key"></div>
      <div class="dk-list-value" v-html="item.value"></div>
    </el-col>
    <slot></slot>
  </el-row>
</template>

<script>
export default {
  name: "DkListKeyValue",
  props: {
    list: {
      type: [Array, Object],
      default() {
        return [];
      },
    },
    // 是否单条数据
    isSingleData: {
      type: Boolean,
      default: false,
    },
    // 对齐
    align: {
      type: String,
      default: "center", // 可选的值 left|center|right
    },
    // 是否按钮
    isButton: {
      type: Boolean,
      default: false,
    },
    // 布局
    // eslint-disable-next-line vue/require-default-prop
    xs: Number,
    // eslint-disable-next-line vue/require-default-prop
    sm: Number,
    // eslint-disable-next-line vue/require-default-prop
    md: Number,
    // eslint-disable-next-line vue/require-default-prop
    lg: Number,
    // eslint-disable-next-line vue/require-default-prop
    xl: Number,
    // eslint-disable-next-line vue/require-default-prop
    span: Number,
  },
};
</script>

<style scoped></style>
