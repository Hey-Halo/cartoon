import cv2 as cv
import cartoonize as ct

cap = cv.VideoCapture("VideoInput.mp4")
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
fps = int(cap.get(cv.CAP_PROP_FPS))

fourcc = cv.VideoWriter_fourcc(*'mp4v')
output = cv.VideoWriter("VideoOutput.mp4", fourcc, fps, (width, height))
cv.namedWindow("Video Player")
cv.resizeWindow("Video Player", 1280, 720)

while (cap.isOpened()):
    success, frame = cap.read()
    if success:
        frame = ct.cartoonize(frame)
        cv.imshow("Video Player", frame)
        output.write(frame)
        quitButton = cv.waitKey(int(1/fps*1000)) & 0xFF == 27
        closeButton = cv.getWindowProperty(
            "Video Player", cv.WND_PROP_VISIBLE) < 1
    else:
        break
    if quitButton or closeButton:
        break

cap.release()
output.release()
cv.destroyAllWindows()