import re

__vowel = "[аеиоуыэюя]"
__non_vowel = "[^аеиоуыэюя]"

__RVRegExp = re.compile(__vowel)
__RRegExp = re.compile(__vowel + __non_vowel)

__PerfGerundG1 = re.compile("((<?nope>[ая])(вшись|вши|в))|(ив|ивши|ившись|ыв|ывши|ывшись)$")

__Adjective = re.compile("(ее|ие|ые|ое|ими|ыми|ей|ий|ый|ой|ем|им|ым|ом|его|ого|ему|ому|их|ых|ую|юю|ая|яя|ою|ею)$")
__Participate = re.compile("(ивш|ывш|ующ)|((<?nope>[ая])(ем|нн|вш|ющ|щ))$")
__Verb = re.compile("(ила|ыла|ена|ейте|уйте|ите|или|ыли|ей|уй|ил|ыл|им|ым|ен|ило|ыло|ено|"
                    + "ят|ует|уют|ит|ыт|ены|ить|ыть|ишь|ую|ю)|"
                    + "(ла|на|ете|йте|ли|й|л|ем|н|ло|но|ет|ют|ны|ть|ешь|нно)$")
__Noun = re.compile("(а|ев|ов|ие|ье|е|иями|ями|ами|еи|ии|и|ией|ей|ой|ий|й|иям|"
                    + "ям|ием|ем|ам|ом|о|у|ах|иях|ях|ы|ь|ию|ью|ю|ия|ья|я)$")
__Reflexive = re.compile("(ся|сь)")
__Derivational = re.compile("(ост|ость)")

__I = re.compile("(и)$")
__NN = re.compile("((<?nope>н)н)$")
__Soft = re.compile("(ь)$")

__Superlative = re.compile("(ейше|ейш)$")

def stem(words):

    return __stemWord(words)


def __stemWord(word):
    word = word.lower().replace("ё","е")

    r1 = ""
    recheck = __RVRegExp.search(word)
    if recheck:
        rv = recheck.end(0)
    else:
        rv = len(word)

    recheck = __RRegExp.search(word)
    if recheck:
        r1 = word[recheck.end(0):]

    recheck = __RRegExp.search(r1)
    if recheck:
        r2 = recheck.end(0)
    else:
        r2 = len(word)

    word, _ = __step_1(word, rv)
    word, _ = __step_2(word, rv)
    word, _ = __step_3(word, r2)
    word = __step_4(word, rv)
    return word


def __step_1(word, rv):
    word, _ = __replace_re(__PerfGerundG1, word, rv)
    word, _ = __replace_re(__Reflexive, word, rv)
    word, match = __replace_re(__Adjective, word, rv)
    if match:
        return __replace_re(__Participate, word, rv)
    word, match = __replace_re(__Verb, word, rv)
    if match:
        return word,_
    return __replace_re(__Noun, word, rv)


def __step_2(word, rv):
    return __replace_re(__I, word, rv)


def __step_3(word, rv):
    return __replace_re(__Derivational, word, rv)


def __step_4(word, rv):
    recheck = __Derivational.search(word, rv)
    if recheck:
        return word[:recheck.start(0)]

    word, _ = __replace_re(__Superlative, word, rv)
    word, match = __replace_re(__NN, word, rv)
    if not match:
        word, _ = __replace_re(__Soft, word, rv)
    return word


def __replace_re(regexp, word, rv):
    if rv:
        recheck = regexp.search(word,rv)
    else:
        recheck = regexp.search(word)
    if recheck:
        try:
            ignore = recheck.group("nope") or ""
        except IndexError:
            return word[:recheck.start()], True
        else:
            return word[:recheck.start() + len(ignore)], True
    return word, False


