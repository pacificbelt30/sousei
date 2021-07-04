/* このコードをhtmlのscriptタグ内に記述
//テーブルのヘッダ部分の配列
table_header = {{table_header|safe}}
// 出席データ
syusseki_list = [];
// 履修データ
risyu_list = {{risyu_list|safe}};
// 出席データ（データベースに保存されてたそのままの状態）
tmplist = {{syusseki_data|safe}};
*/
// risyu_listをもとに 17x履修者分 のsyusseki_listの二次元配列を作成する
// table_idには表のidを文字列で入れる
let table_id = 'attend'
function table_create(){
  syusseki_list = [];
  for(let i=0;i<risyu_list.length;i++){
      syusseki_list.push([]);
      syusseki_list[i].push(risyu_list[i]['number']);
      syusseki_list[i].push(risyu_list[i]['name']);
      for(j=0;j<17;j++){
          syusseki_list[i].push('');
      }
  }
  
  let table = document.getElementById(table_id)
  let rows=[];
  // tmplistのデータをsyusseki_listに格納する．
  for(let i=0;i<tmplist.length;i++){
      for(let j=0;j<syusseki_list.length;j++){
          if(tmplist[i][0]==syusseki_list[j][1]){
              syusseki_list[j][tmplist[i][2]+1] = tmplist[i][1];
              break;
          }
      }
  }
  
  /*
  for(i=0;i<50;i++)
  {
      let table = document.getElementById('targetTable');
      let newRow = table.insertRow();
          
      let newCell = newRow.insertCell();
      let newText = document.createTextNode('B21P010');
      newCell.appendChild(newText);
          
      newCell = newRow.insertCell();
      newText = document.createTextNode('工藤');
      newCell.appendChild(newText);
  
      for(j=0;j<17;j++)
      {
          newCell = newRow.insertCell();
          newText = document.createTextNode('💀');
          newCell.appendChild(newText);
      }
  }
      */
  // 表のbody本体の描画
  let tbody = table.createTBody();
  for(let i=0;i<syusseki_list.length;i++){
      rows.push(tbody.insertRow(-1));
      for(j=0;j<syusseki_list[i].length;j++){
          cell = rows[i].insertCell(-1);
          cell.appendChild(document.createTextNode(syusseki_list[i][j]));
      }
  }
  // 出席回数と遅刻回数の描画
  for(let i=0;i<syusseki_list.length;i++){
    let table_body = document.getElementById('attend').tBodies;
    console.log(i,syusseki_list.length);
    table_body[0].rows[i].cells[17].innerHTML = count_attend(syusseki_list[i]);
    table_body[0].rows[i].cells[18].innerHTML = count_late(syusseki_list[i]);
  }
}

let attend_char = '出席';
let late_char = '遅刻';
let kesseki_char = '欠席';
//一人分出欠リストを引数としての出席回数を返す
function count_attend(syukketu_array){
  let count = 0;
  for(let j=2;j<syukketu_array.length;j++){
    if(syukketu_array[j] == attend_char){
      count++;
    }
  }
  return count;
}

function count_late(syukketu_array){
  let count = 0;
  for(let j=2;j<syukketu_array.length;j++){
    if(syukketu_array[j] == late_char){
      count++;
    }
  }
  return count;
}

//window.onload = table_create;
