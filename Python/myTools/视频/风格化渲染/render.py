import cv2

inp = "input.mp4"
out = "output.mp4"

cap = cv2.VideoCapture(inp)
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
writer = cv2.VideoWriter(out, fourcc, fps, (w, h))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 边缘保留平滑
    smooth = cv2.stylization(frame, sigma_s=60, sigma_r=0.45)

    # 边缘提取
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edge = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY, 9, 2
    )
    edge = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)

    # 合成
    cartoon = cv2.bitwise_and(smooth, edge)

    writer.write(cartoon)

cap.release()
writer.release()
