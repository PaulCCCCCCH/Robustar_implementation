$(function(e) {
	'use strict'

	/*-----Barchart-----*/
	var chartdata = [{
		name: 'New Visitors',
		type: 'bar',
		data: [10, 15, 9, 18, 10, 15, 7, 14],
		symbolSize: 10,
		itemStyle: {
			normal: {
				barBorderRadius: [0, 0, 0, 0],
				color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
					offset: 0,
					color: '#1cc5ef'
				}, {
					offset: 1,
					color: '#1cc5ef'
				}])
			}
		},
	}, {
		name: 'Return Visitors',
		type: 'bar',
		data: [10, 14, 10, 15, 9, 25, 15, 18],
		symbolSize: 10,
		itemStyle: {
			normal: {
				barBorderRadius: [0, 0, 0, 0],
				color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
					offset: 0,
					color: '#24e4ac'
				}, {
					offset: 1,
					color: '#24e4ac'
				}])
			}
		},
	}];
	var chart = document.getElementById('echart');
	var barChart = echarts.init(chart);
	var option = {
		grid: {
			top: '6',
			right: '0',
			bottom: '17',
			left: '25',
		},
		xAxis: {
			data: ['2014', '2015', '2016', '2017', '2018', '2019'],
			axisLine: {
				lineStyle: {
					color: 'rgba(112, 131, 171, .1)'
				}
			},
			axisLabel: {
				fontSize: 10,
				color: '#77778e'
			}
		},
		tooltip: {
			show: true,
			showContent: true,
			alwaysShowContent: true,
			triggerOn: 'mousemove',
			trigger: 'axis',
			axisPointer: {
				label: {
					show: false,
				}
			}
		},
		yAxis: {
			splitLine: {
				lineStyle: {
					color: 'rgba(112, 131, 171, .1)'
				}
			},
			axisLine: {
				lineStyle: {
					color: 'rgba(119, 119, 142, 0.2)'
				}
			},
			axisLabel: {
				fontSize: 10,
				color: '#77778e'
			}
		},
		series: chartdata,
		color: ['#1cc5ef', '#24e4ac']
	};
	barChart.setOption(option);
	/*-----AreaChart Echart-----*/
	
	/*-----canvasDoughnut-----*/
	if ($('#canvasDoughnut').length) {
		var ctx = document.getElementById("canvasDoughnut").getContext("2d");
		new Chart(ctx, {
			type: 'doughnut',
			data: {
				labels: ['Organic', 'Direct', 'Campagion',],
				datasets: [{
					data: [56, 20, 30],
					backgroundColor: ['#ec5444', '#1cc5ef', '#24e4ac'],
					borderColor:'transparent',
				}]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				legend: {
					display: false
				},
				cutoutPercentage: 75,
			}
		});
	}
	/*-----canvasDoughnut-----*/
	
});


