import json  
from django.apps import apps  

def export_models_to_json(app_name):  
    # Récupérer tous les modèles de l'application spécifiée  
    app = apps.get_app_config(app_name)  
    models = {}  

    for model in app.get_models():  
        model_info = {  
            "name": model.__name__,  
            "fields": {}  
        }  

        # Récupérer les champs et leurs types  
        for field in model._meta.get_fields(include_hidden=True):  # include_hidden pour inclure tous les champs  
            field_info = {  
                "type": field.get_internal_type(),  
                "null": field.null,  
            }  

            if hasattr(field, "blank"):  
                field_info["blank"] = field.blank  
            
            # Ignore les champs de relation pour les valeurs par défaut  
            if field.is_relation:  
                field_info["related_model"] = field.related_model.__name__ if field.related_model else None  
            else:  
                # Vérifier si le champ a une valeur par défaut  
                if field.has_default():  
                    default_value = field.default  
                    
                    # Vérifier le type pour s'assurer qu'il est sérialisable  
                    if callable(default_value):  
                        field_info["default"] = "Callable default (function)"  
                    else:  
                        field_info["default"] = default_value  
                else:  
                    field_info["default"] = None  
            
            model_info["fields"][field.name] = field_info  

        models[model.__name__] = model_info  

    # Écrire les données dans un fichier JSON  
    output_file = f'{app_name}_models.json'  
    with open(output_file, 'w') as json_file:  
        json.dump(models, json_file, indent=4)  

    print(f"Les modèles de l'application '{app_name}' ont été exportés vers '{output_file}'.")  

# Appelle la fonction d'exportation pour 'recover_data'  
export_models_to_json('recover_data')