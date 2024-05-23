

// ?argument 0 indicates that no elements should be removed during the insertion;
indexDatesMissing.forEach(dateIndex => { 
  daysList.splice(dateIndex-1, 0, "Feriado");
 })

if (daysList.length !== 7) {
  daysList.unshift("Dia no laboral");
};
 




let isSaturday = 0;

function getDates(numb) {
  let currentDate = new Date()
  let currentDateToModify = new Date();
  var options = { weekday: "long", month: "short", day: "numeric" };
  let currentDateNumber = currentDateToModify.getDate();

  currentDateToModify.setDate(currentDateNumber - numb);

  
  //  if (currentDateToModify.getDay() === 0) {
  //    currentDateToModify.setDate(currentDateNumber - numb - 1);
  //  }
  //   console.log(currentDateToModify);

    // ? si la fecha modificada incluye sabado y issabado es mayor que 2 y la fecha corriente no es sabado
    if (currentDateToModify.toString().includes("Sat") || isSaturday >= 2 && !currentDate.toString().includes("Sat"))  {
      isSaturday += 1;
      if (isSaturday >= 2) {
        currentDateToModify.setDate(currentDateNumber - numb + 1);
      }
    }
  let formattedDate = currentDateToModify.toLocaleDateString("es-ES", options);

    return formattedDate;
  }





HORARIOS = [
      "07:00",
      "07:30",
      "08:00",
      "08:30",
      "09:00",
      "09:30",
      "10:00",
      "10:30",
      "11:00",
      "11:30",
      "12:00",
      "12:30",
      "13:00",
      "13:30",
      "14:00",
      "14:30",
      "15:00",
      "15:30",
      "16:00",
      "16:30",
      "17:00",
      "17:30",
      "18:00",
      "18:30",
      "19:00",
      "19:30",
      "20:00",
      "20:30",
      "21:00",
    ];

const allValuesLists = [];

// daysList.forEach(day => {
//   values_list = []
//   HORARIOS.forEach(horario => {
//         try {
//       let cantidadPersonas = llegadasData[day].time_counts[horario];
//       if (cantidadPersonas === undefined) {
//         values_list.push(0);
//       } else {
//         values_list.push(cantidadPersonas);
//       }
//     } catch (error) {
//       values_list.push(0); // Handle the error by pushing 0 to the list
//     }
//   });

//   allValuesLists.push(values_list);
// });


const ctx1 = document.getElementById('myChart1')
const ctx2 = document.getElementById("myChart2");
const ctx3 = document.getElementById('myChart3')
const ctx4 = document.getElementById('myChart4')
const ctx5 = document.getElementById('myChart5')

    const TITLESIZE = 20
    const LABELSIZE = 15

    const colorBackground = [
      "rgba(75, 192, 192, 0.2)",
      "rgba(255, 99, 132, 0.2)",
      "rgba(255, 205, 86, 0.2)",
      
      
      "rgba(54, 162, 235, 0.2)",
      "rgba(153, 102, 255, 0.2)",
      "rgba(255, 159, 64, 0.2)",

      "rgba(0, 128, 0, 0.2)",
      "rgba(0, 0, 128, 0.2)",
      "rgba(201, 203, 207, 0.2)",
      "rgba(128, 0, 128, 0.2)",
    ];

const colorBorder = [
  "rgb(75, 192, 192)",
  "rgb(255, 99, 132)",
  "rgb(255, 205, 86)",
  "rgb(54, 162, 235)",
  "rgb(153, 102, 255)",
  "rgb(255, 159, 64)",

  "rgb(0, 128, 0)",
  "rgb(0, 0, 128)",
  "rgb(201, 203, 207)",
  "rgb(128, 0, 128)",
];




  // const AsistenciaDia7 = allValuesLists[0]
  // const AsistenciaDia6 = allValuesLists[1]
  // const AsistenciaDia5 = allValuesLists[2]
  // const AsistenciaDia4 = allValuesLists[3]
  // const AsistenciaDia3 = allValuesLists[4]
  // const AsistenciaDia2 = allValuesLists[5]
  // const AsistenciaDia1 = allValuesLists[6]
  // const AsistenciaDia0 = allValuesLists[7]
  
const generoData = [sexoCount.M, sexoCount.F];
const membersData = [activeNonActiveMembers.True, activeNonActiveMembers.False];


// let configLineChartWeek = {
//   type: "line",
//   data: {
//     labels: HORARIOS,
//     datasets: [
//       {
//         label: getDates(6),
//         backgroundColor: colorBackground[0],
//         borderColor: colorBorder[0],
//         data: AsistenciaDia7,
//         fill: true,
//       },
//       {
//         label: getDates(5),
//         fill: true,
//         backgroundColor: colorBackground[1],
//         borderColor: colorBorder[1],
//         data: AsistenciaDia6,
//       },
//       {
//         label: getDates(4),
//         fill: true,
//         backgroundColor: colorBackground[2],
//         borderColor: colorBorder[2],
//         data: AsistenciaDia5,
//       },
//       {
//         label: getDates(3),
//         fill: true,
//         backgroundColor: colorBackground[3],
//         borderColor: colorBorder[3],
//         data: AsistenciaDia4,
//       },
//       {
//         label: getDates(2),
//         fill: true,
//         backgroundColor: colorBackground[4],
//         borderColor: colorBorder[4],
//         data: AsistenciaDia3,
//       },
//       {
//         label: getDates(1),
//         fill: true,
//         backgroundColor: colorBackground[5],
//         borderColor: colorBorder[5],
//         data: AsistenciaDia2,
//       },
//       {
//         label: "Hoy",
//         fill: true,
//         backgroundColor: colorBackground[6],
//         borderColor: colorBorder[6],
//         data: AsistenciaDia1,
//       },
//     ],
//   },
//   options: {
//     plugins: {
//       legend: {
//         position: "top",
//         labels: {
//           font: {
//             size: LABELSIZE,
//           },
//         },
//         onHover: function () {
//           ctx1.style.cursor = "pointer";
//         },
//         onLeave: function () {
//           ctx1.style.cursor = "default";
//         },
//       },
//       title: {
//         display: true,
//         text: "Asistencias por día en horarios",
//         font: {
//           size: TITLESIZE,
//         },
//       },
//     },

//     responsive: true,
//     tooltips: {
//       mode: "index",
//       intersect: false,
//     },
//     hover: {
//       mode: "nearest",
//       intersect: true,
//     },

//     scales: {
//       y: {
//         ticks: {
//           stepSize: 1, // Display only integer values
//         },
//       },
//     },
//   },
// };


let configBarChartCollectedMonth = {
  type: "bar",
  data: {
    labels: collectedMonthly.map(entry => entry.month),
    datasets: [
      {
        data: collectedMonthly.map(entry => entry.total_collected),
        backgroundColor: colorBackground,
        borderColor: colorBorder,
        borderWidth: 2,
      },
    ],
  },
  options: {
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "Recaudado Por Mes",
        font: {
          size: TITLESIZE,
        },
      },
    },

    responsive: true,
    tooltips: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: "nearest",
      intersect: true,
    },
    scales: {
      y: {
        ticks: {
          stepSize: 1, // Display only integer values
        },
      },
    },
  },
};

let configPieChartSex = {
    type: "pie",
    data: {
    labels: ['Masculino', 'Femenino',],
    datasets: [
      {
        data: generoData,
        backgroundColor: colorBackground,
        borderColor : colorBorder,
        borderWidth: 2,
      }
    ]
  },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: "top",
          labels: {
            font: {
              size: LABELSIZE,
            },
          },
        },
        title: {
          display: true,
          text: "Asistencia por género",
          font: {
            size: TITLESIZE,
          },
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              const label = configPieChartSex.data.labels[context.dataIndex];
              const value = generoData[context.dataIndex] || 0;
              const total = generoData.reduce((a, b) => a + b, 0);
              const percentage = ((value / total) * 100).toFixed(2);
              return `${label}: ${value} (${percentage}%)`;
            },
          },
        },
      },
    },
}
  

let a = collectedMonthly.map(entry => entry)
let configBarChartMonths = {
  type: "bar",
  data: {
    labels: usersPaidMonthly.map(entry => entry.month),
    datasets: [
      {
        data: usersPaidMonthly.map(entry => entry.user_count),
        backgroundColor: colorBackground,
        borderColor: colorBorder,
        borderWidth: 2,
      },
    ],
  },
  options: {
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "Cantidad De Personas Que Abonaron Por Mes",
        font: {
          size: TITLESIZE,
        },
      },
    },

    responsive: true,
    tooltips: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: "nearest",
      intersect: true,
    },
    scales: {
      y: {
        ticks: {
          stepSize: 1, // Display only integer values
        },
      },
    },
  },
};


let configBarPerDay = {
  type: "bar",
  data: {
    labels: daysList,
    datasets: [
      {
        data: daysList.map((day) => total_arrivals_per_day[day]),
        backgroundColor: colorBackground,
        borderColor: colorBorder,
        borderWidth: 2,
      },
    ],
  },
  options: {
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: "Asistencias por dia",
        font: {
          size: TITLESIZE,
        },
      },
    },

    responsive: true,
    tooltips: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: "nearest",
      intersect: true,
    },
    scales: {
      y: {
        ticks: {
          stepSize: 1, // Display only integer values
        },
      },
    },
  },
};

let configPieChartMembers = {
  type: "pie",
  data: {
    labels: ["Activos", "Con Cuota Vencida"],
    datasets: [
      {
        data: membersData,
        backgroundColor: ['rgba(0, 128, 0, 0.2)', 'rgba(255, 0, 0, 0.2)'], // Green background
        borderColor: ['rgba(0, 128, 0, 1)','rgba(255, 0, 0, 1)'], // Red border']
        borderWidth: 2,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        
        position: "top",
        labels: {
          font: {
            size: LABELSIZE,
          },
        },
      },
      title: {
        display: true,
        text: "Socios activos y no activos",
        font: {
          size: TITLESIZE,
        },
      },
      tooltip: {
        callbacks: {
          label: function (context) {
            const label = configPieChartMembers.data.labels[context.dataIndex];
            const value = membersData [context.dataIndex] || 0;
            const total = membersData .reduce((a, b) => a + b, 0);
            const percentage = ((value / total) * 100).toFixed(2);
            return `${label}: ${value} (${percentage}%)`;
          },
        },
      },
    },
  },
};

// new Chart(ctx1, configLineChartWeek)
new Chart(ctx1, configBarChartCollectedMonth)
new Chart(ctx2, configBarChartMonths)
new Chart(ctx3, configBarPerDay);
new Chart(ctx4, configPieChartSex);
new Chart(ctx5, configPieChartMembers);
