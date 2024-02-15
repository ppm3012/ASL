import streamlit as st
import helper
import cv2

st.set_page_config(page_title="Art of Silence",
                   page_icon="📝", layout="wide")


def main():
    helper.initialize_UI_session_states()

    st.markdown("<h1 style = 'text-align : left;'> Learn Sign Language with Us </h1>",
                unsafe_allow_html=True)

    st.markdown(
        "This project aims to provide a tool in improving the communication with people with hearing impariments. This project has four features: Sign Language Learner, Sign Language Quiz, Sign Language Calculator, Sign Language To Text."
    )

    st.text(" \n")
    st.text(" \n")
    st.text(" \n")

    if st.session_state.menu:
        _, col_00, col_01, col_10, col_11 = st.columns([1.5, 3, 3, 3, 3])
        with col_00:
            st.image("Images/Icons/learn.png", caption="Learn", width=100)
            st.button(
                "Let's Learn", on_click=helper.change_learning_status, args=["category"])

        with col_01:
            st.image("Images/Icons/quiz.png", caption="Quiz", width=100)
            st.button("Take a Quiz", on_click=helper.take_quiz)

        with col_10:
            st.image("Images/Icons/calculator.png",
                     caption="Calculate", width=100)
            st.button("Calculator", on_click=helper.calculate)

        with col_11:
            st.image("Images/Icons/sign-language.png",
                     caption="Sign to Text", width=100)
            st.button("Sign to Text", on_click=helper.to_text)

    if st.session_state.category_learn:
        helper.initialize_learning_session_states()

        st.markdown(
            "<h2 style = 'text-align : center;'> Let's Learn </h2>", unsafe_allow_html=True)

        col_00, col_01, col_10, _ = st.columns([4, 3, 3, 2])
        with col_00:
            # st.image("Images/Icons/sign-language.png", caption = "Back", width = 100)  # To add go back icon
            st.button("Back", on_click=helper.change_status, args=["menu"])
        with col_01:
            st.image("Images/Icons/learn.png", caption="Alphabet", width=100)
            st.button("Learn Alphabets", on_click=helper.change_status,
                      args=["alphabet_learn"])
        with col_10:
            st.image("Images/Icons/digit.png", caption="Digit", width=100)
            st.button("Learn Digits", on_click=helper.change_status,
                      args=["digit_learn"])
    else:
        if st.session_state.alphabet_learn:
            helper.change_category()
            st.subheader("Learn Alphabets")

            left_col, right_col = st.columns(2)
            with left_col:
                QUIZ_WINDOW = st.image([])
            with right_col:
                FRAME_WINDOW = st.image([])

            _, _, _, col_00, _, _, _ = st.columns([5, 5, 5, 3, 5, 5, 5])
            with col_00:
                st.button("Capture", on_click=helper.stop_streaming)

            helper.learn_sign(QUIZ_WINDOW, FRAME_WINDOW)
            helper.show_result()

            _, _, col_000, col_001, col_010, col_011, col_100, col_101, _, _ = st.columns(
                [3, 3, 1, 1, 1, 1, 1, 1, 3, 3])
            with col_000:
                for i in list("agms"):
                    st.button(i, on_click=helper.change_learning_status,
                              args=["random", i])
            with col_001:
                for j in list("bhnt"):
                    st.button(j, on_click=helper.change_learning_status,
                              args=["random", j])
            with col_010:
                for k in list("ciouy"):
                    st.button(k, on_click=helper.change_learning_status,
                              args=["random", k])
            with col_011:
                for l in list("djpvz"):
                    st.button(l, on_click=helper.change_learning_status,
                              args=["random", l])
            with col_100:
                for m in list("ekqw"):
                    st.button(m, on_click=helper.change_learning_status,
                              args=["random", m])
            with col_101:
                for n in list("flrx"):
                    st.button(n, on_click=helper.change_learning_status,
                              args=["random", n])

        elif st.session_state.digit_learn:
            helper.change_category()
            st.subheader("Learn Digits")

            left_col, right_col = st.columns(2)
            with left_col:
                QUIZ_WINDOW = st.image([])
            with right_col:
                FRAME_WINDOW = st.image([])

            _, _, _, col_00, _, _, _ = st.columns([5, 5, 5, 3, 5, 5, 5])
            with col_00:
                st.button("Capture", on_click=helper.stop_streaming)

            helper.learn_sign(QUIZ_WINDOW, FRAME_WINDOW)
            helper.show_result()

            _, _, col_000, col_001, col_010, col_011, col_100, _, _ = st.columns(
                [3, 3, 1, 1, 1, 1, 1, 3, 3])
            with col_000:
                for i in list("05"):
                    st.button(i, on_click=helper.change_learning_status,
                              args=["random", i])
            with col_001:
                for j in list("16"):
                    st.button(j, on_click=helper.change_learning_status,
                              args=["random", j])
            with col_010:
                for k in list("27"):
                    st.button(k, on_click=helper.change_learning_status,
                              args=["random", k])
            with col_011:
                for l in list("38"):
                    st.button(l, on_click=helper.change_learning_status,
                              args=["random", l])
            with col_100:
                for m in list("49"):
                    st.button(m, on_click=helper.change_learning_status,
                              args=["random", m])

    if "quiz" in st.session_state and st.session_state.quiz:
        helper.initialize_quiz_session_states()

        st.markdown(
            "<h2 style = 'text-align : center;'> Take a Quiz </h2>", unsafe_allow_html=True)

        col_00, _, _, _ = st.columns([4, 3, 3, 2])
        with col_00:
            # st.image("Images/Icons/sign-language.png", caption = "Back", width = 100)  # To add go back icon
            st.button("Back", on_click=helper.change_status, args=["menu"])

        left_col, right_col = st.columns(2)
        with left_col:
            QUIZ_WINDOW = st.image([])
        with right_col:
            FRAME_WINDOW = st.image([])

        _, _, _, col_00, _, _, _ = st.columns([5, 5, 5, 3, 5, 5, 5])
        with col_00:
            st.button("Capture", on_click=helper.stop_streaming)

        st.session_state.result_quiz = helper.test(
            QUIZ_WINDOW, FRAME_WINDOW, st.session_state.quiz_item, helper.load_image(st.session_state.quiz_item))

        if st.session_state.result_quiz:
            st.session_state.score += 10
        else:
            st.session_state.wrong_answers += st.session_state.quiz_item

        helper.show_result()

        st.progress(st.session_state.quiz_count * 10)

    if "revision" in st.session_state and st.session_state["revision"]:
        col_00, _, _, _ = st.columns([4, 3, 3, 2])
        with col_00:
            # st.image("Images/Icons/sign-language.png", caption = "Back", width = 100)  # To add go back icon
            st.button("Back", on_click=helper.take_quiz)

        if st.session_state.score >= 50:
            html_str = f"""<h4 style = 'text-align : center; color : green'> You passed! Your score is {st.session_state.score} </h4>"""
            st.markdown(html_str, unsafe_allow_html=True)
        else:
            html_str = f"""<h4 style = 'text-align : center; color : red'> You failed! Your score is {st.session_state.score} </h4>"""
            st.markdown(html_str, unsafe_allow_html=True)

        if len(st.session_state.wrong_answers) >= 0:
            st.markdown(
                "<h4 style = 'text-align : center; color : blue'> Please Review These", unsafe_allow_html=True)

            for wrong_answer in st.session_state.wrong_answers:
                helper.revision_page(wrong_answer)

    if "calculate" in st.session_state and st.session_state["calculate"]:
        helper.initialize_calculator_session_states()

        check = st.checkbox("Show Instructions")
        if check:
            info_style = """
            <style>
                p{
                    font-size : 13px;
                    font-family : sans-serif;
                    font-weight : bold
                }
            </style>
            """
            st.markdown(info_style, unsafe_allow_html=True)
            st.write("Firstly, click 'Start Process' button to start Sign Language Calculator Proces and click 'Show Results' button to check the calculation results.")
            col_00, col_01 = st.columns(2)
            with col_00:
                st.info("Make sure 'A' sign for '\+' Plus Operator!")
                st.info("Make sure 'C' sign for '\*' Multiply Operator!")
            with col_01:
                st.info("Make sure 'B' sign for '\-' Minus Operator!")
                st.info("Make sure 'D' sign for '\/' Division Operator!")

        btn_style = """
        <style>
            div.stButton > button : first-child {
                background-color : #b3cff7;
                color : #000000;
            }
            div.stButton > button:hover {
                background-color : #c8d5e8;
                color : #172b47
            }
        </style>
        """
        btn_design = st.markdown(btn_style, unsafe_allow_html=True)
        col_00, col_01, col_10, _ = st.columns([4, 3, 3, 2])
        with col_00:
            # st.image("Images/Icons/sign-language.png", caption = "Back", width = 100)  # To add go back icon
            st.button("Back", on_click=helper.change_status, args=["menu"])
        with col_01:
            start = st.button("Start Video")
        with col_10:
            end = st.button("Show Results")

        if start:
            FRAME_WINDOW = st.image([])
            cam = cv2.VideoCapture(0)
            value, prev_label, count = "", "", 0

            while True:
                frame, hand = helper.stream(cam, FRAME_WINDOW)
                label_predicted = helper.predict_label(hand)
                cv2.putText(frame, label_predicted, (90, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                if label_predicted == "U":
                    st.session_state["value"] = value
                    cam.release()
                    break

                if prev_label == label_predicted:
                    count += 1
                    if count > 9:
                        if label_predicted == "V":
                            label_predicted = "+"
                        elif label_predicted == "L":
                            label_predicted = "="
                        elif label_predicted == "del":
                            value = value[:-1]
                        elif label_predicted == "nothing":
                            label_predicted = ""
                        value += label_predicted
                        st.session_state["value"] = value
                        prev_label = ""
                else:
                    prev_label = label_predicted
                    count = 1
                cv2.putText(frame, value, (90, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                FRAME_WINDOW.image(frame)

        if end:
            answer = 0
            st.text("")
            st.success("This is the result of calculation.")
            equation = st.session_state.value
            if equation[1] == "+":
                answer = int(equation[0]) + int(equation[2])
            elif equation[1] == "-":
                answer = int(equation[0]) - int(equation[2])
            elif equation[1] == "*":
                answer = int(equation[0]) * int(equation[2])
            elif equation[1] == "/":
                answer = int(equation[0]) / int(equation[2])
            result_text = """
            <style>
                p{
                    font-size : 25px;
                    font-weight : bold
                }
            </style>
            """
            st.markdown(result_text, unsafe_allow_html=True)
            st.write("{} = {}".format(st.session_state.value, answer))

    if "to_text" in st.session_state and st.session_state.to_text:
        helper.initialize_sign_to_text_session_states()

        btn_style = """
        <style>
            div.stButton > button : first-child {
                background-color : #0099ff;
                color : #ffffff
            }
            div.stButton > button : hover {
                background-color : #ffffff;
                color : #000000
            }
        </style>
        """
        btn_design = st.markdown(btn_style, unsafe_allow_html=True)
        col_00, col_01, col_10, _ = st.columns([4, 3, 3, 2])
        with col_00:
            # st.image("Images/Icons/sign-language.png", caption = "Back", width = 100)  # To add go back icon
            st.button("Back", on_click=helper.change_status, args=["menu"])
        with col_01:
            start = st.button("Start Video")
        with col_10:
            end = st.button("Check")

        if start:
            FRAME_WINDOW = st.image([])
            cam = cv2.VideoCapture(0)
            value, prev_label, count = "", "", 0

            while True:
                frame, hand = helper.stream(cam, FRAME_WINDOW)
                label_predicted = helper.predict_label(hand)
                frame_copy = frame.copy()
                cv2.putText(frame_copy, label_predicted, (90, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                if label_predicted == "U":
                    st.session_state["value"] = value
                    cam.release()
                    break

                if prev_label == label_predicted:
                    count += 1

                    if count > 20:
                        if label_predicted == "space":
                            label_predicted = " "
                        elif label_predicted == "del":
                            value = value[:-1]
                            label_predicted = ""
                        elif label_predicted == "nothing":
                            label_predicted = ""
                        value += label_predicted
                        st.session_state["value"] = value
                        prev_label = ""
                else:
                    prev_label = label_predicted
                    count = 1

                cv2.putText(frame, value, (90, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                FRAME_WINDOW.image(frame)
        if end:
            label_style = """
            <style>
                p{
                    font-size : 18px;
                    font-weight : bold
                }
            </style>
            """
            st.markdown(label_style, unsafe_allow_html=True)
            st.write("The texts you wrote using sign language is : {}".format(
                st.session_state.value))


if __name__ == "__main__":
    main()
