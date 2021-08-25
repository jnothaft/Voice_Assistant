# -*- coding: utf-8 -*-

from funcoes import *
import speech_recognition as sr
import requests
import pyttsx3
import unidecode as unidecode
from gtts import gTTS
import os
from datetime import date


def qrfunc():
    pass


def cardfunc():
    pass


def iosfunc():
    output = 'Para baixar o aplicativo para iphone é muito fácil! Só seguir esse link aqui!'
    myobj = gTTS(text=output, lang=language, slow=False)
    myobj.save("baby.mp3")
    os.system("mpg321 baby.mp3")
    os.system("open https://apps.apple.com/sr/app/ame-digital/id1371680463")


def androidfunc():
    output = 'Para baixar o aplicativo para android é muito fácil! Só seguir esse link aqui!'
    myobj = gTTS(text=output, lang=language, slow=False)
    myobj.save("baby.mp3")
    os.system("mpg321 baby.mp3")
    os.system("open https://play.google.com/store/apps/details?id=com.b2winc.amedigital&hl=en_US&gl=US")


def customer_support():
    pass



convo_tree = {
    'você já baixou o aplicativo da ame digital': {
        'sim': 'você já adicionou e autenticou o seu cartão na sua carteira?',
        'não': 'Você tem iphone ou algum outro telefone?'
    },
    'você já adicionou e autenticou o seu cartão na sua carteira?': {
        'sim': 'você já escaneou o qr code na  catraca?',
        'não': 'Para fazer isso é muito fácil! Abra o aplicativo da ame \
                digital, clique na sua carteira e \
                clique em cadastrar cartão de crédito. Ah e não se esqueça \
                de autenticar seu cartão e colocá-lo como principal!'
    },
    'você já escaneou o qr code na  catraca?': {
        'sim': 'Não se preocupe, você será encaminhado para um atendente\
                assim ele estiver disponível!',
        'não': 'Nesse caso, abra o aplicativo da Ame Digital e siga os seguintes passos: \
                 Primeiro, clique em pagar e depois clique em pagar na lojas americanas. \
                 Aí é só escanear o QR code na catraca!'

    },
    'Não se preocupe, você será encaminhado para um atendente \
     assim ele estiver disponível!': {
        'other': customer_support
    },
    'Nesse caso, abra o aplicativo da Ame Digital e siga os seguintes passos: \
     Primeiro, clique em pagar e depois clique em pagar na lojas americanas. \
     Aí é só escanear o QR code na catraca!': {
        'other': qrfunc
    },
    'Para fazer isso é muito fácil! Abra o aplicativo da ame \
     digital, clique na sua carteira e \
     clique em cadastrar cartão de crédito. Ah e não se esqueça \
     de autenticar seu cartão e colocá-lo como principal!': {
        'other': cardfunc
    },
    'Você tem iphone ou algum outro telefone?': {
        'sim': 'Para baixar o aplicativo para iphone é muito fácil! Só seguir esse link aqui!',
        'não': 'Para baixar o aplicativo para android é muito fácil! Só seguir esse link aqui!'
    },
    'Para baixar o aplicativo para iphone é muito fácil! Só seguir esse link aqui!': {
        'other': iosfunc
    },
    'Para baixar o aplicativo para android é muito fácil! Só seguir esse link aqui!': {
        'other': androidfunc
    }
}


class Amanda:
    def restart_position(self):
        return 'você já baixou o aplicativo da ame digital'

    def __init__(self, convo_config: dict):
        self.conversation_tree = convo_config
        # start position
        self.position = self.restart_position()

    # Returns a string if follow up question, returns a -1 if stopping
    def conv_reponse(self, user_input):
        amanda_reponse = self.conversation_tree[self.position]

        # Map to yes/no to ios/android (makes tree easier)
        if user_input == 'iphone' or user_input == 'outro telefone':
            user_input = 'sim' if user_input == 'iphone' else 'não'

        if user_input in ['sim', 'não']:
            self.position = amanda_reponse[user_input]
            return self.check_for_exit(self.position)

        # repeat the question since input is not understood
        else:
            return self.position

    def check_for_exit(self, pos):
        amanda_reponse = self.conversation_tree[pos]
        if 'other' in amanda_reponse:
            amanda_reponse['other']()
            return "Posso te ajudar com mais alguma coisa???"
        else:
            return pos


mytext = ''
language = 'pt-BR'
# language = 'en-US'

hello_baby = False

ultima_resposta = ''

# Start up amanda
amanda = Amanda(convo_tree)

is_in_store_conversation = False
restart_convo = True

while True:
    try:
        rec = sr.Recognizer()

        with sr.Microphone() as fala:
            frase = rec.listen(fala)

        fala = str(rec.recognize_google(frase, language=language))
        print(fala.lower())

        n = ""

        if fala.lower() == u"oi amanda":
            hello_baby = True
            print(hello_baby)
            mytext = 'olá fulano'
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("baby.mp3")
            os.system("mpg321 baby.mp3")

        if fala.lower() == u"valeu baby":
            hello_baby = False
            print(hello_baby)

        if hello_baby == True:

            user_response = fala.lower()

            if restart_convo:
                mytext = 'Posso te ajudar com alguma coisa???'
                myobj = gTTS(text=mytext, lang=language, slow=False)
                myobj.save("baby.mp3")
                os.system("mpg321 baby.mp3")
                restart_convo = False

            # Check here if should start convo about cannot get into store
            # or if already in convo about that
            if user_response == 'não consigo entrar na loja' or is_in_store_conversation:
                output = amanda.conv_reponse(user_response)
                is_in_store_conversation = True

                if output == 'Posso te ajudar com mais alguma coisa?':
                    is_in_store_conversation = False
                    amanda.position = amanda.restart_position()

                myobj = gTTS(text=output, lang=language, slow=False)
                myobj.save("baby.mp3")
                os.system("mpg321 baby.mp3")

            # Add if statements here
            frases = ["código 7342", "pesquisa no google", "concorrente", "acende a luz", "apaga a luz",
                      "quantos dias para", "olá baby", "valeu baby", "cashback", "entro na loja",
                      "outra pessoa", "meu filho", "cadastrar meu cartão", "não consigo entrar na loja",
                      "sim", 'não']

            for frase in frases:
                if frase in fala.lower():

                    if frase == u"código 7342":
                        mytext = 'Auto destruição em 5 segundos'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        break

                    elif frase == u"pesquisa no google":
                        tmp = fala.lower().split("pesquisa no google ")
                        tmp = tmp[-1]
                        tmp = unidecode.unidecode(tmp)
                        mytext = 'Pesquisando o termo ' + str(tmp)
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        os.system("open https://www.google.com/search?q=" + tmp.replace(" ", "+"))
                        break

                    elif frase == u"concorrente":
                        mytext = 'Ok Google, tocar Molejão!'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        break

                    elif frase == u"acende a luz":
                        mytext = 'Mandando para o Mosquitto'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        os.system("mosquitto_pub -h mqtt.mqtzao.com -t 'julia' -m '2'")
                        break

                    elif frase == u"apaga a luz":
                        mytext = 'Mandando para o Mosquitto'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        os.system("mosquitto_pub -h mqtt.mqtzao.com -t 'julia' -m '1'")
                        break

                    elif frase == u"quantos dias para":
                        tmp = fala.lower().split("quantos dias para ")
                        tmp = tmp[-1]
                        tmp = unidecode.unidecode(tmp)
                        today = date.today()

                        if tmp == "a primavera":
                            estacao = date(2021, 9, 22)
                            dias = estacao - today
                            dias = str(dias)
                            dias = dias.split('days')
                            dias = dias[0]
                            mytext = 'Faltam ' + dias + "dias para " + tmp
                            myobj = gTTS(text=mytext, lang=language, slow=False)
                            myobj.save("baby.mp3")
                            os.system("mpg321 baby.mp3")
                            break

                        elif tmp == "o verao":
                            estacao = date(2021, 12, 21)
                            dias = estacao - today
                            dias = str(dias)
                            dias = dias.split('days')
                            dias = dias[0]
                            mytext = 'Faltam ' + dias + "dias para " + tmp
                            myobj = gTTS(text=mytext, lang=language, slow=False)
                            myobj.save("baby.mp3")
                            os.system("mpg321 baby.mp3")
                            break

                        elif tmp == "o outono":
                            estacao = date(2022, 3, 20)
                            dias = estacao - today
                            dias = str(dias)
                            dias = dias.split('days')
                            dias = dias[0]
                            mytext = 'Faltam ' + dias + "dias para " + tmp
                            myobj = gTTS(text=mytext, lang=language, slow=False)
                            myobj.save("baby.mp3")
                            os.system("mpg321 baby.mp3")
                            break

                        elif tmp == "o inverno":
                            estacao = date(2022, 6, 21)
                            dias = estacao - today
                            dias = str(dias)
                            dias = dias.split('days')
                            dias = dias[0]
                            mytext = 'Faltam ' + dias + "dias para " + tmp
                            myobj = gTTS(text=mytext, lang=language, slow=False)
                            myobj.save("baby.mp3")
                            os.system("mpg321 baby.mp3")
                            break

                    # começo das perguntas sobre a Ame go
                    elif frase == u"cashback":
                        mytext = 'Tenho um vídeo super legal para te explicar melhor o \
                                  que é cashback. Assiste aí!'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        os.system("open https://www.youtube.com/watch?v=ax1ykxRDVVs")
                        break

                    elif frase == u"entro na loja":
                        mytext = 'Só seguir o passo a passo nesse vídeo aqui!'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        os.system("open https://www.youtube.com/watch?v=xpRWgs1YkXI")
                        break

                    elif frase == u"outra pessoa":
                        mytext = 'Pode sim! Para isso basta escanear o mesmo QR code\
                                 para todas as pessoas entrando na loja!'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        break

                    elif frase == u"meu filho":
                        mytext = 'Pode sim! Para isso basta escanear o QR code\
                                 do responsável para você e para o seu filho'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        break

                    elif frase == u"cadastrar meu cartão":
                        mytext = 'Abra o aplicativo da ame digital, clique na sua carteira e \
                                  clique em cadastrar cartão de crédito. Ah e não se esqueça \
                                  de autenticar seu cartão e colocá-lo como principal!'
                        myobj = gTTS(text=mytext, lang=language, slow=False)
                        myobj.save("baby.mp3")
                        os.system("mpg321 baby.mp3")
                        break


    except KeyboardInterrupt:
        print('Caught KeyboardInterrupt')
