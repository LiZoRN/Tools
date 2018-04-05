$(function () {
    $.getJSON('/monitor/api/v1.0/memory', function (data) {
        // Create the chart
        $('#container').highcharts('StockChart', {
            chart:{
                events:{
                    load:function(){
                        var series = this.series[0]
                        setInterval(function(){
                            $.getJSON('/monitor/api/v1.0/memory',function(res){
                                $.each(res,function(i,v){
                                    var x = (new Date()).getTime(),
                                        freeMemory = v.free;
                                    series.addPoint([x,freeMemory])
                                })
                            })
                        },5000)
                    }
                }
            },
            yAxis:  {
                title: {
                    text: '空闲内存'
                },
                plotLines: [{
                    value: data.memory.total,
                    color: 'red',
                    width: 2,
                    label: {
                        text: '总内存'
                    }
                }]
            },


            rangeSelector : {
                selected : 1
            },

            title : {
                text : '内存数据'
            },

            series : [{
                name: '内存变化',
                tooltip: {
                    valueDecimals: 4
                }
            }]
        });
    });

});