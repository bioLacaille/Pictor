/* 公共引入,勿随意修改,修改时需经过确认 */
import Vue from "vue";
import "./element";
import "./support";
import "@/styles/vab.scss";
import "@/styles/dkStyles/main.scss";
import pictor from "@/utils/pictor";
import "@/remixIcon";
import "@/colorfulIcon";
import "@/config/permission";
import "@/utils/errorLog";
import drag from "@/directive/drag";
import permissions from "@/directive/permissions";
import "./AFIcon";
import VabQueryForm from "@/components/VabQueryForm";
import VabQueryFormTopPanel from "@/components/VabQueryForm/VabQueryFormTopPanel";
import VabQueryFormBottomPanel from "@/components/VabQueryForm/VabQueryFormBottomPanel";
import VabQueryFormLeftPanel from "@/components/VabQueryForm/VabQueryFormLeftPanel";
import VabQueryFormRightPanel from "@/components/VabQueryForm/VabQueryFormRightPanel";
import uploader from "vue-simple-uploader";

import {
  FontAwesomeIcon,
  FontAwesomeLayers,
  FontAwesomeLayersText,
} from "@fortawesome/vue-fontawesome";

Vue.component("font-awesome-icon", FontAwesomeIcon);
Vue.component("font-awesome-layers", FontAwesomeLayers);
Vue.component("font-awesome-layers-text", FontAwesomeLayersText);

const VueUploadComponent = require("vue-upload-component");
Vue.component("file-upload", VueUploadComponent);

Vue.use(uploader);
Vue.use(permissions);
Vue.use(drag);
Vue.use(pictor);

Vue.component("vab-query-form", VabQueryForm);
Vue.component("vab-query-form-left-panel", VabQueryFormLeftPanel);
Vue.component("vab-query-form-right-panel", VabQueryFormRightPanel);
Vue.component("vab-query-form-top-panel", VabQueryFormTopPanel);
Vue.component("vab-query-form-bottom-panel", VabQueryFormBottomPanel);
