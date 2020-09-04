<template>
  <el-button
    v-if="status"
    :size="size"
    :disable="disable"
    :type="type"
    :plain="plain"
    icon="el-icon-loading"
  ></el-button>
  <el-button v-else :size="size" :type="type" :plain="plain" @click="submit()"
    ><slot>保存</slot></el-button
  >
</template>

<script>
/**
 * 防抖表单提交按钮组件
 * 防抖：防止重复点击触发事件
 * 首先啥是抖？ 抖就是一哆嗦！原本点一下，现在点了3下！
 * 当持续触发某事件时，一定时间间隔内没有再触发事件时，事件处理函数才会执行一次，如果设定的时间间隔到来之前，又一次触发了事件，就重新开始延时。
 * props:
 * status -> 提交状态
 * type -> 按钮类型
 * emit:
 * btn -> 提交操作
 */
import { debounce } from "@/utils/dataset"; // 导入防抖函数
export default {
  props: {
    // 状态
    status: {
      type: Boolean,
      default: false,
    },
    disable: {
      type: Boolean,
      default: false,
    },
    // 类型
    type: {
      type: String,
      default: "primary",
    },
    // 是否简单样式
    plain: {
      type: Boolean,
      default: false,
    },
    // 大小
    size: {
      type: String,
      default: "medium",
    },
  },
  methods: {
    // 节流输出
    submit: debounce(
      function () {
        this.$emit("btn");
      },
      2000,
      true
    ),
  },
};
</script>
