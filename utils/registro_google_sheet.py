import pygsheets #pip install pygsheets
import pandas as pd #pip instal pandas

class RegistroGoogleSheet:
    ## conexion a google sheets
    def registrar_google_sheets(self, nombre,correo,programa,promocion_julio):
        ##obtener los datos de google sheets
        sheet_id="1ey86lWPswdew9tRFlReERnA-eBY7gvDQUb5GdTzVj6o"
        sheet_name="Interesados" #Si le pusiste otro nombre a la hoja, le cambias aqui
        url=f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

        ##añadimos el nuevo registro al dataframe
        df=pd.read_csv(url)
        print(df)

        df.loc[len(df.index)] = ['123',nombre,correo,programa,promocion_julio]
        print(df)

        try:
            ##luego cargamos a google sheets
            service_account_path='project-advp-assistant-39b91ec77b5e.json'
            gc = pygsheets.authorize(service_file=service_account_path)

            #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
            sh = gc.open_by_url(url)

            #select the first sheet
            wks = sh[0]
            #update the first sheet with df, starting at cell B2.
            wks.set_dataframe(df,(1,1))
            return True
        except:
            return False

#if __name__ == '__main__':
#    registrador = RegistroGoogleSheet()
#    registrador.registrar_google_sheets(nombre="Jeanpier Ancori",
#                                        correo="tarara.tarara@gmail.com",
#                                        programa="Hadop",
#                                        promocion_julio="")