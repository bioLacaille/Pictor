<template>
  <div class="json-editor">
    <label>
      <textarea ref="textarea" />
    </label>
  </div>
</template>

<script>
import CodeMirror from "codemirror";
import "codemirror/addon/lint/lint.css";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/rubyblue.css";
import "codemirror/theme/darcula.css";
import "codemirror/theme/ambiance-mobile.css";
import "codemirror/mode/javascript/javascript";
import "codemirror/addon/lint/lint";
import "codemirror/addon/lint/json-lint";
require("script-loader!jsonlint");

export default {
  name: "CodeEditor",
  props: {
    value: {
      type: [Array, Object, String],
      default: () => {
        return null;
      },
    },
    mode: {
      type: String,
      default: "text/javascript",
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
    width: {
      type: Number,
      default:
        window.innerWidth ||
        document.documentElement.clientWidth ||
        document.body.clientWidth,
    },
    height: {
      type: Number,
      default:
        window.innerHeight ||
        document.documentElement.clientHeight ||
        document.body.clientHeight,
    },
  },
  data() {
    return {
      codeEditor: false,
    };
  },
  watch: {
    value(value) {
      const editorValue = this.codeEditor.getValue();
      // if (editorValue) {
      //   this.$emit("change", editorValue);
      // }
      if (value !== editorValue) {
        // this.codeEditor.setValue(JSON.stringify(this.value, null, 2));
        this.codeEditor.setValue(this.value);
      }
    },
  },
  mounted() {
    this.codeEditor = CodeMirror.fromTextArea(this.$refs.textarea, {
      lineNumbers: true,
      mode: this.mode,
      readOnly: this.readOnly,
      gutters: ["CodeMirror-lint-markers"],
      theme: "darcula",
      lint: true,
    });
    if (this.width !== 0 && this.height === 0) {
      this.codeEditor.setSize(this.width);
    } else if (this.width === 0 && this.height !== 0) {
      this.codeEditor.setSize("100%", this.height);
    } else {
      this.codeEditor.setSize(this.width, this.height);
    }
    this.codeEditor.setValue(this.value);
    // this.codeEditor.on("change", (cm) => {
    //   this.$emit("change", cm.getValue());
    // });
  },
  methods: {
    getValue() {
      return this.codeEditor.getValue();
    },
    isJsonString(str) {
      try {
        if (typeof JSON.parse(str) == "object") {
          return true;
        }
      } catch (e) {}
      return false;
    },
  },
};
</script>

<style scoped>
.json-editor {
  position: relative;
  height: 100%;
  width: 100%;
}

.json-editor >>> .CodeMirror {
  height: auto;
  min-height: 100px;
  /*min-height: calc(100vh - 220px);*/
}

.json-editor >>> .CodeMirror-scroll {
  min-height: 100px;
}

.json-editor >>> .CodeMirror pre.CodeMirror-line,
.json-editor >>> .CodeMirror pre.CodeMirror-line-like {
  /* Reset some styles that the rest of the page might have set */
  -moz-border-radius: 0;
  -webkit-border-radius: 0;
  border-radius: 0;
  border-width: 0;
  background: transparent;
  font-family: inherit;
  font-size: inherit;
  margin: 0;
  white-space: pre;
  word-wrap: normal;
  line-height: inherit;
  color: inherit;
  z-index: 2;
  position: relative;
  overflow: visible;
  -webkit-tap-highlight-color: transparent;
  -webkit-font-variant-ligatures: contextual;
  font-variant-ligatures: contextual;
  padding-left: 10px;
}

/*.json-editor >>> .CodeMirror-linenumbers {*/
/*}*/
/*.json-editor >>> .CodeMirror-linenumber {*/
/*  padding: 0 3px 0;*/
/*  min-width: 20px;*/
/*  text-align: right;*/
/*  color: #999;*/
/*  white-space: nowrap;*/
/*}*/
.json-editor >>> .CodeMirror-linenumber {
  -moz-box-sizing: content-box;
  box-sizing: content-box;
}
.json-editor >>> .CodeMirror-lint-markers {
  width: 25px;
}

.json-editor >>> .cm-s-rubyblue span.cm-string {
  color: #f08047;
}

.json-editor >>> .cm-s-rubyblue .CodeMirror-gutters {
  padding-left: 10px;
  padding-right: 10px;
  /* background: transparent; */
  border-right: 1px solid #fff;
}

.json-editor >>> .cm-s-rubyblue.CodeMirror {
  /* background: #08233e; */
  color: white;
}
</style>
