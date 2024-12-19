import json
from difflib import get_close_matches
from tkinter import Tk, Entry, Button, Text, Scrollbar, Frame, Label, PhotoImage


class Chatbot:
    def __init__(self, window):
        window.title('THE ASSISTANT')
        window.geometry('600x600')  # Increased window size for better space
        window.resizable(0, 0)
        window.configure(bg="#222831")  # Dark background for contrast

        # Chatbot title
        title_label = Label(window, text='THE ASSISTANT', font=("Arial", 24, "bold"), bg="#00ADB5", fg="white")
        title_label.pack(pady=10, padx=20, fill="x")

        # Frame for chat area
        chat_frame = Frame(window, bg="#393E46", bd=5, relief="ridge")
        chat_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Message session with styling
        self.message_session = Text(
            chat_frame, bd=3, relief="flat", font=("Arial", 12), undo=True, wrap="word",
            bg="#EEEEEE", fg="black", padx=10, pady=10
        )
        self.message_session.config(state='disabled', height=18)

        # Scrollbar styling
        self.overscroll = Scrollbar(chat_frame, command=self.message_session.yview, bg="#00ADB5")
        self.overscroll.config(width=15, troughcolor="#393E46", activebackground="#00ADB5")
        self.message_session["yscrollcommand"] = self.overscroll.set

        # Entry for user message with rounded edges and padding
        self.Message_Entry = Entry(window, width=40, font=('Arial', 12), bd=2, relief="flat")
        self.Message_Entry.configure(bg="#393E46", fg="white", insertbackground="white")
        self.Message_Entry.bind('<Return>', self.reply_to_you)

        # Send button with animation
        self.send_button = Button(
            window, text='Send', fg='white', bg='#FF5722', font=('Arial', 12), relief='flat',
            activebackground="#FF3D00", activeforeground="white", command=self.reply_to_you
        )
        self.send_button.configure(width=10, padx=5, pady=5)
        self.send_button.bind("<Enter>", self.on_enter)
        self.send_button.bind("<Leave>", self.on_leave)

        # Layout adjustments for styling
        self.message_session.pack(side="left", fill="both", expand=True)
        self.overscroll.pack(side="right", fill="y")
        self.Message_Entry.pack(pady=(0, 10), padx=10, ipady=5)
        self.send_button.pack(pady=5)

        # Load the knowledge base
        self.Brain = json.load(open('knowledge.json'))

    def on_enter(self, event):
        """Change button color on hover."""
        self.send_button['bg'] = '#FF3D00'

    def on_leave(self, event):
        """Revert button color when not hovering."""
        self.send_button['bg'] = '#FF5722'

    def add_chat(self, message, sender="user"):
        """Add chat to message session with sender differentiation."""
        self.message_session.config(state='normal')
        
        if sender == "user":
            message = f"You: {message}\n"
            self.message_session.tag_configure("user", foreground="black", background="#EAEAEA")
            self.message_session.insert("end", message, "user")
        else:
            message = f"TheBot: {message}\n"
            self.message_session.tag_configure("bot", foreground="white", background="#00ADB5")
            self.message_session.insert("end", message, "bot")

        self.message_session.see("end")
        self.message_session.config(state='disabled')

    def reply_to_you(self, event=None):
        """Handle user input and provide response."""
        user_message = self.Message_Entry.get().strip()
        
        if user_message:
            self.add_chat(user_message, sender="user")
            self.Message_Entry.delete(0, 'end')
            
            # Get the response from the bot's knowledge
            
            bot_reply = self.generate_reply(user_message.lower())
            self.add_chat(bot_reply, sender="bot")

    def generate_reply(self, message):
        """Generate a response based on the user's input."""
        close_match = get_close_matches(message, self.Brain.keys())
        if close_match:
            return self.Brain[close_match[0]][0]
        else:
            return "Sorry, I don't know how to respond to that."

# Initialize the application
root = Tk()
Chatbot(root)
root.mainloop()
