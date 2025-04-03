import streamlit as st
import subprocess
import os
import shutil
import pathlib

st.set_page_config(page_title="URL → App", layout="centered")

st.title("🚀 URL → Native App Converter")
st.write("Transforma qualquer site num app nativo para macOS ou Windows com ícone personalizado.")

url = st.text_input("🔗 Cole o URL do site")
icon = st.file_uploader("🖼️ Ícone personalizado (.png ou .ico)", type=["png", "ico"])
platform = st.radio("🖥️ Sistema Operativo", ["macOS", "Windows"])

if st.button("Gerar App"):
    if not url or not url.startswith("http"):
        st.error("⚠️ Por favor insira um URL válido.")
    else:
        app_name = url.split("//")[-1].split(".")[0].replace(".", "-")
        output_dir = f"builds/{app_name}"
        app_path = f"{output_dir}/{app_name}.app"

        os.makedirs(output_dir, exist_ok=True)

        icon_path = None
        if icon:
            ext = ".ico" if platform == "Windows" else ".png"
            icon_path = os.path.join(output_dir, f"icon{ext}")
            with open(icon_path, "wb") as f:
                f.write(icon.read())
        else:
            st.warning("⚠️ Nenhum ícone enviado. O app usará o ícone padrão.")

        try:
            st.info("🔧 Gerando app... Aguarde.")
            command = [
                "nativefier",
                "--name", app_name,
                "--platform", "mac" if platform == "macOS" else "windows",
                "--electron-version", "25.9.0",
                url,
                output_dir
            ]
            if icon_path:
                command.extend(["--icon", icon_path])

            subprocess.run(command, check=True)

            # PATCH do libffmpeg.dylib para macOS
            if platform == "macOS":
                electron_path = shutil.which("electron")
                if electron_path:
                    base_path = pathlib.Path(electron_path).parent.parent
                    lib_src = base_path / "libffmpeg.dylib"
                    lib_dst = f"{app_path}/Contents/Frameworks/Electron Framework.framework/Libraries/libffmpeg.dylib"
                    os.makedirs(os.path.dirname(lib_dst), exist_ok=True)

                    if os.path.exists(lib_src):
                        shutil.copy2(lib_src, lib_dst)
                        st.success("🔧 Patch libffmpeg.dylib aplicado com sucesso.")
                    else:
                        st.warning(f"⚠️ libffmpeg.dylib não encontrado em {lib_src}.")
                else:
                    st.warning("⚠️ Caminho para o Electron não encontrado. Verifique a instalação.")

            zip_path = shutil.make_archive(output_dir, 'zip', output_dir)
            with open(zip_path, "rb") as f:
                st.success("✅ App gerado com sucesso!")
                st.download_button("📥 Baixar App (.zip)", f, file_name=f"{app_name}.zip")

        except subprocess.CalledProcessError:
            st.error("❌ Erro ao gerar o app. Verifique se o Nativefier está instalado corretamente.")
