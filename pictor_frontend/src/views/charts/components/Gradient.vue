<template>
  <span>{{ numValue }}</span>
</template>

<script>
export default {
  name: "Gradient",
  props: {
    // eslint-disable-next-line vue/require-default-prop
    value: Number,
  },
  data() {
    return {
      numValue: this.value - 100,
    };
  },
  mounted() {
    var interval = setInterval(() => {
      if (this.numValue >= this.value) {
        this.numValue = this.value;
        clearInterval(interval);
        return;
      }
      this.numValue = this.numValue + Math.floor(Math.random() * 10 + 1);
    }, 50);
  },
};
</script>

<style lang="scss" scoped></style>
