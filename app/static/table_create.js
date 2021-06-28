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
  for(i=0;i<risyu_list.length;i++){
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
  for(i=0;i<tmplist.length;i++){
      for(j=0;j<syusseki_list.length;j++){
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
  tbody = table.createTBody();
  for(i=0;i<syusseki_list.length;i++){
      rows.push(tbody.insertRow(-1));
      for(j=0;j<syusseki_list[i].length;j++){
          cell = rows[i].insertCell(-1);
          cell.appendChild(document.createTextNode(syusseki_list[i][j]));
      }
  }
}

//window.onload = table_create;
