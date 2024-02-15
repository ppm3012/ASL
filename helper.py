import streamlit as st
import random
import cv2
import time
import string
from keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np


def initialize_UI_session_states():
    if "classes" not in st.session_state:
        st.session_state["classes"] = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "L", "Q", "X", "Y"]

    if "alphbet_model" not in st.session_state:
        st.session_state["alphbet_model"] = load_model("Model10/my_model")

    if "digit_model" not in st.session_state:
        st.session_state["digit_model"] = load_model("mobilenet_digit_new_1")

    if "current_model" not in st.session_state:
        st.session_state["current_model"] = ""

    if "menu" not in st.session_state:
        st.session_state["menu"] = True

    if "category_learn" not in st.session_state:
        st.session_state["category_learn"] = False

    if "alphabet_learn" not in st.session_state:
        st.session_state["alphabet_learn"] = False

    if "digit_learn" not in st.session_state:
        st.session_state["digit_learn"] = False

    if "quiz" not in st.session_state:
        st.session_state["quiz"] = False

    if "calculate" not in st.session_state:
        st.session_state["calculate"] = False

    if "to_text" not in st.session_state:
        st.session_state["to_text"] = False

    if "streaming" not in st.session_state:
        st.session_state["streaming"] = True


def delete_session_keys():
    for key in st.session_state.keys():
        if key != "digit_model" and key != "alphabet_model":
            del st.session_state[key]


def change_learning_status(status, item='a'):
    st.session_state["status_learn"] = status
    if status == "random":
        st.session_state["status_learn"] = "again"
        st.session_state["current_learn"] = item
    if status == "category":
        st.session_state["category_learn"] = True
        st.session_state["menu"] = False
    st.session_state["streaming"] = True


def take_quiz():
    delete_session_keys()
    initialize_UI_session_states()
    st.session_state["menu"] = False
    st.session_state["quiz"] = True


def review():
    st.session_state["quiz"] = False
    st.session_state["revision"] = True


def calculate():
    delete_session_keys()
    initialize_UI_session_states()
    st.session_state["menu"] = False
    st.session_state["calculate"] = True


def to_text():
    delete_session_keys()
    initialize_UI_session_states()
    st.session_state["menu"] = False
    st.session_state["to_text"] = True


def initialize_learning_session_states():
    delete_session_keys()
    initialize_UI_session_states()

    if "status_learn" not in st.session_state:
        st.session_state["status_learn"] = "start"

    if "result_learn" not in st.session_state:
        st.session_state["result_learn"] = ""

    if "current_learn" not in st.session_state:
        st.session_state["current_learn"] = "a"

    st.session_state["alphabet_learn"] = False
    st.session_state["digit_learn"] = False


def change_status(category):
    st.session_state["menu"] = False
    st.session_state["category_learn"] = False
    st.session_state[category] = True
    if "quiz" in st.session_state:
        st.session_state["quiz"] = False
    if "calculate" in st.session_state:
        st.session_state["calculate"] = False
    if "to_text" in st.session_state:
        st.session_state["to_text"] = False


def change_category():
    if (st.session_state["digit_learn"] and (st.session_state["current_learn"] >= 'a' and st.session_state["current_learn"] <= 'z')):
        st.session_state["current_learn"] = '0'
        st.session_state["current_model"] = st.session_state["digit_model"]

    if (st.session_state["alphabet_learn"] and (st.session_state["current_learn"] >= '0' and st.session_state["current_learn"] <= '9')):
        st.session_state["current_learn"] = 'a'
        st.session_state["current_model"] = st.session_state["alphabet_model"]


def show_result():
    if ("result_quiz" in st.session_state and st.session_state.result_quiz) or ("result_learn" in st.session_state and st.session_state.result_learn):
        st.markdown(
            "<h4 style = 'text-align : center; color : green'> Correct! </h4>", unsafe_allow_html=True)

        _, col00, _, _, col01, col10 = st.columns([1, 1, 4, 4, 1, 1])

        if "result_quiz" in st.session_state and st.session_state.result_quiz:
            with col00:
                st.button("Quit", on_click=change_status, args=["menu"])
            with col10:
                if st.session_state["quiz_count"] >= st.session_state["total_quiz"]:
                    st.button("Finish", on_click=review)
                else:
                    st.button("Next", on_click=next)
        elif "result_learn" in st.session_state and st.session_state.result_learn:
            with col00:
                st.button("Quit", on_click=change_learning_status,
                          args=["category"])
            with col01:
                st.button("Again", on_click=change_learning_status,
                          args=["again"])
            with col10:
                st.button("Next", on_click=change_learning_status,
                          args=["next"])

    else:
        st.markdown(
            "<h4 style = 'text-align : center; color : red'> Incorrect! </h4>", unsafe_allow_html=True)

        _, col00, _, _, _, col01 = st.columns([1, 1, 3, 3, 2, 2])

        if "result_quiz" in st.session_state and not st.session_state.result_quiz:
            with col00:
                st.button("Quit", on_click=change_status, args=["menu"])
            with col01:
                if st.session_state["quiz_count"] >= st.session_state["total_quiz"]:
                    st.button("Finish", on_click=review)
                else:
                    st.button("Next", on_click=next)
        elif "result_learn" in st.session_state and not st.session_state.result_learn:
            with col00:
                st.button("Quit", on_click=change_learning_status,
                          args=["category"])
            with col01:
                st.button("Again", on_click=change_learning_status,
                          args=["again"])


def learn_sign(QUIZ_WINDOW, FRAME_WINDOW):
    item = st.session_state.current_learn

    if st.session_state["status_learn"] == 'next':
        if item == 'z':
            item = 'a'
        elif item == '9':
            item = '0'
        else:
            item = chr(ord(item) + 1)

    st.markdown(f"This is a sign symbol of character {(item)} ")
    result = test(QUIZ_WINDOW, FRAME_WINDOW, item, load_image(item))

    st.session_state["result_learn"] = result
    st.session_state["current_learn"] = item


def stop_streaming():
    st.session_state["streaming"] = False


def predict_label(hand):
#    image = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(hand, cv2.COLOR_BGR2RGB)
    image = cv2.flip(hand, flipCode = 1)

    image = cv2.resize(image, (224, 224))
    #image = image.reshape(-1, 224, 224, 3)

    image = image.astype("float32") / 255.0
    x = img_to_array(image)
    x = np.expand_dims(image, axis=0)

    #prediction = st.session_state.model(x).numpy()
    prediction = st.session_state.current_model.predict(x)
    label_id = np.argmax(prediction)
    label = st.session_state.classes[label_id]
    print(label_id)
    print(label)

    return label


def test(QUIZ_WINDOW, FRAME_WINDOW, test_item, test_image):
    QUIZ_WINDOW.image(test_image)

    frame, hand = capture(st.session_state.streaming, FRAME_WINDOW)

    #resized_frame = predict_label(hand)

    FRAME_WINDOW.image(hand)

    if predict_label(hand) == str.upper(test_item):
        return True
    else:
        return False


def capture(streaming, FRAME_WINDOW):
    cam = cv2.VideoCapture(0)

    frame, hand = capture_timer(streaming, FRAME_WINDOW, cam)
    cam.release()
    return frame, hand


def capture_timer(streaming, FRAME_WINDOW, cam):
    if streaming == False:
        start_time = time.time()
        seconds = 6

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > seconds:
                break

            frame, hand = stream(cam, FRAME_WINDOW, True,
                                 seconds - elapsed_time)
    else:
        while True:
            frame, hand = stream(cam, FRAME_WINDOW)
    return frame, hand


def stream(cam, FRAME_WINDOW, is_counting=False, count_down=None):
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame_copy = frame.copy()
    if is_counting:
        frame_copy = cv2.putText(frame_copy, "Capture in " + str(int(count_down)),
                                 (25, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 5, cv2.LINE_AA)

    height, width, _ = frame_copy.shape

    start_x = int(width / 2) + int(width / 10)
    end_x = width - int(width / 10)

    rect_width = end_x - start_x

    start_y = int(height / 2) - int(rect_width / 2)
    end_y = int(height / 2) + int(rect_width / 2)

    cv2.rectangle(frame_copy, (start_x, start_y),
                  (end_x, end_y), (0, 255, 255), 10)
    FRAME_WINDOW.image(frame_copy)
    return frame_copy, frame[start_y: end_y, start_x: end_x]


def load_image(item):
    if st.session_state["quiz"]:
        image = cv2.imread("Images/ASL/Letters/" + item + ".jpg")
    else:
        image = cv2.imread("Images/ASL/Hand Signs/" + item + ".jpeg")
        image = cv2.flip(image, 1)
    image = cv2.resize(image, (1280, 720))
    return image


def load_random_item(test_list):
    test_item = random.choice(test_list)
    test_list.remove(test_item)
    test_image = load_image(test_item)
    return test_item, test_image, test_list


def initialize_quiz_session_states():
    if "random_seed" not in st.session_state:
        st.session_state["random_seed"] = random.seed(random.random())

    if "quiz_list" not in st.session_state:
        st.session_state["quiz_list"] = list(
            string.ascii_lowercase) + [str(num) for num in range(10)]
        random.shuffle(st.session_state.quiz_list)

    if "quiz_item" not in st.session_state and "quiz_image" not in st.session_state:
        st.session_state["quiz_item"], st.session_state["quiz_image"], st.session_state["quiz_list"] = load_random_item(
            st.session_state.quiz_list)

    if "total_quiz" not in st.session_state:
        st.session_state["total_quiz"] = 3

    if "quiz_count" not in st.session_state:
        st.session_state["quiz_count"] = 1

    if "result_quiz" not in st.session_state:
        st.session_state["result_quiz"] = None

    if "score" not in st.session_state:
        st.session_state["score"] = 0

    if "revision" not in st.session_state:
        st.session_state["revision"] = False

    if "wrong_answers" not in st.session_state:
        st.session_state["wrong_answers"] = []


def next():
    st.session_state.quiz_count += 1
    st.session_state.streaming = True
    st.session_state["quiz_item"], st.session_state["quiz_image"], st.session_state["quiz_list"] = load_random_item(
        st.session_state.quiz_list)


def revision_page(wrong_answer):
    ans_image = cv2.imread("Images/ASL/Letters/" + wrong_answer + ".jpg")
    ans_image = cv2.resize(ans_image, (1280, 720))
    ans_image = cv2.cvtColor(ans_image, cv2.COLOR_BGR2RGB)

    sign_image = cv2.imread("Images/ASL/Hand Signs/" + wrong_answer + ".jpeg")
    sign_image = cv2.resize(sign_image, (1280, 720))
    sign_image = cv2.cvtColor(sign_image, cv2.COLOR_BGR2RGB)

    left_col, right_col = st.columns(2)
    with left_col:
        st.image(ans_image)
    with right_col:
        st.image(sign_image)


def initialize_calculator_session_states():
    if "value" not in st.session_state:
        st.session_state["value"] = ""


def initialize_sign_to_text_session_states():
    if "value" not in st.session_state:
        st.session_state["value"] = ""
