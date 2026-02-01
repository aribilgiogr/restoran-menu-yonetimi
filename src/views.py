import os.path
import uuid

import pandas as pd
import streamlit as st

import src.database as db


def _menu_item_card(menu_item):
    with st.container():
        c1, c2 = st.columns([.3, .7])
        c1.image(menu_item['gorsel_yolu'])
        with c2:
            st.write(f"#### {menu_item['isim']}")
            st.write(f"**{menu_item['kategori']}**")
            st.metric("", f"₺{menu_item['fiyat']:.2f}")
            if menu_item['aciklama']:
                st.text(menu_item['aciklama'])
    st.divider()

def _list_item_card(list_item):
    with st.container():
        c1,c2,c3,c4 = st.columns([1,5,2,1])
        c1.image(list_item['gorsel_yolu'])
        c2.write(f"**{list_item['isim']}**")
        c2.text(list_item['aciklama'])
        c3.text(f"₺{list_item['fiyat']}")
        if c4.button("Sil",key=f'sil_{list_item["id"]}',width="stretch"):
            db.sil(list_item["id"])
            st.rerun()

def menu_sayfasi():
    st.subheader("Menü", divider=True, text_alignment="center")
    menu = db.menuyu_getir()

    if menu:
        df = pd.DataFrame(menu, columns=["id", "isim", "aciklama", "kategori", "fiyat", "gorsel_yolu"])
        for idx, row in df.iterrows():
            _menu_item_card(row)
    else:
        st.info("Menüde henüz ürün bulunmamaktadır!")


def yonetim_sayfasi():
    st.subheader("Ürün Yönetimi", divider=True, text_alignment="center")
    with st.form("ekle_form", True, enter_to_submit=False):
        c1, c2, c3 = st.columns(3)
        isim = c1.text_input("İsim: *")
        fiyat = c2.number_input("Fiyat: *")
        kategori = c3.text_input("Kategori: *")
        gorsel = st.file_uploader("Ürün Görseli: *")
        aciklama = st.text_area("Açıklama:")
        if st.form_submit_button("Ekle", type="primary", use_container_width=True):
            if isim and fiyat and kategori and gorsel:
                gorsel_yolu = os.path.join("src", "img", f"{uuid.uuid4()}{os.path.splitext(gorsel.name)[1]}")
                with open(gorsel_yolu, "wb") as f:
                    f.write(gorsel.getbuffer())
                db.ekle(isim, kategori, fiyat, gorsel_yolu, aciklama)
                st.rerun()
            else:
                st.warning("Lütfen tüm zorunlu alanları doldurun.")

    st.write("**Kayıtlı Ürünler:**")
    menu = db.menuyu_getir()

    if menu:
        print(menu)
        df = pd.DataFrame(menu, columns=["id", "isim", "aciklama", "kategori", "fiyat", "gorsel_yolu"])
        for idx,row in df.iterrows():
            _list_item_card(row)
    else:
        st.info("Menüde henüz ürün bulunmamaktadır!")
