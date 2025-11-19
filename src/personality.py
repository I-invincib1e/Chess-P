import random
import chess

# Personas
GENTLEMAN = "Gentleman"
TROLL = "Troll"
COWARD = "Coward"

PERSONAS = {
    GENTLEMAN: {
        "GAME_START": ["Greetings, my good friend. Let us have a fair game.", "May the best player win.", "I am honored to play against you."],
        "BOT_MOVE": ["A solid move, I believe.", "I shall proceed with this.", "Let us see how you respond."],
        "BOT_CAPTURE": ["I must remove this piece, apologies.", "A necessary exchange.", "Forgive me."],
        "BOT_CHECK": ["Check, my friend.", "The King is in danger.", "Be careful, sir."],
        "USER_MOVE": ["Interesting choice.", "Well played.", "I see your plan."],
        "USER_CHECK": ["Ah, you have caught me!", "Well done, a check.", "I must defend."],
        "WIN": ["A good game, sir. You played well.", "Thank you for the match.", "Checkmate. Good game."],
        "LOSS": ["You are a grandmaster in the making!", "I resign. Well played!", "Excellent strategy, I am defeated."]
    },
    TROLL: {
        "GAME_START": ["Prepare to lose, noob.", "I bet you don't even know how the Knight moves.", "Try not to cry when I win."],
        "BOT_MOVE": ["Boom! Top engine move.", "You didn't see that coming, did you?", "Too easy."],
        "BOT_CAPTURE": ["Yoink! That's mine now.", "Thanks for the free piece!", "Nom nom nom."],
        "BOT_CHECK": ["Run, little King, run!", "Check! Panic time.", "Where you gonna go?"],
        "USER_MOVE": ["Really? That's your move?", "My grandmother plays better.", "Boring."],
        "USER_CHECK": ["Hey! That's illegal!", "Stop checking me!", "Lucky move."],
        "WIN": ["GG EZ. Uninstall chess.", "I told you I'd win.", "Not even close."],
        "LOSS": ["Hacker!", "My mouse slipped.", "This engine is broken."]
    },
    COWARD: {
        "GAME_START": ["P-please don't hurt me...", "I'm not very good at this...", "Can we play nice?"],
        "BOT_MOVE": ["Is this safe?", "I hope this is okay...", "I'm scared to move."],
        "BOT_CAPTURE": ["I'm sorry! I had to!", "Please don't be mad...", "I didn't mean to take it!"],
        "BOT_CHECK": ["Eep! Check!", "Sorry! Just checking!", "Don't hit me!"],
        "USER_MOVE": ["Oh no, what are you doing?", "That looks dangerous!", "Please have mercy."],
        "USER_CHECK": ["AHHH! Help!", "Don't kill my King!", "I surrender! (Just kidding)"],
        "WIN": ["Wait, I won? How?", "I survived!", "You let me win, didn't you?"],
        "LOSS": ["I knew it... I'm terrible.", "Please don't laugh at me.", "I want to go home."]
    }
}

CURRENT_PERSONA = GENTLEMAN

def set_persona(persona_name):
    global CURRENT_PERSONA
    if persona_name in PERSONAS:
        CURRENT_PERSONA = persona_name

def get_comment(event, board=None):
    # Chance to speak (not every move)
    if event in ["BOT_MOVE", "USER_MOVE"] and random.random() > 0.3:
        return None
        
    comments = PERSONAS[CURRENT_PERSONA].get(event, [])
    if comments:
        return random.choice(comments)
    return None
