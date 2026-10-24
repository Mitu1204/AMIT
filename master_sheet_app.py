import streamlit as st
from google import genai
from PIL import Image

# पेज की सेटिंग
st.set_page_config(page_title="Master Sheet Photo Reader", page_icon="📊", layout="centered")

st.title("📊 Master Sheet Photo Reader App")
st.write("अपनी पर्ची या चार्ट की फोटो यहाँ अपलोड करें, यह ऐप तुरंत **Jodi = Amount** फॉर्मेट और कुल टोटल बना देगा।")

# साइडबार या इनपुट में API Key लें
api_key = st.sidebar.text_input("अपनी Gemini API Key दर्ज करें:", type="password")

# इमेज अपलोड करने का ऑप्शन
uploaded_file = st.file_uploader("पर्ची या चार्ट की फोटो चुनें (JPG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="अपलोड की गई पर्ची", use_container_width=True)
    
    if st.button("🚀 मास्टर शीट बनाएं (Process)"):
        if not api_key:
            st.error("⚠️ कृपया पहले बाईं ओर (Sidebar में) अपनी Gemini API Key दर्ज करें।")
        else:
            with st.spinner("फोटो को पढ़ा जा रहा है... कृपया प्रतीक्षा करें..."):
                try:
                    # Gemini Client इनिशियलाइज करें
                    client = genai.Client(api_key=api_key)
                    
                    prompt = """
                    इस इमेज में हाथ से लिखे हुए या प्रिंटेड नंबरों (जोड़ी/Jodi) और उनके सामने लिखे अमाउंट को ध्यान से पढ़ें।
                    इसे केवल नीचे दिए गए फॉर्मेट में साफ़-सुथरी लिस्ट बनाकर दें:
                    * **Jodi** = Amount
                    
                    और अंत में इसका कुल योग (Total Amount) जरूर लिखें।
                    """
                    
                    # यहाँ मॉडल का नाम अपडेट कर दिया गया है
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[image, prompt]
                    )
                    
                    st.success("✨ मास्टर शीट सफलतापूर्वक तैयार हो गई है!")
                    st.markdown("### 📋 परिणाम (Master Sheet):")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"त्रुटि (Error) आई: {e}")