import time
from API_Azure import OCR
from Detection_Shape import Shape
import cv2
import csv


class CSV():
    def __init__(self):
        pass

    def load(self, image):
        #  Load raw image file into memory
        PathToImage = image
        with open(PathToImage, 'rb') as f:
            data = f.read()
        # read image
        image = cv2.imread(PathToImage)

        # Initialize function from other file
        ocr = OCR()
        shape = Shape(image)

        #  Computer Vision parameters
        params = {'mode': 'Handwritten'}

        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = ocr._key
        headers['Content-Type'] = 'application/octet-stream'

        json = None

        operationLocation = ocr.processRequest(json, data, headers, params)

        result = None
        if (operationLocation != None):
            headers = {}
            headers['Ocp-Apim-Subscription-Key'] = ocr._key
            while True:
                time.sleep(1)
                result = ocr.getOCRTextResult(operationLocation, headers)
                if result['status'] == 'Succeeded' or result['status'] == 'Failed':
                    break

        # Récupération des données de sorties des autres fichiers

        self.output = ocr.showResultOnImage(result, image)
        self.timeline = shape.Lines()
        self.output_shape = shape.CC()

    def position(self):
        # Création des listes nécessaires pour traiter et sortir les bonnes données
        month = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
        shape_text = []
        text = ""
        list_text = []
        fin_act = []
        list_month = []
        writing = []

        # On teste si le text est dans une forme puis on stocke la position (début+fin)
        # de la forme ansi que le texte qui lui est associé
        for a in range(len(self.output_shape)):
            for b in range(len(self.output)):
                if self.output_shape[a][1] <= self.output[b][1] <= self.output_shape[a][2] and self.output_shape[a][3] <= self.output[b][2] <= self.output_shape[a][4]:
                    text = text+" "+self.output[b][0]
            xd = self.output_shape[a][1]
            yd = self.output_shape[a][3]
            xf = self.output_shape[a][2]
            yf = self.output_shape[a][4]
            list_text.append([text, xd, yd, self.output_shape[a][0], self.output_shape[a][5], xf, yf])
            text = ""

        # La méthode juste avant laisse un espace avant chaque mot donc on l'enlève ici
        for c in range(len(list_text)):
            list_text[c][0] = list_text[c][0].strip()
            # si il n'y a pas de txt sur une forme ou qu'il n'a pas été détecté,
            # on le remplace par None (estéthique pour le csv)
            if list_text[c][0] == "":
                list_text[c][0] = "None"

        # Si il y a un mois entre chaque ligne verticale trouvée par le programme sur la photo
        # le mois et sa position sont sorties de la liste global des mots(azure) et stocké à part
        for i in range(len(self.timeline)):
            for j in range(len(self.output)):
                if i != len(self.timeline)-1:
                    if self.timeline[i] <= self.output[j][1] <= self.timeline[i+1] and self.output[j][0] in month:
                        list_month.append([self.output[j][0], self.output[j][1], self.output[j][2]])

        # Entre chaque ligne si il y a un mois c'est notre date sinon None
        for i in range(len(self.timeline)):
            block_month = False
            if not block_month:
                for k in range(len(list_month)):
                    if self.timeline[i] <= list_month[k][1] <= self.timeline[i + 1]:
                        date = list_month[k][0]
                        block_month = True
                        break
                    else:
                        date = "None"
            if i != len(self.timeline)-1:
                # si il y a la position début d'une forme+txt on ajoute
                # sa date de début, son type, couleur, txt et index(pour mois de fin)
                for j in range(len(list_text)):
                    if self.timeline[i] < list_text[j][1] <= self.timeline[i + 1]:
                        type = list_text[j][3]
                        color = list_text[j][4]
                        activity = list_text[j][0]
                        shape_text.append([activity, date, color, type, j])
                    # si la position de fin d'une forme est dans la colonne on ajoute le mois concerné ou None
                    # ainsi que l'index de la forme
                    if self.timeline[i] <= list_text[j][5] <= self.timeline[i+1]:
                        fin_act.append([j, date])

        # grâce à l'index on fait correspondre les mois de fin pour chaque forme
        for z in range(len(shape_text)):
            for y in range(len(fin_act)):
                if shape_text[z][4] == fin_act[y][0]:
                    writing.append([shape_text[z][0], shape_text[z][1], fin_act[y][1], shape_text[z][2], shape_text[z][3]])
        # notre liste complète avec seulement les infos nécessaires
        return writing

    def write(self, name):
        # récupération de la liste
        words = self.position(self)
        with open(name+".csv", 'w', newline='') as csvfile:
            fieldnames = ['Activity', 'Début', 'Fin', 'Color', 'Type']
            self.writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            self.writer.writeheader()
            # on écrit les données qui vont bien en face de chaque fieldnames
            for i in range(len(words)):
                self.writer.writerow({'Activity': words[i][0], 'Début': words[i][1], 'Fin': words[i][2], 'Color': words[i][3], 'Type': words[i][4]})
            csvfile.close()






