import google.generativeai as genai
import streamlit as st

st.set_page_config(page_title="Master Sheet Photo & SMS Reader", page_icon="📊")

st.title("📊 Master Sheet Photo & SMS Reader App")
st.write(
    "Yahan aap ya toh apni parchiyan/chart ki **photo upload** karein ya fir **SMS ka text paste** karein, yeh app turant *Jodi = Amount* format aur total bana dega."
)

# Sidebar ya Main area mein API Key input
api_key = st.text_input("अपनी Gemini API Key दर्ज करें:", type="password")

if api_key:
  genai.configure(api_key=api_key)
  # Model setup (Gemini 2.5 Flash ya jo aap use kar rahe hain)
  model = genai.GenerativeModel("gemini-2.5-flash")

  # Input Type Selection (Photo ya SMS Text)
  input_type = st.radio(
    "Kiska use karna chahte hain?", ("Photo Upload (JPG/PNG)", "SMS Text Paste")
  )

  if input_type == "Photo Upload (JPG/PNG)":
    uploaded_file = st.file_uploader(
      "पर्ची या चार्ट की फोटो चुनें", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
      st.image(uploaded_file, caption="Upload ki gayi photo", use_column_width=True)

      if st.button("Read Photo & Generate Sheet"):
        with st.spinner("Processing image..."):
          bytes_data = uploaded_file.getvalue()
          image_part = {
              "mime_type": uploaded_file.type,
              "data": bytes_data,
          }

          prompt = (
              "Is image mein di gayi jodi aur amount ko padhein. Isko"
              " 'Jodi = Amount' ke format mein saaf-saaf likhein aur aakhir mein"
              " sabhi amounts ka total (kul jod) bhi batayein."
          )

          response = model.generate_content([image_part, prompt])
          st.subheader("Master Sheet Result:")
          st.write(response.text)

  else:
    sms_text = st.text_area(
        "Yahan apna SMS text paste karein:",
        placeholder="Apna message yahan daalein...",
    )

    if st.button("Read SMS & Generate Sheet"):
      if sms_text.strip() != "":
        with st.spinner("Processing SMS..."):
          prompt = (
              "Is SMS text mein diye gaye numbers/jodi aur amount ko padhein."
              " Isko 'Jodi = Amount' ke format mein saaf-saaf likhein aur"
              " aakhir mein sabhi amounts ka total (kul jod) bhi batayein."
              f"\n\nSMS Text:\n{sms_text}"
          )

          response = model.generate_content(prompt)
          st.subheader("Master Sheet Result:")
          st.write(response.text)
      else:
        st.warning("Kripya pehle SMS text enter karein.")

else:
  st.warning("Kripya aage badhne ke liye apni Gemini API Key darj karein.")
