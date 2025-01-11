from numerize import numerize
import streamlit as st
from streamlit_lottie import st_lottie
from KNN.knnclass import KNN_Classifier
from PIL import Image
from pyecharts.charts import Bar
from pyecharts import options as opts
from streamlit_echarts import st_pyecharts
from pyecharts.globals import ThemeType
import requests

def search():

    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_coding = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_hwcplx4x.json")

    with st.container():
        st.write("""
                <h2 style='text-align: center;'>
                Cari tau Influencermu yuk!🤩
                </h2>""", unsafe_allow_html=True)
        st_lottie(lottie_coding, height = 200, key = "home")

    with st.container():
        left, center, right = st.columns((1,1,1))
        with center:
            username = st.text_input(label="", placeholder="Masukkan id username tanpa @")
            username = username.lower()
            username = username.strip()
            # cari = st.button("🔍Cari")
    if username:
        try :
            isinfluencer = KNN_Classifier.profile_classifier(username)
            if isinfluencer == 1:
                data = KNN_Classifier.jenis_classifier(username)
                data_profile = KNN_Classifier.get_data_profile(username)
                with st.container():
                    left, center, right = st.columns((1,2,1))
                    with left:
                        st.image(f"img/{username}.jpg", width=200)
                    with center:
                        with st.container():
                            if data_profile['verified'] == 1:
                                st.write(f"""
                                ### {data_profile["username"]} ✔""")
                            else:
                                st.write(f"""
                                ### {data_profile["username"]}""")
                            st.write(f"""###### {numerize.numerize(data_profile["count_follower"])} Followers | {numerize.numerize(data_profile["post_count"])} Posts""")
                            st.write(f"""
                            ###### {data_profile["fullname"]}""")
                            st.write(f"""
                            {data_profile["bio"]}
                            """)
                    with right:
                            st.write("Jenis Influencer :")
                            st.write(f"""
                            #### {KNN_Classifier.influencer_classification(username)}""")
                            st.write("Persona :")
                            st.write(f"""
                            #### {data}""")
        
                display_image = KNN_Classifier.get_img_post(username)
                with st.expander(f'Engagement Rate dari @{username}'):
                    with st.container():
                        engagement_rate = KNN_Classifier.engagement_rate(username)
                        urutan = []
                        for i in range(len(engagement_rate)):
                            untuk_urutan = i+1
                            untuk_urutan = f"Post-{untuk_urutan}"
                            urutan.append(untuk_urutan)
                        bar = (
                        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
                        .add_xaxis(urutan)
                        .add_yaxis("", engagement_rate)
                        .set_global_opts(title_opts=opts.TitleOpts(title="Engagement Rate per Unggahan", subtitle="data dalam satuan persen (%)"))
                        )
                        st_pyecharts(bar)

                with st.expander(f'''9 unggahan terbaru dari @{username}'''):
                    a=0
                    for i in range(3):
                        if a<9:
                            with st.container():
                                left, center, right = st.columns((1,1,1))
                                list_like = display_image.get('like')
                                list_comment = display_image.get('comment')
                                with left:
                                    image = Image.open(f"img_post/{username}{a}.jpg")
                                    st.image (image, width = 375)
                                    st.write (f""" <h4 style='text-align: center;'> ❤️ {numerize.numerize(list_like[a])} | 💬 {numerize.numerize(list_comment[a])} </h3>""", unsafe_allow_html=True)
                                    a = a+1
                                with center:
                                    image = Image.open(f"img_post/{username}{a}.jpg")
                                    st.image (image, width = 375)
                                    st.write (f""" <h4 style='text-align: center;'> ❤️ {numerize.numerize(list_like[a])} | 💬 {numerize.numerize(list_comment[a])} </h3>""", unsafe_allow_html=True)
                                    a = a+1
                                with right:
                                    image = Image.open(f"img_post/{username}{a}.jpg")
                                    st.image (image, width = 375)
                                    st.write (f""" <h4 style='text-align: center;'> ❤️ {numerize.numerize(list_like[a])} | 💬 {numerize.numerize(list_comment[a])} </h3>""", unsafe_allow_html=True)
                                    a = a+1
            else:
                data_profile = KNN_Classifier.get_data_profile(username)
                with st.container():
                        left, center, right = st.columns((1,2,1))
                        with left:
                            st.image(f"img/{username}.jpg", width=200)
                        with center:
                            with st.container():
                                st.write(f"""
                                ### {data_profile["username"]}""")
                                st.write(f"""###### {numerize.numerize(data_profile["count_follower"])} Followers | {numerize.numerize(data_profile["post_count"])} Posts""")
                                st.write(f"""
                                ###### {data_profile["fullname"]}""")
                                st.write(f"""
                                {data_profile["bio"]}
                                """)
                            with right:
                                st.write("Jenis Influencer :")
                                st.write(f"""
                                #### Bukan Influencer😐""")
                                st.write("Persona :")
                                st.write(f"""
                                #### -""")
                with st.container():
                    left, center, right = st.columns((1,2,1))
                    with center:
                        st.error ('⛔ Tentu saja informasi yang kamu cari tidak ada disini')
        except :
            st.error("Sepertinya Username yang kamu masukin kurang tepat🤔")
    back = st.button("🔙")
    if back:
        st.session_state.active_page = 'Landing'
search()
