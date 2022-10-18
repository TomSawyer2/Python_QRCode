import axios from '@/utils/axios';

export interface EncodeQRCodeParams {
  data: string;
  backColor?: string;
  fillColor?: string;
}

export interface DecodeQRCodeParams {
  data: string;
}

// 编码生成二维码
export async function encodeQRCode(params: EncodeQRCodeParams) {
  const url = '/api/encode';

  const { data } = await axios.post(url, params);
  return data;
}

// 解码二维码
export async function decodeQRCode(params: DecodeQRCodeParams) {
  const url = '/api/decode';

  const { data } = await axios.post(url, params);
  return data;
}
