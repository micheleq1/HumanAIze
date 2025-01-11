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
            "breast_size": float(predictions[0][9]),
            "breast_firmness": float(predictions[0][10]),
            "vertical_position": float(predictions[0][11]),
            "horizontal_distance": float(predictions[0][12]),
            "pointiness": float(predictions[0][13]),
            "breast_volume": float(predictions[0][14]),
            "nipple_size": float(predictions[0][15]),
            "nipple_point": float(predictions[0][16]),
            "face_age": float(predictions[0][17]),
            "face_head_fat": float(predictions[0][18]),
            "face_angle": float(predictions[0][19]),
            "face_oval": float(predictions[0][20]),
            "face_round": float(predictions[0][21]),
            "face_rectangular": float(predictions[0][22]),
            "face_square": float(predictions[0][23]),
            "face_triangular": float(predictions[0][24]),
            "face_invertedtriangular": float(predictions[0][25]),
            "face_diamond": float(predictions[0][26]),
            "torso_scale_depht":float(predictions[0][27]),
            "torso_scale_horizontally":float(predictions[0][28]),
            "torso_scale_vertically":float(predictions[0][29]),
            "torso_move_horizontally":float(predictions[0][30]),
            "torso_move_depht":float(predictions[0][31]),
            "torso_scale_cone_shape":float(predictions[0][32]),
            "torso_dorsi_muscle":float(predictions[0][33]),
            "torso_pectoral_muscle":float(predictions[0][34]),
            "fingers_distance": float(predictions[0][35]),
            "fingers_diameter": float(predictions[0][36]),
            "fingers_lenght": float(predictions[0][37]),
            "scale_hand": float(predictions[0][38]),
            "hand_position": float(predictions[0][39]),
            "neck_circum": float(predictions[0][40]),
            "neck_height": float(predictions[0][41]),


        }

        return parameters

    def setHeightCm(self, human, height_cm, updateModifier=True):
        current_bBox = human.getBoundingBox()
        current_height_cm = 10 * (current_bBox[1][1] - current_bBox[0][1])
        log.message(f"bounding: {current_bBox[1][1]}, {current_bBox[0][1]}, {current_bBox[1][1]-current_bBox[0][1]}, altezza corrente: {current_height_cm}")

        if current_height_cm == 0:
            raise ValueError("Current height is zero. Cannot normalize height.")

        normalized_height = height_cm / current_height_cm * human.getHeight()
        normalized_height = min(max(normalized_height, 0.0), 1.0)

        return normalized_height

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

            if "macrodetails-height/Height" in human.getModifierNames():
                height_value=self.setHeightCm(human, parameters["height"], updateModifier=True)
                human.getModifier("macrodetails-height/Height").setValue(height_value)

                log.message(f"Set Height: Input={parameters['height']} | NormalizedValue={height_value} ")


        if "macrodetails-universal/Weight" in human.getModifierNames():  #corretto
            weight_value = parameters["weight"]   # Normalizza il peso (assumendo massimo 150 kg)
            normalized_weight=(weight_value - 50) / (150 - 50)
            human.getModifier("macrodetails-universal/Weight").setValue(normalized_weight)
            log.message(f"Set Weight: Input={parameters['weight']} | NormalizedValue={normalized_weight}")
        if "macrodetails-universal/Muscle" in human.getModifierNames(): #abbastanza corretto
            muscle_value = parameters["muscle"]
            normalized_muscle=(muscle_value - 0) / (100 - 0)
            human.getModifier("macrodetails-universal/Muscle").setValue(normalized_muscle)
            log.message(f"Set Muscle: Input={parameters['muscle']} | NormalizedValue={normalized_muscle}")
        if "macrodetails-proportions/BodyProportions" in human.getModifierNames(): #sembra funzionare
            proportions_value = parameters["proportions"]
            normalized_proportions=(proportions_value - 0) / (100 - 0)
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
        if "breast/BreastSize" in human.getModifierNames():
            breast_size_value = parameters["breast_size"]
            normalized_breast_size = (breast_size_value - 0) / (100 - 0)
            human.getModifier("breast/BreastSize").setValue(normalized_breast_size)
            log.message(f"Set breast_size: Input={parameters['breast_size']} | NormalizedValue={normalized_breast_size}")
        if "breast/BreastFirmness" in human.getModifierNames():
            breast_firmness_value = parameters["breast_firmness"]
            normalized_breast_firmness = (breast_firmness_value - 0) / (100 - 0)
            human.getModifier("breast/BreastFirmness").setValue(normalized_breast_firmness)
            log.message(f"Set breast_firmness: Input={parameters['breast_firmness']} | NormalizedValue={normalized_breast_firmness}")
        if "breast/breast-trans-down|up" in human.getModifierNames():
            vertical_position_value = parameters["vertical_position"]
            normalized_vertical_position = (vertical_position_value - 0) / (100 - 0)
            human.getModifier("breast/breast-trans-down|up").setValue(normalized_vertical_position)
            log.message(f"Set vertical_position: Input={parameters['vertical_position']} | NormalizedValue={normalized_vertical_position}")
        if "breast/breast-dist-decr|incr" in human.getModifierNames():
            horizontal_distance_value = parameters["horizontal_distance"]
            normalized_horizontal_distance = (horizontal_distance_value - 0) / (100 - 0)
            human.getModifier("breast/breast-dist-decr|incr").setValue(normalized_horizontal_distance)
            log.message(f"Set horizontal_distance: Input={parameters['horizontal_distance']} | NormalizedValue={normalized_horizontal_distance}")
        if "breast/breast-point-decr|incr" in human.getModifierNames():
            pointiness_value = parameters["pointiness"]
            normalized_pointiness = (pointiness_value - 0) / (100 - 0)
            human.getModifier("breast/breast-point-decr|incr").setValue(normalized_pointiness)
            log.message(f"Set pointiness: Input={parameters['pointiness']} | NormalizedValue={normalized_pointiness}")
        if "breast/breast-volume-vert-down|up" in human.getModifierNames():
            breast_volume_value = parameters["breast_volume"]
            normalized_breast_volume = (breast_volume_value - 0) / (100 - 0)
            human.getModifier("breast/breast-volume-vert-down|up").setValue(normalized_breast_volume)
            log.message(f"Set breast_volume: Input={parameters['breast_volume']} | NormalizedValue={normalized_breast_volume}")
        if "breast/nipple-size-decr|incr" in human.getModifierNames():
            nipple_size_value = parameters["nipple_size"]
            normalized_nipple_size = (nipple_size_value - 0) / (100 - 0)
            human.getModifier("breast/nipple-size-decr|incr").setValue(normalized_nipple_size)
            log.message(f"Set nipple_size: Input={parameters['nipple_size']} | NormalizedValue={normalized_nipple_size}")
        if "breast/nipple-point-decr|incr" in human.getModifierNames():
            nipple_point_value = parameters["nipple_size"]
            normalized_nipple_point = (nipple_point_value - 0) / (100 - 0)
            human.getModifier("breast/nipple-point-decr|incr").setValue(normalized_nipple_point)
            log.message(f"Set nipple_point: Input={parameters['nipple_point']} | NormalizedValue={normalized_nipple_point}")
        if "head/head-age-decr|incr" in human.getModifierNames():
            face_age_value = parameters["face_age"]
            normalized_face_age = (face_age_value - 0) / (100 - 0)
            human.getModifier("head/head-age-decr|incr").setValue(normalized_face_age)
            log.message(f"Set face_age: Input={parameters['face_age']} | NormalizedValue={normalized_face_age}")
        if "head/head-fat-decr|incr" in human.getModifierNames():
            face_head_fat_value = parameters["face_head_fat"]
            normalized_face_head_fat = (face_head_fat_value - 0) / (100 - 0)
            human.getModifier("head/head-fat-decr|incr").setValue(normalized_face_head_fat)
            log.message(f"Set face_head_fat: Input={parameters['face_head_fat']} | NormalizedValue={normalized_face_head_fat}")
        if "head/head-angle-in|out" in human.getModifierNames():
            face_angle_value = parameters["face_angle"]
            normalized_face_angle = (face_angle_value - 0) / (100 - 0)
            human.getModifier("head/head-angle-in|out").setValue(normalized_face_angle)
            log.message(f"Set face_angle: Input={parameters['face_angle']} | NormalizedValue={normalized_face_angle}")
        if "head/head-oval" in human.getModifierNames():
            face_oval_value = parameters["face_oval"]
            normalized_face_oval = (face_oval_value - 0) / (100 - 0)
            human.getModifier("head/head-oval").setValue(normalized_face_oval)
            log.message(f"Set face_oval: Input={parameters['face_oval']} | NormalizedValue={normalized_face_oval}")
        if "head/head-round" in human.getModifierNames():
            face_round_value = parameters["face_round"]
            normalized_face_round = (face_round_value - 0) / (100 - 0)
            human.getModifier("head/head-round").setValue(normalized_face_round)
            log.message(f"Set face_round: Input={parameters['face_round']} | NormalizedValue={normalized_face_round}")
        if "head/head-rectangular" in human.getModifierNames():
            face_rectangular_value = parameters["face_rectangular"]
            normalized_face_rectangular = (face_rectangular_value - 0) / (100 - 0)
            human.getModifier("head/head-rectangular").setValue(normalized_face_rectangular)
            log.message(f"Set face_rectangular: Input={parameters['face_rectangular']} | NormalizedValue={normalized_face_rectangular}")
        if "head/head-square" in human.getModifierNames():
            face_square_value = parameters["face_square"]
            normalized_face_square = (face_square_value - 0) / (100 - 0)
            human.getModifier("head/head-square").setValue(normalized_face_square)
            log.message(f"Set face_square: Input={parameters['face_square']} | NormalizedValue={normalized_face_square}")
        if "head/head-triangular" in human.getModifierNames():
            face_triangular_value = parameters["face_triangular"]
            normalized_face_triangular = (face_triangular_value - 0) / (100 - 0)
            human.getModifier("head/head-triangular").setValue(normalized_face_triangular)
            log.message(f"Set face_triangular: Input={parameters['face_triangular']} | NormalizedValue={normalized_face_triangular}")
        if "head/head-invertedtriangular" in human.getModifierNames():
            face_invertedtriangular_value = parameters["face_invertedtriangular"]
            normalized_face_invertedtriangular = (face_invertedtriangular_value - 0) / (100 - 0)
            human.getModifier("head/head-invertedtriangular").setValue(normalized_face_invertedtriangular)
            log.message(f"Set face_invertedtriangular: Input={parameters['face_invertedtriangular']} | NormalizedValue={normalized_face_invertedtriangular}")
        if "head/head-diamond" in human.getModifierNames():
            face_diamond_value = parameters["face_diamond"]
            normalized_face_diamond = (face_diamond_value - 0) / (100 - 0)
            human.getModifier("head/head-diamond").setValue(normalized_face_diamond)
            log.message(f"Set face_diamondr: Input={parameters['face_diamond']} | NormalizedValue={normalized_face_diamond}")
        if "torso/torso-scale-depth-decr|incr" in human.getModifierNames():
            torso_scale_depht_value = parameters["torso_scale_depht"]
            normalized_torso_scale_depht = (torso_scale_depht_value - 0) / (100 - 0)
            human.getModifier("torso/torso-scale-depth-decr|incr").setValue(normalized_torso_scale_depht)
            log.message(f"Set torso_scale_depht: Input={parameters['torso_scale_depht']} | NormalizedValue={normalized_torso_scale_depht}")
        if "torso/torso-scale-horiz-decr|incr" in human.getModifierNames():
            torso_scale_horizontally_value = parameters["torso_scale_horizontally"]
            normalized_torso_scale_horizontally = (torso_scale_horizontally_value - 0) / (100 - 0)
            human.getModifier("torso/torso-scale-horiz-decr|incr").setValue(normalized_torso_scale_horizontally)
            log.message(f"Set torso_scale_horizontally: Input={parameters['torso_scale_horizontally']} | NormalizedValue={normalized_torso_scale_horizontally}")
        if "torso/torso-scale-vert-decr|incr" in human.getModifierNames():
            torso_scale_vertically_value = parameters["torso_scale_vertically"]
            normalized_torso_scale_vertically = (torso_scale_vertically_value - 0) / (100 - 0)
            human.getModifier("torso/torso-scale-vert-decr|incr").setValue(normalized_torso_scale_vertically)
            log.message(f"Set torso_scale_vertically: Input={parameters['torso_scale_vertically']} | NormalizedValue={normalized_torso_scale_vertically}")
        if "torso/torso-trans-in|out" in human.getModifierNames():
            torso_move_horizontally_value = parameters["torso_move_horizontally"]
            normalized_torso_move_horizontally = (torso_move_horizontally_value - 0) / (100 - 0)
            human.getModifier("torso/torso-trans-in|out").setValue(normalized_torso_move_horizontally)
            log.message(f"Set torso_move_horizontally: Input={parameters['torso_move_horizontally']} | NormalizedValue={normalized_torso_move_horizontally}")
        if "torso/torso-trans-backward|forward" in human.getModifierNames():
            torso_move_depht_value = parameters["torso_move_depht"]
            normalized_torso_move_depht = (torso_move_depht_value - 0) / (100 - 0)
            human.getModifier("torso/torso-trans-backward|forward").setValue(normalized_torso_move_depht)
            log.message(f"Set torso_move_depht: Input={parameters['torso_move_depht']} | NormalizedValue={normalized_torso_move_depht}")
        if "torso/torso-vshape-decr|incr" in human.getModifierNames():
            torso_scale_cone_shape_value = parameters["torso_scale_cone_shape"]
            normalized_torso_scale_cone_shape = (torso_scale_cone_shape_value - 0) / (100 - 0)
            human.getModifier("torso/torso-vshape-decr|incr").setValue(normalized_torso_scale_cone_shape)
            log.message(f"Set torso_scale_cone_shape: Input={parameters['torso_scale_cone_shape']} | NormalizedValue={normalized_torso_scale_cone_shape}")
        if "torso/torso-muscle-dorsi-decr|incr" in human.getModifierNames():
            torso_dorsi_muscle_value = parameters["torso_dorsi_muscle"]
            normalized_torso_dorsi_muscle = (torso_dorsi_muscle_value - 0) / (100 - 0)
            human.getModifier("torso/torso-muscle-dorsi-decr|incr").setValue(normalized_torso_dorsi_muscle)
            log.message(f"Set torso_dorsi_muscle: Input={parameters['torso_dorsi_muscle']} | NormalizedValue={normalized_torso_dorsi_muscle}")
        if "torso/torso-muscle-pectoral-decr|incr" in human.getModifierNames():
            torso_pectoral_muscle_value = parameters["torso_pectoral_muscle"]
            normalized_torso_pectoral_muscle = (torso_pectoral_muscle_value - 0) / (100 - 0)
            human.getModifier("torso/torso-muscle-pectoral-decr|incr").setValue(normalized_torso_pectoral_muscle)
            log.message(f"Set torso_pectoral_muscle: Input={parameters['torso_pectoral_muscle']} | NormalizedValue={normalized_torso_pectoral_muscle}")
        if "armslegs/r-hand-fingers-distance-decr|incr" in human.getModifierNames():
            fingers_distance_value = parameters["fingers_distance"]
            normalized_fingers_distance = (fingers_distance_value - 0) / (100 - 0)
            human.getModifier("armslegs/r-hand-fingers-distance-decr|incr").setValue(normalized_fingers_distance)
            log.message(f"Set fingers_distance: Input={parameters['fingers_distance']} | NormalizedValue={normalized_fingers_distance}")
        if "armslegs/r-hand-fingers-diameter-decr|incr" in human.getModifierNames():
            fingers_diameter_value = parameters["fingers_diameter"]
            normalized_fingers_diameter = (fingers_diameter_value - 0) / (100 - 0)
            human.getModifier("armslegs/r-hand-fingers-diameter-decr|incr").setValue(normalized_fingers_diameter)
            log.message(f"Set fingers_diameter: Input={parameters['fingers_diameter']} | NormalizedValue={normalized_fingers_diameter}")
        if "armslegs/r-hand-fingers-length-decr|incr" in human.getModifierNames():
            fingers_lenght_value = parameters["fingers_lenght"]
            normalized_fingers_lenght = (fingers_lenght_value - 0) / (100 - 0)
            human.getModifier("armslegs/r-hand-fingers-length-decr|incr").setValue(normalized_fingers_lenght)
            log.message(f"Set fingers_lenght: Input={parameters['fingers_lenght']} | NormalizedValue={normalized_fingers_lenght}")
        if "armslegs/r-hand-scale-decr|incr" in human.getModifierNames():
            scale_hand_value = parameters["scale_hand"]
            normalized_scale_hand = (scale_hand_value - 0) / (100 - 0)
            human.getModifier("armslegs/r-hand-scale-decr|incr").setValue(normalized_scale_hand)
            log.message(f"Set scale_hand: Input={parameters['scale_hand']} | NormalizedValue={normalized_scale_hand}")
        if "armslegs/l-hand-trans-in|out" in human.getModifierNames():
            hand_position_value = parameters["hand_position"]
            normalized_hand_position = (hand_position_value - 0) / (100 - 0)
            human.getModifier("armslegs/l-hand-trans-in|out").setValue(normalized_hand_position)
            log.message(f"Set hand_position: Input={parameters['hand_position']} | NormalizedValue={normalized_hand_position}")
        if "measure/measure-neck-circ-decr|incr" in human.getModifierNames():
            face_neck_circum = parameters["neck_circum"]
            normalized_neck_circum = (face_neck_circum - 0) / (100 - 0)
            human.getModifier("measure/measure-neck-circ-decr|incr").setValue(normalized_neck_circum)
            log.message(f"Set neck_circum: Input={parameters['neck_circum']} | NormalizedValue={normalized_neck_circum}")
        if "measure/measure-neck-height-decr|incr" in human.getModifierNames():
            face_neck_height = parameters["neck_height"]
            normalized_neck_height = (face_neck_height - 0) / (100 - 0)
            human.getModifier("measure/measure-neck-height-decr|incr").setValue(normalized_neck_height)
            log.message(f"Set neck_height: Input={parameters['neck_height']} | NormalizedValue={normalized_neck_height}")





        # Applica tutti i modificatori al modello
        human.applyAllTargets()

        log.message("Parameters applied successfully!")

    def onShow(self, event):
        gui3d.app.statusPersist("Prompt Generator Loaded!")

    def onHide(self, event):
        gui3d.app.statusPersist("Prompt Generator Unloaded!")
