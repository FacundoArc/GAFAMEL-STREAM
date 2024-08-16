import streamlit as st
import pandas as pd

def main():
    st.title("FILTRO DELFOS A GAFAMEL")

    # File Upload
    uploaded_file = st.file_uploader("ELEGIR FILE XLS", type=["xls", "xlsx"])
    
    #INPUT PARA TIPO DE CAMBIO 

    
    # Get user input and create a variable
    user_input = st.number_input("INGRESAR TIPO DE CAMBIO DE DOLAR OFICIAL SEGUN PAGINA WEB DE DELFOS:")

    #    Use the variable
    if user_input != True:
        st.write("TARIFA DE CAMBIO OFICIAL U$D ", user_input)


    if uploaded_file is not None:
        # Read the Excel file
        try:
            df = pd.read_excel(uploaded_file)
            st.success("File successfully uploaded and loaded!")

            


            #DATAFRAME LIMPIO
            completo = st.checkbox('Mostrar Cuadro completo. En las secciones inferiores se encuentran los datos filtrados segun el tipo de servicio.')
            #df_limpio = df.drop(['id_producto'], axis=1)
            if completo:
                st.dataframe(df)
                st.dataframe(df_limpio)

            
            valores_unicos = df_limpio['nombre_producto'].unique()
            
            
            # Create checkboxes for each DataFrame
            checkboxes = {}
            for servicio in valores_unicos:
                checkboxes[servicio] = st.checkbox(f"Show DataFrame for Servicio: {servicio}")

            # Dividir el DataFrame por los valores únicos de la columna 'nombre_producto'
            subconjuntos = {valor: df_limpio[df_limpio['nombre_producto'] == valor] for valor in valores_unicos}
            
            
            # Mostrar los subconjuntos
            
            for valor, subconjunto in subconjuntos.items():
                if checkboxes[valor]:
                #LIMPIAR
                    subconjunto_limpio = subconjunto.drop(['regreso'], axis = 1)
                
                    st.header(f"Servicio ' {valor}':")
                    st.dataframe(subconjunto_limpio, width=2000)
                    suma_montos = subconjunto_limpio['saldo_para_pagina'].sum().round(2)

                    moneda = df_limpio['moneda_pagina'].unique() 
                #SALDOS PENDIENTES O FAVOR
                    suma_montos_afavor = subconjunto_limpio['cobrado_para_pagina'].sum().round(2)
                    suma_montos_pendientes = subconjunto_limpio['saldo_para_pagina'].sum().round(2)

                    usd_ars = suma_montos*user_input

                    if subconjunto_limpio is not False:
                        st.write(f"La suma del saldo pendiente es de: $ **{suma_montos}**")
                #CADA SERVICIO VA A CONTAR CON SECCION PERSONALIZADA PARA FILTRAR
                        
                        ### ------------ TERRESTRE INTERNACIONAL------------- ###
                    if valor == 'TERRESTRE INTERNACIONAL       ' :
                        st.write('Terrestres internacionales emitidos en dolares pueden ser pagados en pesos segun el cambio oficial')
                        st.write(f'Teniendo en cuenta la Tarifa de Cambio USD **{user_input}**, el total a pagar es de AR$ **{usd_ars}** ')
                        filtro = st.checkbox('FILTRO TERRESTRE INTERNACIONAL')
                        if filtro:
                            filas_seleccionadas = st.multiselect("Selecciona Expendientes que quieras pagar:",  subconjunto_limpio['id_file'].unique())

                # Filtrar el DataFrame según las filas seleccionadas
                            df_seleccionado = subconjunto_limpio[subconjunto_limpio['id_file'].isin(filas_seleccionadas)]

                # Mostrar el DataFrame filtrado
                            st.subheader(f"EXPENDIENTE SELECCIONADOS DEL SERVICIO '{valor}':")

                            df_listo = df_seleccionado.set_index('id_file')

                            df_listo = df_listo.drop(['nombre_producto'] , axis=1)    

                            st.dataframe(df_listo)

                            suma_montos_filtrado = df_seleccionado['saldo_para_pagina'].sum().round(2)
                            usd_ars_filtrado = suma_montos_filtrado*user_input
                            if subconjunto is not False:
                                st.write(f"La suma del saldo pendiente es de: $ {suma_montos_filtrado}")

                            if valor == 'TERRESTRE INTERNACIONAL       ' :
                                st.write('Terrestres internacionales emitidos en dolares pueden ser pagados en pesos segun el cambio oficial')
                                st.write(f'Teniendo en cuenta la Tarifa de Cambio USD{user_input}, el total a pagar es de AR$  **{usd_ars_filtrado.round(2)}** ')

                
                       
                    ### ------------ AEREOS UY------------- ###
                    elif valor == 'AEREOS UY PES                 ':
                        st.write('Aereos emitidos en URUGUAY')
                        st.write('Con vencimiento de 2 dias posteriores a la emision. ')
                        filtro_uy = st.checkbox('FILTRO UY')
                        if filtro_uy:
                            filas_seleccionadas = st.multiselect("Selecciona Expendientes que quieras   pagar:",  subconjunto_limpio['id_file'].unique())

                            # Filtrar el DataFrame según las filas seleccionadas
                            df_seleccionado = subconjunto_limpio[subconjunto_limpio['id_file'].isin(filas_seleccionadas)]

                            # Mostrar el DataFrame filtrado
                            st.subheader(f"EXPENDIENTE SELECCIONADOS DEL SERVICIO '{valor}':")

                            df_listo = df_seleccionado.set_index('id_file')

                            df_listo = df_listo.drop(['nombre_producto'] , axis=1)    

                            st.dataframe(df_listo)

                            suma_montos_filtrado = df_seleccionado['saldo_para_pagina'].sum().round(2)
                            usd_ars_filtrado = suma_montos_filtrado*user_input
                            if subconjunto is not False:
                                st.write(f"La suma del saldo pendiente es de: $ {suma_montos_filtrado}")

                            if valor == 'TERRESTRE INTERNACIONAL       ' :
                                st.write('Terrestres internacionales emitidos en dolares pueden ser pagados en pesos segun el cambio oficial')
                                st.write(f'Teniendo en cuenta la Tarifa de Cambio USD{user_input}, el total a pagar es de AR$  **{usd_ars_filtrado.round(2)}** ')
                    ### ------------ AEREOS INTERNACIONAL------------- ###
                    elif valor == 'AEREOS INTERNACIONAL          ':
                        df_limpio_ai = df_limpio.drop(['regreso'] , axis = 1 )
                        filtro_ai = st.checkbox('FILTRO AEREO INTERNACIONAL INTERNACIONAL')
                        if filtro_ai:
                            filas_seleccionadas_ai = st.multiselect("Selecciona Expendientes que quieras pagar:",  subconjunto_limpio['id_file'].unique())
                

                            
                # Filtrar el DataFrame según las filas seleccionadas
                            df_seleccionado = subconjunto_limpio[subconjunto_limpio['id_file'].isin(filas_seleccionadas_ai)]

                # Mostrar el DataFrame filtrado
                            st.subheader(f"EXPENDIENTE SELECCIONADOS DEL SERVICIO '{valor}':")

                            df_listo = df_seleccionado.set_index('id_file')

                            df_listo = df_listo.drop(['nombre_producto'] , axis=1)    

                            st.dataframe(df_listo)

                            suma_montos_filtrado = df_seleccionado['saldo_para_pagina'].sum().round(2)
                            usd_ars_filtrado = suma_montos_filtrado*user_input
                            if subconjunto is not False:
                                st.write(f"La suma del saldo pendiente es de: $ {suma_montos_filtrado}")
                        for mon in moneda:
                            st.subheader(f"{valor} EN '{mon}'")
                            df_moneda = df_limpio_ai[(df_limpio['moneda_pagina'] == mon) & (df_limpio_ai['nombre_producto'] == 'AEREOS INTERNACIONAL          ')]
                            st.dataframe(df_moneda)                            
                    ### ------------AEREOS DOMESTICOS------------- ###
                    elif valor == 'AEREOS DOMESTICO              ':
                    
                        st.write('BSP Emitidos con 15 dias de vencimiento. DELFOS admite el pago en USD Billete.')
                    ### ------------ CARGO------------- ###                
                    elif valor == 'CARGO                         ':
                        
                        df_limpio_cargo = df_limpio.drop(['regreso','salida'] , axis = 1 )
                                                       
                        st.write('Los Cargos pueden ser dos tipos: ')
                        st.write('Un saldo creado por penalidad en un pago o saldo a favor para usar en cualquier momento dependiendo la moneda')

                        for mon in moneda:
                            st.subheader(f"{valor} EN '{mon}'")
                            df_moneda = df_limpio_cargo[(df_limpio_cargo['moneda_pagina'] == mon) & (df_limpio['nombre_producto'] == 'CARGO                         ')]
                            st.dataframe(df_moneda)
                        
                        
                            #CONDICION POR SI PRESENTA UN SALDO PENDIENTE O 
                            if (df_moneda['cobrado_para_pagina'] == 0).any():
                                st.write(f'Presenta un SALDO PENDIENTE de **{mon}   {suma_montos_pendientes}**')
                        
                            #CONDICION DE SI PRESENTA UN SALDO A FAVOR
                            if (df_moneda['saldo_para_pagina'] == 0).any():
                                st.write(f'Presenta un SALDO A FAVOR **{mon} {suma_montos_afavor}** ')
                        
                    
                       
                

               
                
                    
                
                
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.info("Please upload an XLS file.")
def clean_data(df):
    # Example cleaning operation: Remove null values
    cleaned_df = df.dropna()
    return cleaned_df



if __name__ == "__main__":
    main()
