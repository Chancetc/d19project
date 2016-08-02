$(document).ready(function(){


    // 登录按钮
    $("#all-tag-btn").click(function(){
        // showAllMyTags()
    });

    var recordData = $('#chart-container1').attr("value");
    var chartData = getHighChartDataFromRecordData(recordData);

    $('#chart-container1').highcharts(chartData);
    
    $('#nav-progress-bar').animate({
        width:'60%'
    },500);
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

// ajax加载图表
function loadUserRecords(tag,date,start,end){

    $.post("/queryRequestForUserRecords",{
        userId:getCookie('userId'),
        tag:tag,
        recordDate:date,
        start:start,
        end:end
    },function(data,status){
        if (data.retCode != 0) {
            alert(data.msg);
        }else{
            console.log("loadUserRecords:");
            console.log(data.data);
            console.log("loadUserRecords:end");
            if (data.data.length == 0) {
                alert("sorry, there is no data to show!");
            }else{
                constructDomsWithRecordDatas(data.data["records"]);
                $('#nav-progress-bar').animate({width:'100%'}, 100, function(){
                    // $('#nav-progress-barCon').hide();
                    setTimeout(function(){
                        document.getElementById("nav-progress-barCon").style.display="none";
                    },500);
                    
                });
                
            }
        }
    });
}

// 根据后台返回构建节点并生成图表
function constructDomsWithRecordDatas(recordDatas){

    var lastTag = "";
    for (var i = 0; i < recordDatas.length; i++) {
        var recordData = recordDatas[i]["chartData"];
        var chartData = getHighChartDataFromRecordData(recordData);
        var idForCharDiv = "chart-container1"+i;
        var selForChart = "#"+idForCharDiv+"";
        var chartDicLeftStr = "<div class='row' role = 'main' style='border-bottom: 1px solid #eee; margin-bottom:20px'>";
        if (lastTag != recordDatas[i]["tag"]) {
            chartDicLeftStr += "<h2>日期: "+recordDatas[i]["firstDate"]+"  标签: "+recordDatas[i]["tag"]+"</h2><div class='col-md-5'><ul class='record-date-ul'>";
        }else{
            chartDicLeftStr += "<div class='col-md-5'><ul class='record-date-ul'>"
        }
        lastTag = recordDatas[i]["tag"];
        for (var j = 0; j < recordDatas[i]["dateList"].length; j++) {
            var dateItem = "<li>Record "+(j+1)+": tag:"+recordDatas[i]["tag"]+" date:"+recordDatas[i]["dateList"][j]+"</li>";
            chartDicLeftStr += dateItem;
        }
        chartDicLeftStr += "</ul></div><div class='col-md-7'>";
        var chartDivRightStr = "<div id="+idForCharDiv+" class='chart-container'></div></div></div>";
        var chartDivStr = chartDicLeftStr +chartDivRightStr;
        $('#main-contaner').append(chartDivStr);
        $(selForChart).highcharts(chartData);
    }
}

// 根据rawdata生成图表可用的图表数据
function getHighChartDataFromRecordData(recordData){

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
    high['series'] = eval(recordData)
    return high;
}
function getCookie(c_name){
    
    if (document.cookie.length>0){ 
        c_start=document.cookie.indexOf(c_name + "=")
        if (c_start!=-1){ 
            c_start=c_start + c_name.length+1 
            c_end=document.cookie.indexOf(";",c_start)
            if (c_end==-1) c_end=document.cookie.length
                return unescape(document.cookie.substring(c_start,c_end))
        } 
    }
    return ""
}

function setCookie(c_name,value,expiredays){

    var exdate=new Date()
    exdate.setDate(exdate.getDate()+expiredays)
    document.cookie=c_name+ "=" +escape(value)+((expiredays==null) ? "" : "; expires="+exdate.toGMTString())
}

