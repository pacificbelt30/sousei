/*
onclick="graph_download('{{kamoku}}.png')"
<canvas id="myChart" height=500 width=800></canvas>
 * */
let filter_times = []; // 未実装のフィルタ機能に用いる
let filter_stu = []; // 未実装のフィルタ機能に用いる
let times = [];
let attend = []; // 出席者数
let late = []; // 遅刻者数
let absent = []; // 欠席者数
console.log('DEBUG');


function val_reset_tate(){
  times = [];
  attend = [];
  late = [];
  absent = [];
  filter_times = lectured_list;
  for (i = 0, k = 0, m = 0; i < 15; i++){ 
      if (i == filter_times[k] - 1) { // 対応する生徒がフィルタに引っかかってないか
          times.push(i + 1); // 存在する授業日のラベルを追加
          attend.push(0); // 出席者の配列に0を追加（インクリメントするため）
          late.push(0); // 遅刻者の配列に0を追加
          absent.push(0); // 欠席者の配列に0を追加
          
          for (j = 0, l = 0; j < syusseki_list.push(); j++) {
              if (j != filter_stu[j] - 1){ // 対応する授業日がフィルタに引っかかってないか
                  if (syusseki_list[j][i + 2] == '出席') {
                      attend[m]++;
                  } else if (syusseki_list[j][i + 2] == '遅刻') {
                      late[m]++;
                  } else { absent[m]++ }
              } else { l++; }
          }
          attend[m] = attend[m]/syusseki_list.length;
          late[m] = late[m]/syusseki_list.length;
          absent[m] = absent[m]/syusseki_list.length;
          m++;
      } else { k++; }
  }
}
/*
window.onload = async function () {
  const myCanvas = document.getElementById("myChart");
  new Chart(myCanvas, {
    type: "bar", // 横なら "horizontalBar" を指定
    data: {
      labels: times,
      datasets: [
        {
          label: "出席",
          data: attend,
          backgroundColor: "#F6AD3C",
        },
        {
          label: "遅刻",
          data: late,
          backgroundColor: "#A64A97",
        },
        {
          label: "欠席",
          data: absent,
          backgroundColor: "#AACF52",
        },
      ]
    },
    options: {
      // 凡例
      legend: {
        position: 'right'
      },
      responsive: false,
      scales: {
        // X軸
        xAxes: [{
        scaleLabel: {
            display: true,
            fontColor: "#999",
            labelString: "授業回数"
          },
          stacked: true
        }],
        // Y軸
        yAxes: [{
        scaleLabel: {
            display: true,
            fontColor: "#999",
            labelString: "人数"
          },
          stacked: true
        }]
      }
    }
  });
  const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  await _sleep(2000);
    let link = document.createElement("a");
    link.href = myCanvas.toDataURL("image/png");
    link.download = "test.png";
    link.click();
}
*/

function val_reset(){
  times = []
  attend = []
  late = []
  absent = []
  for (i = 0, k = 0, m = 0; i < syusseki_list.length; i++){ 
      if (i != filter_stu[k] - 1){ // 対応する授業日がフィルタに引っかかってないか
          times.push(syusseki_list[i][1]); // 存在する授業日のラベルを追加
          attend.push(0); // 出席者の配列に0を追加（インクリメントするため）
          late.push(0); // 遅刻者の配列に0を追加
          absent.push(0); // 欠席者の配列に0を追加
          
          for (j = 0, l = 0; j < syusseki_list[0].length-2; j++) {
              if (j != filter_times[j] - 1) { // 対応する生徒がフィルタに引っかかってないか
                  if (syusseki_list[i][j + 2] == '出席') {
                      attend[m]++;
                  } else if (syusseki_list[i][j + 2] == '遅刻') {
                      late[m]++;
                  } else { absent[m]++ }
              } else { l++; }
          }
          attend[m] = attend[m]/syusseki_list.length;
          late[m] = late[m]/syusseki_list.length;
          absent[m] = absent[m]/syusseki_list.length;
          m++;
      } else { k++; }
  }
}
function draw_graph() {
  const myCanvas = document.getElementById("myChart");
    val_reset_tate();
    //if(mychart){
        //mychart.destroy();
    //}

  window.mychart = new Chart(myCanvas, {
    //type: "horizontalBar", // 横なら "horizontalBar" を指定
    type: "bar", // 横なら "horizontalBar" を指定
    data: {
      labels: times,
      datasets: [
        {
          label: "出席",
          data: attend,
          backgroundColor: "#F6AD3C",
        },
        {
          label: "遅刻",
          data: late,
          backgroundColor: "#A64A97",
        },
        {
          label: "欠席",
          data: absent,
          backgroundColor: "#AACF52",
        },
      ]
    },
    options: {
      //indexAxis:'y',
      // 凡例
      legend: {
        position: 'right'
      },
      //responsive: true,
      responsive: false,
      scales: {
        // X軸
        x: {
            title:{
                display: true,
                fontColor: "#999",
                text: "授業回数",
            },
            stacked: true,
        },
        y: {
            title:{
                display: true,
                fontColor: "#999",
                text:"出席率",
            },
            stacked: true,
        },
      }
    }
  });
  //const _sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  //await _sleep(2000);
}

function graph_download(filename){
    let myCanvas = document.getElementById("myChart");
    let link = document.createElement("a");
    link.href = myCanvas.toDataURL("image/png");
    link.download = filename;
    link.click();
}

window.onload = draw_graph;
