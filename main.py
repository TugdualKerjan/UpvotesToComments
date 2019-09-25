import requests
import pprint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import imageio

#Make the array
thing = [[], [], []]


#Animation


# Get the initial memes
response = requests.get("http://9gag.com")
jsonResponse = response.text
position = jsonResponse.find('"position":1,"url":"https:\\/\\/9gag.com\\/gag\\/')
position = position + len('"position":1,"url":"https:\\/\\/9gag.com\\/gag\\/')
nextCursor = jsonResponse[position:position + 7]
initUrl = "https://9gag.com/v1/group-posts/group/default/type/hot?%s" % nextCursor
response = requests.get(initUrl)
jsonResponse = response.json()
amountOfMemes = int(len(jsonResponse['data']['posts'])) - 1
nextCursor = jsonResponse['data']['nextCursor']
pprint.pprint(jsonResponse)

def checkIfLast():
    global amountOfMemes, nextCursor, initUrl, response, jsonResponse
    initUrl = "https://9gag.com/v1/group-posts/group/default/type/hot?%s" % nextCursor
    response = requests.get(initUrl)
    jsonResponse = response.json()
    amountOfMemes = int(len(jsonResponse['data']['posts'])) - 1
    nextCursor = jsonResponse['data']['nextCursor']

def callback():
    global amountOfMemes
    comments = jsonResponse['data']['posts'][amountOfMemes]['commentsCount']
    votes = jsonResponse['data']['posts'][amountOfMemes]['upVoteCount']
    thing[1].append(votes)
    thing[0].append(comments)
    if jsonResponse['data']['posts'][amountOfMemes]['type'] == "Photo":
        thing[2].append('red')
    else:
        thing[2].append('blue')
    print("type of thing: " + jsonResponse['data']['posts'][amountOfMemes]['type'])

    amountOfMemes = amountOfMemes - 1
    if amountOfMemes == -1:
        checkIfLast()

    #Pie
    fig, ax = plt.subplots(1, 2, figsize=[8, 4])
    labels = 'Images', 'Animated'

    amountOfImages = 0
    amountOfVideos = 0
    for x in thing[2]:
        if x == 'red':
            amountOfImages += 1
        else:
            amountOfVideos += 1

    sizes = [(amountOfImages / float(amountOfVideos + amountOfImages)) * 100,
             (amountOfVideos / float(amountOfImages + amountOfVideos)) * 100]

    ax[0].pie(sizes, labels=labels, colors=['red', 'blue'])
    ax[0].axis('equal')
    print(sizes)
    # IMPORTANT ANIMATION CODE HERE
    # Used to keep the limits constant
    # Used to return the plot as an image rray
    # draw the canvas, cache the renderer

    #Grid
    ax[1].scatter(thing[0], thing[1], c=thing[2])
    ax[1].grid()
    ax[1].set(xlabel='Comments', ylabel='Votes',
           title='Relation between comments and votes')
    # IMPORTANT ANIMATION CODE HERE
    # Used to keep the limits constant
    ax[1].set_ylim(0, 20000)
    ax[1].set_xlim(0, 1000)

    # Used to return the plot as an image rray
    fig.canvas.draw()  # draw the canvas, cache the renderer
    plt.pause(0.1)
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image


kwargs_write = {'fps':1.0, 'quantizer':'nq'}
imageio.mimsave('./pleaseWork2.gif', [callback() for i in range(500)], fps=50)


"""fig, ax = plt.subplots(1)
ax.scatter(thing[0], thing[1], c=thing[2])
ax.grid()
ax.set(xlabel='Comments', ylabel='Votes',
       title='Relation between comments and votes')

# IMPORTANT ANIMATION CODE HERE
# Used to keep the limits constant
ax.set_ylim(0, 20000)
ax.set_xlim(0, 1000)

x_mean_image = 0.0
x_mean_anime = 0.0

amountOfImages = 0
amountOfVideos = 0
for x in range(thing[0].__len__()):
    if thing[2][x] == 'red':
        x_mean_image += thing[0][x]
        amountOfImages += 1
    else:
        x_mean_anime += thing[0][x]
        amountOfVideos += 1
x_mean_image /= float(amountOfImages)
x_mean_anime /= amountOfVideos

y_mean_image = 0
y_mean_anime = 0

amountOfImages = 0
amountOfVideos = 0
for y in range(thing[1].__len__()):
    if thing[2][y] == 'red':
        y_mean_image += thing[1][y]
        amountOfImages += 1
    else:
        y_mean_anime += thing[1][y]
        amountOfVideos += 1
y_mean_image /= amountOfImages
y_mean_anime /= amountOfVideos

plt.scatter(x=thing[0], y=thing[1], c=thing[2])

print("Thing: " + str(x_mean_image) + " " + str(y_mean_image))
print("Thing: " + str(x_mean_anime) + " " + str(y_mean_anime))

plt.plot([0, x_mean_image*20], [0, y_mean_image*20], color='blue')
plt.plot([0, x_mean_anime*20], [0, y_mean_anime*20], color='red')
plt.show()
"""
