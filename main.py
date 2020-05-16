import speech_recognition as sr
import distance as dis
import matplotlib.pyplot as plot
import wavio

class Speech:
    def __init__(self, name):
        self.original = []
        self.recognized = []
        self.similarity = []
        self.name = name
  
    def read_original(self, inFile):
        with open(inFile, "r") as file:
            self.original = file.readlines()

    def conv_audio(self, inDir):
        r = sr.Recognizer()
        audioFile = sr.WavFile(inDir)
        sentence = ""
        with audioFile as source:
            audio = r.record(source)
        try:
            sentence = r.recognize_google(audio)
            self.recognized.append(sentence)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            self.recognized.append("")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return sentence

    def comp_string(self):
        for o, r in zip(self.original, self.recognized):
            sentence_og = o.rstrip().split()
            sentence_rec = r.rstrip().split()
            self.similarity.append(dis.levenshtein(sentence_og, sentence_rec))
        return self.similarity

    def add_string(self, sentence):
        with open(self.name+".txt", "a") as f:
            f.write(sentence+"\n")


if __name__ == '__main__':
    female = Speech("female")
    female.read_original("original.txt")
    for i in range(1, 26):
        if i < 10:
            sentence = "03-English-Female-Sent0" + str(i) + ".wav"
        else:
            sentence = "03-English-Female-Sent" + str(i) + ".wav"
        female.conv_audio(sentence)

    accent = Speech("accent")
    accent.original = female.original
    for i in range(1, 26):
      if i < 10:

        sentence = "11-Chinese-Male-Sent0" + str(i) + ".wav"
      else:
        sentence = "11-Chinese-Male-Sent" + str(i) + ".wav"
      accent.conv_audio(sentence)


    justin = Speech("justin")
    justin.original = female.original
    for i in range(1, 26):
        if i < 10:
            sentence = "09-English-Male-Sent0" + str(i) + ".wav"
        else:
            sentence = "09-English-Male-Sent" + str(i) + ".wav"
        justin.conv_audio(sentence)

    plot.boxplot([justin.comp_string(), accent.comp_string()])
    plot.title("English vs Chinese")
    plot.xticks([1, 2], ["English", "Chinese"])
    plot.ylabel("Data")
    plot.show()

    plot.boxplot([justin.comp_string(), female.comp_string()])
    plot.title("Male vs Female")
    plot.xticks([1, 2], ["Male", "Female"])
    plot.ylabel("Data")
    plot.show()





