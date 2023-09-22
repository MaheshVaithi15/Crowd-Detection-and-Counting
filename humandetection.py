import tkinter.messagebox as mbox

from tkinter import *

from tkinter import simpledialog

import tkinter as tk

from tkinter import filedialog

from PIL import Image, ImageTk

import time
import cv2

import argparse

import matplotlib.pyplot as plt

from skimage.feature import hog

from odapi import DetectorAPI



# GUI for Main Window

root = Tk()
root.geometry("1000x600")
root.title("GUI")
root.config(bg="white")
root.resizable(0, 0)
root.iconbitmap('Images/icon1.png')

tk.Label(text="People Detection and Counting",font=("Arial",35,"bold"),fg="cyan").place(x=100,y=20)

def startwindow():
    root.destroy()

Button(root,text="Enter",command=startwindow,font=("Times New Roman",20),bg="Orange",fg="Green",cursor="hand2",borderwidth=2,relief="groove").place(x=150,y=470)

# Image on Main Window

path1 = "Images/icon1.png"

img1=ImageTk.PhotoImage(Image.open(path1))

panel1 = tk.Label(root,image=img1)

panel1.place(x=300,y=150)

exit1=False

def exitwindow():
    global exit1

    if mbox.askokcancel("Exit Window","Do you want to exit?"):

        exit1=True

        root.destroy()

Button(root,text="Exit",command=exitwindow,font=("Times New Roman",20),bg="red",fg="green",cursor="hand2",borderwidth=2,relief="groove").place(x=680,y=470)

root.protocol("WM_DELETE_WINDOW",exitwindow)

root.mainloop()

if exit1==False:

    root1=tk.Tk()

    root1.title("Options")

    root1.geometry('1000x700')

    #root1.iconbitmap('icon1.png')

    filename=""
    filename1=""
    filenameimg=""
    filename2=""
    filenamevid=""

    def argparser():

        arg_parse=argparse.ArgumentParser()

        arg_parse.add_argument("-i", "--image", default=None,help="Path to the image")

        arg_parse.add_argument("-v", "--video", default=None,help="Path to the video")
        
        arg_parse.add_argument("-c", "--camera", default=False, help="Set true if you want to use the camera.")

        arg_parse.add_argument("-o", "--output",type=str,help="path to the output file")

        args = vars(arg_parse.parse_args()) 

        return args

# New Window for Opening Image

    def opt_img():

        rootimg = tk.Tk()
        rootimg.geometry('1000x700')
        rootimg.title('Image Window')

        def open_img():

            global filename1
            
            global filenameimg

            filename1 = filedialog.askopenfilename(title="Select Image",parent=rootimg)
            path_text1.delete("1.0","end")
            path_text1.insert(END,filename1)

        def prev_img():

            global filename1
            
            global filenameimg

            img3 = cv2.imread(filename1,1)
            
            #imgd = cv2.imread(filenameimg,1)

            img3 =  cv2.resize(img3,(800,800))

            cv2.imshow("Preview Image",img3)

        path_text1=tk.Text(rootimg,height=1,width=37,font=("Arial",25),bg="lightgreen",fg="Blue",borderwidth=2,relief="solid")
        path_text1.place(x=80,y=260)
        
        def detect_img():
            img_path = filename1
            
            if img_path == "":
                
                mbox.showerror("Error","Image Not Selected",parent=rootimg)
                
                return
            info1.config(text = "Extracting...")
            
            mbox.showinfo("Please Wait","Extracting...",parent=rootimg)
            
            detectbyimgpath(img_path)
            
            
        def detectbyimgpath(path):
            
            global filename1
            
            image = cv2.imread(path)
            
            resize_img = cv2.resize(image,(128*4,64*4))
            
            fd , hogimg = hog(resize_img, orientations=9, pixels_per_cell=(8, 8),
                	cells_per_block=(2, 2), visualize=True, channel_axis=-1)
            
            #cv2.imshow("Original Image",image)
            
            cv2.imshow("Resized Image",resize_img)
            
            plt.axis('off')
            plt.imshow(hogimg,cmap='copper')
            plt.show()
            
            
            
            info1.config(text="                                                  ")
            info1.config(text="Completed")
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        info1 = tk.Label(rootimg,font=( "Arial", 30),fg="gray")
        info1.place(x=100, y=445)
        
        def detectby_img():
            img_path = filename1
            
            if img_path == "":
                
                mbox.showerror("Error","Image Not Selected",parent=rootimg)
                
                return
            info2.config(text = "Detecting...")
            
            mbox.showinfo("Please Wait","Detecting...",parent=rootimg)
            
            detectbyimg(img_path)

        def detectbyimg(pathe):
            
            global filename1
            
            img = cv2.imread(pathe)

            person = 0
        
            
            odapi = DetectorAPI()
            threshold = 0.8
            
            resizeimg = cv2.resize(img,(img.shape[1],img.shape[0]))
            
            boxes, scores, classes, num = odapi.processFrame(resizeimg)
            
            for i in range(len(boxes)):

                if classes[i] == 1 and scores[i] > threshold:
                    box = boxes[i]
                    person+=1
                    
                    cv2.rectangle(resizeimg, (box[1], box[0]), (box[3], box[2]), (255,0,0), 2)
                    cv2.putText(resizeimg, f'{round(scores[i], 2)}', (box[1] - 30, box[0] - 8), cv2.FONT_HERSHEY_COMPLEX,0.5, (255, 0, 0), 1)
            cv2.putText(resizeimg,'Count='+format(str(person)),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA) 
                    
            

                    
            cv2.imshow('Detected From Image',resizeimg)
             
            info2.config(text="                                                  ")
            info2.config(text="Completed")
            info2.config(text="                                                  ")
            info2.config(text="Human Count:"+str(person))
            
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        info2 = tk.Label(rootimg,font=( "Arial", 30),fg="gray")
        info2.place(x=100, y=445)

                
        def exit_wini():
            if mbox.askokcancel("Exit", "Do you want to exit?", parent = rootimg):
                rootimg.destroy()
        rootimg.protocol("WM_DELETE_WINDOW", exit_wini)
        
        Button(rootimg, text="Select", command=open_img, cursor="hand2", font=("Arial", 20), bg="light yellow", fg="blue").place(x=20, y=350)
        Button(rootimg, text="Preview",command=prev_img, cursor="hand2", font=("Arial", 20), bg = "light yellow", fg = "blue").place(x = 220, y = 350)
        Button(rootimg, text="Extract Feature",command=detect_img, cursor="hand2", font=("Arial", 20), bg = "orange", fg = "blue").place(x = 420, y = 350)
        Button(rootimg, text="Detect",command=detectby_img, cursor="hand2", font=("Arial", 20), bg = "orange", fg = "blue").place(x = 720, y = 350)


    
    
    Button(root1, text="From Image",command=opt_img, cursor="hand2", font=("Arial",30), bg = "light green", fg = "blue").place(x = 350, y = 150)
    
# New Window for Opening Video

    def opt_video():

        rootvideo = tk.Tk()
        rootvideo.geometry('1000x700')
        rootvideo.title('Preview Video')

        def open_video():

            global filename2

            filename2 = filedialog.askopenfilename(title="Select Video",parent=rootvideo)

            path_text2.delete("1.0","end")
            path_text2.insert(END,filename2)
            
        def detect_video():
            global filename2
            video_path = filename2
            if (video_path == ""):
                mbox.showerror("No Video Found",parent=rootvideo)
                return
            info1.config(text="Please wait...Extracting From Video....")
            mbox.showinfo("Extracting....",parent=rootvideo)
            
            args = argparser()
            writer = None
            if args['output'] is not None:
                writer = cv2.VideoWriter(args['output'], cv2.VideoWriter_fourcc(*'MJPG'), 10, (600, 600))

            detectbyvideopath(video_path, writer)
            
        def detectbyvideopath(path,writer):
            
            global filename2
            
            video = cv2.VideoCapture(path)
            
            fgbg = cv2.createBackgroundSubtractorMOG2()
            
            check, frame = video.read()
            
            if(check == False):
                print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
                return
            
            while video.isOpened():
                
                check,frame = video.read()
                
                if(check == True):
                    
                    imgv = cv2.resize(frame,(128*4,64*4))
                    
                    fd , hogv = hog(imgv,orientations=9,pixels_per_cell=(8,8),cells_per_block=(2,2),visualize=True,channel_axis=-1)
                    
                    imgfg = fgbg.apply(hogv)
                    
                    

                            
                    if writer is not None:
                        writer.write(imgv)

                    cv2.imshow("Feature Extracted",imgfg)
                    
                    cv2.imshow("Original Video",frame)
                    
                    cv2.imshow("Resized Video",imgv)
                    
                    key = cv2.waitKey(1)
                    if key & 0xFF == ord('q'):
                        break
                    
            video.release()
            info1.config(text="Completed")
            
            #cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        info1 = tk.Label(rootvideo, font=("Arial", 30), fg="gray") 
        info1.place(x=100, y=440)
        
        def detectby_video():
            global filename2
            video_path = filename2
            if (video_path == ""):
                mbox.showerror("No Video Found",parent=rootvideo)
                return
            info2.config(text="Please wait...Detecting From Video....")
            mbox.showinfo("Detecting....",parent=rootvideo)
            
            args = argparser()
            writer = None
            if args['output'] is not None:
                writer = cv2.VideoWriter(args['output'], cv2.VideoWriter_fourcc(*'MJPG'), 10, (600, 600))
                        
                    
            detectbyvid(video_path,writer)
        
        def detectbyvid(pathv,writer):
            global filename2
            
            odapi = DetectorAPI()
            threshold = 0.7

            #person=0
            maxcv=0
            #p=0

            #p=[]
            
            vid = cv2.VideoCapture(pathv)
            
            check,frame = vid.read()
            
            if(check == False):
                print('Video Not Found. Please Enter a Valid Path (Full path of Video Should be Provided).')
                return
            
            while vid.isOpened():
                
                check,frame = vid.read()
                
                if(check == True):
                
                    resizevid = cv2.resize(frame,(800,500))

                    boxes, scores, classes, num = odapi.processFrame(resizevid)

                    person = 0

                    
                    
                    for i in range(len(boxes)):

                        if classes[i] == 1 and scores[i] > threshold:
                            box = boxes[i]
                            person+=1

                            #person = p
                            
                            cv2.rectangle(resizevid, (box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)
                            cv2.putText(resizevid, f'{round(scores[i], 2)}', (box[1] - 30, box[0] - 8), cv2.FONT_HERSHEY_COMPLEX,0.5, (255, 0, 0), 1)
                            #cv2.putText(resizevid,'Count='+format(str(len(boxes))),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1,cv2.LINE_AA)
                    cv2.putText(resizevid,'Count='+format(str(person)),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)
                    if(person>maxcv):
                        maxcv = person

                    
                    if writer is not None:
                        writer.write(resizevid)
                        
                    cv2.imshow("Human Detection from Video", resizevid)
                    key = cv2.waitKey(1)
                    if key & 0xFF == ord('q'):
                        break
                else:
                    break

            vid.release()
            info2.config(text="Completed")
            info2.config(text="                                                  ")
            info2.config(text="Human Count:" + str(maxcv))
            #info2.config(text="Human Count:" + str(person))

            #info22.config(text="                                                  ")
            #info22.config(text="Human Count:"+str(person))
            
            #cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        info2 = tk.Label(rootvideo, font=("Arial", 30), fg="gray") 
        info2.place(x=100, y=440)

        #info22 = tk.Label(rootvideo, font=("Arial", 30), fg="gray") 
        #info22.place(x=100, y=540)


        def prev_video():

            global filename2

            cap = cv2.VideoCapture(filename2)

            while(cap.isOpened()):
                ret, frame = cap.read()
                
                if ret == True:

                    imgv = cv2.resize(frame,(800,500))

                    cv2.imshow("Preview Video",imgv)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):

                        break
                else:

                    break
            cap.release()
            cv2.destroyAllWindows()
          

        path_text2=tk.Text(rootvideo,height=1,width=37,font=("Arial",25),bg="Light blue",fg="red",borderwidth=2,relief="solid")

        path_text2.place(x=80,y=260)

        def exit_winv():

            if mbox.askokcancel("Exit", "Do you want to exit?", parent =rootvideo):

                rootvideo.destroy()

        rootvideo.protocol("WM_DELETE_WINDOW",exit_winv)

        Button(rootvideo, text="Select", command=open_video, cursor="hand2", font=("Arial", 20), bg="light yellow", fg="blue").place(x=20, y=350)
        Button(rootvideo, text="Preview",command=prev_video, cursor="hand2", font=("Arial", 20), bg = "light yellow", fg = "blue").place(x = 210, y = 350)
        Button(rootvideo, text="Extract Feature",command=detect_video, cursor="hand2", font=("Arial", 20), bg = "orange", fg = "blue").place(x = 420, y = 350)
        Button(rootvideo, text="Detect",command=detectby_video, cursor="hand2", font=("Arial", 20), bg = "orange", fg = "blue").place(x = 720, y = 350)


    Button(root1, text="From Video",command=opt_video, cursor="hand2", font=("Arial",30), bg = "light green", fg = "blue").place(x = 350, y = 300)

    
    # New Window  For Live Camera
    
    def opt_camera():
        rootcam = tk.Tk()
        rootcam.title("From Live Camera")
        rootcam.geometry('1000x700')
        
        def open_camera():
            
            args = argparser()
            
            info1.config(text="Opening Camera...")
            
            mbox.showinfo("Opening Camera...",parent=rootcam)
            
            cam = cv2.VideoCapture(0)
            
            while True:
                
                ret,frame = cam.read()
                
                cv2.imshow(frame,'Camera')
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    
                    break
            cam.release()
            cv2.destroyAllWindows()
           
            
        info1 = tk.Label(rootcam, font=("Arial", 30), fg="gray")  # same way bg
        info1.place(x=100, y=330)
        
        Button(rootcam, text="Preview Camera", command=open_camera, cursor="hand2", font=("Arial", 20), bg="light green", fg="blue").place(x=370, y=230)
        
        def fdcamera():
            
            cap = cv2.VideoCapture(0)
            
            fgbg = cv2.createBackgroundSubtractorMOG2()
            
            while True:
                
                ret , frame = cap.read()
                
                resizedcam = cv2.resize(frame,(128*4,64*4))
                
                fd , hogcam = hog(resizedcam,orientations=9,pixels_per_cell=(8,8),cells_per_block=(2,2),visualize=True,channel_axis=-1)
                
                fgcam = fgbg.apply(hogcam)
                
                cv2.imshow("FE Cam",fgcam)
                
                cv2.imshow("Original Camera",frame)
                
                cv2.imshow("Resized Camera",resizedcam)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    
                    break
            cap.release()
            cv2.destroyAllWindows()
            
        def detcamera():
            
            cap = cv2.VideoCapture(0)
            #cap = cv2.VideoCapture(simpledialog.askstring(title="IP",prompt="Enter the IP Address of the camera"))
            odapi = DetectorAPI()
            threshold = 0.7

            while True:
                
                ret , frame = cap.read()
                
                
                resizecam = cv2.resize(frame,(800,500))
                
                boxes, scores, classes, num = odapi.processFrame(resizecam)
                person = 0
                count = 0
                for i in range(len(boxes)):

                    if classes[i] == 1 and scores[i] > threshold:
                        box = boxes[i]
                        person=person+1

                        #time.sleep(0.5)
                        
                        count = person
                        
                        cv2.rectangle(resizecam,(box[1], box[0]), (box[3], box[2]), (255, 0, 0), 2)
                        cv2.putText(resizecam, f'{round(scores[i], 2)}', (box[1] - 30, box[0] - 8), cv2.FONT_HERSHEY_COMPLEX,0.5, (255, 0, 0), 1)
                        #cv2.putText(resizecam,'Count='+str(count),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA) 
                        #cv2.putText(resizecam,'Count='+str(person),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)
                cv2.putText(resizecam,'Count='+str(person),(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)
                
                cv2.imshow('FROM LIVE CAMERA',resizecam)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    
                    break
            cap.release()
            cv2.destroyAllWindows()
            #resizecam.destroy()
                
                
            
            
            
            
        Button(rootcam, text="Feature Extraction From Camera", command=fdcamera, cursor="hand2", font=("Arial", 20), bg="light green", fg="blue").place(x=370, y=230)
        Button(rootcam, text="Detect From Camera", command=detcamera, cursor="hand2", font=("Arial", 20), bg="light green", fg="blue").place(x=370, y=430)
        
        # Exit condition for camera Window
        def exit_winc():
            if mbox.askokcancel("Exit", "Do you want to exit?", parent = rootcam):
                rootcam.destroy()
        rootcam.protocol("WM_DELETE_WINDOW", exit_winc)
        
    Button(root1, text="From Camera", command=opt_camera, cursor="hand2", font=("Arial", 25), bg="light green", fg="blue").place(x=350, y=450)   


# Exit Condition of Options Window

    def exit_win1():
        if mbox.askokcancel("Exit","Do you want to exit?"):
            root1.destroy()
    root1.protocol("WM_DELETE_WINDOW", exit_win1)
    root1.mainloop()

















