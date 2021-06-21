/*
 * 文字列をハッシュ化するためのjs
 * digestMessage()の引数として文字列を入力するとハッシュ化した文字列を返す．
 * 非同期関数なのでexampleのようにして使われたし
 */

/*
 "SHA-1" (but don't use this in cryptographic applications)
 "SHA-256"
 "SHA-384"
 "SHA-512"
*/
const algo = "SHA-256";

// input data:
const str = "この文字列をハッシュ化します";

async function digestMessage(message) {
  const msgUint8 = new TextEncoder().encode(message);                           // encode as (utf-8) Uint8Array
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);           // hash the message
  const hashArray = Array.from(new Uint8Array(hashBuffer));                     // convert buffer to byte array
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // convert bytes to hex string
  return hashHex;
}

// example
(async() =>{
  const digestHex = await digestMessage(str);
  console.log(digestHex);
})();

