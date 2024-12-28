from humanAIze_plugin.core.prompt_task import PromptTaskView

def load(app):
    category = app.getCategory('Utilities')  # Usa una categoria esistente
    category.addTask(PromptTaskView(category))

def unload(app):
    pass  # Puoi aggiungere log o altre azioni di cleanup se necessario
