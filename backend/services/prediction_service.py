from engine import get_db
from models.model_db import AccidentPrediction



# Fonction pour save mes données dans une base de données :
def save_prediction (accident, result, metadonnee) :
    db = next(get_db())
    try :
        data_dict = {**accident.model_dump(), **result, **metadonnee}  ##** = méthode python qui permet directement d'assigner les valeurs qd c'est un dict le contenu de la varibale 

        # Convertir booléens correctement parceque j'ai plein de problème
        bool_cols = ['presence_enfant','presence_senior','presence_pieton','presence_passager','nuit','success']
        for col in bool_cols:
            if col in data_dict:
                data_dict[col] = bool(data_dict[col])

        # Convertir error_message en string (pareil plein de bug)
        if 'error_message' in data_dict:
            data_dict['error_message'] = str(data_dict['error_message'])

        new_pred = AccidentPrediction(**data_dict)   #Appel de ma class sqlachemy
        db.add(new_pred)
        db.commit()
    finally :
        db.close()


# def save_prediction ( accident, result, metadonnee) :
#     with Session() as session:
#         data_dict = {**accident, **result, **metadonnee}

#         # Convertir booléens correctement
#         bool_cols = ['presence_enfant','presence_senior','presence_pieton','presence_passager','nuit','success']
#         for col in bool_cols:
#             if col in data_dict:
#                 data_dict[col] = bool(data_dict[col])

#         # Convertir error_message en string
#         if 'error_message' in data_dict:
#             data_dict['error_message'] = str(data_dict['error_message'])

#         new_pred = Prediction_requete(**data_dict)
#         session.add(new_pred)
#         session.commit()
