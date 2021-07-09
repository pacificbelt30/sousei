/*
 * https://ryotah.hatenablog.com/entry/2017/03/22/211227 より拝借
onclick="download(arrToCSV(join_head_body()),'{{kamoku}}.csv')"
 */
function arrToCSV(arr) {
  return arr
  .map(row => row.map(str => '"' + (str ? str.replace(/"/g, '""') : '') + '"')
  )
  .map(row => row.join(','))
  .join('\n');
}

function download(data, name) {
  const anchor = document.createElement('a');
  if (window.URL && anchor.download !== undefined) {
    // utf8
    const bom = '\uFEFF';
    const blob = new Blob([bom, data], { type: 'text/csv' });
    anchor.download = name;

    // window.URL.createObjectURLを利用
    // https://developer.mozilla.org/ja/docs/Web/API/URL/createObjectURL
    anchor.href = window.URL.createObjectURL(blob);

    // これでも可
    // anchor.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(bom + data);

    // firefoxでは一度addしないと動かない
    document.body.appendChild(anchor);
    anchor.click();
    anchor.parentNode.removeChild(anchor);
  }
}

function join_head_body(arr){
  //let arr = syusseki_list;
  tmp = arr;
  tmp.unshift(table_header);
  console.log(tmp);
  return tmp;
}
