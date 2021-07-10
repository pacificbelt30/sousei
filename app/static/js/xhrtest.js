const xhr = new XMLHttpRequest();

// リクエスト
xhr.open("GET", 'http://localhost/test');

//リクエスト送信
xhr.send();

// 自動的に呼ばれる関数
xhr.onreadystatechange = () =>{
  // readyState XMLHttpRequest の状態 4: リクエストが終了して準備が完了
  // status httpステータス
  if (xhr.readyState == 4 && xhr.status == 200) {
    // jsonをオブジェクトに変更
    const jsonObj = JSON.parse(xhr.responseText);      

    console.log(jsonObj);

  }  
}
