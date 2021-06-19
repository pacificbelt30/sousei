/*
 * https://ryotah.hatenablog.com/entry/2017/03/22/211227 より拝借
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

function join_head_body(){
  let arr = syusseki_list;
  arr.unshift(table_header);
  console.log(arr);
  return arr;
}
