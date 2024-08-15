css = '''
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

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <svg xmlns="http://www.w3.org/2000/svg" width="3em" height="3em" viewBox="0 0 24 24"><path fill="#ed6002" d="M12 22q-.65 0-1.175-.312T10 20.85H8V15.3q-1.475-.975-2.363-2.575T4.75 9.25q0-3.025 2.113-5.137T12 2q3.025 0 5.138 2.113T19.25 9.25q0 1.925-.888 3.5T16 15.3v5.55h-2q-.3.525-.825.838T12 22m-2-3.15h4v-.9h-4zm0-1.9h4V16h-4zM9.8 14h1.45v-2.7l-2.2-2.2l1.05-1.05l1.9 1.9l1.9-1.9l1.05 1.05l-2.2 2.2V14h1.45q1.35-.65 2.2-1.912t.85-2.838q0-2.2-1.525-3.725T12 4Q9.8 4 8.275 5.525T6.75 9.25q0 1.575.85 2.838T9.8 14M12 9"/></svg>
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <svg xmlns="http://www.w3.org/2000/svg" width="3em" height="3em" viewBox="0 0 24 24"><path fill="#26caf2" d="M20 7V5h-2V3h2V1h2v2h2v2h-2v2zm-4.5 4q.625 0 1.063-.437T17 9.5q0-.625-.437-1.062T15.5 8q-.625 0-1.062.438T14 9.5q0 .625.438 1.063T15.5 11m-7 0q.625 0 1.063-.437T10 9.5q0-.625-.437-1.062T8.5 8q-.625 0-1.062.438T7 9.5q0 .625.438 1.063T8.5 11m3.5 6.5q1.7 0 3.088-.962T17.1 14H6.9q.625 1.575 2.013 2.538T12 17.5m0 4.5q-2.075 0-3.9-.788t-3.175-2.137q-1.35-1.35-2.137-3.175T2 12q0-2.075.788-3.9t2.137-3.175q1.35-1.35 3.175-2.137T12 2q1.075 0 2.075.213T16 2.825V7h2v2h3.55q.225.725.338 1.463T22 12q0 2.075-.788 3.9t-2.137 3.175q-1.35 1.35-3.175 2.138T12 22"/></svg>
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''