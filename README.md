# 🍿 Que coño ver !!! `#YConCervezaEsMejor`

App web hecha en **Python + Streamlit**, estilo retro 8-bit (NES), para
llevar tu propia lista de películas y series, calificarlas de **1 café ☕
(lo peor)** a **6 birras 🍺🍺🍺🍺🍺🍺 "LA MAJOE" (lo mejor)**, comparar gustos
con amigos y compartir todo por WhatsApp.

Un proyecto para **Rock And Birra Radio** — [rockandbirra.com](https://rockandbirra.com/)

100% Python. Sin APIs de pago, sin servicios externos. Base de datos SQLite
local. Gratis para uso personal.

---

## ✨ Funcionalidades

- 🎬 Lista de **Películas** y 📺 lista de **Series**, con portada opcional
  (sube una imagen desde tu teléfono).
- 🍺 Escala de calificación tipo "six pack": de **6 birras (LA MAJOE)**
  hasta **1 birra**, y **1 café** como peor nota posible.
- 🏆 **Ranking automático**: SQLite ordena tu lista en tiempo real de
  mejor a peor calificación.
- ✏️ Editar y 🗑️ eliminar títulos en cualquier momento.
- 👤 Sistema simple de **usuarios** (sin contraseñas, pensado para uso
  personal/entre amigos).
- 👥 **Amigos**: sigue a otros jugadores y compara vuestra
  ❤️ **compatibilidad de gustos** automáticamente.
- 📊 **Perfil** con tus estadísticas (nº de pelis, series, media de birras).
- 📲 **Compartir por WhatsApp**: tu lista, tu ranking o tu perfil, con un
  solo botón.
- 🖼️ **Tarjeta gráfica** de tu ranking (imagen PNG) descargable para
  adjuntar en WhatsApp.
- 🎮 Interfaz visual estilo **Nintendo NES** de los 80/90 (tipografía
  pixelada, botones con relieve, menú lateral tipo cartucho).
- 🌐 Botón directo a **Rock And Birra Radio**.

---

## 📁 Estructura del proyecto

```
que_cono_ver/
├── app.py              # Interfaz Streamlit (todas las pantallas)
├── database.py         # Acceso a SQLite (usuarios, items, amigos)
├── utils.py             # WhatsApp + generación de tarjeta gráfica
├── requirements.txt     # Dependencias (streamlit, pillow)
├── .streamlit/
│   └── config.toml      # Tema visual (colores retro)
├── assets/
│   └── logo.jpg          # Logo Rock And Birra
├── covers/               # Portadas subidas por los usuarios (se autogenera)
└── README.md
```

---

## 🖥️ Probarlo en tu ordenador (local)

Necesitas **Python 3.9+** instalado.

```bash
# 1. Entra en la carpeta del proyecto
cd que_cono_ver

# 2. (Recomendado) crea un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Arranca la app
streamlit run app.py
```

Se abrirá sola en tu navegador en `http://localhost:8501`.

---

## 📤 Subirlo a tu cuenta de GitHub

1. Crea un repositorio nuevo en GitHub, por ejemplo `que-cono-ver`.
2. Desde la carpeta del proyecto (donde está `app.py`):

```bash
cd que_cono_ver
git init
git add .
git commit -m "Primera versión: Que coño ver!!! #YConCervezaEsMejor"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/que-cono-ver.git
git push -u origin main
```

> Sustituye `TU_USUARIO` por tu usuario de GitHub. Si te pide login, usa
> tu usuario y un *Personal Access Token* (no la contraseña normal).

---

## ☁️ Publicarlo gratis en la nube (Streamlit Community Cloud)

1. Ve a **https://share.streamlit.io** e inicia sesión con tu cuenta de
   GitHub.
2. Pulsa **"New app"**.
3. Elige tu repositorio `que-cono-ver`, la rama `main` y como archivo
   principal `app.py`.
4. Pulsa **"Deploy"**. En 1-2 minutos tendrás una URL pública tipo:
   `https://que-cono-ver.streamlit.app`
5. Comparte esa URL con tus amigos: podrán abrirla desde el móvil como si
   fuera una app (puedes añadirla a la pantalla de inicio de Android/iOS
   desde el navegador: menú → "Añadir a pantalla de inicio").

### ⚠️ Nota importante sobre los datos en la nube

Streamlit Community Cloud (plan gratuito) usa almacenamiento **temporal**:
si la app se reinicia o se actualiza el código, el archivo `quecono.db`
(y las portadas subidas) se resetean. Para uso personal o de prueba entre
amigos esto no suele ser problema, pero si quieres persistencia permanente
más adelante, la opción más sencilla sin salir de Streamlit es migrar
`database.py` a un servicio de base de datos gratuito compatible (por
ejemplo, Turso o Supabase) — el resto de la app no necesita cambios porque
toda la lógica SQL está aislada en ese único archivo.

---

## 🍺 La escala de calificación

| Valor | Significado |
|-------|-------------|
| 6 🍺🍺🍺🍺🍺🍺 | **LA MAJOE** — lo mejor de lo mejor |
| 5 🍺🍺🍺🍺🍺 | Muy buena |
| 4 🍺🍺🍺🍺 | Buena |
| 3 🍺🍺🍺 | Normalita |
| 2 🍺🍺 | Floja |
| 1 🍺 | Mala |
| ☕ 1 Café | Lo peor — ni birra se merece |

---

## 🌐 Rock And Birra Radio

`#YConCervezaEsMejor`
👉 https://rockandbirra.com/
