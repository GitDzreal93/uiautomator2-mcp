"""
OCR模块 - 提供基于PaddleOCR的文本识别和定位功能
"""

import os
import time
from typing import List, Dict, Tuple, Optional
import numpy as np
from paddleocr import PaddleOCR
import cv2
from .android import get_device

class OCRManager:
    _instance = None
    _ocr = None
    _last_screen = None
    _last_result = None
    _last_time = 0
    _cache_timeout = 1  # 缓存超时时间(秒)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OCRManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._ocr is None:
            self._ocr = PaddleOCR(use_angle_cls=True, lang="ch", show_log=False)

    def _get_screenshot(self) -> np.ndarray:
        """获取当前屏幕截图"""
        device = get_device()
        screenshot = device.screenshot(format='opencv')
        return screenshot

    def _should_refresh_cache(self) -> bool:
        """判断是否需要刷新缓存"""
        return (time.time() - self._last_time) > self._cache_timeout

    def ocr_screen(self, use_cache: bool = True) -> List[Dict]:
        """
        对当前屏幕进行OCR识别
        Args:
            use_cache: 是否使用缓存结果
        Returns:
            List[Dict]: OCR识别结果列表，每个Dict包含:
                - text: 识别的文本
                - confidence: 置信度
                - position: 文本框坐标 ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
        """
        if use_cache and not self._should_refresh_cache() and self._last_result is not None:
            return self._last_result

        # 获取屏幕截图
        self._last_screen = self._get_screenshot()
        
        # 执行OCR识别
        result = self._ocr.ocr(self._last_screen, cls=True)
        
        # 格式化结果
        formatted_result = []
        if result:
            for line in result[0]:
                position, (text, confidence) = line
                formatted_result.append({
                    'text': text,
                    'confidence': confidence,
                    'position': position
                })

        # 更新缓存
        self._last_result = formatted_result
        self._last_time = time.time()
        
        return formatted_result

    def find_text_position(self, text: str, confidence_threshold: float = 0.5) -> Optional[Tuple[int, int]]:
        """
        查找文本位置
        Args:
            text: 要查找的文本
            confidence_threshold: 置信度阈值
        Returns:
            Tuple[int, int]: 文本中心点坐标，如果未找到返回None
        """
        results = self.ocr_screen()
        
        # 查找匹配的文本
        for item in results:
            if (text in item['text'] and 
                item['confidence'] >= confidence_threshold):
                # 计算中心点坐标
                position = item['position']
                center_x = int(sum(x for x, _ in position) / 4)
                center_y = int(sum(y for _, y in position) / 4)
                return (center_x, center_y)
        
        return None

    def click_text(self, text: str, confidence_threshold: float = 0.5) -> bool:
        """
        点击指定文本
        Args:
            text: 要点击的文本
            confidence_threshold: 置信度阈值
        Returns:
            bool: 是否点击成功
        """
        position = self.find_text_position(text, confidence_threshold)
        if position:
            return self.click_position(*position)
        return False

    def click_position(self, x: int, y: int) -> bool:
        """
        点击指定坐标
        Args:
            x: X坐标
            y: Y坐标
        Returns:
            bool: 是否点击成功
        """
        try:
            device = get_device()
            device.click(x, y)
            return True
        except Exception:
            return False

# 创建全局OCR管理器实例
ocr_manager = OCRManager() 