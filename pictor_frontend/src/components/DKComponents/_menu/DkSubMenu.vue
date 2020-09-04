<template functional>
  <el-submenu
    v-if="props.menu"
    :popper-class="props.popperClass"
    :index="props.menu.key"
  >
    <template slot="title"
      ><i
        :class="
          props.menu.icon
            ? props.menu.icon
            : props.level === 0
            ? 'el-icon-document'
            : 'ion-empty'
        "
      ></i
      ><span slot="title">{{ props.menu.title }}</span></template
    >
    <template v-for="(item, i) in props.menu.children">
      <dk-sub-menu
        v-if="item.children && item.children.length > 0"
        :key="i"
        :menu="item"
        :level="props.level + 1"
      ></dk-sub-menu>
      <el-menu-item v-else :key="i" :index="item.key"
        ><i class="ion-empty"></i
        ><span slot="title">{{ item.title }}</span></el-menu-item
      >
    </template>
  </el-submenu>
</template>

<script>
export default {
  name: "DkSubMenu",
  props: {
    // eslint-disable-next-line vue/require-default-prop
    menu: Object,
    level: {
      type: Number,
      default: 0,
    },
    popperClass: {
      type: String,
      default: "",
    },
  },
};
</script>
