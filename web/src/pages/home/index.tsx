import React, { useState } from 'react';
import { Button, Col, Input, message, Row, Spin, Tooltip, Upload } from 'antd';

import HeaderBar from '@/components/HeaderBar';
import { decodeQRCode, encodeQRCode } from '@/services/qrcode';
import { saveImg } from '@/utils/saveImg';

import './index.less';

const Page: React.FC = () => {
  const [encodeData, setEncodeData] = useState<string>('');
  const [encodeImg, setEncodeImg] = useState<string>('');
  const [encodeLoading, setEncodeLoading] = useState<boolean>(false);

  const [decodeInput, setDecodeInput] = useState<string>('');
  const [decodeOutput, setDecodeOutput] = useState<string>('');
  const [decodeLoading, setDecodeLoading] = useState<boolean>(false);

  // const [backColor, setBackColor] = useState<string>('#ffffff');
  // const [fillColor, setFillColor] = useState<string>('#000000');

  const checkBeforeUpload = async (file: File) => {
    const isJPG = file.type === 'image/jpeg';
    const isPNG = file.type === 'image/png';
    if (!isJPG && !isPNG) {
      message.error('You can only upload JPG/PNG file!');
      return false;
    }
    const isLt5M = file.size / 1024 / 1024 < 5;
    if (!isLt5M) {
      message.error('Image must smaller than 2MB!');
      return false;
    }
    // 将file转为base64
    let base64Param = '';
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = async () => {
      const base64 = reader.result as string;
      base64Param = base64.replace('data:image/png;base64,', '') as string;
      setDecodeInput(base64Param);
      return false;
    };
  };

  const handleEncode = async () => {
    setEncodeLoading(true);
    try {
      const data = await encodeQRCode({ data: encodeData });
      setEncodeImg(`data:image/png;base64,${data}`);
      message.success('生成成功');
    } catch (err) {
      console.error(err);
    }
    setEncodeLoading(false);
  };

  const handleDecode = async () => {
    if (!decodeInput) return;
    setDecodeLoading(true);
    try {
      const data = await decodeQRCode({ data: decodeInput });
      setDecodeOutput(data?.[0]);
      message.success('解码成功');
    } catch (err) {
      console.error(err);
    }
    setDecodeLoading(false);
  };

  const handleSave = () => {
    const fileName = `output-${new Date().getTime()}.png`;
    saveImg(encodeImg, fileName);
  };

  return (
    <div className="container">
      <HeaderBar />
      <Row className="qr">
        <Col
          className="qr-card"
          span={8}
        >
          <div className="encode">
            <Input.TextArea
              rows={4}
              allowClear
              className="encode-input"
              placeholder="请输入要编码的内容"
              onChange={(e) => setEncodeData(e.target.value)}
            />
            <div className="encode-img">
              {encodeImg === '' ? (
                <div className="empty-img-box">{encodeLoading && <Spin />}</div>
              ) : (
                <div className="img-box">
                  {encodeLoading ? (
                    <Spin />
                  ) : (
                    <img
                      className="image"
                      src={encodeImg}
                    />
                  )}
                </div>
              )}
            </div>
            <div>
              <Button
                className="encode-btn"
                onClick={() => handleEncode()}
                disabled={encodeData === '' || encodeLoading}
              >
                <span className="encode-btn-text">生成</span>
              </Button>
              <Button
                type="primary"
                className="encode-btn"
                onClick={() => handleSave()}
                disabled={encodeData === '' || encodeLoading}
              >
                <span className="encode-btn-text">保存</span>
              </Button>
            </div>
          </div>
        </Col>
        <Col
          className="qr-card"
          span={8}
        >
          <div className="decode">
            <div className="decode-img">
              <Upload.Dragger
                showUploadList={false}
                beforeUpload={checkBeforeUpload}
              >
                <div className="img-box">
                  {decodeInput === '' ? (
                    <div className="empty-img-box-upload" />
                  ) : (
                    <div className="mask-box">
                      <img
                        className="image"
                        src={`data:image/png;base64,${decodeInput}`}
                      />
                      <div className="mask">
                        <Button>更新</Button>
                      </div>
                    </div>
                  )}
                </div>
              </Upload.Dragger>
            </div>
            <div className="decode-output">
              {decodeLoading ? (
                <Spin />
              ) : (
                <Tooltip
                  placement="top"
                  title={decodeOutput}
                >
                  <span className="output-text">{decodeOutput}</span>
                </Tooltip>
              )}
            </div>
            <Button
              type="primary"
              className="decode-btn"
              onClick={() => handleDecode()}
            >
              <span className="decode-btn-text">识别</span>
            </Button>
          </div>
        </Col>
      </Row>
      <div className="bg" />
    </div>
  );
};

export default Page;
