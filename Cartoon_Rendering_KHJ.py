import cv2 as cv
import numpy as np
import sys
import os

# --- 입력 이미지 읽기 ---
img_path = sys.argv[1] if len(sys.argv) > 1 else "input.jpg"
img = cv.imread(img_path)
if img is None:
    print(f"Error: '{img_path}' 파일을 읽을 수 없습니다.")
    sys.exit(1)

# [1] Bilateral Filter로 색상 평탄화 (엣지 보존 Smoothing)
color = cv.bilateralFilter(img, 9, 300, 300)

# [2] 그레이스케일 변환 후 Median Blur로 노이즈 제거
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
gray = cv.medianBlur(gray, 7)

# [3] Adaptive Thresholding으로 윤곽선 마스크 생성
edges = cv.adaptiveThreshold(
    gray, 255,
    cv.ADAPTIVE_THRESH_MEAN_C,
    cv.THRESH_BINARY,
    blockSize=9, C=5
)

# [4] Morphological Closing으로 엣지 끊김 정리
kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, kernel)

# [5] 윤곽선 마스크 + 색상 이미지 합성
cartoon = cv.bitwise_and(color, color, mask=edges)

# --- 결과 저장 ---
os.makedirs("Saved", exist_ok=True)
base_name = os.path.splitext(os.path.basename(img_path))[0]
out_path = os.path.join("Saved", f"{base_name}_cartoon.png")
cv.imwrite(out_path, cartoon)
print(f"결과 저장: {out_path}")

# --- 화면 표시 ---
cv.imshow("Original", img)
cv.imshow("Cartoon", cartoon)
cv.waitKey(0)
cv.destroyAllWindows()
