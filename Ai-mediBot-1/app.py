import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Set Streamlit page config (MUST be first Streamlit command)
st.set_page_config(
    page_title="Disease Analysis System", 
    page_icon="🩺", 
    layout="wide"
)

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Gemini API key not found.")
    st.stop()

# Configure Gemini models
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class DiseaseAnalyzer:
    def __init__(self):
        self.conversation_history = []

    def safe_generate_content(self, prompt):
        """Generate content with error handling."""
        try:
            response = model.generate_content(prompt, safety_settings={
                'HARASSMENT': 'BLOCK_NONE',
                'HATE': 'BLOCK_NONE',
                'SEXUAL': 'BLOCK_NONE',
                'DANGEROUS': 'BLOCK_NONE'
            })
            return response.text
        except Exception as e:
            st.error(f"Content generation error: {e}")
            return None

    def interactive_diagnosis(self):
        """Interactive symptom diagnosis workflow."""
        st.title("🩺 Disease Analysis System")
        
        # Initialize session state
        if 'conversation_state' not in st.session_state:
            st.session_state.conversation_state = [
                {"role": "System", "message": "Hello! I'll help analyze your health concern through a few key questions."},
                {"role": "System", "message": "What is your age?"}
            ]
            st.session_state.patient_data = {
                'age': None,
                'gender': None,
                'primary_symptom': None,
                'symptom_duration': None,
                'severity': None,
                'medical_history': None
            }
            st.session_state.analysis_complete = False

        # Display conversation
        for msg in st.session_state.conversation_state:
            if msg['role'] == 'System':
                st.markdown(f"**🩺 System:** {msg['message']}")
            else:
                st.markdown(f"**👤 You:** {msg['message']}")

        # Generate analysis when complete
        if st.session_state.analysis_complete:
            analysis = self.generate_analysis(st.session_state.patient_data)
            st.markdown("## 📋 Disease Analysis Report")
            st.write(analysis)
            return

        # User input
        user_response = st.text_input("Your response:", key="user_input")

        if st.button("Send") and user_response.strip():
            # Add user response to conversation
            st.session_state.conversation_state.append({
                "role": "Patient", 
                "message": user_response
            })

            # Update patient data
            if st.session_state.patient_data['age'] is None:
                st.session_state.patient_data['age'] = user_response
            elif st.session_state.patient_data['gender'] is None:
                st.session_state.patient_data['gender'] = user_response
            elif st.session_state.patient_data['primary_symptom'] is None:
                st.session_state.patient_data['primary_symptom'] = user_response
            elif st.session_state.patient_data['symptom_duration'] is None:
                st.session_state.patient_data['symptom_duration'] = user_response
            elif st.session_state.patient_data['severity'] is None:
                st.session_state.patient_data['severity'] = user_response
            elif st.session_state.patient_data['medical_history'] is None:
                st.session_state.patient_data['medical_history'] = user_response
                st.session_state.analysis_complete = True

            # Get next question
            next_step = self.get_next_question(st.session_state.patient_data)

            # Add system's next message
            st.session_state.conversation_state.append({
                "role": "System", 
                "message": next_step
            })
        
            st.rerun()

    def get_next_question(self, patient_data):
        """Determine next question in diagnosis flow."""
        if patient_data['age'] is None:
            return "What is your age?"
        if patient_data['gender'] is None:
            return "What is your gender?"
        if patient_data['primary_symptom'] is None:
            return "What are your main symptoms? Please describe in detail."
        if patient_data['symptom_duration'] is None:
            return "How long have you had these symptoms?"
        if patient_data['severity'] is None:
            return "On a scale of 1-10, how severe are your symptoms?"
        if patient_data['medical_history'] is None:
            return "Do you have any existing medical conditions?"
        return "Thank you for providing all details. Generating analysis..."

    def generate_analysis(self, patient_data):
        """Generate detailed disease analysis report."""
        prompt = f"""Disease Analysis Report:

Patient Information:
- Age: {patient_data['age']} years
- Gender: {patient_data['gender']}
- Main Symptoms: {patient_data['primary_symptom']}
- Duration: {patient_data['symptom_duration']}
- Severity: {patient_data['severity']}/10
- Medical History: {patient_data['medical_history']}

Provide a detailed analysis including:
1. Potential Conditions
2. Common Causes
3. Risk Factors
4. Prevention Methods
5. Recommended Treatments
6. When to Seek Medical Care
7. Lifestyle Recommendations"""

        analysis = self.safe_generate_content(prompt)
        return analysis if analysis else "Unable to generate analysis."

def main():
    analyzer = DiseaseAnalyzer()
    analyzer.interactive_diagnosis()

if __name__ == "__main__":
    main()
