from tkinter import filedialog, messagebox
import os
import cv2
import customtkinter as ctk
from PIL import Image, ImageTk

from image_tools import read_image, show_histogram

from operations import (
    add_images,
    subtract_images,
    divide_images,
    complement_image,
    change_red_channel,
    swap_red_green,
    eliminate_red_channel,
    histogram_stretching,
    histogram_equalization,
    average_filter,
    laplacian_filter,
    maximum_filter,
    minimum_filter,
    median_filter,
    mode_filter,
    add_salt_pepper_noise,
    salt_pepper_average_filter,
    salt_pepper_median_filter,
    salt_pepper_outlier_method,
    add_gaussian_noise,
    image_averaging,
    gaussian_average_filter,
    basic_global_thresholding,
    automatic_thresholding,
    adaptive_thresholding,
    sobel_detector,
    image_dilation,
    image_erosion,
    image_opening,
    internal_boundary,
    external_boundary,
    morphological_gradient,
)


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


BINARY_OPERATIONS = {
    "Addition",
    "Subtraction",
    "Division"
}


HISTOGRAM_OPERATIONS = {
    "Histogram Stretching",
    "Histogram Equalization"
}


NORMAL_OPERATIONS = {

    "Addition": add_images,
    "Subtraction": subtract_images,
    "Division": divide_images,

    "Complement": complement_image,

    "Change Red Channel":
        lambda image: change_red_channel(image,60),

    "Swap Red and Green":
        swap_red_green,

    "Eliminate Red Channel":
        eliminate_red_channel,


    "Histogram Stretching":
        histogram_stretching,

    "Histogram Equalization":
        histogram_equalization,


    "Average Filter":
        average_filter,

    "Laplacian Filter":
        laplacian_filter,

    "Maximum Filter":
        maximum_filter,

    "Minimum Filter":
        minimum_filter,

    "Median Filter":
        median_filter,

    "Mode Filter":
        mode_filter,


    "Basic Global Thresholding":
        basic_global_thresholding,

    "Automatic Thresholding":
        automatic_thresholding,

    "Adaptive Thresholding":
        adaptive_thresholding,


    "Sobel Detector":
        sobel_detector,


    "Image Dilation":
        image_dilation,

    "Image Erosion":
        image_erosion,

    "Image Opening":
        image_opening,


    "Internal Boundary":
        internal_boundary,

    "External Boundary":
        external_boundary,

    "Morphological Gradient":
        morphological_gradient,
}



NOISE_OPERATIONS = [

    "Add Salt & Pepper Noise",

    "Salt & Pepper Average Filter",

    "Salt & Pepper Median Filter",

    "Salt & Pepper Outlier Method",

    "Add Gaussian Noise",

    "Image Averaging",

    "Gaussian Average Filter",

]


ALL_OPERATIONS = list(NORMAL_OPERATIONS.keys()) + NOISE_OPERATIONS

class ImageProcessingApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Image Processing Project")

        self.geometry("1200x850")

        self.resizable(False,False)


        self.first_image_path = None

        self.second_image_path = None


        self.last_salt_pepper_image = None

        self.last_gaussian_image = None


        self.create_widgets()

    def create_widgets(self):
         
        self.main_frame = ctk.CTkFrame(
            self,
            width=1120,
            height=790,
            corner_radius=18,
            fg_color="#ffffff"
        )

        self.main_frame.pack(padx=30,pady=30)

        self.main_frame.pack_propagate(False)



        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Image Processing Project",
            font=("Arial",34,"bold")
        )

        self.title_label.pack(pady=(20,15))



        self.buttons_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.buttons_frame.pack(pady=5)



        self.first_image_button = ctk.CTkButton(
            self.buttons_frame,
            text="Choose First Image",
            command=self.choose_first_image,
            width=230,
            height=42,
            font=("Arial",16,"bold")
        )

        self.first_image_button.grid(
            row=0,
            column=0,
            padx=10
        )



        self.second_image_button = ctk.CTkButton(
            self.buttons_frame,
            text="Choose Second Image",
            command=self.choose_second_image,
            width=230,
            height=42,
            font=("Arial",16,"bold")
        )

        self.second_image_button.grid(
            row=0,
            column=1,
            padx=10
        )



        self.images_names_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.images_names_frame.pack(
            pady=(5,12)
        )



        self.first_image_label = ctk.CTkLabel(
            self.images_names_frame,
            text="No first image selected",
            width=360,
            font=("Arial",13),
            text_color="gray"
        )

        self.first_image_label.grid(
            row=0,
            column=0,
            padx=10
        )



        self.second_image_label = ctk.CTkLabel(
            self.images_names_frame,
            text="No second image selected",
            width=360,
            font=("Arial",13),
            text_color="gray"
        )

        self.second_image_label.grid(
            row=0,
            column=1,
            padx=10
        )



        self.operation_label = ctk.CTkLabel(
            self.main_frame,
            text="Select Operation",
            font=("Arial",18,"bold")
        )

        self.operation_label.pack(
            pady=(5,5)
        )



        self.operation_box = ctk.CTkComboBox(
            self.main_frame,
            values=ALL_OPERATIONS,
            width=420,
            height=40,
            font=("Arial",15),
            state="disabled"
        )

        self.operation_box.pack(
            pady=(0,12)
        )



        self.process_button = ctk.CTkButton(
            self.main_frame,
            text="Process Image",
            command=self.process_operation,
            width=230,
            height=45,
            font=("Arial",17,"bold"),
            state="disabled"
        )

        self.process_button.pack(
            pady=(0,15)
        )



        self.result_title = ctk.CTkLabel(
            self.main_frame,
            text="Result will appear here",
            font=("Arial",18,"bold")
        )

        self.result_title.pack(
            pady=(0,10)
        )



        self.preview_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.preview_frame.pack(
            pady=5
        )



        self.input_display = self.create_image_box(
            self.preview_frame,
            "Input Image"
        )

        self.input_display.grid(
            row=0,
            column=0,
            padx=20
        )



        self.result_display = self.create_image_box(
            self.preview_frame,
            "Result Image"
        )

        self.result_display.grid(
            row=0,
            column=1,
            padx=20
        )
        
    def create_image_box(self, parent, text):

        return ctk.CTkLabel(
            parent,
            text=text,
            width=450,
            height=320,
            fg_color="#1f1f1f",
            corner_radius=12,
            font=("Arial",16)
        )



    def choose_file(self,title):

        return filedialog.askopenfilename(
            title=title,
            filetypes=[
                ("Image Files","*.png *.jpg *.jpeg *.bmp")
            ]
        )



    def choose_first_image(self):

        path = self.choose_file(
            "Choose the first image"
        )

        if not path:
            return


        self.first_image_path = path

        self.last_salt_pepper_image = None
        self.last_gaussian_image = None


        self.first_image_label.configure(
            text=os.path.basename(path)
        )


        self.operation_box.configure(
            state="readonly"
        )

        self.process_button.configure(
            state="normal"
        )


        self.clear_preview()



    def choose_second_image(self):

        path = self.choose_file(
            "Choose the second image"
        )


        if not path:
            return


        self.second_image_path = path


        self.second_image_label.configure(
            text=os.path.basename(path)
        )



    def clear_preview(self):

        self.result_title.configure(
            text="Result will appear here"
        )


        self.input_display.configure(
            image=None,
            text="Input Image"
        )

        self.input_display.image = None



        self.result_display.configure(
            image=None,
            text="Result Image"
        )

        self.result_display.image = None




    def prepare_image(self,image,size=(450,320)):


        if len(image.shape)==2:

            image=cv2.cvtColor(
                image,
                cv2.COLOR_GRAY2RGB
            )

        else:

            image=cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )



        image=Image.fromarray(image)

        image.thumbnail(size)


        return ImageTk.PhotoImage(image)




    def show_result(self,input_image,result_image,operation_name):


        input_photo=self.prepare_image(input_image)

        result_photo=self.prepare_image(result_image)



        self.input_display.configure(
            image=input_photo,
            text=""
        )

        self.input_display.image=input_photo



        self.result_display.configure(
            image=result_photo,
            text=""
        )

        self.result_display.image=result_photo



        self.result_title.configure(
            text=f"Result: {operation_name}"
        )




    def get_first_image(self):

        if not self.first_image_path:

            messagebox.showerror(
                "Missing image",
                "Please choose the first image."
            )

            return None


        return read_image(
            self.first_image_path
        )



    def get_second_image(self):

        if not self.second_image_path:

            messagebox.showerror(
                "Missing image",
                "This operation needs two images."
            )

            return None


        return read_image(
            self.second_image_path
        )  
    def process_operation(self):

        operation_name = self.operation_box.get()


        if not operation_name:

            messagebox.showerror(
                "No operation",
                "Please choose an operation first."
            )

            return



        try:

            image1 = self.get_first_image()


            if image1 is None:
                return



            if operation_name in BINARY_OPERATIONS:


                image2 = self.get_second_image()


                if image2 is None:
                    return



                result = NORMAL_OPERATIONS[operation_name](
                    image1,
                    image2
                )



            elif operation_name == "Add Salt & Pepper Noise":


                result = add_salt_pepper_noise(image1)

                self.last_salt_pepper_image = result



            elif operation_name == "Salt & Pepper Average Filter":


                if self.last_salt_pepper_image is None:

                    messagebox.showerror(
                        "Missing noisy image",
                        "Apply Salt & Pepper Noise first."
                    )

                    return



                image1 = self.last_salt_pepper_image


                result = salt_pepper_average_filter(
                    image1
                )




            elif operation_name == "Salt & Pepper Median Filter":


                if self.last_salt_pepper_image is None:

                    messagebox.showerror(
                        "Missing noisy image",
                        "Apply Salt & Pepper Noise first."
                    )

                    return



                image1 = self.last_salt_pepper_image


                result = salt_pepper_median_filter(
                    image1
                )




            elif operation_name == "Salt & Pepper Outlier Method":


                if self.last_salt_pepper_image is None:


                    messagebox.showerror(
                        "Missing noisy image",
                        "Apply Salt & Pepper Noise first."
                    )

                    return



                image1 = self.last_salt_pepper_image


                result = salt_pepper_outlier_method(
                    image1
                )




            elif operation_name == "Add Gaussian Noise":


                result = add_gaussian_noise(image1)

                self.last_gaussian_image = result




            elif operation_name == "Gaussian Average Filter":


                if self.last_gaussian_image is None:


                    messagebox.showerror(
                        "Missing noisy image",
                        "Apply Gaussian Noise first."
                    )

                    return



                image1 = self.last_gaussian_image


                result = gaussian_average_filter(
                    image1
                )




            elif operation_name == "Image Averaging":



                noisy_images = [

                    add_gaussian_noise(image1),

                    add_gaussian_noise(image1),

                    add_gaussian_noise(image1)

                ]



                image1 = noisy_images[0]


                result = image_averaging(
                    noisy_images
                )




            else:


                result = NORMAL_OPERATIONS[operation_name](
                    image1
                )



            self.show_result(
                image1,
                result,
                operation_name
            )



            if operation_name in HISTOGRAM_OPERATIONS:

                show_histogram(
                    result,
                    operation_name
                )



        except Exception as error:


            messagebox.showerror(
                "Processing Error",
                str(error)
            )





if __name__ == "__main__":


    app = ImageProcessingApp()

    app.mainloop()    
