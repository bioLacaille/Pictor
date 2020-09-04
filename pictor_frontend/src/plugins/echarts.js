import "echarts";
import "echarts/map/js/china";
import "echarts/map/js/world";

import "echarts-wordcloud";

import VabChart from "vue-echarts";
import theme from "./pictor-echarts-theme.json";

VabChart.registerTheme("pictor-echarts-theme", theme);
export default VabChart;
