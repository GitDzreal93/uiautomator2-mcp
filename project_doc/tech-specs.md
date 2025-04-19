# 技术规格说明

## OCR集成方案

### 1. OCR引擎选择
- 使用PaddleOCR作为OCR引擎
- 支持中英文识别
- 支持文本定位和识别

### 2. 主要功能
- 屏幕文本识别：对当前屏幕进行OCR识别
- 文本定位：通过文本内容定位坐标
- 坐标点击：支持通过坐标进行精确点击

### 3. 技术依赖
- paddleocr: OCR引擎
- opencv-python: 图像处理
- numpy: 数据处理

### 4. API设计
```python
def ocr_screen() -> List[Dict]:
    """获取当前屏幕的OCR识别结果"""
    pass

def find_text_position(text: str) -> Tuple[int, int]:
    """查找文本位置，返回中心点坐标"""
    pass

def click_position(x: int, y: int) -> bool:
    """点击指定坐标"""
    pass
```

### 5. 性能考虑
- OCR结果缓存
- 识别结果的置信度阈值
- 坐标点击的容错范围 