$(document).ready(function () {
    var opts = $('#ex_select option').map(function () {
        return [[this.value, $(this).text()]];
    });
    var rx_opts = $('#rx_select option').map(function () {
        return [[this.value, $(this).text()]];
    });
    
    
    var colors = ["#e74c3c", "#1abc9c", "#2ecc71"];
    $(".datepicker").datepicker({dateFormat: 'dd-MM-yy'});
    $(".timepicker").datetimepicker({
        timeFormat: 'HH:mm:ss',
        stepHour: 1,
        stepMinute: 1,
        stepSecond: 20
    });

    $('#en_input').keyup(function () {
        var rxp = new RegExp($('#en_input').val(), 'i');
        var optlist = $('#en_select').empty();
        opts.each(function () {
            if (rxp.test(this[1])) {
                optlist.append($('<option/>').attr('value', this[0]).text(this[1]));
            }
        });

    });
    $('#api_show').click(function (){
        $('#ex_analytics').hide(500);
        $('#en_analytics').hide(500);
        $('#rx_analytics').hide(500);
        $('#api').show(500);
    });
    $("#api_onetime_go").click(function(){
        var start = new Date();
        epoch = new Date($('#api_onetime_time1').val()).getTime()/1000.0;
        $("#output").empty();
        $.get("/api/0.1/loop_detector/mto", {time1: epoch},function(result){
            result=JSON.parse(result);
            
            for (i=0; i<result.length; i++){
                var html = "<div class='api_onetime'>";
                for (var key in result[i]) {
                    var line = "<strong>" + key + ": </strong>" + result[i][key] + "\n";
                    //console.log(line);
                    html += "<p> " + line + "</p>";
                    console.log(i);
                }
                html += "</div>";
                $("#output").append('<li style="background-color:' + colors[i % 3] + ';"' + html + '</li>');

            }
            console.log(result);
            var end = new Date();
            var duration = (end-start)/1000;
            $("#result_title").empty();
            $("#result_title").html("<h3>Took <strong>"+duration+"</strong> seconds!!<br />Showing 10 results</h3>");
            $("#output").css("overflow", "");
            $("#result_show").show(500);
            //date_value_chart(JSON.parse(result));
            //$("#result_title").empty();
            //$("#result_title").html("<h3>Number of vechicles entering per day</h3>");
            //$("#result_show").show(500);
            //console.log("after show");
        });
    });
    $("#api_twotime_go").click(function(){
        var start = new Date();
        epoch1 = new Date($('#api_twotime_time1').val()).getTime()/1000.0;
        epoch2 = new Date($('#api_twotime_time2').val()).getTime()/1000.0;
        $("#output").empty();
        $.get("/api/0.1/loop_detector/mto", {time1: epoch1, time2: epoch2},function(result){
            result=JSON.parse(result);
            
            for (i=0; i<result.length; i++){
                var html = "<div class='api_twotime'>";
                for (var key in result[i]) {
                    var line = "<strong>" + key + ": </strong>" + result[i][key] + "\n";
                    //console.log(line);
                    html += "<p> " + line + "</p>";
                }
                html += "</div>";
                $("#output").append('<li style="background-color:' + colors[i % 3] + ';"' + html + '</li>');

            }
            var end = new Date();
            var duration = (end-start)/1000;
            $("#result_title").empty();
            $("#result_title").html("<h3>Took <strong>"+duration+"</strong> seconds!!<br />Showing 10 results</h3>");
            $("#result_show").show(500);

            //date_value_chart(JSON.parse(result));
            //$("#result_title").empty();
            //$("#result_title").html("<h3>Number of vechicles entering per day</h3>");
            //$("#result_show").show(500);
            //console.log("after show");
        });
    });
    $('#en_show').click(function (){
        $('#ex_analytics').hide(500);
        $('#api').hide(500);
        $('#rx_analytics').hide(500);
        $('#en_analytics').show(500);
    });
    $("#en_go").click(function(){
        var start = new Date();
        $.get("/entry_exit", {name: $('#en_select').find(":selected").text(),
                        frequency: $('#en_freq').find(":selected").text(),
                        time1: $('#en_date1').datepicker('getDate')/1000,
                        time2: $('#en_date2').datepicker('getDate')/1000
                        },function(result){
            multi_trend_date_chart(JSON.parse(result));
            
            
            var end = new Date();
            var duration = (end-start)/1000;
            $("#result_title").empty();
            $("#result_title").html("<h3>Took <strong>"+duration+"</strong> seconds!!<br />Number of vechicles entering per day</h3>");
            $("#result_show").show(500);
            console.log("after show");
        });
    });


    $('#ex_input').keyup(function () {
        var rxp = new RegExp($('#ex_input').val(), 'i');
        var optlist = $('#ex_select').empty();
        opts.each(function () {
            if (rxp.test(this[1])) {
                optlist.append($('<option/>').attr('value', this[0]).text(this[1]));
            }
        });

    });
    $('#ex_show').click(function (){
        $('#en_analytics').hide(500);
        $('#api').hide(500);
        $('#rx_analytics').hide(500);
        $('#ex_analytics').show(500);
    });
    $("#ex_go").click(function(){
        var start = new Date();
        $.get("/entry_exit", {name: $('#ex_select').find(":selected").text(),
                        frequency: $('#ex_freq').find(":selected").text(),
                        time1: $('#ex_date1').datepicker('getDate')/1000,
                        time2: $('#ex_date2').datepicker('getDate')/1000
                        },function(result){

            multi_trend_date_chart(JSON.parse(result));
            
            var end = new Date();
            var duration = (end-start)/1000;
            $("#result_title").empty();
            $("#result_title").html("<h3>Took <strong>"+duration+"</strong> seconds!!<br />Number of vechicles exiting per day</h3>");
            $("#result_show").show(500);
            console.log("after show");
        });
    });

    $('#rx_input').keyup(function () {
        var rxp = new RegExp($('#rx_input').val(), 'i');
        var optlist = $('#rx_select').empty();
        rx_opts.each(function () {
            if (rxp.test(this[1])) {
                optlist.append($('<option/>').attr('value', this[0]).text(this[1]));
            }
        });

    });
    $('#rx_show').click(function (){
        $('#en_analytics').hide(500);
	$('#ex_analytics').hide(500);
        $('#api').hide(500);
        $('#rx_analytics').show(500);
    });
    $("#rx_go").click(function(){
        var start = new Date();
	var contractID = document.getElementById('rx_input').value;
	console.log("value is " + contractID);
        $.get("/genmissing", {name: $('#rx_select').find(":selected").text(),
			      //name: contractID
                        frequency: $('#rx_freq').find(":selected").text(),
                        time1: $('#rx_date1').datetimepicker('getDate')/1000,
                        time2: $('#rx_date2').datetimepicker('getDate')/1000
                        },function(result){

            console.log(result);
	    resultS = JSON.parse(result);
	    
            if(typeof resultS.error != 'undefined'){
		console.log("have error");
		console.log(resultS.error);
		console.log(resultS.message);
                $("#result_title").empty();
	        $("#result_title").html("<h3>" + resultS.message + "</h3>");
		$("#result_show").show(500);
                $("#output").hide(500);
	    }else{

            genmissing_chart(resultS);
            var end = new Date();
            var duration = (end-start)/1000;
            $("#result_title").empty();
            $("#result_title").html("<h3>Took <strong>"+duration+"</strong> seconds!!<br />Number of vechicles exiting per day</h3>");
            $("#result_show").show(500);
            console.log("after show");
            $("#output").show(500);
	   }
        });
    });
});


function multi_trend_date_chart(result){
    var chart = AmCharts.makeChart("output", {
        "type": "serial",
        "theme": "light",
        "legend": {
            "useGraphSettings": true
        },
        "dataProvider": result,
        "valueAxes": [{
            "id":"v1",
            "axisColor": "#3A539B",
            "axisThickness": 2,
            "gridAlpha": 0,
            "axisAlpha": 1,
            "position": "left"
        }],
        "graphs": [{
            "valueAxis": "v1",
            "lineColor": "#FF6600",
            "bullet": "round",
            "bulletBorderThickness": 1,
            "hideBulletsCount": 30,
            "title": "Volume Before",
            "valueField": "before",
            "fillAlphas": 0
        }, {
            "valueAxis": "v2",
            "lineColor": "#FCD202",
            "bullet": "square",
            "bulletBorderThickness": 1,
            "hideBulletsCount": 30,
            "title": "Volume After",
            "valueField": "after",
            "fillAlphas": 0
        }, {
            "valueAxis": "v3",
            "lineColor": "#B0DE09",
            "bullet": "triangleUp",
            "bulletBorderThickness": 1,
            "hideBulletsCount": 30,
            "title": "Volume Difference",
            "valueField": "difference",
            "fillAlphas": 0
        }],
        "chartScrollbar": {},
        "chartCursor": {
            "categoryBalloonDateFormat":"MMM DD JJ:NN",
            "cursorPosition": "mouse"
        },
        "categoryField": "date",
        "categoryAxis": {
            "parseDates": true,
            "axisColor": "#DADADA",
            "minPeriod":"hh",
            "minorGridEnabled": true
        },
        "export": {
            "enabled": true,
            "position": "bottom-right"
         }
    });
};

function genmissing_chart(result){
    var chart = AmCharts.makeChart("output", {
        "type": "serial",
        "theme": "light",
        "legend": {
            "useGraphSettings": true
        },
        "marginRight": 80,
        "dataProvider": result,
        "valueAxes": [{
            "axisAlpha": 0.1
        }],
        "categoryAxis": {
            "parseDates": true,
            "axisColor": "#DADADA",
            "minorGridEnabled": true
        },
        "graphs": [{
            "balloonText": "[[value]]",
            "lineThickness": 2,
            "bullet": "round",
            "title": "Volume Before",
            "valueField": "before"
        },
        {
            "balloonText": "[[value]]",
            "lineThickness": 2,
            "bullet": "square",
            "title": "Volume After",
            "valueField": "after"
        },
        {
            "balloonText": "[[value]]",
            "lineThickness": 2,
            "bullet": "triangleUp",
            "title": "Volume Difference",
            "valueField": "difference"
        }],
        "zoomOutButtonRollOverAlpha": 0.15,
        "chartCursor": {
            "categoryBalloonDateFormat": "MMM DD JJ:NN",
            "cursorPosition": "mouse",
            "showNextAvailable": true
        },
        "autoMarginOffset": 5,
        "chartScrollbar": {},
        "columnWidth": 1,
        "categoryField": "date",
        "categoryAxis": {
            "minPeriod": "ss",
            "parseDates": true
        },
        "export": {
            "enabled": true
        }
    });
};   

function multi_trend_hourly_chart(result){
    var chart = AmCharts.makeChart("output", {
        "type": "serial",
        "theme": "light",
        "legend": {
            "useGraphSettings": true
        },
        "marginRight": 80,
        "dataProvider": result,
        "valueAxes": [{
            "axisAlpha": 0.1
        }],
        "categoryAxis": {
            "parseDates": true,
            "axisColor": "#DADADA",
            "minorGridEnabled": true
        },
        "graphs": [{
            "balloonText": "[[value]]",
            "lineThickness": 2,
            "bullet": "round",
            "title": "Volume Before",
            "valueField": "before"
        },
        {
            "balloonText": "[[value]]",
            "lineThickness": 2,
            "bullet": "square",
            "title": "Volume After",
            "valueField": "after"
        },
        {
            "balloonText": "[[value]]",
            "lineThickness": 2,
            "bullet": "triangleUp",
            "title": "Volume Difference",
            "valueField": "difference"
        }],
        "zoomOutButtonRollOverAlpha": 0.15,
        "chartCursor": {
            "categoryBalloonDateFormat": "MMM DD JJ:NN",
            "cursorPosition": "mouse",
            "showNextAvailable": true
        },
        "autoMarginOffset": 5,
        "chartScrollbar": {},
        "columnWidth": 1,
        "categoryField": "date",
        "categoryAxis": {
            "minPeriod": "hh",
            "parseDates": true
        },
        "export": {
            "enabled": true
        }
    });
};   
