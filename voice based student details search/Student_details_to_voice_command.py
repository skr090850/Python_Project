import speech_recognition as sr
import gtts
import playsound
import student_record as st
s=sr.Recognizer()

#inputted data whether voice or type.........
data= input("For say to type 'S' and For write to type any other character = ")
if data == 'S':
    print("Say Student I'D....")
    
    # input id number through voice command.......
    with sr.Microphone() as m:
        audio=s.listen(m)
        
        # recognize and convert voice command to written type data in english language
        text=s.recognize_google(audio,language='eng-in')
        
        #print inputted id number of voice in english language........
        print("\n\nYou said I'D is....",text)
else:
    
    # input id number from type command..........
    text=input("Enter the student I'D: ")

print("\n\n")
    
#search record of student from other module(student_record)
text=st.search_id(text)

#print student record of inputted id number
print(text)

#convert data of student record to voice type 
sound=gtts.gTTS(text,lang="en")
sound.save("student_record.mp3")
#play data of student_record
playsound.playsound("student_record.mp3")












# repeat=input("If you stop the program then type 'ST' and for repeat the program you type any character = ")
# if repeat=='ST':
#     break
