$(function(e) {
	'use strict';

	/*-----Chart-----*/
	var options = {
		chart: {
			height: 380,
			type: 'bar',
		},
		plotOptions: {
			bar: {
				horizontal: true,
				dataLabels: {
				position: 'top',
			},
		}
		},
		dataLabels: {
			enabled: true,
			offsetX: -56,
			style: {
				fontSize: '12px',
				colors: ['#fff']
			}
		},
		series: [{
			data: [123, 255, 141, 364, 422, 143, 321, 444, 255, 141, 264, 122, 243, 211]
		}],
		xaxis: {
			categories: ['January', 'February', 'March', 'April ', 'May',  'June', 'July', 'August', 'September', 'October', 'November', 'December'],
		},
		fill: {
          type: 'gradient',
          gradient: {
            shade: 'dark',
            gradientToColors: ['#525ce5', '#765be6'],
            shadeIntensity: 5,
			inverseColors: true,
            type: 'horizontal',
            opacityFrom: .9,
            opacityTo: .9,
          },
        },
		grid: {
			borderColor: 'rgba(112, 131, 171, .1)',
			xaxis: {
				lines: {
					show: true,
					borderColor: 'rgba(112, 131, 171, .1)',
				}
			},
			yaxis: {
				lines: {
					show: false,
				}
			},
			padding: {
			  top: 0,
			  right: 0,
			  bottom: 0,
			  left: 10
			},
		},
	}
	var chart = new ApexCharts(
		document.querySelector("#learners"),
		options
	);
	chart.render();
	/*---- Chart8----*/

	/*---- morrisBar8----*/
	new Morris.Donut({
		element: 'morrisBar8',
		data: [{
			value: 23,
			label: 'Completed'
		}, {
			value: 16,
			label: 'In Progress'
		},  {
			value: 15,
			label: 'Not Completed'
		}, {
			value: 5,
			label: 'Not Started'
		}],
		backgroundColor: 'transparent',
		labelColor: '#2f4c7d',
		colors: ['#1cc5ef', "#6044ec", '#24e4ac', "#ec447c"],
		formatter: function(x) {
			return x + "%"
		}
	}).on('click', function(i, row) {
		console.log(i, row);
	});

});





