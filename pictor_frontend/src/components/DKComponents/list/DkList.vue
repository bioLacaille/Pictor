<template>
  <ul class="dk-list">
    <li
      v-for="(item,index) in (isSingleData?[list]:list)"
      :key="index"
      class="dk-media dk-list-item"
    >
      <div
        :class="[
          'dk-media-aside',
          'dk-media-' + mediaShape,
          'dk-media-' + mediaPosition,
        ]"
      >
        <slot name="media" :row="item">
          <font-awesome-layers full-width class="fa-3x">
            <font-awesome-icon
              icon="tasks"
              :style="{ color: '#ADD8E6' }"
              size="lg"
            />
          </font-awesome-layers>
        </slot>
      </div>
      <div class="dk-media-body">
        <div
          v-if="typeof item.serial_number !== 'undefined'"
          class="dk-media-heading"
        >
          <slot name="header" :row="item">
            <h4 v-html="item.serial_number"></h4>
          </slot>
        </div>
        <slot name="body" :row="item">
          <div
            v-if="typeof item.created_time !== 'undefined'"
            class="dk-media-description"
            v-html="item.created_time"
          ></div>
        </slot>
      </div>
      <slot :row="item"></slot>
    </li>
  </ul>
</template>

<script>
export default {
  name: "DkList",
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
    // 图片形状
    mediaShape: {
      type: String,
      default: "square", // 可选的值 circle|square
    },
    // 图片位置
    mediaPosition: {
      type: String,
      default: "left", // 可选的值 left|right
    },
  },
};
</script>
