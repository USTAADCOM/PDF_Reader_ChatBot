"""
html document for streamlit gui.
"""
CSS = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''
BOT_TEMPLATE = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://chatgpt-3ai.com/wp-content/uploads/2023/04/cropped-fotor_2023-4-1_14_30_8.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
USER_TEMPLATE = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiOH80WRk1WEtUqNcwmVf6MfxzLuSQHoojxGD7ge6eAlGyA-ZkL-5mJ99z8n2rsQHlZlo&usqp=CAU"  style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
