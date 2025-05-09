import streamlit as st
import os
import time
import pyautogui
from PIL import Image
import smtplib
from smtplib import SMTPResponseException
from email.message import EmailMessage

# === Configuração da Página (única e primeira chamada do Streamlit) ===
st.set_page_config(
    page_title="TI Helpdesk Automação",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === Credenciais embutidas (substitua pelos seus dados) ===
EMAIL_USER = "patrickgamer364@gmail.com"
EMAIL_PASS = "fauz hszo temr tsua"

# === Função de automação para capturar prints de Sistema, IP e Net User ===
def capture_system_info():
    sistema_path   = 'sistema_info.png'
    ipconfig_path  = 'ipconfig_info.png'
    netuser_path   = 'netuser_info.png'

    def run_cmd_and_capture(command, path):
        pyautogui.press('winleft'); time.sleep(3)
        pyautogui.write('cmd', interval=0.05); time.sleep(3)
        pyautogui.press('enter'); time.sleep(1)
        pyautogui.write(command, interval=0.05); pyautogui.press('enter'); time.sleep(2)
        pyautogui.screenshot(path); time.sleep(3)
        pyautogui.hotkey('alt', 'f4'); time.sleep(3)

    # 1) Exibir nome do computador
    pyautogui.press('winleft'); time.sleep(3)
    pyautogui.write('exibir nome', interval=0.05); time.sleep(3)
    pyautogui.press('enter'); time.sleep(3)
    pyautogui.screenshot(sistema_path); time.sleep(3)
    pyautogui.hotkey('alt', 'f4'); time.sleep(3)

    # 2) Capturar saída de ipconfig
    run_cmd_and_capture('ipconfig', ipconfig_path)

    # 3) Capturar saída de net user
    run_cmd_and_capture('net user', netuser_path)

    return sistema_path, ipconfig_path, netuser_path

# === Interface do Streamlit ===
def main():
    st.title("💻 TI Helpdesk Automação")
    st.write("Preencha seus dados e clique para capturar informações do sistema e enviá-las por e-mail.")

    # Campos obrigatórios
    nome = st.text_input("Nome do solicitante")
    depto = st.text_input("Departamento")

    # Validação
    if st.button("Executar Captura"):
        if not nome.strip() or not depto.strip():
            st.error("Por favor, informe Nome e Departamento antes de continuar.")
            return

        with st.spinner("Executando automação…"):
            sistema_png, ipconfig_png, netuser_png = capture_system_info()
        st.success("Capturas concluídas!")

        # Exibir dados do solicitante
        st.markdown(f"**Solicitante:** {nome}  ")
        st.markdown(f"**Departamento:** {depto}")

        # Pré-visualização das imagens
        st.image(sistema_png, caption="Informações do Sistema", use_container_width=True)
        st.image(ipconfig_png, caption="Saída do ipconfig", use_container_width=True)
        st.image(netuser_png, caption="Saída do net user", use_container_width=True)

        # Preparar e enviar e-mail
        destinatario = 'suporteti03.go@dolpengenharia.com.br'

        msg = EmailMessage()
        msg['Subject'] = f'Chamado TI - {nome} ({depto})'
        msg['From']    = EMAIL_USER
        msg['To']      = destinatario
        msg.set_content(f'Solicitante: {nome}\nDepartamento: {depto}\n\nSeguem em anexo os prints solicitados.')

        for path in (sistema_png, ipconfig_png, netuser_png):
            with open(path, 'rb') as f:
                msg.add_attachment(
                    f.read(),
                    maintype='image',
                    subtype='png',
                    filename=os.path.basename(path)
                )

        # Envio manual do e-mail com tratamento do QUIT
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        try:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
            st.success("E-mail enviado com sucesso!")
        except Exception as e:
            st.error(f"Falha no envio do e-mail: {e}")
        finally:
            try:
                smtp.quit()
            except SMTPResponseException:
                pass
            except Exception:
                smtp.close()

        # Limpeza dos arquivos temporários
        for path in (sistema_png, ipconfig_png, netuser_png):
            os.remove(path)

if __name__ == "__main__":
    main()
