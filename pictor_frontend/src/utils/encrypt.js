/**
 Author: Alan Fu
 Email: fualan1990@gmail.com
 * */

import { JSEncrypt } from "jsencrypt";

const privateKey = "PICTOR";

/**
 * @description RSA加密
 * @param data
 * @returns {Promise<{param: PromiseLike<ArrayBuffer>}|*>}
 */
export async function encryptedData(data) {
  let publicKey = "";
  const res = await getPublicKey();
  publicKey = res.data;
  if (publicKey.mockServer) {
    publicKey = "";
  }
  if (publicKey === "") {
    return data;
  }

  const encrypt = new JSEncrypt();
  encrypt.setPublicKey(
    `-----BEGIN PUBLIC KEY-----${publicKey}-----END PUBLIC KEY-----`
  );
  data = encrypt.encrypt(JSON.stringify(data));
  return {
    param: data,
  };
}

/**
 * @description RSA解密
 * @param data
 * @returns {PromiseLike<ArrayBuffer>}
 */
export function decryptedData(data) {
  const decrypt = new JSEncrypt();
  decrypt.setPrivateKey(
    `-----BEGIN RSA PRIVATE KEY-----${privateKey}-----END RSA PRIVATE KEY-----`
  );
  data = decrypt.decrypt(JSON.stringify(data));
  return data;
}
