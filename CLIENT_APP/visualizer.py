import matplotlib.pyplot as plt

def barChartCellSeedDetection(list):
    
    # x axis values 
    tick_label = range(len(list))
    
    height = []
    
    # corresponding y axis values
    for i in list: 
        height.append(i)
    
    plt.figure(figsize=(8.5,11))
    plt.plot(tick_label,height)
    plt.title('Cell seed detection results')
    plt.ylabel('Number of detected cell nuclei')
    plt.xlabel('Tiles')
    plt.grid(True)
    plt.show()
