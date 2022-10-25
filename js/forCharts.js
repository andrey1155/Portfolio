var pCanvas = document.getElementById('pitchChart');
var yCanvas = document.getElementById('yawChart');

var hCanvas = document.getElementById('heightChart');
var sCanvas = document.getElementById('speedChart');

var ch1Canvas = document.getElementById('ch1Chart');
var ch2Canvas = document.getElementById('ch2Chart');

const resetZoom = {
  id: 'resetZoom',
  beforeDraw: (chart, args, options) => {
      const {ctx, chartArea: {top, bottom, left, right, width, height}} = chart;
      ctx.save();

      const text = "Reset zoom";
      const textWidth = ctx.measureText(text).width;

      ctx.textAlign = 'left';
      ctx.fillText(text,textWidth,10);
      console.log('a');
      //chart.resetZoom();
  }
}


const settings = {
  elements: {
    point:{
        radius: 0
    },
    line:{
      borderWidth: 1,
    }
},
   plugins: {
     zoom: {
       zoom: {
         wheel: {
           enabled: true,
         },
         pinch: {
           enabled: true
         },
         mode: 'xy',
         drag: {
           enabled: true
         }
       }
     },
    
     resetZoom: resetZoom

   }
 }

var pitchChart
var yawChart

var speedChart
var heightChart

var ch1Chart
var ch2Chart

ChartSetup()
function ChartSetup(){

    var xmlhttp = new XMLHttpRequest();
    var url = "/data";
    
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var data = JSON.parse(this.responseText);
            //console.log(data.t);
            console.log(data);
            SetupPitch(data)
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    function SetupPitch(Data){
        pitchChart = new Chart(pCanvas, {
            type: 'line',
            data: {
               labels: Data.T_arr,
               datasets: [{
                   label: 'Pitch',
                   data: Data.Pitch_arr,
                   borderColor: 'rgb(255,0,0)'
               },{
                label: 'Attack angle',
                data: Data.A_arr,
                borderColor: 'rgb(0,255,0)'
            },{
              label: 'Path angle',
              data: Data.Theta_arr,
              borderColor: 'rgb(0,0,255)'
          }]
            },
            options: settings          
           })

           yawChart = new Chart(yCanvas, {
            type: 'line',
            data: {
               labels: Data.T_arr,
               datasets: [{
                   label: 'Yaw',
                   data: Data.Yaw_arr
                   ,
                   borderColor: 'rgb(255,0,0)'
               },{
                label: 'Heading',
                data: Data.Heading_arr
                ,
                borderColor: 'rgb(0,255,0)'
            },{
              label: 'Drift angle',
              data: Data.B_arr,
              borderColor: 'rgb(0,0,255)'
          },{
            label: 'Roll',
            data: Data.Roll_arr,
            borderColor: 'rgb(0,255,255)'
        }]
            },
            options: settings          
           })

           heightChart = new Chart(hCanvas, {
            type: 'line',
            data: {
               labels: Data.T_arr,
               datasets: [{
                   label: 'Height',
                   data: Data.H_arr
                   ,
                   borderColor: 'rgb(255,0,0)'
               }]
            },
            options: settings          
           })

           speedChart = new Chart(sCanvas, {
            type: 'line',
            data: {
               labels: Data.T_arr,
               datasets: [{
                   label: 'Speed',
                   data: Data.Speed_arr
                   ,
                   borderColor: 'rgb(255,0,0)'
               }]
            },
            options: settings          
           })
    }

}



function resetAllZoom(){

  //pitchChart.chart.options.scales.xAxes[0].ticks.min   = null;
  //pitchChart.chart.options.scales.xAxes[0].ticks.max   = null;
  pitchChart.resetZoom();
  yawChart.resetZoom();
  heightChart.resetZoom();
  steamChart.resetZoom();

  pitchChart.update();
  yawChart.update();
  heightChart.update();
  steamChart.update();
}
