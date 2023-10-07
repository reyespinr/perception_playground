import pyzed.sl as sl
import cv2

def main():
    # Create a Camera object
    zed = sl.Camera()

    # Open the camera
    init = sl.InitParameters()
    status = zed.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    # Create matrices to hold images
    image = sl.Mat()

    key = ''
    while key != 113:  # Press 'q' key to exit
        # Grab an image from the camera
        if zed.grab(sl.RuntimeParameters()) == sl.ERROR_CODE.SUCCESS:
            # Retrieve the left image
            zed.retrieve_image(image, sl.VIEW.LEFT)
            
            # Convert the image to a format that can be displayed with OpenCV
            img_cv2 = image.get_data()

            # Display the image
            cv2.imshow("ZED Mini Output", img_cv2)

            key = cv2.waitKey(10)

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
