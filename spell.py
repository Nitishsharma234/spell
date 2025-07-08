import streamlit as st
from symspellpy import SymSpell, Verbosity
import os

# Load SymSpell only once
@st.cache_resource
def load_symspell():
    sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
    dictionary_path = "frequency_dictionary_en_82_765.txt"

    if not sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1):
        st.error("❌ Dictionary not found! Please place `frequency_dictionary_en_82_765.txt` in the same folder.")
        st.stop()

    # Add custom important words (like your name)
    sym_spell.create_dictionary_entry("nitish", 1000)
    sym_spell.create_dictionary_entry("ai", 500)
    sym_spell.create_dictionary_entry("ml", 500)
    return sym_spell

def correct_text(input_text, sym_spell):
    suggestions = sym_spell.lookup_compound(input_text, max_edit_distance=2)
    if suggestions:
        return suggestions[0].term
    return input_text

# Streamlit UI
def main():
    st.title("🧠 Spell Checker (Streamlit + SymSpell)")
    st.markdown("Check spelling from text input **or** upload a `.txt` file.")

    sym_spell = load_symspell()

    # Option 1: Text Typing
    st.subheader("✍️ Type Your Sentence")
    user_input = st.text_area("Write here...", "my naem is nitish and i liek astroonomy")

    if st.button("✅ Correct Typed Text"):
        corrected = correct_text(user_input, sym_spell)
        st.success("Corrected Text:")
        st.text(corrected)

    st.markdown("---")

    # Option 2: File Upload
    st.subheader("📂 Upload a `.txt` File")
    uploaded_file = st.file_uploader("Choose a text file", type=["txt"])

    if uploaded_file:
        file_contents = uploaded_file.read().decode("utf-8")
        st.text("📄 Original File Content:")
        st.text(file_contents)

        corrected_file_text = correct_text(file_contents, sym_spell)
        st.success("✅ Corrected File Text:")
        st.text(corrected_file_text)

        st.download_button("📥 Download Corrected File", corrected_file_text, file_name="corrected_text.txt")

if __name__ == "__main__":
    main()
