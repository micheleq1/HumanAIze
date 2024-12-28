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
            "weight": "macrodetails-universal/Weight"
            # Aggiungi altre mappature se necessario
        }

        # Costruisce il dizionario di parametri compatibile
        parameters = {
            "gender": "male" if predictions[0][0] < 0.5 else "female",
            "age": int(predictions[0][1]),
            "height": float(predictions[0][2]),
            "weight": float(predictions[0][3])
        }

        return parameters

    def applyParametersToMakeHuman(self, parameters):
        human = G.app.selectedHuman

        # Mappatura dei valori stringa a numerici
        gender_map = {"male": 0.0, "female": 1.0}  # Esempio: 0 per male, 1 per female

        # Applica i modificatori
        if "macrodetails/Gender" in human.getModifierNames():
            gender_value = gender_map.get(parameters["gender"], 0.0)  # Default a male
            human.getModifier("macrodetails/Gender").setValue(gender_value)

        if "macrodetails/Age" in human.getModifierNames():
            age_value = parameters["age"] / 100.0  # Normalizza l'età (assumendo 0-100 anni)
            human.getModifier("macrodetails/Age").setValue(age_value)

        if "macrodetails-height/Height" in human.getModifierNames():
            height_value = parameters["height"] / 2.5  # Normalizza l'altezza (assumendo massimo 2.5 metri)
            human.getModifier("macrodetails-height/Height").setValue(height_value)

        if "macrodetails-universal/Weight" in human.getModifierNames():
            weight_value = parameters["weight"] / 150.0  # Normalizza il peso (assumendo massimo 150 kg)
            human.getModifier("macrodetails-universal/Weight").setValue(weight_value)

        # Applica tutti i modificatori al modello
        human.applyAllTargets()
        log.message("Parameters applied successfully!")

    def onShow(self, event):
        gui3d.app.statusPersist("Prompt Generator Loaded!")

    def onHide(self, event):
        gui3d.app.statusPersist("Prompt Generator Unloaded!")
