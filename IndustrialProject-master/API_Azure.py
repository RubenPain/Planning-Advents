import time
import requests
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


# Clé 1: 30746cd927de4568821fb06deb00139e
# Clé 2: 6dc9ac3a6be04607984c830a6c4cab27

# Variables
class OCR():
    def __init__(self):

        self._url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/RecognizeText'
        self._key = "30746cd927de4568821fb06deb00139e"
        self._maxNumRetries = 10


    def processRequest(self, json, data, headers, params):
        """
        Helper function to process the request to Project Oxford

        Parameters:
        json: Used when processing images from its URL. See API Documentation
        data: Used when processing image read from disk. See API Documentation
        headers: Used to pass the key information and the data type request
        """

        retries = 0
        result = None

        while True:
            response = requests.request('post', self._url, json=json, data=data, headers=headers, params=params)

            if response.status_code == 429:
                print("Message: %s" % (response.json()))
                if retries <= self._maxNumRetries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying!')
                    break
            elif response.status_code == 202:
                result = response.headers['Operation-Location']
            else:
                print("Error code: %d" % (response.status_code))
                print("Message: %s" % (response.json()))
            break

        return result

    def getOCRTextResult(self, operationLocation, headers ):
        """
        Helper function to get text result from operation location

        Parameters:
        operationLocation: operationLocation to get text result, See API Documentation
        headers: Used to pass the key information
        """

        retries = 0
        result = None

        while True:
            response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
            if response.status_code == 429:
                print("Message: %s" % (response.json()))
                if retries <= self._maxNumRetries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying!')
                    break
            elif response.status_code == 200:
                result = response.json()
            else:
                print("Error code: %d" % (response.status_code))
                print("Message: %s" % (response.json()))
            break

        return result


    def showResultOnImage(self, result, img):
        """Display the obtained results onto the input image"""
        img = img[:, :, (2, 1, 0)]
        fig, ax = plt.subplots(figsize=(12, 12))
        ax.imshow(img, aspect='equal')

        lines = result['recognitionResult']['lines']

        output = []

        for i in range(len(lines)):
            words = lines[i]['words']
            for j in range(len(words)):
                tl = (words[j]['boundingBox'][0], words[j]['boundingBox'][1])
                tr = (words[j]['boundingBox'][2], words[j]['boundingBox'][3])
                br = (words[j]['boundingBox'][4], words[j]['boundingBox'][5])
                bl = (words[j]['boundingBox'][6], words[j]['boundingBox'][7])
                text = words[j]['text']
                x = [tl[0], tr[0], tr[0], br[0], br[0], bl[0], bl[0], tl[0]]
                y = [tl[1], tr[1], tr[1], br[1], br[1], bl[1], bl[1], tl[1]]
                line = Line2D(x, y, linewidth=3.5, color='red')
                ax.add_line(line)
                ax.text(tl[0], tl[1]-2, '{:s}'.format(text),
                        bbox=dict(facecolor='blue', alpha=0.5),
                        fontsize=14, color='white')
                # recover only the values ​​that interest us
                # plt is not the same library as cv2,some difference
                output.append([text, tl[0], tl[1]])
        plt.axis('off')
        plt.tight_layout()
        plt.draw()
        #plt.show()
        return output


