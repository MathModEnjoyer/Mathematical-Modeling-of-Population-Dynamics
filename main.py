from tkinter import *
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import sys

def formShow():
    def graph():
        def update(frameIteration):
            def colorPick(digit):
                if digit % 5 == 0:
                    return 'r'
                elif digit % 5 == 1:
                    return 'g'
                elif digit % 5 == 2:
                    return 'b'
                elif digit % 5 == 3:
                    return 'y'
                elif digit % 5 == 4:
                    return 'b'

            populationSum = 0
            if(frameIteration != int(float(eTime.get()) / float(eStep.get())) // 100 - 1):
                for i in range(int(ePopulationStrength.get())):
                    plt.plot(timeRange[frameIteration * 100: 100 * frameIteration + 100:], populationCount[i][frameIteration * 100: 100 * frameIteration + 100:], c = colorPick(i))  
                    populationInfo[i]['text'] = "Популяция " + str(i) + ", количество: " + str(populationCount[i][100 * frameIteration + 100])
                    populationSum+=populationCount[i][100 * frameIteration + 100]
            else:
                for i in range(int(ePopulationStrength.get())):
                    plt.plot(timeRange[frameIteration * 100: -1:], populationCount[i][frameIteration * 100: -1:], c = colorPick(i))  
                    populationInfo[i]['text'] = "Популяция " + str(i) + ", количество: " + str(populationCount[i][-1])
                    populationSum+=populationCount[i][-1]
            populationInfo[-1]['text'] = "Cуммарное количество: " + str(populationSum)

        plt.clf()
        fig = plt.figure("figure")
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().place(x = 250, y = 240)
        # toolBar = NavigationToolbar2Tk(canvas, window, pack_toolbar=True)
        # toolBar.place(x = 250, y = 240)

        frame3 = Frame(window)
        frame3.place(x = 890, y = 240)
        frame3.configure(width = 550, height = 480)
        populationInfo = []
        for i in range(int(ePopulationStrength.get())):
            populationInfo.append(Label(frame3, text = "Популяция " + str(i) + ", количество: "))
            populationInfo[i].place(x = 120, y = 20 + 20 * i)
        populationInfo.append(Label(frame3, text = "Cуммарное количество: "))
        populationInfo[-1].place(x = 120, y = 40 + 20 * int(ePopulationStrength.get()))

        populationCount = []
        for i in range(int(ePopulationStrength.get())):
            populationCount.append([float(ePopulationStartCount[i].get())])
        
        plt.xlim(0, float(eTime.get()))
        plt.ylim(0, max(populationCount[:][0])*10)

        plt.xlabel("Время моделирования, лет")
        plt.ylabel("Численность популяции, шт")

        timeRange = [0]
        while timeRange[-1] <= float(eTime.get()):
            for i in range(int(ePopulationStrength.get())):
                dnDt = (float(ePopulationIncreaseCoefficient[i].get()) - float(ePopulationIncreaseCoefficient[i].get()) / 100 * random.randint(0, int(eRandomCoefficent.get()))) * populationCount[i][-1]
                for j in range(int(ePopulationStrength.get())):
                    dnDt += float(ePopulationMatrix[i][j].get()) * populationCount[i][-1] * populationCount[j][-1]
                populationCount[i][-1] += dnDt * float(eStep.get())
                populationCount[i].append(populationCount[i][-1])
            timeRange.append(timeRange[-1] + float(eStep.get()))

        global anim
        anim = FuncAnimation(fig, update, frames = int(float(eTime.get()) / float(eStep.get())) // 100, interval= 20, repeat = False)

    frame2 = Frame(window)
    frame2.configure(width = 1200, height = 240)
    frame2.place(x = 250)

    Label(frame2, text = "Начальная численность: ").place(x = 730)
    Label(frame2, text = "Коэффициенты естественного прироста:").place(x = 10)
    Label(frame2, text = "Коэффициенты матрицы взаимодействия:").place(x = 260)
    ePopulationStartCount = []
    ePopulationIncreaseCoefficient = []
    ePopulationMatrix = []

    for i in range(int(ePopulationStrength.get())):
        ePopulationStartCount.append(Entry(frame2, justify= 'center'))
        ePopulationStartCount[i].place(x = 730, y =  20 + i * 20)
        ePopulationStartCount[i].insert(0, str(100 + i * 100))

        Label(frame2, text = str(i)).place(y = 20 +  i * 20)
        Label(frame2, text = str(i)).place(x = 300 + 120 * i , y = 20 + 20 * int(ePopulationStrength.get()))
        ePopulationIncreaseCoefficient.append(Entry(frame2, justify= 'center'))
        ePopulationIncreaseCoefficient[i].place(x = 10, y = 20 + 20*i)
        if (i == 0):
            ePopulationIncreaseCoefficient[i].insert(0, '0.01')
        else:
            ePopulationIncreaseCoefficient[i].insert(0, '-0.01')
        ePopulationMatrix.append([])
        isMeetMean = False
        for j in range(int(ePopulationStrength.get())):
            ePopulationMatrix[i].append(Entry(frame2, justify= 'center'))
            ePopulationMatrix[i][j].place(x = 240 + 120 * j, y = 20 + 20*i)
            if(i == j):
                ePopulationMatrix[i][j].insert(0, '0')
                isMeetMean = True
            elif(isMeetMean == True and i != j):
                ePopulationMatrix[i][j].insert(0, '-0.0001')
            elif(isMeetMean == False and i != j):
                ePopulationMatrix[i][j].insert(0, '0.0001')

    Label(frame2, text = "Время моделирования:").place(x = 880)
    eTime = Entry(frame2, justify= 'center')
    eTime.place(x = 880, y = 20)
    eTime.insert(0, "1000")

    Label(frame2, text = "Шаг дифференциирования:").place(x = 880, y = 40)
    eStep = Entry(frame2, justify= 'center')
    eStep.place(x = 880, y = 60)
    eStep.insert(0, "1")

    Button(frame2, text='Построить график', command=graph).place(x = 1080)

def on_close():
    sys.exit(0)

window = Tk()
window.protocol("WM_DELETE_WINDOW", on_close)
window.title('Mat Mod Population program')
window.geometry('1450x730')
window.configure(bg = "grey")

frame = Frame(window)
frame.configure(width = 250, height = 175)
frame.place(x = 0)

Label(frame, text = "Количество популяций:").place(x = 10, y = 20)
ePopulationStrength = Entry(frame, justify= 'center')
ePopulationStrength.place(x = 10, y = 40)
ePopulationStrength.insert(0, "2")

Label(frame, text = "Максимальное процентное отклонение").place(x = 10, y = 60)
Label(frame, text = "коэффициентов естественного прироста:").place(x = 10, y = 80)
eRandomCoefficent = Entry(frame, justify= 'center')
eRandomCoefficent.place(x = 10, y = 110)
eRandomCoefficent.insert(0, "0")

Button(frame, text='Ввести данные', command=formShow).place(x = 10, y = 145)

window.mainloop()
