/* ===================Scene2===================== */
function NormalizeData(initialData) {
  var chartData = [];
  for (var i = 0; i < initialData.length / 5; i++) {
    var pos = i * 5;
    var year = parseInt(initialData[pos]);
    var month = parseInt(initialData[pos+1]);
    var day = parseInt(initialData[pos+2]);
    var sum = parseFloat(initialData[pos+3]);
    var num = parseInt(initialData[pos+4]);
    var newTime = new Date(year, month-1, day);
    if (num != 0) {
      chartData.push({
        date: newTime,
        total: sum,
        average: sum / num
      });
    } else {
      chartData.push({
        date: newTime,
        total: 0,
        average: 0
      });
    }
  }
  return chartData;
}

function GenerateChart2(chartData, min_date_interval) {
  // serial chart
  var chart = new AmCharts.AmSerialChart();
  chart.dataProvider = chartData;
  chart.categoryField = "date";
  // AXES
  // 1. Category
  var categoryAxis = chart.categoryAxis;
  categoryAxis.parseDates = true;
  categoryAxis.minPeriod = min_date_interval;
  categoryAxis.gridAlpha = 0.07;
  categoryAxis.gridCount = 50;
  categoryAxis.axisColor = "#DADADA";
  categoryAxis.gridColor = "#000000";
  categoryAxis.dateFormats = [{
    period: 'DD',
    format: 'DD'
  }, {
    period: 'MM',
    format: 'MMM'
  }, {
    period: 'YYYY',
    format: 'YYYY'
  }];
  // 2. Value
  var avgAxis = new AmCharts.ValueAxis();
  avgAxis.title = "Average Purchase Cost Per Period(RMB)";
  avgAxis.gridAlpha = 0.07;
  avgAxis.axisAlpha = 0;
  avgAxis.tickLength = 0;
  avgAxis.inside = true;
  chart.addValueAxis(avgAxis);
  var totalAxis = new AmCharts.ValueAxis();
  totalAxis.title = "Total Purchase Cost Per Period(RMB)";
  totalAxis.gridAlpha = 0;
  totalAxis.axisAlpha = 0;
  totalAxis.tickLength = 0;
  totalAxis.inside = true;
  totalAxis.position = "right";
  chart.addValueAxis(totalAxis);
  // GRAPHS
  // average graph
  var avgGraph = new AmCharts.AmGraph();
  avgGraph.valueField = "average";
  avgGraph.title = "average";
  avgGraph.type = "line";
  avgGraph.valueAxis = avgAxis;
  avgGraph.lineColor = "#CC0000";
  avgGraph.balloonText = "[[value]]";
  avgGraph.lineThickness = 1;
  avgGraph.legendValueText = "[[value]]";
  avgGraph.bullet = "square";
  avgGraph.bulletBorderColor = "#CC0000";
  avgGraph.bulletBorderAlpha = 1;
  avgGraph.bulletBorderThickness = 1;
  chart.addGraph(avgGraph);
  // total graph
  var totalGraph = new AmCharts.AmGraph();
  totalGraph.title = "total";
  totalGraph.valueField = "total";
  totalGraph.type = "column";
  totalGraph.fillAlphas = 0.5;
  totalGraph.valueAxis = totalAxis;
  totalGraph.balloonText = "[[value]]";
  totalGraph.legendValueText = "[[value]]";
  totalGraph.lineColor = "#000000";
  totalGraph.lineAlpha = 0;
  chart.addGraph(totalGraph);
  // CURSOR
  var chartCursor = new AmCharts.ChartCursor();
  chartCursor.cursorPosition = "mouse";
  chartCursor.categoryBalloonDateFormat = "MMM DD, YYYY";
  chartCursor.cursorAlpha = 0;
  chartCursor.valueLineEnabled = true;
  chartCursor.valueLineBallonEnabled = true;
  chartCursor.valueLineAxis = totalAxis;
  chart.addChartCursor(chartCursor);
  // LEGEND
  var legend = new AmCharts.AmLegend();
  legend.bulletType = "round";
  legend.equalWidths = false;
  legend.valueWidth = 120;
  legend.color = "#000000";
  legend.useGraphSettings = true;
  chart.addLegend(legend);
  // SCROLLBAR
  var chartScrollbar = new AmCharts.ChartScrollbar();
  chart.addChartScrollbar(chartScrollbar);
  return chart;
}
