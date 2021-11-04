var barChartType=1;
var currentChartData=[]
function refershChartData(imgURL){
    var client = new HttpClient();
    client.get(imgURL, function(result) {

        currentChartData=[]
        result=result.split("_")
        console.log("model output:",result)
        for(var i=0;i<result.length;i++){
            currentChartData.push(parseFloat(result[i]))
        }
        drawBarChart()
        updateInterpretation()
        
        // setTimeout(document.querySelector(".show-img-v").setAttribute("src","/imgv/"+Math.random()),100);
    });
}
var myChart=undefined
function drawBarChart(){
    if(myChart!=undefined){
        myChart.data.datasets[0]['data']=currentChartData
        myChart.update()
        return
    }
    var ctx = document.getElementById('bar-chart').getContext('2d');
    myChart = new Chart(ctx, {
        type: barChartType==1?'horizontalBar':'bar',
        data: {
            //labels: ['Plane', 'Cat', 'Bird', 'Cat', 'Deer', 'Dog',"Frog","Horse","Ship","Truck"],
            labels:['bird','cat','crab','dog','fish','frog','insect','primate','turtle'],
            datasets: [{
                label: 'probability',
                data: currentChartData,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}