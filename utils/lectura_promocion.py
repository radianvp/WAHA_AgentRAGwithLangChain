# db_utils.py

import os
from supabase import create_client, Client
from dotenv import load_dotenv

class GetPromotions:
    def __init__(self):
        load_dotenv()
        self.client = self.get_supabase_client()

    def get_supabase_client(self) -> Client:
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
        return create_client(supabase_url, supabase_key)

    def get_active_promotions(self, promocion_curso: str, limit: int = 3) -> list:
        response = ( 
            self.client.table("promociones_cursos")
            .select("curso, modalidad, precio_regular, promo_julio, detalles_promocion, vigencia")
            .filter("curso", "ilike", f"%{promocion_curso}%")
            .limit(limit)
            .execute()
        )

        if hasattr(response, "error") and response.error is not None:
            print("Error al obtener las promociones:", response.error)
            return []

        return response.data
    
    def get_all_active_promotions(self):
        response = ( 
            self.client.table("promociones_cursos")
            .select("curso, modalidad, precio_regular, promo_julio, detalles_promocion, vigencia")
            .limit(1)
            .execute()
        )

        if not response.data:
            return []

        # Deduplicar por curso y promo_julio
        seen = set()
        distinct_results = []
        for item in response.data:
            key = (item["curso"], item["promo_julio"])
            if key not in seen:
                seen.add(key)
                distinct_results.append(item)

        return distinct_results
    
    @staticmethod
    def format_promotions_output(promotions: list) -> str:
        template = []
        for i, promo in enumerate(promotions, 1):
            formatted = f'''P{i}: {{
            "curso": "{promo['curso']}",
            "modalidad": "{promo['modalidad']}",
            "precio_regular": "{promo['precio_regular']}",
            "promo_julio": "{promo['promo_julio']}",
            "detalles_promocion": "{promo['detalles_promocion']}",
            "vigencia": "{promo['vigencia']}"}}'''
            template.append(formatted)
        return "\n".join(template)
    
#if __name__ == '__main__':
#    print('PARA PROBAR, LECTURA DE PROMOCIONES')
#    promotions=GetPromotions()
#    list_promocion = promotions.get_active_promotions("Looker",3)
#    #list_all_promocion = promocion.get_all_active_promotions(None)
#    formatted_promocion = promotions.format_promotions_output(list_promocion)
#    print(formatted_promocion)
