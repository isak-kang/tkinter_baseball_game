import random
import itertools
import time
import tkinter as tk

tkt = tk.Tk()

class NotANumberError(Exception): # 숫자가 아닐 때 나타나는 오류
    pass
class DuplicateNumberError(Exception): # 중복숫자가 있을 때 나타나는 오류
    pass

#변수들.
my_secret_number = []   # 내 숫자
my_stovlaue = ""    # 내가 컴퓨터 숫자를 예측한 결과를 저장
com_stovlaue = ""   # 컴퓨터가 내 숫자를 예측한 결과를 저장
all_number = list(itertools.permutations(range(0, 9), 3))   #0~9까지 중복되지 않는 3가지 숫자의 모든 경우의 수
end_game = 0 #게임이 끝나면 1 그게 아니면 0


## 기본 함수
#모든 경우의 수
def generate_all_possible_numbers():
    return list(itertools.permutations(range(0, 9), 3))

# 컴퓨터가 자신의 숫자를 정함.
def generate_secret_number(): 
    return list(random.sample(range(0,9),3))



## 프레임 전환에 관한 함수
# 화면전화
def open_frame(frame):
    global com_secret_number

    frame.place(x=0,y=0) # 프레임 배치
    com_secret_number = generate_secret_number() # 컴퓨터 숫자 다시정함.

    if frame == solo_frame: # solo모드의 창의 크기와 위치 
        width = 800 #넓이
        height = 350 #높이
        pos_x = 300 #x축 위치
        pos_y = 200 #y축 위치
        tkt.geometry("{}x{}+{}+{}".format(width,height,pos_x,pos_y)) 
    elif frame == vscom_frame : # vscom모드의 창의 크기
        width = 1130
        height = 380
        pos_x = 300
        pos_y = 200
        tkt.geometry("{}x{}+{}+{}".format(width,height,pos_x,pos_y))
    else : # main화면의 창의 크기
        width = 800
        height = 400
        pos_x = 300
        pos_y = 200
        tkt.geometry("{}x{}+{}+{}".format(width,height,pos_x,pos_y))

# 화면 숨기기
def hide_frame(frame):
    frame.place_forget() #프레임 숨기기

## vs com
# 내 비밀숫자 정하기 
def 내숫자정하기(n):
    global my_secret_number

    choice_number = vscom_entry.get().split() # 입력창에서 숫자 이력 받기 (문자열형식으로 리스트에 저장) ex) 1 2 3
    my_number_text = vscom_my_number_label_1.cget("text")  # 내 숫자에 첫번째 칸에 텍스트를 가져옴
    
    if my_number_text: # 만약 내 숫자가 입력되어 있다면 밑에 함수를 실행 
        vscom_game_my_turn(choice_number)

    else: # 만약 없다면 내 숫자가 없다면 내 숫자를 정함.
        try:
            if len(choice_number) != 3: # 만약 입력값이 3자리 숫자가 아니면 IndexError실행
                raise IndexError("*오류* 내 비밀숫자를 정하는 과정\n 3자리 숫자를 입력해주세요.")
            for i in range(3):
                if not choice_number[i].isdigit(): # 각자리에 값들이 숫자가 아니면 NotANumberError실행
                    raise NotANumberError("*오류* 내 비밀숫자를 정하는 과정\n 숫자를 입력하세요.")
                if not (0 <= int(choice_number[i]) < 10): # 각자리에 값들이 0~9의 범위가 아니면 ValueError 실행
                    raise ValueError("*오류* 내 비밀숫자를 정하는 과정\n 0에서 9 사이의 숫자를 입력하세요.")

            choice_number = list(map(int, choice_number)) # 문자열형식을 정수형식으로 바꾸고 리스트에 저장

            if len(set(choice_number)) < 3: # 중복숫자가 있으면 DuplicateNumberError실행
                raise DuplicateNumberError("*오류* 내 비밀숫자를 정하는 과정\n 중복된 숫자가 있습니다.")

            my_secret_number = choice_number #입력한 숫자를 내 숫자로 지정함.

            vscom_my_number_label_1.config(text = my_secret_number[0]) # 내 숫자를 각각 보여줌. 
            vscom_my_number_label_2.config(text = my_secret_number[1])
            vscom_my_number_label_3.config(text = my_secret_number[2])
            vscom_entry.delete(0, tk.END) # 입력창 초기화
#?            vscom_my_display_label.config(text = "                                    ")

        # 각각의 예외들이 나타났을 때
        except DuplicateNumberError as dne:#중복        
            vscom_my_display_label.config(text= dne)
            vscom_entry.delete(0, tk.END)
        except NotANumberError as nane:#숫자x
            vscom_my_display_label.config(text= nane)
            vscom_entry.delete(0, tk.END)        
        except ValueError as ve:#각 숫자가 범위에 벗어남
            vscom_my_display_label.config(text= ve)
            vscom_entry.delete(0, tk.END)        
        except IndexError as ie:#3자리 숫자가 아님.
            vscom_my_display_label.config(text= ie)
            vscom_entry.delete(0, tk.END)        
        except Exception:#예상치못한오류
            vscom_my_display_label.config(text= "*오류* 내 비밀숫자를 정하는 과정\n 예상치못한오류")
            vscom_entry.delete(0, tk.END)
            
# 컴퓨터 비밀 숫자 예측하는 함수
def vscom_game_my_turn(choice_number):
    global my_stovlaue,com_secret_number,end_game
    if end_game == 0 : # 게임이 종료되었냐 안되었냐를 나타내는 함수 (0 : 실행중, 1: 종료)
        try:
            if len(choice_number) != 3:
                raise IndexError("*오류* 3자리 숫자를 입력해주세요.")
            for i in range(3):
                if not choice_number[i].isdigit():
                    raise NotANumberError("*오류* 숫자를 입력하세요.")
                if not (0 <= int(choice_number[i]) < 10):
                    raise ValueError("*오류* 0에서 9 사이의 숫자를 입력하세요.")

            choice_number = list(map(int, choice_number))

            if len(set(choice_number)) < 3:
                raise DuplicateNumberError("*오류* 중복된 숫자가 있습니다.")

            s,b = 0,0 #strike , ball

            if com_secret_number == choice_number : # 상대(컴퓨터)숫자와 내가 입력한 값이 같을 때 
                vscom_my_display_label.config(text= my_stovlaue + f"{com_secret_number} : 정답 !!") # 지금까지의 결과와 정답을 공개
                vscom_com_number_label_1.config(text=com_secret_number[0]) # 정답을 맞췄기 때문에 상대(컴퓨터)숫자를 공개
                vscom_com_number_label_2.config(text=com_secret_number[1]) 
                vscom_com_number_label_3.config(text=com_secret_number[2])
                vscom_entry.delete(0, tk.END) 
                vscom_com_display_label.config(text= com_stovlaue + "닝겐 봐줬다 다시 뜨자.") # 컴퓨터의 결과창에 지금까지의 결과와 "졌다"를 선언
                vscom_com_input_display_label.config(text= "내가 졌다. 닝겐 ㅜ^ㅜ ") # 컴퓨터의 입력창? 진행창?에 "졌다"를 선언  
                end_game = 1 #게임이 종료 되었으니 end_game = 1로 지정
            else : # # 상대(컴퓨터)숫자와 내가 입력한 값이 다를 때 
                for i in range(3):
                    if choice_number[i] in com_secret_number: # 입력한 값의 각 숫자들이 상대(컴퓨터)의 숫자에 존재함. (ball)
                        if choice_number[i] == com_secret_number[i]: # 위의 조건에 부합하면서 순서까지 같음. (strike)
                            s += 1 #(내가 입력한 숫자와 상대(컴퓨터) 숫자가 순서도 같고 값도 같으면 s의 값이 1오름)
                        else :
                            b += 1 #(내가 입력한 숫자와 상대(컴퓨터) 숫자가 순서가 다르지만 값이 같으면 b의 값이 1오름)
                my_stovlaue = my_stovlaue + f"{choice_number} : {s}스트라이크 {b}볼\n" # 지금까지의 결과와 이번결과가 같이 저장됨.
                vscom_my_display_label.config(text= my_stovlaue) # 내 결과창에 strike, ball 결과가 나옴. (이전꺼도 포함,.)
                vscom_entry.delete(0, tk.END) 
                vscom_game_com_turn(1) # 컴퓨터의 턴으로 넘어감.
        except DuplicateNumberError as dne:        
            vscom_my_display_label.config(text= dne)
            vscom_entry.delete(0, tk.END)
        except NotANumberError as nane:
            vscom_my_display_label.config(text= nane)
            vscom_entry.delete(0, tk.END)        
        except ValueError as ve:
            vscom_my_display_label.config(text= ve)
            vscom_entry.delete(0, tk.END)        
        except IndexError as ie:
            vscom_my_display_label.config(text= ie)
            vscom_entry.delete(0, tk.END)        
        except Exception as e:
            vscom_my_display_label.config(text= "*오류* 예상치못한오류")
            vscom_entry.delete(0, tk.END)
    else : # end_game = 1 일 때를 말함. 게임이 종료된 상태, 만약 게임이 끝난 상황에 다시 한번 입력창에 아무거나 입력하면 실행됨
        vscom_my_display_label.config(text= "게임이 종료됐습니다.\n 다시하기 또는 뒤로가리 버튼을 \n 눌러주세요.") #게임종료를 다시 알림.
        vscom_entry.delete(0, tk.END)
        vscom_entry.config(state="disabled") # 입력창이 강제로 비활성화됨.


# 컴퓨터가 상대방의 숫자를 예측할 숫자를 정함.
def com_choice_number():
    return list(all_number[random.randint(0, len(all_number) - 1)])

# 상대방의 숫자와 내가 예측한 숫자의 결과값을 출력 (s,b)
def strike_and_ball(com_choice):
    s,b = 0,0
    for i in range(3):
        if com_choice[i] in my_secret_number:   # ball
            if com_choice[i] == my_secret_number[i]:    #strike
                s += 1
            else :
                b += 1
    return (s,b)
# 경우의 수 줄이기.
def remove_value(com_choice,s_b): 
    global all_number

    i = 0 # 인덱스

    while i<len(all_number):    # 모든 경우의 수를 다 계산하면 종료 
                                # 모든 경우의 수에서 s,b 이 똑같이 나올 수 있는 경우를 뺴고는 모두 제거함.
        st,ba = 0,0
        for j in range(3):
            if com_choice[j] in all_number[i]: 
                if com_choice[j] == all_number[i][j]:
                    st += 1
                else :
                    ba += 1
        result =(st,ba)
    
        if result == s_b : # 예측한 숫자와 all_number안에 값들의 s,t가 같으면 제거하지 않고 다음 숫자로 넘어감.
            i += 1
        else :
            all_number.pop(i)   # 반대로 틀리면 제거함.

# 컴퓨터가 내 비밀 숫자를 예측 
def vscom_game_com_turn(n):
    global com_stovlaue,all_number,end_game

    com_choice =com_choice_number() # 컴퓨터의 내 숫자 예측값
    s_b = strike_and_ball(com_choice) # strike and ball 나타냄.
    
    #? if not (vscom_my_number_label_1.cget("text")) : # 만약 내 숫자가 없으면 
    #?    vscom_my_display_label.config(text= "*오류* 내 시크릿넘버가 없습니다.")  - > 턴 넘김 버튼이 있을 때
    
    if my_secret_number == com_choice : # 내 숫자와 컴퓨터의 예측값이 같을 때
        vscom_com_display_label.config(text= com_stovlaue + f"{my_secret_number} : 정답 !!")
        vscom_com_input_display_label.config(text= "내가 이겼다 닝겐")
        vscom_my_display_label.config(text= my_stovlaue + "졌습니다. 설욕하실려면 다시하기를 누르세요.")
        vscom_com_number_label_1.config(text=com_secret_number[0]) # 게임이 끝났으니 상대(컴퓨터) 숫자를 공개
        vscom_com_number_label_2.config(text=com_secret_number[1])
        vscom_com_number_label_3.config(text=com_secret_number[2])           
        all_number = list(itertools.permutations(range(0, 9), 3)) # 모든 경우의 수를 다시 초기화함.
        end_game = 1 # 게임이 끝났으니 0 -> 1로 바꿨줬음.
    else :
        vscom_entry.delete(0,tk.END)
        vscom_com_input_display_label.config(text= "예측중입니다.....") # (상대(컴퓨터) 진행창)
        vscom_frame.update() # sleep을 쓰면 보든 동작이 멈춤으로 그 전에 업데이트를 해둠. (위에 "예측중입니다를")
        time.sleep(1) # 1초 기다렸다가. (호흡 가다듬을려고 만듬.)
        com_stovlaue = com_stovlaue + f"{com_choice} : {s_b[0]}스트라이크 {s_b[1]}볼\n"
        vscom_com_display_label.config(text= com_stovlaue)
        vscom_com_input_display_label.config(text= "예측완료\n턴을 넘기겠습니다.")
        remove_value(com_choice,s_b) # 내 결과를 토대로 경우의 수를 줄이는 함수 실행.

#초기화  - vscom
def vscom_reset():
    global my_stovlaue,com_secret_number,all_number,com_stovlaue,my_secret_number,end_game

    end_game = 0 # 게임 진행
    com_stovlaue = "" # 컴퓨터의 결과값 초기화
    my_stovlaue = "" # 내 결과값 초기화
    my_secret_number = [] # 내 숫자 초기화
    

    vscom_my_display_label.config(text= "                                    ") # 내 결과창 초기화
    vscom_com_display_label.config(text= "                                    ") # 상대(컴퓨터) 결과창 초기화

    vscom_my_number_label_1.config(text="") # 내 숫자칸 초기화
    vscom_my_number_label_2.config(text="")
    vscom_my_number_label_3.config(text="")
    vscom_com_number_label_1.config(text="?") # 상대(컴퓨터) 숫자칸 초기화
    vscom_com_number_label_2.config(text="?")
    vscom_com_number_label_3.config(text="?")
    
    vscom_entry.delete(0, tk.END)
    vscom_entry.config(state="normal") # 내 입력창 다시 활성화
    vscom_com_input_display_label.config(text= "                                    ") # 상대(컴퓨터) 진행창 초기화


    com_secret_number = generate_secret_number() # 상대(컴퓨터) 숫자 초기화
    all_number = list(itertools.permutations(range(0, 9), 3)) # 경우의 수 초기화 (컴퓨터 사용)



## solo game
# 컴퓨터 숫자예측
def solo_game(n):
    global my_stovlaue,com_secret_number, end_game
    if end_game == 0:      # 게임 진행중
        try:
            choice_number = solo_entry.get().split() # 예측숫자 (문자열)
            if len(choice_number) != 3:
                raise IndexError("*오류* 3자리 숫자를 입력해주세요.")
            for i in range(3):
                if not choice_number[i].isdigit():
                    raise NotANumberError("*오류* 숫자를 입력하세요.")
                if not (0 <= int(choice_number[i]) < 10):
                    raise ValueError("*오류* 0에서 9 사이의 숫자를 입력하세요.")

            choice_number = list(map(int, choice_number)) # 예측숫자 (정수형)

            if len(set(choice_number)) < 3:
                raise DuplicateNumberError("*오류* 중복된 숫자가 있습니다.")

            s,b = 0,0

            if com_secret_number == choice_number : # 내 예측과 상대(컴퓨터)숫자가 같을 때
                solo_display_label.config(text= my_stovlaue + f"{com_secret_number} : 정답 !!")
                solo_number_label_1.config(text=com_secret_number[0])
                solo_number_label_2.config(text=com_secret_number[1])
                solo_number_label_3.config(text=com_secret_number[2])
                solo_entry.delete(0, tk.END)
                end_game = 1
            else : # 내 예측과 상대(컴퓨터) 숫자가 다를 때
                for i in range(3):
                    if choice_number[i] in com_secret_number:
                        if choice_number[i] == com_secret_number[i]:
                            s += 1
                        else :
                            b += 1
                my_stovlaue = my_stovlaue + f"{choice_number} : {s}스트라이크 {b}볼\n"
                solo_display_label.config(text= my_stovlaue)
                solo_entry.delete(0, tk.END)

        except DuplicateNumberError as dne:        
            solo_display_label.config(text= dne)
            solo_entry.delete(0, tk.END)
        except NotANumberError as nane:
            solo_display_label.config(text= nane)
            solo_entry.delete(0, tk.END)        
        except ValueError as ve:
            solo_display_label.config(text= ve)
            solo_entry.delete(0, tk.END)        
        except IndexError as ie:
            solo_display_label.config(text= ie)
            solo_entry.delete(0, tk.END)        
        except Exception as e:
            solo_display_label.config(text= "*오류* 예상치못한오류")
            solo_entry.delete(0, tk.END)        
    else: 
        solo_display_label.config(text= "게임이 종료됐습니다.\n 다시하기 또는 뒤로가리 버튼을 \n 눌러주세요.")
        solo_entry.delete(0, tk.END)
        solo_entry.config(state="disabled")
    

# 초기화 - solo
def solo_reset(): 
    global my_stovlaue,com_secret_number,end_game

    end_game = 0
    my_stovlaue = ""
    
    solo_display_label.config(text= "                                    ")
    solo_number_label_1.config(text="?")
    solo_number_label_2.config(text="?")
    solo_number_label_3.config(text="?")
    solo_entry.config(state="normal")
    com_secret_number = generate_secret_number()





# 프로그램 이름
tkt.title("야구게임")


# 프레임 생성
main_frame = tk.Frame(tkt)
solo_frame = tk.Frame(tkt)
vscom_frame = tk.Frame(tkt)

# 게임 모드 선택 (혼자 , vs com) 버튼 클릭하면 다른 프레임으로 이동.
solo_mode_button = tk.Button(main_frame,text="solo", width=30, height=5,borderwidth=2, relief="solid", command= lambda : (open_frame(solo_frame),hide_frame(main_frame)))
solo_mode_button.grid(column=0,row=0,padx=300,pady=(100,0)) 
vscom_mode_button = tk.Button(main_frame,text="vs com", width=30, height=5,borderwidth=2, relief="solid", command= lambda : (open_frame(vscom_frame),hide_frame(main_frame)))
vscom_mode_button.grid(column=0,row=1,padx=300,pady=(0,50)) 



## vscom mode
# 내가 컴퓨터 비밀 숫자를 예측한 결과 나오는 창
vscom_my_display_label = tk.Label(vscom_frame,text="                                    ",bg="gray",height=15,anchor="n",borderwidth=2, relief="solid")
vscom_my_display_label.grid(column=0,row=1,ipadx=50,columnspan=3,ipady=15,sticky="w")
# 상대(컴퓨터)의 숫자를 나타내는 창
vscom_com_number_label = tk.Label(vscom_frame,width=10,height=15,borderwidth=2, relief="solid") # 각 값들을 나타내는 라벨들의 배경
vscom_com_number_label.grid(column=0,row=0,columnspan=3,ipadx=50)
vscom_com_number_label.grid_columnconfigure((0,1,2),weight=1) # 가중치 각 열에 - > 중앙 정렬 시키기위해
vscom_com_number_label_1 = tk.Label(vscom_com_number_label,text= "?",width=5) # 각각의 상대 숫자를 나타내는 창(1)
vscom_com_number_label_1.grid(column=0,row=0,sticky="n")
vscom_com_number_label_2 = tk.Label(vscom_com_number_label,text= "?",width=5) # 각각의 상대 숫자를 나타내는 창(2)
vscom_com_number_label_2.grid(column=1,row=0,sticky="n")
vscom_com_number_label_3 = tk.Label(vscom_com_number_label,text= "?",width=5) # 각각의 상대 숫자를 나타내는 창(3)
vscom_com_number_label_3.grid(column=2,row=0,sticky="n")
# 상대(컴퓨터)가 숫자를 예측한 결과 나오는 창 (상대(컴퓨터)의 결과창)
vscom_com_display_label = tk.Label(vscom_frame,text="                                    ",bg="gray",height=15,anchor="n",borderwidth=2, relief="solid")
vscom_com_display_label.grid(column=5,row=1,ipadx=50,columnspan=3,ipady=15,sticky="w")
# 내 숫자를 보여주는 창
vscom_my_number_label = tk.Label(vscom_frame,width=10,height=15,borderwidth=2, relief="solid") # 각 값들을 나타내는 라벨들의 배경
vscom_my_number_label.grid(column=5,row=0,columnspan=3,ipadx=50)
vscom_my_number_label.grid_columnconfigure((0,1,2),weight=1) # 가중치 각 열에 - > 중앙 정렬 시키기위해
vscom_my_number_label_1 = tk.Label(vscom_my_number_label,text= "",width=5) # 각각의 내 숫자를 나타내는 창(1)
vscom_my_number_label_1.grid(column=0,row=0,sticky="n")
vscom_my_number_label_2 = tk.Label(vscom_my_number_label,text= "",width=5) # 각각의 내 숫자를 나타내는 창(2)
vscom_my_number_label_2.grid(column=1,row=0,sticky="n")
vscom_my_number_label_3 = tk.Label(vscom_my_number_label,text= "",width=5) # 각각의 내 숫자를 나타내는 창(3)
vscom_my_number_label_3.grid(column=2,row=0,sticky="n")
# 상대(컴퓨터)의 현재 동작을 설명해주는 창 (진행창)
vscom_com_input_display_label = tk.Label(vscom_frame,text="                                    ",anchor="n",bg="white",borderwidth=2, relief="solid")
vscom_com_input_display_label.grid(column=5,row=2,ipadx=50,columnspan=3,ipady=15,sticky="w")
# 입력창 (내 숫자 입력, 상대(컴퓨터) 숫자 예측값 입력)
vscom_entry = tk.Entry(vscom_frame,justify="right")
vscom_entry.grid(column=0,row=2,columnspan=3,ipadx=50,ipady=15)
vscom_entry.bind("<Return>",내숫자정하기)   # 입력창에서 엔터를 누르면 '내숫자정하기'함수 실행
# 입력창에서 입력된 값으로 '내숫자정하기'함수 실행 (입력버튼)
vscom_ok_button = tk.Button(vscom_frame, text="입력",command= lambda : 내숫자정하기(1)).grid(column=3,row=2,ipady=15,sticky="w",padx=(0,40)) 
# 뒤로가기버튼 
vscom_back_button = tk.Button(vscom_frame,text="뒤로가기",command= lambda : (open_frame(main_frame),hide_frame(vscom_frame),vscom_reset()))
vscom_back_button.grid(column=8,row=0,sticky="e",padx=20)
# 다시하기버튼
reset_button = tk.Button(vscom_frame,text="다시하기",command= lambda : vscom_reset()) 
reset_button.grid(column=8,row=1,sticky="en",padx=20)
# 턴넘김버튼
#? vscom_turn_pass = tk.Button(vscom_frame,text="턴넘김",command= lambda : vscom_game_com_turn(my_secret_number))
#? vscom_turn_pass.grid(column=4,row=1,padx=(0,40),sticky="w") - >이제는 필요없는 부분

# 설명서
game_manual_label = tk.Label(vscom_frame,text= 
"""1. 내 secret number를 지정합니다.
2. 그 후 상대(컴퓨터)의 secret number를 예측합니다.
3. 내가 예측한 다음 컴퓨터가 자동으로 내 secret number를 예측합니다.
4. 게임이 끝나면 다시하기나 뒤로가기 버튼을 누릅니다.

입력창 작성 방법 = 숫자와 숫자사이 띄어쓰기
EX) 1 2 3
중복숫자x, 숫자범위 = 0~9, 오직 숫자만입력가능, 무조건 3자리 숫자만 입력가능""",
justify="left")
game_manual_label.grid(column=9,row=1,columnspan=10,sticky="wn")



## solo mode
# 내가 컴퓨터 비밀 숫자를 예측한 결과 나오는 창(결과창)
solo_display_label = tk.Label(solo_frame, text="                                    ",bg="gray",height=15,anchor="n",borderwidth=2, relief="solid")
solo_display_label.grid(column=0,row=1,ipadx=50,columnspan=3,ipady=15,sticky="wn")              
# 상대(컴퓨터)의 숫자를 나타내는 창
solo_number_label = tk.Label(solo_frame,width=10,height=15,borderwidth=2, relief="solid") # 각 값들을 나타내는 라벨들의 배경
solo_number_label.grid(column=0,row=0,columnspan=3,ipadx=50)
solo_number_label.grid_columnconfigure((0,1,2),weight=1) # 각 열에 가중치 -> 중앙 정렬 시키기위해
solo_number_label_1 = tk.Label(solo_number_label,text= "?",width=5) # 각각의 상대 숫자를 나타내는 창(1)
solo_number_label_1.grid(column=0,row=0)
solo_number_label_2 = tk.Label(solo_number_label,text= "?",width=5) # 각각의 상대 숫자를 나타내는 창(2)
solo_number_label_2.grid(column=1,row=0)
solo_number_label_3 = tk.Label(solo_number_label,text= "?",width=5) # 각각의 상대 숫자를 나타내는 창(3)
solo_number_label_3.grid(column=2,row=0)
# 입력창 (컴퓨터 숫자 예측값 입력)
solo_entry = tk.Entry(solo_frame, justify="right")
solo_entry.grid(column=0,row=2,columnspan=3,ipadx=50,ipady=15)
solo_entry.bind("<Return>",solo_game) # 엔터치면 solo_game함수 실행
# 버튼 누르면 solo_game함수 실행 (입력버튼)
solo_ok_button = tk.Button(solo_frame, text="입력",command= lambda : solo_game(1)).grid(column=3,row=2,ipady=15,sticky="w")
# 뒤로가기버튼
solo_back_button = tk.Button(solo_frame,text="뒤로가기",command= lambda : (open_frame(main_frame),hide_frame(solo_frame),solo_reset()))
solo_back_button.grid(column=4,row=0,sticky="en")
# 다시하기버튼
reset_button = tk.Button(solo_frame,text="다시하기",command= lambda : (solo_reset()))
reset_button.grid(column=4,row=1,sticky="en")

# 설명서
game_manual_label = tk.Label(solo_frame,text= 
"""입력창 작성 방법 = 숫자와 숫자사이 띄어쓰기
EX) 1 2 3
중복숫자x, 숫자범위 = 0~9, 오직 숫자만입력가능, 무조건 3자리 숫자만 입력가능""",
justify="left")
game_manual_label.grid(column=5,row=1,columnspan=10,sticky="wn")







# 시작 프레임은 main frame
open_frame(main_frame)
# 시작
tkt.mainloop()

## 뒤로가기 버튼
## 게임성공하면 다시하기 버튼
## 버그찾기

        
## 경우의 수 줄이는 함수 만들기
## 한턴씩 돌아가면서 게임할 수 있게 한턴에 대한 함수 만들기
## 메인게임 전체에 대해 정의하기.


# 함수에 변수주기 안됐음.
# 변수의 위치
# 적절한 알고리즘찾기
# 프레임 전환에 문제점 -> 다른 프레임의 위젯이 보임 ->.place.forget() ?? 그냥 배치 안하다가 배치하는 방법은?? 
# config 안되네 a(~~).grid()하면 
