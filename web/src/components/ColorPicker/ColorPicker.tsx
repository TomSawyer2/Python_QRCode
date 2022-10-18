import { ChromePicker } from 'react-color';
import React from 'react';
import { Popover } from 'antd';

import './styles.less';

interface ColorPickerParams {
  color: string;
  onChange: (color: string) => void;
}

const ColorPicker: React.FC<ColorPickerParams> = (props) => {
  const { color, onChange } = props;

  return (
    <Popover
      content={
        <ChromePicker
          color={color}
          onChangeComplete={(colorObj) => onChange(colorObj.hex)}
        />
      }
    >
      <div
        className="color-circle"
        style={{ backgroundColor: color }}
      />
    </Popover>
  );
};

export default ColorPicker;
