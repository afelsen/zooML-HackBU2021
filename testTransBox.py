import FaceBox
import cv2

zoom = cv2.imread("images/input.png", cv2.IMREAD_COLOR)
boxes = FaceBox.getTransBoxes(zoom)
cv2.imwrite("images/output.png", boxes)
