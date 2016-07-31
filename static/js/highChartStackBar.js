$(document).ready(function(){


    // 登录按钮
    $("#all-tag-btn").click(function(){
        // showAllMyTags()
    });

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

function showAllMyTags(){

    $.post("/queryRequetForAllRecorderTags",{

  },function(data,status){
    if (data.retCode != 0) {
      alert(data.msg);
    }else{
      console.log(data.data);
    }
  });
}