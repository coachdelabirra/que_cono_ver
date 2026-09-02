"""
🍿 Que coño ver !!!  #YConCervezaEsMejor
==========================================
App Streamlit, 100% Python, sin APIs ni servicios externos.
Base de datos: SQLite local. Interfaz: estilo retro 8-bit (NES).

Autor: generado para Rock And Birra Radio - www.rockandbirra.com
"""

import os
import uuid
import streamlit as st

import database as db
from database import RATING_LEVELS
import utils

APP_TITLE = "🍿 Que coño ver !!!"
APP_TAG = "#YConCervezaEsMejor"
ROCKANDBIRRA_URL = "https://rockandbirra.com/"
LOGO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.jpg")
COVERS_DIR = db.COVERS_DIR

st.set_page_config(
    page_title="Que coño ver !!!",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded",
)

db.init_db()

# ---------------------------------------------------------------------------
# ESTILO RETRO NES (CSS puro, sin librerías externas)
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

html, body, [class*="css"]  {
    font-family: 'Press Start 2P', monospace;
}

.stApp {
    background: repeating-linear-gradient(
        0deg, #141218, #141218 2px, #17151b 2px, #17151b 4px
    );
    color: #f5f5f5;
}

h1, h2, h3, h4 {
    font-family: 'Press Start 2P', monospace !important;
    color: #de8d3f !important;
    text-shadow: 3px 3px 0px #000000;
    letter-spacing: 1px;
}

p, div, span, label, li {
    font-family: 'VT323', 'Press Start 2P', monospace;
}

/* ---------- Botones estilo NES (pixel, con relieve) ---------- */
.stButton > button, .stLinkButton > a, .stDownloadButton > button {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 11px !important;
    background: #de8d3f !important;
    color: #141218 !important;
    border: 3px solid #141218 !important;
    border-radius: 0px !important;
    box-shadow: 4px 4px 0px #000000 !important;
    padding: 10px 14px !important;
    transition: transform 0.08s ease-in-out;
}
.stButton > button:hover, .stLinkButton > a:hover, .stDownloadButton > button:hover {
    transform: translate(2px, 2px);
    box-shadow: 2px 2px 0px #000000 !important;
    background: #f0a75a !important;
}

/* ---------- Sidebar tipo "cartucho" ---------- */
section[data-testid="stSidebar"] {
    background: #0f0d12;
    border-right: 6px solid #de8d3f;
}
section[data-testid="stSidebar"] label {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 11px !important;
    color: #f5f5f5 !important;
    padding: 6px 4px;
    transition: transform 0.12s ease-in-out, color 0.12s ease-in-out;
    display: inline-block;
}
section[data-testid="stSidebar"] label:hover {
    transform: scale(1.15);
    color: #de8d3f !important;
}

/* ---------- Tarjetas de items ---------- */
.nes-card {
    background: #1f1c26;
    border: 3px solid #de8d3f;
    box-shadow: 6px 6px 0px #000000;
    padding: 14px;
    margin-bottom: 16px;
    border-radius: 0px;
}

.pixel-hint {
    color: #f0a75a;
    font-family: 'Press Start 2P', monospace;
    font-size: 12px;
    text-align: center;
    animation: blink 1s step-start infinite;
    margin-bottom: 6px;
}
@keyframes blink { 50% { opacity: 0; } }

.rating-tag {
    display: inline-block;
    background: #de8d3f;
    color: #141218;
    font-family: 'Press Start 2P', monospace;
    font-size: 11px;
    padding: 4px 8px;
    border: 2px solid #000;
    margin-top: 6px;
}

hr { border-color: #de8d3f !important; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ESTADO DE SESION
# ---------------------------------------------------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None


def save_uploaded_cover(uploaded_file):
    if uploaded_file is None:
        return None
    ext = os.path.splitext(uploaded_file.name)[1] or ".jpg"
    fname = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(COVERS_DIR, fname)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path


# ---------------------------------------------------------------------------
# PANTALLA DE LOGIN ("INSERT COIN")
# ---------------------------------------------------------------------------
def login_screen():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        st.markdown(f"<h1 style='text-align:center;'>{APP_TITLE}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='pixel-hint'>{APP_TAG}</p>", unsafe_allow_html=True)
        st.markdown("<div class='pixel-hint'>▼ INSERT COIN — ES AQUÍ, PINCHA ▼</div>", unsafe_allow_html=True)

        st.markdown("### 🎮 Jugador existente")
        users = db.get_users()
        names = [u["username"] for u in users]
        if names:
            chosen = st.selectbox("Elige tu jugador", options=["—"] + names, label_visibility="collapsed")
            if st.button("▶ CONTINUAR", use_container_width=True):
                if chosen and chosen != "—":
                    u = db.get_user_by_name(chosen)
                    st.session_state.user_id = u["id"]
                    st.rerun()
                else:
                    st.warning("Elige un jugador primero.")
        else:
            st.info("Aún no hay jugadores. ¡Crea el primero!")

        st.markdown("### 🆕 Nuevo jugador")
        avatar = st.selectbox("Avatar", ["🎮", "🍺", "🎸", "🍿", "👾", "🧟", "🎃", "🏆"])
        new_name = st.text_input("Nombre de jugador", max_chars=20, label_visibility="collapsed",
                                  placeholder="Nombre de jugador")
        if st.button("＋ CREAR JUGADOR", use_container_width=True):
            if new_name.strip():
                ok, msg = db.create_user(new_name, avatar)
                if ok:
                    u = db.get_user_by_name(new_name.strip())
                    st.session_state.user_id = u["id"]
                    st.rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Escribe un nombre.")

        st.divider()
        st.link_button("🌐 ROCK AND BIRRA RADIO", ROCKANDBIRRA_URL, use_container_width=True)


# ---------------------------------------------------------------------------
# SECCIONES DE LA APP (con sesión iniciada)
# ---------------------------------------------------------------------------
def render_item_form(user_id, category, edit_item=None):
    """Formulario para añadir o editar una peli/serie."""
    label = "película" if category == "pelicula" else "serie"
    key_prefix = f"{category}_{edit_item['id'] if edit_item else 'new'}"

    with st.form(key=f"form_{key_prefix}", clear_on_submit=(edit_item is None)):
        title = st.text_input(f"Título de la {label}", value=edit_item["title"] if edit_item else "")
        rating = st.select_slider(
            "🍺 Calificación (six pack de birras)",
            options=list(RATING_LEVELS.keys()),
            value=edit_item["rating"] if edit_item else 3,
            format_func=lambda k: RATING_LEVELS[k],
        )
        notes = st.text_area("Notas (opcional)", value=edit_item["notes"] if edit_item and edit_item["notes"] else "")
        cover = st.file_uploader("Portada (opcional, desde tu teléfono)", type=["png", "jpg", "jpeg", "webp"])
        submitted = st.form_submit_button("💾 GUARDAR" if edit_item else f"＋ AÑADIR {label.upper()}")

        if submitted:
            if not title.strip():
                st.warning("El título no puede estar vacío.")
                return
            cover_path = save_uploaded_cover(cover) if cover else None
            if edit_item:
                db.update_item(edit_item["id"], title, rating, notes, cover_path=cover_path)
                st.success("¡Actualizado!")
            else:
                db.add_item(user_id, title, category, rating, cover_path=cover_path, notes=notes)
                st.success(f"¡{label.capitalize()} añadida!")
            st.rerun()


def render_item_card(item, allow_edit=True):
    with st.container():
        st.markdown("<div class='nes-card'>", unsafe_allow_html=True)
        cols = st.columns([1, 3])
        with cols[0]:
            if item["cover_path"] and os.path.exists(item["cover_path"]):
                st.image(item["cover_path"], use_container_width=True)
            else:
                emoji = "🎬" if item["category"] == "pelicula" else "📺"
                st.markdown(f"<div style='font-size:48px; text-align:center;'>{emoji}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"**{item['title']}**")
            st.markdown(f"<span class='rating-tag'>{RATING_LEVELS[item['rating']]}</span>", unsafe_allow_html=True)
            if item["notes"]:
                st.caption(item["notes"])

            if allow_edit:
                bcols = st.columns(3)
                with bcols[0]:
                    if st.button("✏️ Editar", key=f"editbtn_{item['id']}"):
                        st.session_state[f"editing_{item['id']}"] = True
                with bcols[1]:
                    if st.button("🗑️ Eliminar", key=f"delbtn_{item['id']}"):
                        st.session_state.confirm_delete = item["id"]
                with bcols[2]:
                    wa_text = f"🍿 {item['title']} — {RATING_LEVELS[item['rating']]}\n{APP_TAG}\nwww.rockandbirra.com"
                    st.link_button("📲 WhatsApp", utils.whatsapp_link(wa_text), use_container_width=True)

                if st.session_state.confirm_delete == item["id"]:
                    st.warning(f"¿Seguro que quieres eliminar «{item['title']}»?")
                    ccols = st.columns(2)
                    with ccols[0]:
                        if st.button("✅ Sí, eliminar", key=f"confirmdel_{item['id']}"):
                            db.delete_item(item["id"])
                            st.session_state.confirm_delete = None
                            st.rerun()
                    with ccols[1]:
                        if st.button("❌ Cancelar", key=f"canceldel_{item['id']}"):
                            st.session_state.confirm_delete = None
                            st.rerun()

                if st.session_state.get(f"editing_{item['id']}"):
                    render_item_form(item["user_id"], item["category"], edit_item=item)
        st.markdown("</div>", unsafe_allow_html=True)


def page_catalogo(user, category):
    label = "🎬 Películas" if category == "pelicula" else "📺 Series"
    st.header(label)
    with st.expander("＋ AÑADIR NUEVO TÍTULO", expanded=False):
        render_item_form(user["id"], category)

    items = db.get_items(user["id"], category=category)
    st.caption(f"{len(items)} título(s) — ordenados automáticamente por calificación 🍺")
    if not items:
        st.info("Todavía no hay nada aquí. ¡Añade tu primer título!")
    for it in items:
        render_item_card(it)


def page_ranking(user):
    st.header("🏆 Ranking automático — LA MAJOE")
    st.caption("Ordenado en tiempo real de 6🍺 (LA MAJOE) a 1☕ (lo peor)")
    items = db.get_items(user["id"])
    if not items:
        st.info("Añade películas o series para ver tu ranking.")
        return

    for pos, it in enumerate(items, start=1):
        cols = st.columns([0.5, 3, 1.5])
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(pos, f"#{pos}")
        emoji = "🎬" if it["category"] == "pelicula" else "📺"
        with cols[0]:
            st.markdown(f"### {medal}")
        with cols[1]:
            st.markdown(f"**{emoji} {it['title']}**")
        with cols[2]:
            st.markdown(f"<span class='rating-tag'>{RATING_LEVELS[it['rating']]}</span>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📲 Compartir mi ranking")
    share_text = utils.build_list_share_text(user["username"], items)
    st.link_button("📲 Compartir lista por WhatsApp", utils.whatsapp_link(share_text), use_container_width=True)

    card_bytes = utils.generate_ranking_card(user["username"], items)
    st.image(card_bytes, caption="Vista previa de tu tarjeta de ranking", width=400)
    st.download_button(
        "⬇️ Descargar tarjeta gráfica (PNG)",
        data=card_bytes,
        file_name=f"ranking_{user['username']}.png",
        mime="image/png",
        use_container_width=True,
    )
    st.caption("Descarga la tarjeta y adjúntala en tu chat de WhatsApp 📎")


def page_amigos(user):
    st.header("👥 Amigos")
    all_users = [u for u in db.get_users() if u["id"] != user["id"]]
    friends = db.get_friends(user["id"])
    friend_ids = {f["id"] for f in friends}

    st.subheader("➕ Seguir a otro jugador")
    candidates = [u["username"] for u in all_users if u["id"] not in friend_ids]
    if candidates:
        pick = st.selectbox("Buscar jugador", options=["—"] + candidates)
        if st.button("👥 Seguir", use_container_width=True) and pick != "—":
            target = db.get_user_by_name(pick)
            ok, msg = db.add_friend(user["id"], target["id"])
            st.success(msg) if ok else st.warning(msg)
            st.rerun()
    else:
        st.caption("Ya sigues a todos los jugadores registrados.")

    st.divider()
    st.subheader("❤️ Compatibilidad de gustos")
    if not friends:
        st.info("Aún no sigues a nadie. ¡Añade amigos para comparar gustos!")
    for f in friends:
        score, common = db.compute_compatibility(user["id"], f["id"])
        with st.container():
            st.markdown("<div class='nes-card'>", unsafe_allow_html=True)
            cols = st.columns([3, 2, 1])
            with cols[0]:
                st.markdown(f"**{f['avatar_emoji']} {f['username']}**")
                st.caption(f"{common} título(s) en común")
            with cols[1]:
                st.progress(score / 100, text=f"❤️ {score}% compatible")
            with cols[2]:
                if st.button("🗑️ Dejar de seguir", key=f"unfollow_{f['id']}"):
                    db.remove_friend(user["id"], f["id"])
                    st.rerun()

            with st.expander(f"Ver ranking de {f['username']}"):
                f_items = db.get_items(f["id"])
                if not f_items:
                    st.caption("Sin títulos todavía.")
                for it in f_items:
                    emoji = "🎬" if it["category"] == "pelicula" else "📺"
                    st.markdown(f"{emoji} **{it['title']}** — {RATING_LEVELS[it['rating']]}")
            st.markdown("</div>", unsafe_allow_html=True)


def page_perfil(user):
    st.header("📊 Perfil")
    cols = st.columns([1, 3])
    with cols[0]:
        st.markdown(f"<div style='font-size:64px; text-align:center;'>{user['avatar_emoji']}</div>", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"### {user['username']}")
        st.caption(f"Jugador desde {user['created_at'][:10]}")

    items = db.get_items(user["id"])
    pelis = [i for i in items if i["category"] == "pelicula"]
    series = [i for i in items if i["category"] == "serie"]
    friends = db.get_friends(user["id"])

    m1, m2, m3 = st.columns(3)
    m1.metric("🎬 Películas", len(pelis))
    m2.metric("📺 Series", len(series))
    m3.metric("👥 Amigos", len(friends))

    if items:
        avg = sum(i["rating"] for i in items) / len(items)
        st.markdown(f"**🍺 Calificación media:** {avg:.1f} / 6")

    st.divider()
    st.subheader("🔗 Compartir mi perfil")
    profile_text = utils.build_profile_share_text(user["username"])
    st.link_button("📲 Compartir perfil por WhatsApp", utils.whatsapp_link(profile_text), use_container_width=True)

    st.divider()
    if st.button("🚪 Cerrar sesión", use_container_width=True):
        st.session_state.user_id = None
        st.rerun()


# ---------------------------------------------------------------------------
# APP PRINCIPAL
# ---------------------------------------------------------------------------
def main_app(user):
    with st.sidebar:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, use_container_width=True)
        st.markdown(f"<p class='pixel-hint'>👉 ES AQUÍ, PINCHA 👈</p>", unsafe_allow_html=True)
        menu = st.radio(
            "Menú",
            [
                "🎬 Películas",
                "📺 Series",
                "🏆 Ranking",
                "👥 Amigos",
                "📊 Perfil",
            ],
            label_visibility="collapsed",
        )
        st.divider()
        st.caption(f"🎮 Sesión: **{user['username']}**")
        st.link_button("🌐 ROCK AND BIRRA RADIO", ROCKANDBIRRA_URL, use_container_width=True)
        st.markdown(f"<p style='text-align:center; font-size:10px; margin-top:10px;'>{APP_TAG}</p>", unsafe_allow_html=True)

    st.markdown(f"<h1>{APP_TITLE}</h1>", unsafe_allow_html=True)

    if menu == "🎬 Películas":
        page_catalogo(user, "pelicula")
    elif menu == "📺 Series":
        page_catalogo(user, "serie")
    elif menu == "🏆 Ranking":
        page_ranking(user)
    elif menu == "👥 Amigos":
        page_amigos(user)
    elif menu == "📊 Perfil":
        page_perfil(user)


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if st.session_state.user_id is None:
    login_screen()
else:
    current_user = db.get_user_by_id(st.session_state.user_id)
    if current_user is None:
        st.session_state.user_id = None
        st.rerun()
    else:
        main_app(current_user)
