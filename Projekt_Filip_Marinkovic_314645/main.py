import cv2 as cv
import cartoonize as ct
import sys
import os


def main():
    sys.argv[0] = input("Enter the name of the file you wish to open: \n")
    fileName = sys.argv[0]
    fileExists = os.path.isfile(fileName)

    if fileExists == False:
        print("""Error:File does not exist\n 
        Check the spelling of the name, file extension or check if the file is in the right directory\n""")
        return None

    __cap = cv.Video__capture(fileName)

    try:
        __cap.isOpened()
    except:
        print("%s file couldn't be opened" % fileName)

    __height = int(__cap.get(cv.__cap_PROP_FRAME_HEIGHT))
    __width = int(__cap.get(cv.__cap_PROP_FRAME_WIDTH))
    __fps = int(__cap.get(cv.__cap_PROP_FPS))
    __fourcc = cv.VideoWriter_fourcc(*'mp4v')

    try:
        output = cv.VideoWriter("VideoOutput.mp4", __fourcc,
                                __fps, (__width, __height))
    except:
        print("There is a problem with this directory or file extension")

    cv.namedWindow("Video Player")
    cv.resizeWindow("Video Player", 1280, 720)

    while __cap.isOpened():
        __success, __frame = __cap.read()
        if __success:
            __frame = ct.cartoonize(__frame)
            cv.imshow("Video Player", __frame)
            output.write(__frame)
        else:
            print("There was a problem with reading the video")
            break

        __quitKey = cv.waitKey(int(1/__fps*1000)) & 0xFF == 27
        __closeButton = cv.getWindowProperty(
            "Video Player", cv.WND_PROP_VISIBLE) < 1

        if __quitKey or __closeButton:
            break

    __cap.release()
    output.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
