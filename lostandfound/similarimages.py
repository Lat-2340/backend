from keras.preprocessing.image import load_img, img_to_array
from keras.applications.vgg16 import VGG16, preprocess_input
from keras import Model
from .utils import get_image_filename
import heapq
import os
import numpy as np


def load_image_from_file(filepath):
    img = load_img(filepath, target_size=(224, 224))
    img = img_to_array(img)
    return img


def get_all_files(folder):
    files = []
    for filename in os.listdir("./media/"+folder):
        if filename is not None and filename != ".DS_Store":
            files.append(filename)
    print(files)
    return files


def collect_data(file_path, match_folder):
    to_match_img = load_image_from_file(file_path)
    match_files = get_all_files(match_folder)
    total_max = len(match_files) + 1
    batch = total_max
    min_idx = 0
    max_idx = min_idx + batch
    dim = 224
    X = np.zeros(((max_idx-min_idx), dim, dim, 3))
    X[0, :, :, :] = to_match_img
    for i in range(min_idx+1, max_idx):
        img = load_image_from_file(os.path.join("./media/"+match_folder, match_files[i-1]))
        X[i-min_idx, :, :, :] = img
    #X = preprocess_input(X)
    return X, match_files


def create_model_one():
    vgg = VGG16(include_top=True, weights='imagenet')
    model2 = Model(vgg.input, vgg.layers[-2].output)
    model2.save('vgg_4096.h5')
    return model2


def create_model():
    model = VGG16(include_top=False, weights='imagenet')
    return model


def compute_K_nearst_neighbour(preds, match_file, K):
    a = preds[0]
    heap = []
    K = K
    print("input feature", a.shape)
    for i, b in enumerate(preds[1:, :]):
        dot = np.dot(a, b)
        norma = np.linalg.norm(a)
        normb = np.linalg.norm(b)
        cos = dot / (norma * normb)
        print(match_file[i], cos)
        heapq.heappush(heap, [cos, i])
        if len(heap) > K:
            heapq.heappop(heap)
    return heap


def get_similar_image(itemid, match_folder, K):
    filepath = get_image_filename(itemid, match_folder == "found/")
    X, match_files = collect_data(filepath, match_folder)
    model = create_model_one()
    preds = model.predict(X)
    print(X.shape)
    print("preds size", preds.shape[0])

    # reshape for the model with no fully connected layer
    #cols = int(preds.ravel().shape[0]/preds.shape[0])
    #shp = (preds.shape[0], cols)
    #preds = preds.reshape(shp)

    similar_imgs = compute_K_nearst_neighbour(preds, match_files, K)
    for i in range(len(similar_imgs)):
        similar_imgs[i][0] = round(float(similar_imgs[i][0]), 2)
        similar_imgs[i][1] = match_files[similar_imgs[i][1]]

    return similar_imgs


if __name__ == "__main__":
    res = get_similar_image("id2", "found/", 3)
    print(res)
