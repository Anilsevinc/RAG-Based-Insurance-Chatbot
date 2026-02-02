import gradio as gr
from pathlib import Path
from dotenv import load_dotenv
import sys


PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_DIR))
load_dotenv(dotenv_path=PROJECT_DIR / ".env")


try:
    from backend.chatbot import handle_user_query
except ImportError:
    def handle_user_query(query):
        """Placeholder for the actual backend function"""
        if "deductible" in query.lower():
            return "A deductible is the amount you pay out-of-pocket before your insurance coverage begins to pay."
        elif "claim" in query.lower():
            return "You can file a claim online through our customer portal, or by calling our claims department at 555-CLAIM."
        elif "expire" in query.lower():
            return "Your car policy expiration date can be found on your policy documents or by logging into your account."
        elif "approved" in query.lower():
            return "I can check the status of your last claim. Could you please provide your claim number?"
        else:
            return f"I received your question: '{query}'. How else can I assist you with your insurance inquiries?"



SAMPLE_QUESTIONS = [
    "What is a deductible?",
    "How can I file a claim?",
    "When does my car policy expire?",
    "Did my last claim get approved?",
    "Can I change my payment method?",
]



def gradio_chat(user_message, chat_history):
    """Handle user message and return bot response"""
    if not user_message or not user_message.strip():
        return "", chat_history

    if chat_history is None:
        chat_history = []

    # Get bot response
    bot_response = handle_user_query(user_message)

    # Update chat history
    chat_history.append((user_message, bot_response))

    return "", chat_history


def click_sample_question(question, chat_history):
    """Handle sample question button click"""
    if chat_history is None:
        chat_history = []

    bot_response = handle_user_query(question)
    chat_history.append((question, bot_response))

    return "", chat_history


def clear_chat():
    """Clear chat history"""
    return None, ""



custom_css = """
/* Global styling - Koyu Mor Arka Plan / Lacivert Konteyner Tema */
:root {
    /* ANA RENKLER (GRADIENTLERLE YENİDEN TASARLANDI) */
    --page-bg: linear-gradient(135deg, #0E0B1F, #1B2347, #0E162B);  /* Koyu mor-lacivert karışımı */
    --container-bg: linear-gradient(145deg, #1A2140, #1C2F54);      /* Lacivert geçişli arka plan */
    --text-color: #E8EAF6;                                          /* Hafif lavanta beyazı */

    /* VURGU VE ÇERÇEVE RENKLERİ */
    --accent-color: #6E72FF;                                        /* Mor-mavi parlayan vurgu */
    --border-color: #2E3D66;                                        /* Lacivert kenar çizgileri */

    /* MESAJ VE INPUT RENKLERİ */
    --card-bg: linear-gradient(160deg, #24345B, #1F2B46);           /* Hafif gradientli kart */
    --input-bg: linear-gradient(160deg, #283A61, #1F2940);          /* Textarea arka planı */
    --bot-msg-bg: linear-gradient(160deg, #24355A, #1F2B45);        /* Bot mesajları */
    --user-msg-bg: linear-gradient(160deg, #32457A, #283A61);       /* Kullanıcı mesajları */
}

body, .gradio-container {
    background: var(--page-bg) !important;
    font-family: 'Söhne', 'ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', sans-serif !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    max-width: 100% !important;
}

/* YENİ: Chatbot ve Örnek Soruları çevreleyen Body Container (Lacivert) */
.main-body-container {
    max-width: 950px; 
    margin: 20px auto; 
    padding: 24px;
    background: var(--container-bg); /* LACİVERT */
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
    height: calc(100vh - 40px); 
    display: flex;
    flex-direction: column;
}


/* Header */
.header-section {
    background: var(--container-bg); /* LACİVERT */
    border-bottom: 1px solid var(--border-color);
    padding: 12px 16px;
    flex-shrink: 0;
}

.logo-text {
    color: var(--text-color);
    font-size: 16px;
    font-weight: 600;
    text-align: center;
    margin: 0;
}

/* Chat container - full height */
.chat-container {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    background: var(--container-bg); /* LACİVERT */
    padding: 0 16px;
    overflow: hidden;
}

/* Chatbot area */
#chatbot {
    background: var(--container-bg) !important; /* LACİVERT */
    border: none !important;
    border-radius: 0 !important;
    height: 100% !important;
    overflow-y: auto !important;
    padding: 16px 0 !important;
    box-shadow: none !important;
    flex-grow: 1;
}

/* Welcome section with sample questions */
.welcome-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 48px 16px;
    max-width: 768px;
    margin: 0 auto;
}

.welcome-title {
    color: var(--text-color);
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 48px;
    text-align: center;
}

/* Sample question cards */
.sample-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    width: 100%;
    max-width: 720px;
}

.sample-card {
    background: var(--card-bg) !important; 
    border: 1px solid var(--border-color) !important;
    color: var(--text-color) !important;
    /* ... (diğer stiller) ... */
}

.sample-card:hover {
    background: var(--user-msg-bg) !important; /* Hafif koyu lacivert */
    border-color: var(--accent-color) !important; /* Vurgu rengi */
}

/* Input container - Bütünleşik Alan */
.input-container {
    background: var(--container-bg); /* LACİVERT */
    padding: 16px 0;
    border-top: 1px solid var(--border-color);
    flex-shrink: 0;
}

.input-wrapper {
    max-width: 768px;
    margin: 0 auto;
    display: flex;
    align-items: flex-end;
    gap: 8px;
    background: var(--container-bg); /* LACİVERT */
    border: 1px solid var(--border-color);
    border-radius: 24px;
    padding: 8px; 
}

#user_input {
    flex: 1;
}

#user_input textarea {
    background: var(--input-bg) !important; 
    /* Çerçeve, mor-mavi palete uygun hale getirildi */
    border: 1px solid var(--border-color) !important;
    
    box-shadow: none !important;
    color: var(--text-color) !important;
    /* ... (diğer stiller) ... */
    
    /* ÖNEMLİ: Odaklanma (Focus) halkasını sıfırlar (Mavi rengi engeller) */
    outline: none !important; 
}

/* Textarea'ya tıklanıldığında oluşabilecek mavi focus gölgesini/çerçevesini sıfırlar. */
#user_input textarea:focus {
    box-shadow: none !important; 
    border-color: var(--accent-color) !important; /* Parlak vurgu */
}

/* Input Wrapper'ı da focus renginden korumak için */
.input-wrapper:has(#user_input textarea:focus) {
    border-color: var(--accent-color) !important; /* Parlak vurgu */
    box-shadow: none !important;
}


/* Send button hizalama - Parlak Vurgu */
.send-button {
    background: var(--accent-color) !important; /* Parlak Mavi/Mor Vurgu */
    color: white !important; /* Beyaz ikon */
    /* ... (diğer stiller) ... */
}

.send-button:hover {
    background: #9092FF !important; /* Hafif açılmış vurgu */
}

.send-button:disabled {
    background: var(--border-color) !important; /* Daha koyu border rengi */
    color: #A0A0B5 !important;
    cursor: not-allowed !important;
}

/* Footer info */
.footer-info {
    text-align: center;
    color: #A0A0B5; /* Hafif mor-gri */
    font-size: 12px;
    padding: 12px 16px;
    background: var(--container-bg); /* LACİVERT */
    flex-shrink: 0;
}

/* Chat messages styling */
.message {
    padding: 16px 24px !important;
    max-width: 768px !important;
    margin: 8px auto !important;
    border-radius: 12px !important;
    word-wrap: break-word;
}

.message.user {
    background: var(--user-msg-bg) !important; /* Kullanıcı mesajı (Koyu Lacivert) */
}

.message.bot {
    background: var(--bot-msg-bg) !important; /* Bot mesajı (Daha açık Lacivert) */
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--container-bg); /* LACİVERT */
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--user-msg-bg);
}

/* Remove Gradio branding */
footer {
    display: none !important;
}

.gradio-container .prose {
    color: var(--text-color) !important;
}

/* Responsive */
@media (max-width: 950px) {
    .main-body-container {
        max-width: 100%; /* Mobil cihazlarda tam genişlik */
        margin: 0;
        padding: 0;
        height: 100vh;
        border-radius: 0;
        box-shadow: none;
    }
    .input-wrapper {
        border-radius: 12px;
        margin: 0 16px;
    }
}
@media (max-width: 768px) {
    .sample-grid {
        grid-template-columns: 1fr;
    }
    
    .welcome-title {
        font-size: 24px;
    }
}
"""


# Create Gradio interface
with gr.Blocks(css=custom_css, title="Tenacitics") as demo:
    
   
    with gr.Column(elem_classes="main-body-container"):
        
        # Header
        gr.HTML("""
            <div class="header-section">
                <p class="logo-text"> Insurance Assistant</p>
            </div>
        """)
        
        # Chat area
        with gr.Column(elem_classes="chat-container"):
            chatbot_ui = gr.Chatbot(
                elem_id="chatbot",
                show_label=False,
                container=False,
                height="100%"
            )
            
           
            with gr.Column(visible=True, elem_classes="welcome-container") as sample_questions_container:
                gr.HTML('<h1 class="welcome-title">How can I help you today?</h1>')
                
                sample_btns = []
                with gr.Column(elem_classes="sample-grid"):
                    
                   
                    questions_row_1 = SAMPLE_QUESTIONS[:3]
                    questions_row_2 = SAMPLE_QUESTIONS[3:]

                    
                    with gr.Row():
                        for q in questions_row_1:
                            btn = gr.Button(q, elem_classes="sample-card")
                            sample_btns.append(btn)
                    
                    
                    with gr.Row():
                        for q in questions_row_2:
                            btn = gr.Button(q, elem_classes="sample-card")
                            sample_btns.append(btn)
        
       
        with gr.Column(elem_classes="input-container"):
            with gr.Row(elem_classes="input-wrapper"):
                message_input = gr.Textbox(
                    placeholder="Ask me about your insurance, claims, policies, and more!",
                    show_label=False,
                    elem_id="user_input",
                    lines=1,
                    max_lines=10,
                    container=False,
                    scale=20
                )
                send_button = gr.Button("➤", elem_classes="send-button", scale=1)
        
        # Footer
        gr.HTML("""
            <div class="footer-info" style="text-align:center; font-size:0.85rem; color:#BFC7E6; padding:14px 0; border-top:1px solid rgba(255,255,255,0.05); background:linear-gradient(135deg, #181B2E, #1B2B4C); opacity:0.9;">
    © 2025 
    <a href="https://anilsevinc.net" target="_blank" rel="noopener noreferrer"
       style="color:#BFC7E6; text-decoration:none; font-weight:600;">
       Anıl Sevinç
    </a>. 
    All rights reserved.
</div>
        """)
    
    
    
    
    message_input.submit(
        gradio_chat,
        inputs=[message_input, chatbot_ui],
        outputs=[message_input, chatbot_ui], # Sadece input ve chatbot güncelleniyor
    )
    
    send_button.click(
        gradio_chat,
        inputs=[message_input, chatbot_ui],
        outputs=[message_input, chatbot_ui], # Sadece input ve chatbot güncelleniyor
    )
    
    # Sample question handlers
    for btn in sample_btns:
        btn.click(
            click_sample_question,
            inputs=[btn, chatbot_ui],
            outputs=[message_input, chatbot_ui], # Sadece input ve chatbot güncelleniyor
        )

    # İşlevsellik 2'deki clear_chat'i kullanmak için bir buton eklenebilir
    # gr.Button("🗑️ Clear Chat", elem_classes="footer-btn").click(clear_chat, outputs=[chatbot_ui, message_input])


# Launch the app
if __name__ == "__main__":
    demo.launch(share=True)
