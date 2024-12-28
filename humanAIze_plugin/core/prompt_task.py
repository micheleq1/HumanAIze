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
        # Simula la generazione dei parametri dal prompt
        log.message(f"Processing prompt: {prompt}")
        parameters = {
            "gender": "male",
            "age": 30,
            "height": 1.8,
            "weight": 70,
        }
        self.applyParametersToMakeHuman(parameters)

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
