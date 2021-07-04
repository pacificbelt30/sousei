// 要注意者を表示する関数
let attention_limit = 2
function create_attention_table(){
  let attend_table = document.getElementById('attend');
  let table = document.getElementById('attention');
  //var num = [[1, 1, 1, 1,1], [1,1, 1, 3, 4], [5,1, 3, 2, 2], [1,1, 2, 2, 3]];
  let num = syusseki_list;
  let lectured = lectured_list;
  //len_row = num.length;
  //len_str = num[0].length;
  let len_row = num.length;
  let len_str = lectured.length;
  
  var count = 0;
  
  var num_search = '';
  
  for(let i=0; i<len_row; i++){  
      count = 0;                          
      for(let j=0; j<len_str; j++){
          if (num_search == num[i][lectured[j]+1]){
              count = count+1;
          }else{
              ;
          }
      }
      // if の数字で何回から要注意者か設定する
      if(count>=attention_limit){
              attend_table.rows[i+2].cells[0].style.background = 'red'; // 要注意者のidのセルを赤くした
              let newRow = table.insertRow();
              let newCell = newRow.insertCell();
              let newText = document.createTextNode(num[i][1]);
              newCell.appendChild(newText);
      }
  }
}

function attention(){

}
