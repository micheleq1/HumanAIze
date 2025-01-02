from .humanaize import predizione_personalizzata

import gui3d
import gui
import log
from core import G

class PromptTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, "Prompt Generator")

        # Crea un box per i widget
        box = self.addLeftWidget(gui.GroupBox("Prompt Generator"))

        # Aggiungi un TextEdit per inserire il prompt
        self.promptInput = box.addWidget(gui.TextEdit(text="Enter prompt here..."))

        # Aggiungi un bottone per generare i parametri
        button = box.addWidget(gui.Button("Generate from Prompt"))

        @button.mhEvent
        def onClicked(event):
            log.message("Button clicked! Processing the prompt.")
            prompt = self.promptInput.getText()
            self.processPrompt(prompt)

    def processPrompt(self, prompt):
        try:
            # Chiama il modello IA per predire i parametri
            predictions = predizione_personalizzata(prompt)
            log.message(f"Predicted parameters: {predictions}")


            # Converte le predizioni in un dizionario di parametri
            parameters = self.mapPredictionsToParameters(predictions)

            # Applica i parametri a MakeHuman
            self.applyParametersToMakeHuman(parameters)
        except Exception as e:
            log.error(f"Error processing prompt: {e}")

    def mapPredictionsToParameters(self, predictions):
        # Esempio di mappatura: usa i nomi esatti dei modificatori di MakeHuman
        modifier_mapping = {
            "gender": "macrodetails/Gender",
            "age": "macrodetails/Age",
            "height": "macrodetails-height/Height",
            "weight": "macrodetails-universal/Weight",
            "muscle": "macrodetails-universal/Muscle"
        }

        # Costruisce il dizionario di parametri compatibile
        parameters = {
            "gender": "female" if predictions[0][0] < 0.5 else ("neutral" if predictions[0][0] < 1.5 else "male"),
            "age": float(predictions[0][1]),
            "muscle": float(predictions[0][2]),
            "weight": float(predictions[0][3]),
            "height": float(predictions[0][4]),
            "proportions": float(predictions[0][5]),
            "african": float(predictions[0][6]),
            "asian": float(predictions[0][7]),
            "caucasian": float(predictions[0][8]),

        }

        return parameters

    def applyParametersToMakeHuman(self, parameters):
        human = G.app.selectedHuman


        # Mappatura dei valori stringa a numerici
        gender_map = {"female": 0.0, "neutral": 1.0, "male": 2.0}

        # Applica i modificatori
        if "macrodetails/Gender" in human.getModifierNames(): #corretto
            # Ottieni il valore da parameters["gender"]
            raw_gender_value = parameters.get("gender", "neutral")  # Default neutral
            gender_value = gender_map.get(raw_gender_value, 1.0)  # Mappatura stringa -> numerico

            # Divisione per 2 per adattare al range [0, 1]
            gender_value /= 2

            # Imposta il valore modificato
            human.getModifier("macrodetails/Gender").setValue(gender_value)
            log.message(f"Set Gender: Input={parameters['gender']} | MappedValue={gender_value}")

        if "macrodetails/Age" in human.getModifierNames(): #bene
            age_value = parameters["age"]  # Normalizza l'età (assumendo 0-100 anni)
            if age_value < 25:
                normalized_age = (age_value - 1) / ((25 - 1) * 2)
            else:
                normalized_age = ((age_value - 25) / ((90 - 25) * 2)) + 0.5
            human.getModifier("macrodetails/Age").setValue(normalized_age)
            log.message(f"Set Age: Input={parameters['age']} | NormalizedValue={normalized_age}")

        if "macrodetails-height/Height" in human.getModifierNames(): #sbagliato
            height_value = parameters["height"]  # Normalizza l'altezza (assumendo massimo 2.5 metri)
            normalized_height = (height_value - 133.40) / (242.28 - 133.40)
            human.getModifier("macrodetails-height/Height").setValue(normalized_height)
            log.message(f"Set Height: Input={parameters['height']} | NormalizedValue={normalized_height}")

        if "macrodetails-universal/Weight" in human.getModifierNames():  #corretto
            weight_value = parameters["weight"]   # Normalizza il peso (assumendo massimo 150 kg)
            normalized_weight=(weight_value - 50) / (150 - 50)
            human.getModifier("macrodetails-universal/Weight").setValue(normalized_weight)
            log.message(f"Set Weight: Input={parameters['weight']} | NormalizedValue={normalized_weight}")
        if "macrodetails-universal/Muscle" in human.getModifierNames(): #abbastanza corretto
            muscle_value = parameters["muscle"]
            normalized_muscle=(muscle_value - 1) / (100 - 1)
            human.getModifier("macrodetails-universal/Muscle").setValue(normalized_muscle)
            log.message(f"Set Muscle: Input={parameters['muscle']} | NormalizedValue={normalized_muscle}")
        if "macrodetails-proportions/BodyProportions" in human.getModifierNames(): #sembra funzionare
            proportions_value = parameters["proportions"]
            normalized_proportions=(proportions_value - 1) / (100 - 1)
            human.getModifier("macrodetails-proportions/BodyProportions").setValue(normalized_proportions)
            log.message(f"Set proportions: Input={parameters['proportions']} | NormalizedValue={normalized_proportions}")
        if "macrodetails/African" in human.getModifierNames():
            african_value=parameters["african"]
            normalized_african = (african_value - 0) / (100 - 0)
            human.getModifier("macrodetails/African").setValue(normalized_african)
            log.message(f"Set african: Input={parameters['african']} | NormalizedValue={normalized_african}")
        if "macrodetails/Asian" in human.getModifierNames():
            asian_value = parameters["asian"]
            normalized_asian = (asian_value - 0) / (100 - 0)
            human.getModifier("macrodetails/Asian").setValue(normalized_asian)
            log.message(f"Set asian: Input={parameters['asian']} | NormalizedValue={normalized_asian}")
        if "macrodetails/Caucasian" in human.getModifierNames():
            caucasian_value = parameters["caucasian"]
            normalized_caucasian = (caucasian_value - 0) / (100 - 0)
            human.getModifier("macrodetails/Caucasian").setValue(normalized_caucasian)
            log.message(f"Set caucasian: Input={parameters['caucasian']} | NormalizedValue={normalized_caucasian}")




        # Applica tutti i modificatori al modello
        human.applyAllTargets()

        log.message("Parameters applied successfully!")

    def onShow(self, event):
        gui3d.app.statusPersist("Prompt Generator Loaded!")

    def onHide(self, event):
        gui3d.app.statusPersist("Prompt Generator Unloaded!")
