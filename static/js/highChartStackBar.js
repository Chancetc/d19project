$(document).ready(function(){


	var high = {
                    chart: {
                        type: 'bar'
                    },
                    title: {
                        text: '耗时统计'
                    },
                    xAxis: {
                        categories: ['第一次', '第二次', '第三次', '第四次', '第五次', '第六次', '第七次', '第八次', '第九次', '第十次' ]
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: '耗时(ms)'
                        }
                    },
                    legend: {
                        reversed: true
                    },
                    plotOptions: {
                        series: {
                            stacking: 'normal'
                        }
                    }
                };
    var chartData = $('#chart-container1').attr("value")
    high['series'] = eval(chartData)
    $('#chart-container1').highcharts(high);
    $('#chart-container2').highcharts(high);
});