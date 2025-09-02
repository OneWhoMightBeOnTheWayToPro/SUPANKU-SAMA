# pip install opencv-python

import cv2
from ultralytics import YOLO
import urllib.request
import time

index = 0
arr = []
while True:
    cap = cv2.VideoCapture(index)
    if not cap.read()[0]:
        break
    else:
        arr.append(index)
    cap.release()
    index += 1
print(arr)

model = YOLO('yolo11n-pose.pt')
print(model.names)
webcamera = cv2.VideoCapture(arr[0])
# webcamera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# webcamera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
target_width = 1080

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4',fourcc, 20.0, (target_width,480))
tolerance = 20
while True:
    success, frame = webcamera.read()
    height, width, _ = frame.shape
    center_x, center_y = width // 2, height // 2
    aspect_ratio = width / height
    results = model.track(frame, classes=0, conf=0.8, imgsz=480)
    target_height = int(target_width / aspect_ratio)
    cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0), 2)
    cv2.putText(frame, f"Total: {len(results[0].boxes)}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    if results[0].keypoints:
        for keypoints in results[0].keypoints:
            keypoints_xy = keypoints.xy[0].cpu().numpy()
            x_11 = 0
            y_11 = 0
            x_12 = 0
            y_12 = 0
            for i, (x,y) in enumerate(keypoints_xy):
                if (i == 11):
                    x_11, y_11 = int(x), int(y)
                if (i == 12):
                    x_12, y_12 = int(x), int(y)
                    ass_x = (x_11 + x_12) // 2
                    ass_y = (y_11 + y_12) // 2
                    cv2.circle(frame, (ass_x, ass_y), 5, (255, 255, 255), 2)
                    text = "CROTCH"
                    instruction = "TURN!"
                    if(x_11 - x_12 < 0):
                        text = "ARSE"
                        if(ass_x > center_x + tolerance):
                            instruction = "<----"
                        elif(ass_x < center_x - tolerance):
                            instruction = "---->"
                        else:
                            instruction = "GOOD!"
                            contents = urllib.request.urlopen("http://192.168.4.1/H").read()
                            time.sleep(3)
                    cv2.putText(frame, instruction, (center_x + 5, center_y - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                    cv2.putText(frame, text, (ass_x, ass_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                #if(i > 0):
                    #cv2.circle(frame, (int(x),int(y)), 10, (255,0, 0 ), 2) # -1
                    #cv2.putText(frame, str(i), (int(x)+10, int(y) -10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    resized_frame = cv2.resize(results[0].plot(), (target_width, target_height))
    cv2.namedWindow("Live Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live Camera", target_width, target_height)
    cv2.imshow("Live Camera", resized_frame)
    #out.write(resized_frame)
    if cv2.waitKey(1) == ord('q'):
        break

webcamera.release()
out.release()
cv2.destroyAllWindows()

# For Realsense camera
   # def initialize_realsense():
    #    import pyrealsense2 as rs
    #    pipeline = rs.pipeline()
     #   camera_aconfig = rs.config()
      #  camera_aconfig.enable_stream(rs.stream.depth, *config.DEPTH_CAMERA_RESOLUTION, rs.format.z16, config.DEPTH_CAMERA_FPS)
     #   camera_aconfig.enable_stream(rs.stream.color, *config.COLOR_CAMERA_RESOLUTION, rs.format.bgr8, config.COLOR_CAMERA_FPS)
     #   pipeline.start(camera_aconfig)
      #  return pipeline
# try:
#     # Try to initialize RealSense Camera
#     camera = initialize_realsense()
#     get_frame = get_frame_realsense
# except Exception as e:
#     print("RealSense camera not found, using default webcam.")
#     camera = initialize_webcam()
#     get_frame = get_frame_webcam

# Function to get frames from RealSense
# def get_frame_realsense(pipeline):
#     import pyrealsense2 as rs
#     frames = pipeline.wait_for_frames()
#     depth_frame = frames.get_depth_frame()
#     color_frame = frames.get_color_frame()
#     if not depth_frame or not color_frame:
#         return None, None
#     depth_image = np.asanyarray(depth_frame.get_data())
#     color_image = np.asanyarray(color_frame.get_data())
#     return depth_image, color_image

# # Function to get frame from webcam
# def get_frame_webcam(cap):
#     ret, frame = cap.read()
#     return None, frame if ret else None