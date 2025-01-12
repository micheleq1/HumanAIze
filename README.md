# HumanAIze

## Authors

- Edoardo Dominicis - [Github](https://github.com/reDev27)
- Michele Quaglia - [Github](https://github.com/micheleq1)

## Project Description

**HumanAIze** is a plugin developed for [MakeHuman](https://static.makehumancommunity.org/makehuman.html), an open-source software for creating personalized 3D anthropometric models. The project uses machine learning algorithms to generate customized parameters based on textual descriptions, simplifying and speeding up the creation of complex humanoid characters without the need for advanced modeling tools.

### Goals of the Project

- **Integrating AI in MakeHuman:** Enhance personalization capabilities and speed up tedious processes.
- **Automating model creation:** Use an AI capable of predicting parameters from short textual descriptions (e.g., "A robust man, 50 years old").
- **Learning Objectives:**
  - Explore machine learning techniques (e.g., linear regression, boosting, and preprocessing).
  - Understand Python and plugin development for MakeHuman.
  - Build and use a synthetic dataset to train the model.

### Pre-existing Environment and Design Choices

#### Pre-existing Environment

- **MakeHuman** (ver 1.3.0): An open-source software tool for generating 3D anthropometric models.

#### Design Choices

- **Use of XGBoost:** Selected for its efficiency and interpretability.
- **Modular architecture(not yet implemented):** Divided into preprocessing, model training, and integration with MakeHuman, ensuring modularity and maintainability.

## Dataset

### Sources and Description

The dataset was synthetically generated using ChatGPT, as no existing dataset paired textual descriptions with the specific physical parameters accepted by MakeHuman.

#### Example Parameters:

- **General Parameters:** gender, age, height, weight, muscle.
- **Facial Features:** head angle, face fat, head oval.
- **Torso Features:** scale depth, dorsi muscle.
- **Extremities:** finger length, hand scale, neck height.

Each row represents a unique configuration of anthropometric parameters derived from textual descriptions.

### Preprocessing

#### Data Cleaning

- Manual adjustments for specific parameters required by MakeHuman.
- Missing values filled with mode (categorical).

#### Feature Engineering

- Textual descriptions were transformed into numerical vectors using TF-IDF.
- Numerical values were normalized to ensure consistency.

#### Train-Test Split

- The dataset was split into 80% training and 20% testing data, ensuring a balanced representation.

### Limitations and Potential Improvements

#### Potential Improvements

- Use more advanced algorithms like neural networks.
- Expand the dataset for better generalizability.

## Installation

### Requirements

- MakeHuman version 1.3.0 [(download here)](https://files2.makehumancommunity.org/releases/)
- Required libraries:
  - `pandas`
  - `xgboost`
  - `scikit-learn`

### Steps

1. Open the terminal and go to the Python MakeHuman console folder:
   ```bash
   cd C:/Path/to/Makehuman/../makehuman-community/Python 
2. Install the requirements in the MakeHuman Python console using pip:
    ```bash
   ./python -m pip install pandas xgboost scikit-learn
3. Download _humanAlze_plugin.zip_ from the release.
4. Extract it, so you have a folder with this structure:
    ```
   humanAlze_plugin/
    ├── core/
    │   ├── humanaize.py        # AI module
    │   ├── prompt_task.py      # Supporting functions
    ├── data/
    │   ├── dataset.csv         # Dataset used
    ├── resources/
    │   ├── icon.png            # Graphic resources
    ├── __init__.py             # Initialization file
5. Place the extracted humanAIze_plugin folder into the specified path:
    ```
   C:/Path/to/Documents/../makehuman/v1py3/plugins
**ATTENTION:**

If you can't find the folder at the specified path, make sure to open MakeHuman, go to: **Settings → User Plugins** and click on **'Reload User Plugins'**.

![img.png](MHinstr.png)
<br>

6. Close (if necessary) MakeHuman and restart, now you can use _HumanAIze_ going to **Utilities → Prompt Generator**

## Repository structure

    HumanAIze/
    ├── humanAlze_plugin/
    │   ├── core/
    │   │   ├── humanaize.py        # AI module
    │   │   ├── prompt_task.py      # Supporting functions
    │   ├── data/
    │   │   ├── dataset.csv         # Dataset used
    │   ├── resources/
    │   │   ├── icon.png            # Graphic resources
    │   ├── __init__.py             # Initialization file
    ├── ModifierNames               # Parameter configuration file
    ├── README.md                   # Project documentation

## Contributions
Pull requests are welcome. For significant changes, please open an issue first to discuss what you would like to change. Other instructions on how to replicate the developing sandbox will be added soon.
