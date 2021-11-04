$(function(e) {

	/*widget1 */
	var ctx = document.getElementById("widget1");
	var myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"],
			type: 'line',
			datasets: [{
				label: "Total Active Users",
				data: [45, 55, 32, 67, 49, 72, 52],
				backgroundColor: 'rgba(68, 124, 236,0.6)',
				borderColor: '#525ce5',
				borderWidth: 0,
				pointStyle: 'circle',
				pointRadius: 0,
				pointBorderColor: 'transparent',
				pointBackgroundColor: '#525ce5',
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			tooltips: {
				mode: 'index',
				titleFontSize: 12,
				titleFontColor: 'rgba(0,0,0,0.9)',
				bodyFontColor: 'rgba(0,0,0,0.9)',
				backgroundColor: '#fff',
				bodyFontFamily: 'Montserrat',
				cornerRadius: 0,
				intersect: false,
			},
			legend: {
				display: false,
				labels: {
					usePointStyle: true,
					fontFamily: 'Montserrat',
				},
			},
			scales: {
				xAxes: [{
					display: false,
					gridLines: {
						color: 'rgba(112, 131, 171, .1)'
					},
					scaleLabel: {
						display: false,
						labelString: '',
						fontColor: '#77778e'
					}
				}],
				yAxes: [{
					display: false,
					gridLines: {
						display: false,
						drawBorder: true
					},
					scaleLabel: {
						display: false,
						labelString: 'Customer retention in %',
						fontColor: '#77778e'
					}
				}]
			},
			title: {
				display: false,
				text: 'Normal Legend'
			}
		}
	});
	/*widget1*/


	/*widget2 */
	var ctx = document.getElementById("widget2");
	var myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["Mon", "Tues", "Wed", "Thur", "Fri", "Sat", "Sun"],
			type: 'line',
			datasets: [{
				label: "Total Uninstalled",
				data: [45, 55, 42, 67, 49, 62, 52],
				backgroundColor: 'rgba(89, 200, 227,0.6)',
				borderColor: '#1cc5ef',
				borderWidth: 0,
				pointStyle: 'circle',
				pointRadius: 0,
				pointBorderColor: 'transparent',
				pointBackgroundColor: '#1cc5ef',
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			tooltips: {
				mode: 'index',
				titleFontSize: 12,
				titleFontColor: 'rgba(0,0,0,0.9)',
				bodyFontColor: 'rgba(0,0,0,0.9)',
				backgroundColor: '#fff',
				bodyFontFamily: 'Montserrat',
				cornerRadius: 0,
				intersect: false,
			},
			legend: {
				display: false,
				labels: {
					usePointStyle: true,
					fontFamily: 'Montserrat',
				},
			},
			scales: {
				xAxes: [{
					display: false,
					gridLines: {
						color: 'rgba(112, 131, 171, .2)'
					},
					scaleLabel: {
						display: false,
						labelString: '',
						fontColor: 'rgba(0,0,0,0.61)'
					}
				}],
				yAxes: [{
					display: false,
					gridLines: {
						display: false,
						drawBorder: true
					},
					scaleLabel: {
						display: false,
						labelString: 'Customer retention in %',
						fontColor: 'rgba(0,0,0,0.61)'
					}
				}]
			},
			title: {
				display: false,
				text: 'Normal Legend'
			}
		}
	});
	/*widget2*/

	/* Chartjs (#leads) */
	var myCanvas = document.getElementById("devices");
	myCanvas.height = 330;
	var myCanvasContext = myCanvas.getContext("2d");
	var gradientStroke1 = myCanvasContext.createLinearGradient(0, 0, 0, 500);
	gradientStroke1.addColorStop(0, 'rgba(68, 124, 236,0.8)');

	var gradientStroke2 = myCanvasContext.createLinearGradient(0, 0, 0, 390);
	gradientStroke2.addColorStop(0, 'rgba(28, 197, 239,0.8)');

	var gradientStroke3 = myCanvasContext.createLinearGradient(0, 0, 0, 390);
	gradientStroke3.addColorStop(0, 'rgba(36, 228, 172,0.8)');

    var myChart = new Chart( myCanvas, {
		type: 'bar',
		data: {
			labels: ["Jan", "Feb", "Mar", "Apr", "May", "June" , "July"],
			datasets: [{
				label: 'Android',
				data: [3, 3, 7, 4, 6, 3, 5, 3, 5, 3,4,14],
				backgroundColor: gradientStroke1,
				borderWidth: 1,
				hoverBackgroundColor: gradientStroke1,
				hoverBorderWidth: 0,
				borderColor: gradientStroke1,
				hoverBorderColor: 'gradientStroke1',
				lineTension: .3,
				pointBorderWidth: 0,
				pointHoverRadius: 4,
				pointHoverBorderColor: "gradientStroke1",
				pointHoverBorderWidth: 0,
				pointRadius: 0,
				pointHitRadius: 0,
			}, {

			    label: 'Windows',
				data: [7, 6, 10, 6, 8, 10, 9, 5, 10, 4],
				backgroundColor: gradientStroke2,
				borderWidth: 1,
				hoverBackgroundColor: gradientStroke2,
				hoverBorderWidth: 0,
				borderColor: gradientStroke2,
				hoverBorderColor: 'gradientStroke2',
				lineTension: .3,
				pointBorderWidth: 0,
				pointHoverRadius: 4,
				pointHoverBorderColor: "gradientStroke2",
				pointHoverBorderWidth: 0,
				pointRadius: 0,
				pointHitRadius: 0,
			},
			{

			    label: 'Mac',
				data: [12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
				backgroundColor: gradientStroke3,
				borderWidth: 1,
				hoverBackgroundColor: gradientStroke3,
				hoverBorderWidth: 0,
				borderColor: gradientStroke3,
				hoverBorderColor: 'gradientStroke3',
				lineTension: .3,
				pointBorderWidth: 0,
				pointHoverRadius: 4,
				pointHoverBorderColor: "gradientStroke3",
				pointHoverBorderWidth: 0,
				pointRadius: 0,
				pointHitRadius: 0,
			}
		  ]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			layout: {
				padding: {
					left: 0,
					right: 0,
					top: 0,
					bottom: 0
				}
			},
			scales: {
				yAxes: [{
					display: true,
					gridLines: {
						display: true,
						color: "rgba(112, 131, 171, .1)",
					},
					ticks: {
						beginAtZero: false,
						fontColor: "#77778e"
					},
				}],
				xAxes: [{
                    barPercentage: 0.2,
					barValueSpacing :3,
					barDatasetSpacing : 3,
					stacked: true,
					ticks: {
						beginAtZero: true,
						fontColor: "#77778e"
					},
					gridLines: {
						color: "rgba(112, 131, 171, .1)",
						display: true
					},

				}]
			},
			legend: {
				display: true,
			},
			elements: {
				point: {
					radius: 0
				}
			}
		}
	});
	/* Chartjs (#leads) closed */


	/* Chartjs (#total-coversations) */
	var ctx = document.getElementById('total-Installed').getContext('2d');
	ctx.height = 350;
	var gradientStroke = myCanvasContext.createLinearGradient(0, 0, 0, 300);
	gradientStroke.addColorStop(0, '#525ce5');
	gradientStroke.addColorStop(1, '#525ce5');
    var myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
			datasets: [{
				label: "Total-Uninstalled",
				borderColor: gradientStroke,
				borderWidth: 4,
				backgroundColor: 'transparent',
				data: [0, 50, 0, 100, 50, 130, 100, 140]
			}]
		},
        options: {

            maintainAspectRatio: false,
            legend: {
                display: false
            },
            responsive: true,
            tooltips: {
                mode: 'index',
                titleFontSize: 12,
                titleFontColor: '#000',
                bodyFontColor: '#000',
                backgroundColor: '#fff',
                cornerRadius: 0,
                intersect: false,
            },
            scales: {
                xAxes: [ {
                    gridLines: {
                        color: 'transparent',
                        zeroLineColor: 'transparent'
                    },
                    ticks: {
                        fontSize: 2,
                        fontColor: 'transparent'
                    }
                } ],
                yAxes: [ {
                    display:false,
                    ticks: {
                        display: false,
                    }
                } ]
            },
            title: {
                display: false,
            },
            elements: {
                line: {
                    borderWidth: 6
                },
                point: {
                    radius: 0,
                    hitRadius: 10,
                    hoverRadius: 4
                }
            }
        }
    });
	/* Chartjs (#total-coversations) closed */

});


