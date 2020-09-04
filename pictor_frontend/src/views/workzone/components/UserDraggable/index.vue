<template>
  <div class="board-column">
    <div class="board-column-header">
      {{ headerText }}
    </div>
    <draggable
      :list="list"
      v-bind="$attrs"
      class="board-column-content"
      :set-data="setData"
      @change="checkChange"
    >
      <div v-for="element in list" :key="element.id" class="board-item">
        {{ element.name }}
      </div>
    </draggable>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import { saveWorkZoneMember } from "@/api/workzone";

export default {
  name: "UserDraggable",
  components: {
    draggable,
  },
  props: {
    headerText: {
      type: String,
      default: "Header",
    },
    draggableType: {
      type: Number,
      default: 0,
    },
    instanceId: {
      type: Number,
      default: 0,
    },
    options: {
      type: Object,
      default() {
        return {};
      },
    },
    list: {
      type: Array,
      default() {
        return [];
      },
    },
  },
  created() {},
  methods: {
    async checkChange(event) {
      if (event.added) {
        const member = event.added.element;
        const level = this.draggableType;
        const instance_id = this.instanceId;
        const data = await saveWorkZoneMember(instance_id, {
          user: member.id,
          level: level,
        });
        const { messages, results } = data;
        this.$baseMessage(messages, "success");
        this.$emit("refreshMembers");
      }
    },
    setData(dataTransfer) {
      // to avoid Firefox bug
      // Detail see : https://github.com/RubaXa/Sortable/issues/1012
      dataTransfer.setData("Text", "");
    },
  },
};
</script>
<style lang="scss" scoped>
.board-column {
  min-width: 15%;
  min-height: 100px;
  margin-left: 10px;
  height: auto;
  /*overflow: hidden;*/
  background: #f0f0f0;
  border-radius: 3px;

  .board-column-header {
    height: 50px;
    line-height: 50px;
    overflow: hidden;
    padding: 0 20px;
    text-align: center;
    background: #333;
    color: #fff;
    border-radius: 3px 3px 0 0;
  }

  .board-column-content {
    /*height: auto;*/
    /*overflow: hidden;*/
    border: 10px solid transparent;
    min-height: 600px;
    display: flex;
    justify-content: flex-start;
    flex-direction: column;
    align-items: center;

    .board-item {
      cursor: pointer;
      width: 100%;
      height: 64px;
      margin: 5px 0;
      background-color: #fff;
      text-align: left;
      line-height: 54px;
      padding: 5px 10px;
      box-sizing: border-box;
      box-shadow: 0px 1px 3px 0 rgba(0, 0, 0, 0.2);
    }
  }
}
</style>
