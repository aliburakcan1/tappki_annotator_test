import streamlit as st
import random
from tweet import Tweet
from functions import split_lines, write_to_db, find_record_by_id
st.set_page_config(layout="wide")

if "tweet_ids" not in st.session_state:
    st.session_state.tweet_ids = list(split_lines("tweet_ids"))

if "tweet_id" not in st.session_state:
    st.session_state.tweet_id = random.choice(st.session_state.tweet_ids)

if "list_elements" not in st.session_state:
    multiselect_dict = {
        "people": list(split_lines("person")),
        "tags": list(split_lines("tag")),
        "programs": ["-"] + list(split_lines("program")),
        "sports": ["-"] + list(split_lines("sport")),
        "animals": ["-"] + list(split_lines("animal")),
    }
    st.session_state.list_elements = multiselect_dict

#print({k:v for k,v in st.session_state.items() if k != "tweet_ids"})



col1, col2 = st.columns(2)

with col1:
    new_tweet = st.session_state.next if "next" in st.session_state else False
    if new_tweet:
        current_tweet_id = random.choice(st.session_state.tweet_ids)
        tweet = Tweet("https://twitter.com/i/status/{}".format(current_tweet_id), tweet_ids=st.session_state.tweet_ids)
        current_tweet_id = tweet.get_tweet_id()
        tweet.component()
        st.session_state.tweet_id = current_tweet_id
    else:
        Tweet("https://twitter.com/i/status/{}".format(st.session_state.tweet_id), st.session_state.tweet_ids).component()
        

with col2:
    if new_tweet:
        
        video_labels = find_record_by_id(
                            username=st.secrets["username"],
                            password=st.secrets["password"],
                            database=st.secrets["database"],
                            tweet_id=st.session_state["tweet_id"]
                            )
        print("tweet_id", st.session_state.tweet_id, "video_labels", video_labels)
        if not video_labels:
            video_labels = dict(
                title="",
                content="",
                people=[],
                tags=[],
                program="-",
                sport="-",
                animal="-",
                music=""
            )
        for k,v in video_labels.items():
            st.session_state[k] = v

    #print({k:v for k,v in st.session_state.items() if k != "tweet_ids"})
    col1, col2 = st.columns(2)
    list_elements = st.session_state["list_elements"]
    if "add" in st.session_state:
        if st.session_state.add:
            if st.session_state.add_type == "Kişi":
                if st.session_state.add_input.lower() not in [i.lower() for i in st.session_state.list_elements["people"]]:
                    st.session_state.list_elements["people"].insert(0, st.session_state.add_input)
            elif st.session_state.add_type == "Etiket":
                if st.session_state.add_input.lower() not in [i.lower() for i in st.session_state.list_elements["tags"]]:
                    st.session_state.list_elements["tags"].insert(0, st.session_state.add_input)
            elif st.session_state.add_type == "Film - Dizi - Program - YT kanalı":
                if st.session_state.add_input.lower() not in [i.lower() for i in st.session_state.list_elements["programs"]]:
                    st.session_state.list_elements["programs"].insert(0, st.session_state.add_input)
            elif st.session_state.add_type == "Spor":
                if st.session_state.add_input.lower() not in [i.lower() for i in st.session_state.list_elements["sports"]]:
                    st.session_state.list_elements["sports"].insert(0, st.session_state.add_input)
            elif st.session_state.add_type == "Hayvan":
                if st.session_state.add_input.lower() not in [i.lower() for i in st.session_state.list_elements["animals"]]:
                    st.session_state.list_elements["animals"].insert(0, st.session_state.add_input)
            else:
                st.error("Bir hata oluştu")
    with col1:
        

        #for k,v in video_labels.items():
        #    st.session_state[k] = v
        #for k,v in st.session_state.items():
        #    if k not in ["tweet_ids", "tweet_id", "list_elements"]:
        #        print(k, v)
        title = st.text_input("Başlık", key="title", placeholder="Tepki Başlığı")
        content = st.text_area("İçerik", key="content", placeholder="Tepkinin içinde geçen tüm cümleyi/cümleleri yazın.")
        people = st.multiselect("Kişiler", list_elements["people"], key="people", help="Tepkinin içinde varsa fenomenleri/ünlüleri seçin.")
        tags = st.multiselect("Etiketler", list_elements["tags"], key="tags", help="Tepki için en uygun olan etiketleri seçin.")
    with col2:
        program = st.selectbox("Film - Dizi - Program - YT kanalı", list_elements["programs"], key="program", help="Tepkinin hangi program içerisinde gerçekleştiğini girin.")
        sport = st.selectbox("Spor", list_elements["sports"], key="sport", help="Tepkinin hangi spor dalı ile ilgili olduğunu seçin.")
        animal = st.selectbox("Hayvan", list_elements["animals"], key="animal", help="Tepkinin hangi hayvan ile ilgili olduğunu seçin.")
        music = st.text_input("Müzik", key="music", placeholder="Müzik", help="Tepkinin içinde geçen müzik varsa yazın.")
    
        if st.button("Tepkiyi Kaydet", key="save", type="primary", use_container_width=True):
            #print({"tweet_id": st.session_state["tweet_id"], "title": title, "content": content, "people": people, "tags": tags, "program": program, "music": music, "animal": animal})
            st.success("Kaydedildi Sırada ki tweet'e geçebilirsiniz.")
        
        st.button("Sonraki Tweet", key="next", type="secondary", use_container_width=True)
    
    with st.expander("Tepkide var seçeneklerde yoksa buraya tıklayın"):
        type_list = ["Kişi", "Etiket", "Film - Dizi - Program - YT kanalı", "Spor", "Hayvan"]
        add_type = st.selectbox("Tip", type_list, key="add_type", help="Ekleme yapmak istediğiniz seçeneği seçin.", label_visibility="collapsed")
        add_input = st.text_input("Değer", key="add_input", placeholder=f"Eklemek istediğiniz {add_type} girin.", help=f"{add_type} adını girin.", label_visibility="collapsed")
        st.session_state.added_key = add_type
        st.session_state.added_val = add_input
        
        if st.button("Ekle", key="add", type="primary", use_container_width=True):
            st.success(f"{add_input} ismindeki {add_type} eklendi")


if "save" in st.session_state:
    if st.session_state.save:
        write_to_db(
                username=st.secrets["username"],
                password=st.secrets["password"],
                database=st.secrets["database"],
                collection={
                    "tweet_id": st.session_state["tweet_id"], 
                    "title": title, "content": content, 
                    "people": people, "tags": tags, 
                    "program": program, "music": music, 
                    "animal": animal, "sport": sport
                    }
            )