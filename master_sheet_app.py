import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Master Sheet Photo & SMS Reader & Chat", page_icon="📊"
)

st.title("📊 Master Sheet Photo & SMS Reader & Chat App")
st.write(
    "Yahan aap photo upload karein, SMS text paste karein, ya fir seedhe Gemini"
    " se chat karke command dein!"
)

# Sidebar ya Main section me API Key input
api_key = st.text_input(
    "अपनी Gemini API Key दर्ज करें:", type="password", key="gemini_api_key"
)

if api_key:
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel("gemini-1.5-flash")

  st.divider()

  # ----------------- SECTION 1: PHOTO & SMS READER -----------------
  st.subheader("📁 Reader Mode (Photo & SMS)")
  task_type = st.radio(
    "Kiska use karna chahte hain?",
    ("Photo Upload (JPG/PNG)", "SMS Text Paste"),
  )

  if task_type == "Photo Upload (JPG/PNG)":
    uploaded_file = st.file_uploader(
      "Apni parchiyon ya chart ki photo upload karein", type=["jpg", "jpeg", "png"]
    )
    if uploaded_file and st.button("Read Photo & Generate Sheet"):
      with st.spinner("Photo read ki ja rahi hai..."):
        try:
          bytes_data = uploaded_file.getvalue()
          image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
          prompt = "Is image me diye gaye data ko padho aur 'Jodi = Amount' format me list karke aakhir me 'Kul Jod (Total Amount)' nikalo."
          response = model.generate_content([prompt, image_parts[0]])
          st.markdown("### Result:")
          st.markdown(response.text)
        except Exception as e:
          st.error(f"Error: {e}")

  else:
    sms_text = st.text_area(
      "Yahan apna SMS text paste karein:",
      placeholder="Yahan SMS paste karein...",
    )
    if sms_text and st.button("Read SMS & Generate Sheet"):
      with st.spinner("SMS read kiya ja raha hai..."):
        try:
          prompt = f"Neeche diye gaye SMS text ko padho aur usme se 'Jodi = Amount' ka vivran nikalo aur aakhir me 'Kul Jod (Total Amount)' ka sum batao:\n\n{sms_text}"
          response = model.generate_content(prompt)
          st.markdown("### Result:")
          st.markdown(response.text)
        except Exception as e:
          st.error(f"Error: {e}")

  st.divider()

  # ----------------- SECTION 2: CHAT COMMAND INTERFACE -----------------
  st.subheader("💬 Gemini Chat & Command Mode")
  st.write(
    "Jaise aap mujhse chat karte hain, waise hi yahan likh kar koi bhi command"
    " de sakte hain ya baat kar sakte hain."
  )

  if "chat_history" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

  for message in st.session_state.chat.history:
    with st.chat_message(
        "user" if message.role == "user" else "model"
    ):
      st.markdown(message.parts[0].text)

  if user_prompt := st.chat_input("Yahan apni command likhein..."):
    with st.chat_message("user"):
      st.markdown(user_prompt)

    with st.chat_message("model"):
      with st.spinner("Soch raha hu..."):
        response = st.session_state.chat.send_message(user_prompt)
        st.markdown(response.text)

else:
  st.warning(
    "Kripya upar apni valid Gemini API Key darj karein taaki app kaam kar"
    " sake."
  )
