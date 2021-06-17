
/*
 "SHA-1" (but don't use this in cryptographic applications)
 "SHA-256"
 "SHA-384"
 "SHA-512"
*/
const algo = "SHA-256";

// input data:
const str = "P011";

async function digestMessage(message) {
  const msgUint8 = new TextEncoder().encode(message);                           // encode as (utf-8) Uint8Array
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);           // hash the message
  const hashArray = Array.from(new Uint8Array(hashBuffer));                     // convert buffer to byte array
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join(''); // convert bytes to hex string
  return hashHex;
}

(async() =>{
  const digestHex = await digestMessage(str);
  console.log(digestHex);
})();

