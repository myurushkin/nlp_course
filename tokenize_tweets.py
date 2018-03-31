import sys
import re

FLAGS = re.MULTILINE | re.DOTALL

def hashtag(text):
    text = text.group()
    hashtag_body = text[1:]
    if hashtag_body.isupper():
        result = "HASHTAG {} ALLCAPS".format(hashtag_body)
    else:
        result = " ".join(["HASHTAG"] + re.split(r"(?=[A-Z])", hashtag_body, flags=FLAGS))
    return result

def allcaps(text):
    text = text.group()
    return text + " ALLCAPS"


def tokenize(text):
    # Different regex parts for smiley faces
    eyes = r"[8:=;]"
    nose = r"['`\-]?"

    # function so code less repetitive
    def re_sub(pattern, repl):
        return re.sub(pattern, repl, text, flags=FLAGS)

    text = re_sub(r"https?:\/\/\S+\b|www\.(\w+\.)+\S*", "URL")
    text = re_sub(r"/"," / ")
    text = re_sub(r"@\w+", "USER")
    text = re_sub(r"{}{}[)dD]+|[)dD]+{}{}".format(eyes, nose, nose, eyes), "SMILE")
    text = re_sub(r"{}{}p+".format(eyes, nose), "LOLFACE")
    text = re_sub(r"{}{}\(+|\)+{}{}".format(eyes, nose, nose, eyes), "SADFACE")
    text = re_sub(r"{}{}[\/|l*]".format(eyes, nose), "NEUTRALFACE")
    text = re_sub(r"<3","HEART")
    text = re_sub(r"[-+]?[.\d]*[\d]+[:,.\d]*", "NUMBER")
    text = re_sub(r"#\S+", hashtag)
    text = re_sub(r"([!?.]){2,}", r"\1 REPEAT")
    text = re_sub(r"\b(\S*?)(.)\2{2,}\b", r"\1\2 ELONG")

    ## -- I just don't understand why the Ruby script adds <allcaps> to everything so I limited the selection.
    # text = re_sub(r"([^a-z0-9()<>'`\-]){2,}", allcaps)
    text = re_sub(r"([A-Z]){2,}", allcaps)

    return text
