import cv2
import gradio as gr


def rgb_to_gray(image):
    output = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return output


def main():
    interface = gr.Interface(fn=rgb_to_gray, inputs=gr.Image(), outputs=gr.Image())
    # BUG: gradio 摄像头打不开
    # interface = gr.Interface(lambda x: x, gr.Image(sources=["webcam"], streaming=True), gr.Image(), live=True)
    interface.launch(inbrowser=True)


if __name__ == '__main__':
    main()
