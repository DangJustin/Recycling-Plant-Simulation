import matplotlib.pyplot as plt
import pandas as pd
import simulation


def main(containers):
    accuracy_list = []
    for i in range(1, 21):
        accurate = simulation.main(i, containers, 1)
        accuracy = accurate / containers
        accuracy_list.append((i, accuracy))

    x, y = zip(*accuracy_list)
    plt.scatter(x, y)
    plt.title("Accuracy vs Speed")
    plt.ylabel("Accuracy")
    plt.xlabel("Speed")
    plt.show()
    df = pd.DataFrame(accuracy_list, columns=['Speed','Accuracy'])
    df.to_csv('speed_vs_accuracy_analysis.csv',index=False)

    accuracy_list=[]
    for frequency in [1,2,5,10]:
        accurate = simulation.main(5, containers, frequency)
        accuracy = accurate / containers
        accuracy_list.append((frequency, accuracy))
    x, y = zip(*accuracy_list)
    plt.scatter(x, y)
    plt.title("Accuracy vs Frequency")
    plt.ylabel("Accuracy")
    plt.xlabel("Frequency")
    plt.show()
    df = pd.DataFrame(accuracy_list, columns=['Frequency', 'Accuracy'])
    df.to_csv('frequency_vs_accuracy_analysis.csv',index=False)

if __name__ == '__main__':
    main(100)
