import torch
import config
import utils
import glob
import numpy as np
import cv2

def inference_1img(model, img_name, device):
    img = cv2.imread(img_name)

    # display
    cv2.imshow("input image", img)
    cv2.waitKey(0)

    # convert to tensor
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.float32)
    img /= 255.0
    img = np.transpose(img, (2,0,1)) # HWC -> CHW
    img = torch.tensor(img, dtype=torch.float).to(device)
    img = torch.unsqueeze(img,0) # add batch dim

    with torch.no_grad():
        prediction = model(img)
    print(f"inference on {img_name} done.")




def main():
    # load model
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    saved_name='result/last_model.pth'
    checkpoint = torch.load(saved_name, map_location=device)
    model = utils.get_model_object_detector(config.num_classes)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device).eval()

    # load data
    test_dir = 'data/test'
    img_format="jpg"
    test_imgs = glob.glob(f"{test_dir}/*.{img_format}")

    # prepare for drawing
    class_colors = np.random.uniform(0, 255, size=(config.num_classes, 3))

    # inference
    for i in range(len(test_imgs)):
        img_name = test_imgs[i]
        inference_1img(model, img_name, device)

if __name__ == "__main__":
    main()
