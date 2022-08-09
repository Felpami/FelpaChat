import emoji

def emoji_converter(msg):
    if ":D" in msg:
        return msg.replace(":D", ":grinning_face_with_smiling_eyes:")
    elif "xD" in msg:
        return msg.replace("xD", ":rolling_on_the_floor_laughing:")
    elif "Dx" in msg:
        return msg.replace("Dx", ":persevering_face:")
    elif ":)" in msg:
        return msg.replace(":)", ":slightly_smiling_face:")
    elif "(:" in msg:
        return msg.replace("(:", ":slightly_smiling_face:")
    elif ":(" in msg:
        return msg.replace(":(", ":slightly_frowning_face:")
    elif "):" in msg:
        return msg.replace("):", ":slightly_frowning_face:")
    elif "._." in msg:
        return msg.replace("._.", ":neutral_face:")
    elif "-_-" in msg:
        return msg.replace("-_-", ":expressionless_face:")
    elif "q.q" in msg:
        return msg.replace("q.q", ":loudly_crying_face:")
    elif "Q.Q" in msg:
        return msg.replace("Q.Q", ":loudly_crying_face:")
    elif "Q_Q" in msg:
        return msg.replace("Q_Q", ":loudly_crying_face:")
    elif "<3" in msg:
        return msg.replace("<3", ":red_heart:")
    elif "UwU" in msg:
        return msg.replace("UwU", ":smiling_face_with_heart-eyes:")
    else:
        return msg

